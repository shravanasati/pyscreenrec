from multiprocessing import Queue, Value
from threading import Thread
import time
from warnings import warn

import cv2
import mss
from mss.models import Monitor
from mss.screenshot import ScreenShot
import numpy as np


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
        self.queue: Queue[ScreenShot | None] = Queue()

    def _start_recording(self) -> None:
        """
        (Protected) Starts screen recording.

        This function is meant to be run in a separate thread.
        It continuosly grabs screenshots using mss and sends them
        to the saver thread, which is responsible for writing these
        images to the video stream.
        """
        # ! not instantiating this in the constructor because mss has issues
        # ! with using instances from main thread in sub-threads
        # ! AttributeError: '_thread._local' object has no attribute 'srcdc'
        with mss.mss() as sct:
            # checking if screen is already being recorded
            if self.__running.value != 0:
                warn("Screen recording is already running.", ScreenRecordingInProgress)

            else:
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
                    self.queue.put(sct.grab(self.mon))
                    st_total = time.perf_counter() - st_start
                    time.sleep(max(0, 1 / self.fps - st_total))

    @staticmethod
    def _get_monitor(mon: Monitor | None):
        if mon is None:
            with mss.mss() as sct:
                return sct.monitors[0]

        return mon

    def start_recording(self, video_name: str, fps: int, monitor: Monitor | None = None) -> None:
        """
        Starts screen recording. It is a non-blocking call.
        The `stop_recording` method must be called after this
        function call for the video to be rendered.

        Raises a warning `ScreenRecordingInProgress` if this method is called while
        the screen recording is already running.

        @params

        video_name (str) --> The name of the output screen recording. Must end with `.mp4`.

        fps (int) --> The Frames Per Second for the screen recording. Implies how much screenshots will be taken in a second.

        monitor (Monitor, optional) -> The monitor that needs to be captured, here you can specify the region of the screen you want to record. It must be dictionary with these fields:

        {
            "mon": 1,
            "left": 100,
            "top": 100,
            "width": 1000,
            "height": 1000
        }

        If this parameter is not provided, pyscreenrec captures the entire screen.
        """
        self.fps = fps
        self.video_name = video_name

        self.mon = self._get_monitor(monitor)

        # checking for video extension
        if not self.video_name.endswith(".mp4"):
            raise ValueError("The video's extension can only be '.mp4'.")

        self.recorder_thread = Thread(target=self._start_recording)
        self.recorder_thread.start()
        self.saver_proc = Thread(target=self._write_img_to_stream)
        self.saver_proc.start()

    def _write_img_to_stream(self):
        """
        (Protected) This function is also meant to be run in a separate thread.

        It creates a video writer object and listens on the queue for images that
        need to written to the video, and also releases the video when `stop_recording`
        is called.
        """
        try:
            img = self.queue.get()
            if img is None:
                return

            frame = cv2.cvtColor(np.array(img), cv2.COLOR_BGRA2BGR)
            height, width = frame.shape[:2]

            if width <= 0 or height <= 0:
                raise ValueError("Invalid width or height.")

            video = cv2.VideoWriter(
                self.video_name, cv2.VideoWriter_fourcc(*"mp4v"), self.fps, (width, height)
            )

            video.write(frame)

            while True:
                img = self.queue.get()
                if img is None:
                    break
                video.write(cv2.cvtColor(np.array(img), cv2.COLOR_BGRA2BGR))

        except Exception as e:
            logger.error(f"Error in video writing: {e}")
        finally:
            video.release()

    def stop_recording(self) -> None:
        """
        Stops screen recording.

        Raises a warning `NoScreenRecordingInProgress` if this method is called while
        no screen recording is already running.
        """
        if self.__running.value == 0:
            warn(
                "No screen recording session is going on.", NoScreenRecordingInProgress
            )
            return

        # stop both the processes
        self.__running.value = 0
        self.recorder_thread.join()

        # signal _save_image process to quit
        self.queue.put(None)
        self.saver_proc.join()

    def pause_recording(self) -> None:
        """
        Pauses screen recording.

        Raises a warning `NoScreenRecordingInProgress` if this method is called while
        no screen recording is already running.
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

        Raises a warning `ScreenRecordingInProgress` if this method is called while
        the screen recording is already running.
        """
        if self.__running.value != 0:
            warn("Screen recording is already running.", ScreenRecordingInProgress)
            return

        # the first call to start_recording already sets up saver process
        # so we dont need to start it again
        self.recorder_thread = Thread(target=self._start_recording)
        self.recorder_thread.start()

    def __repr__(self) -> str:
        return f"ScreenRecorder <running = {bool(self.__running.value)}>"


if __name__ == "__main__":
    rec = ScreenRecorder()

    print("recording started")
    rec.start_recording("Recording.mp4", fps=30, monitor={
        "mon": 1,
        "left": 100,
        "top": 100,
        "width": 1000,
        "height": 1000
    })
    time.sleep(5)

    print("pausing")
    rec.pause_recording()
    time.sleep(2)

    print("resuming")
    rec.resume_recording()
    time.sleep(5)

    print("recording ended")
    rec.stop_recording()
