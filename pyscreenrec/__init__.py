# type: ignore
from pyscreeze import screenshot
from time import sleep
# type: ignore
import cv2
import os
from threading import Thread
# type: ignore
from natsort import natsorted

class InvalidCodec(Exception):
    pass

class InvalidStartMode(Exception):
    pass

class InvalidFPS(Exception):
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
        self._start_mode = "start"
        self.screenshot_folder = os.path.join(os.path.expanduser("~"), "Documents", "pyscreenrec_data")

        # making the screenshot directory if not exists
        if not os.path.exists(self.screenshot_folder):
            os.mkdir(self.screenshot_folder)
        # clearing all the previous data if last session ended unsuccessfully
        self._clear_data()


    def _start_recording(self, video_name:str, fps:int):
        """
        (Protected) Starts screen recording.

        @params 
        
        video_name --> The name of the screen recording video.

        fps --> The Frames Per Second for the screen recording. Implies how much screenshots will be taken in a second.
        """
        # checking for video extension and fps
        if not video_name.endswith(".mp4"):
            raise InvalidCodec("The video's extension can only be '.mp4'.")
        if fps > 60:
            raise InvalidFPS("The FPS for the screen recording can be maximum 60 FPS.")
        self.fps = fps
        self.video_name = video_name

        # checking if screen is already being recorded
        if self._running:
            print("Screen recording is already running.")

        else:
            if self._start_mode == "start":
                self._running = True
                i = 1

                # starting screenshotting
                while self._running:
                    screenshot(os.path.join(self.screenshot_folder, f"s{i}.jpg"))
                    sleep(1/self.fps)
                    i += 1

            elif self._start_mode == "resume":
                self._running = True
                i = len(natsorted([img for img in os.listdir(self.screenshot_folder) if img.endswith(".jpg")])) + 1

                while self._running:
                    screenshot(os.path.join(self.screenshot_folder, f"s{i}.jpg"))
                    sleep(1/self.fps)
                    i += 1

            else:
                raise InvalidStartMode("The `self._start_mode` can only be 'start' or 'resume'.")


    def start_recording(self, video_name:str="Recording.mp4", fps:int=15):
        """
        Starts screen recording.

        @params 
        
        video_name --> The name of the output screen recording.

        fps --> The Frames Per Second for the screen recording. Implies how much screenshots will be taken in a second.
        """
        t = Thread(target=self._start_recording, args=(video_name,fps))
        t.start()

    def stop_recording(self):
        """
        Stops screen recording.
        """
        if not self._running:
            print("No screen recording session is going on.")
            return None
        self._running = False

        # saving the video and clearing all screenshots
        self._save_video(self.video_name)
        self._clear_data()


    def pause_recording(self):
        """
        Pauses screen recording.
        """
        if not self._running:
            print("No screen recording session is going on.")
            return None

        self._running = False

    def resume_recording(self):
        """
        Resumes screen recording.
        """
        if self._running:
            print("Screen recording is already running.")
            return None

        self._start_mode = "resume"
        self.start_recording(self.video_name)


    def _save_video(self, video_name:str):
        """
        Makes a video out of the screenshots.
        """
        # fetching image info
        images = natsorted([img for img in os.listdir(self.screenshot_folder) if img.endswith(".jpg")])
        frame = cv2.imread(os.path.join(self.screenshot_folder, images[0]))
        height, width, _ = frame.shape

        # making a videowriter object 
        video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'mp4v'), self.fps, (width,height))

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
        # deleting all screenshots present in the screenshot directory
        for screenshot in os.listdir(self.screenshot_folder):
            os.remove(os.path.join(self.screenshot_folder, screenshot))
