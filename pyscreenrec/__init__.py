import os
from threading import Thread
import time
from warnings import warn

import cv2
from natsort import natsorted
from mss import mss


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
        self.__running = False
        self.__start_mode = "start"
        self.screenshot_folder = os.path.join(
            os.path.expanduser("~"), ".pyscreenrec_data"
        )
        os.makedirs(self.screenshot_folder, exist_ok=True)

        # clearing all the previous data if last session ended unsuccessfully
        self._clear_data()

        # used for maintaining screenshot count
        self.__count = 1

    def _screenshot(self, filename: str) -> float:
        """
        A helper function which saves a screenshot to `self.screenshot_folder` with the
        given filename, and returns the duration it took to perform the operation.
        """
        st_start = time.perf_counter()
        self.screenshotter.shot(output=os.path.join(self.screenshot_folder, filename))
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

        # checking if screen is already being recorded
        if self.__running:
            warn("Screen recording is already running.", ScreenRecordingInProgress)

        else:
            if self.__start_mode not in ("start", "resume"):
                raise InvalidStartMode(
                    "The `self.__start_mode` can only be 'start' or 'resume'."
                )

            self.__running = True

            while self.__running:
                # not sleeping for exactly 1/self.fps seconds because
                # otherwise time is lost in sleeping which could be used in
                # capturing frames
                # since due to thread context-switching, this screenshotter
                # thread doesn't get all the time that it needs
                # thus, if more than required time has been spent just on
                # screenshotting, don't sleep at all
                st_total = self._screenshot(f"s{self.__count}.png")
                time.sleep(max(0, 1 / self.fps - st_total))
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

        t = Thread(target=self._start_recording)
        t.start()

    def stop_recording(self) -> None:
        """
        Stops screen recording.
        """
        if not self.__running:
            warn(
                "No screen recording session is going on.", NoScreenRecordingInProgress
            )
            return

        self.__running = False
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
        if not self.__running:
            warn(
                "No screen recording session is going on.", NoScreenRecordingInProgress
            )
            return

        self.__running = False

    def resume_recording(self) -> None:
        """
        Resumes screen recording.
        """
        if self.__running:
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
