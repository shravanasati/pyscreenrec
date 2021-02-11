from pyscreeze import screenshot
from time import sleep, time
import cv2
import os
from threading import Thread
from natsort import natsorted

class InvalidCodec(Exception):
    pass


class ScreenRecorder:
    """
    Base class for screen recording.
    """

    def __init__(self) -> None:
        """
        Constructor.
        """
        self._running = False
        self.screenshot_folder = os.path.join(os.path.expanduser("~"), "Documents//pyscreenrec_data")

        # making the screenshot directory if not exists
        if not os.path.exists(self.screenshot_folder):
            os.mkdir(self.screenshot_folder)
        # clearing all the previous data if last session ended unsuccessfully
        self._clear_data()


    def _start_recording(self, video_name:str, timeout):
        """
        (Protected) Starts screen recording.

        @params 
        
        video_name --> The name of the screen recording video.

        timeout --> (Optional) The time in seconds after which the recording will automatically stop.
        """
        # checking for video extension
        if not video_name.endswith(".mp4"):
            raise InvalidCodec("The video's extension can only be '.mp4'.")

        # checking if screen is already being recorded
        if self._running:
            print("Screen recording is already running.")

        else:
            self._running = True
            i = 1

            if timeout != None:
                # running a thread for checking timeout
                t1 = Thread(target=self._check_for_timeout, args=(timeout,))
                t1.start()

            # starting screenshotting
            while self._running:
                screenshot(os.path.join(self.screenshot_folder, f"s{i}.jpg"))
                sleep(1)
                i += 1

            # saving the video and clearing all screenshots
            self._save_video(video_name)
            self._clear_data()

    def start_recording(self, video_name:str="Recording.mp4", timeout=None):
        """
        Starts screen recording.

        @params 
        
        video_name --> The name of the output screen recording.

        timeout --> (Optional) The time in seconds after which the recording will automatically stop.
        """
        t = Thread(target=self._start_recording, args=(video_name, timeout))
        t.start()

    def stop_recording(self):
        """
        Stops screen recording.
        """
        self._running = False


    def _check_for_timeout(self, timeout):
        """
        A method which checks for timeout and stops screen recording if the timeout is over.

        @params

        timeout --> timeout in seconds after which the recording will stop.
        """
        # intialising the current time
        init = time()

        # starting an infinite loop to check if timeout is over
        while True:
            if time() - init > timeout:
                self.stop_recording()
                break
            sleep(1)

    def _save_video(self, video_name:str):
        """
        Makes a video out of the screenshots.
        """
        # fetching image info
        images = natsorted([img for img in os.listdir(self.screenshot_folder) if img.endswith(".jpg")])
        frame = cv2.imread(os.path.join(self.screenshot_folder, images[0]))
        height, width, _ = frame.shape

        # making a videowriter object 
        video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'mp4v'), 1, (width,height))

        # writing all the images to a video
        for image in images:
            video.write(cv2.imread(os.path.join(self.screenshot_folder, image)))

        # releasing video
        cv2.destroyAllWindows()
        video.release()

    def _clear_data(self):
        """
        Deletes all screenshots present in the screenshot folder taken during screen recording.
        """
        for screenshot in os.listdir(self.screenshot_folder):
            os.remove(os.path.join(self.screenshot_folder, screenshot))
