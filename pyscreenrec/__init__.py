from multiprocessing import Queue, Process, Value
import os
import time
from warnings import warn

import cv2
from natsort import natsorted
from mss import mss, tools as mss_tools
from pyscreeze import screenshot


class InvalidCodec(Exception):
    pass


class InvalidStartMode(Exception):
    pass


class ScreenRecordingInProgress(Warning):
    """
    This warning is raised when the `start_recording` or `resume_recording` methods
    are called upon a `ScreenRecorder` instance which is already running.
    """

    pass


class NoScreenRecordingInProgress(Warning):
    """
    This warning is raised when the `stop_recording` or `pause_recording` methods
    are called upon a `ScreenRecorder` instance which is not running.
    """

    pass


class ScreenRecorder:
    """
    Base class for screen recording.
    """

    def __init__(self) -> None:
        """
        Constructor.
        """
        # 0 -> False, 1 -> True
        self.__running = Value("i", 0)
        self.__start_mode = "start"
        self.screenshot_folder = os.path.join(
            os.path.expanduser("~"), ".pyscreenrec_data"
        )
        os.makedirs(self.screenshot_folder, exist_ok=True)

        # clearing all the previous data if last session ended unsuccessfully
        self._clear_data()

        # used for maintaining screenshot count
        self.__count = 1
        self.queue = Queue()

    def _screenshot(self, filename: str) -> float:
        """
        A helper function which saves a screenshot to `self.screenshot_folder` with the
        given filename, and returns the duration it took to perform the operation.
        """
        st_start = time.perf_counter()
        # self.screenshotter.shot(output=os.path.join(self.screenshot_folder, filename))
        screenshot(os.path.join(self.screenshot_folder, filename))
        st_end = time.perf_counter()
        return st_end - st_start

    def _start_recording(self) -> None:
        """
        (Protected) Starts screen recording.

        @params

        video_name (str) --> The name of the screen recording video.

        fps (int) --> The Frames Per Second for the screen recording. Implies how much screenshots will be taken in a second.
        """
        # ! not instantiating this in the constructor because mss has issues
        # ! with using instances from main thread in sub-threads
        # ! AttributeError: '_thread._local' object has no attribute 'srcdc'
        self.screenshotter = mss()
        mon = self.screenshotter.monitors[0]

        # checking if screen is already being recorded
        if self.__running.value != 0:
            warn("Screen recording is already running.", ScreenRecordingInProgress)

        else:
            if self.__start_mode not in ("start", "resume"):
                raise InvalidStartMode(
                    "The `self.__start_mode` can only be 'start' or 'resume'."
                )

            self.__running.value = 1

            while self.__running.value != 0:
                # not sleeping for exactly 1/self.fps seconds because
                # otherwise time is lost in sleeping which could be used in
                # capturing frames
                # since due to thread context-switching, this screenshotter
                # thread doesn't get all the time that it needs
                # thus, if more than required time has been spent just on
                # screenshotting, don't sleep at all
                st_start = time.perf_counter()
                self.queue.put(self.screenshotter.grab(mon))
                st_total = time.perf_counter() - st_start
                time.sleep(max(0, 1 / self.fps - st_total))
                # st_total = self._screenshot(f"s{self.__count}.png")
                # self.__count += 1

        # signal _save_image process to quit
        self.queue.put(None)

    def _save_image(self):
        output = os.path.join(self.screenshot_folder, "s{}.png")
        while True:
            img = self.queue.get()
            if img is None:
                break
            mss_tools.to_png(img.rgb, img.size, output=output.format(self.__count))
            self.__count += 1

    def start_recording(self, video_name: str = "Recording.mp4", fps: int = 15) -> None:
        """
        Starts screen recording.

        @params

        video_name (str) --> The name of the output screen recording.

        fps (int) --> The Frames Per Second for the screen recording. Implies how much screenshots will be taken in a second.
        """
        self.fps = fps
        self.video_name = video_name

        # checking for video extension
        if not self.video_name.endswith(".mp4"):
            raise InvalidCodec("The video's extension can only be '.mp4'.")

        recorder_process = Process(target=self._start_recording)
        self.saver_process = Process(target=self._save_image)
        recorder_process.start()
        self.saver_process.start()

    def stop_recording(self) -> None:
        """
        Stops screen recording.
        """
        if self.__running.value == 0:
            warn(
                "No screen recording session is going on.", NoScreenRecordingInProgress
            )
            return

        # stop both the processes
        self.__running.value = 0
        # wait until saver process has finished working
        self.saver_process.join()

        # reset screenshot count and start_mode
        self.__count = 1
        self.__start_mode = "start"

        # saving the video and clearing all screenshots
        self._save_video(self.video_name)
        self._clear_data()

    def pause_recording(self) -> None:
        """
        Pauses screen recording.
        """
        if self.__running.value == 0:
            warn(
                "No screen recording session is going on.", NoScreenRecordingInProgress
            )
            return

        self.__running.value = 0

    def resume_recording(self) -> None:
        """
        Resumes screen recording.
        """
        if self.__running.value != 0:
            warn("Screen recording is already running.", ScreenRecordingInProgress)
            return

        self.__start_mode = "resume"
        self.start_recording(self.video_name)

    def _save_video(self, video_name: str) -> None:
        """
        (Protected) Makes a video out of the screenshots.

        @params

        video_name (str) --> Name or path to the output video.
        """
        # fetching image info
        images = natsorted(
            [img for img in os.listdir(self.screenshot_folder) if img.endswith(".png")]
        )
        print(f"{len(images)=}")
        frame = cv2.imread(os.path.join(self.screenshot_folder, images[0]))
        height, width, _ = frame.shape

        # making a videowriter object
        video = cv2.VideoWriter(
            video_name, cv2.VideoWriter_fourcc(*"mp4v"), self.fps, (width, height)
        )

        # writing all the images to a video
        for image in images:
            video.write(cv2.imread(os.path.join(self.screenshot_folder, image)))

        # releasing video
        cv2.destroyAllWindows()
        video.release()

    def _clear_data(self) -> None:
        """
        (Protected) Deletes all screenshots present in the screenshot folder taken during screen recording.
        """
        # deleting all screenshots present in the screenshot directory
        for image in os.listdir(self.screenshot_folder):
            os.remove(os.path.join(self.screenshot_folder, image))

    def __repr__(self) -> str:
        return "pyscreenrec is a small and cross-platform python library that can be used to record screen. \nFor more info, visit https://github.com/shravanasati/pyscreenrec#readme."


if __name__ == "__main__":
    rec = ScreenRecorder()
    print("recording started")
    rec.start_recording(fps=30)
    time.sleep(10)
    print("recording ended")
    rec.stop_recording()
    # print("pausing")
    # rec.pause_recording()
    # time.sleep(2)
    # print("resuming")
    # rec.resume_recording()
    # time.sleep(5)
    # print("recording ended")
    # rec.stop_recording()
