import tkinter as tk
from tkinter import messagebox
from warnings import filterwarnings

from pyscreenrec import ScreenRecorder, ScreenRecordingInProgress, NoScreenRecordingInProgress

filterwarnings("error")

COORDINATES = None

class RegionSelector(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Select Recording Region")
        self.geometry("800x600")
        self.attributes('-alpha', 0.3)
        self.attributes('-fullscreen', True)
        self.configure(background='grey')

        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None

        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)

        self.canvas.bind('<Button-1>', self.start_selection)
        self.canvas.bind('<B1-Motion>', self.update_selection)
        self.canvas.bind('<ButtonRelease-1>', self.end_selection)

        self.selection_rect = None

    def start_selection(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.selection_rect:
            self.canvas.delete(self.selection_rect)

    def update_selection(self, event):
        if self.selection_rect:
            self.canvas.delete(self.selection_rect)
        self.selection_rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, event.x, event.y, outline='red'
        )

    def end_selection(self, event):
        self.end_x = event.x
        self.end_y = event.y
        global COORDINATES
        COORDINATES = self.get_coordinates()
        self.destroy()

    def get_coordinates(self):
        # Ensure coordinates are in the correct order
        left = min(self.start_x, self.end_x)
        top = min(self.start_y, self.end_y)
        x2 = max(self.start_x, self.end_x)
        y2 = max(self.start_y, self.end_y)
        width = x2 - left
        height = y2 - top
        return {
            "top": top,
            "left": left,
            "height": height,
            "width": width,
        }


class GUIScreenRecorder(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Screen Recorder")
        self.geometry("500x400")

        self.recorder = ScreenRecorder()

        self.start_button = tk.Button(self, text="Start Recording", command=self.start_recording)
        self.start_button.pack(pady=10)

        self.select_region_button = tk.Button(self, text="Select Region", command=self.select_recording_region)
        self.select_region_button.pack(pady=10)

        self.pause_button = tk.Button(self, text="Pause Recording", command=self.pause_recording)
        self.pause_button.pack(pady=10)

        self.resume_button = tk.Button(self, text="Resume Recording", command=self.resume_recording)
        self.resume_button.pack(pady=10)

        self.stop_button = tk.Button(self, text="Stop Recording", command=self.stop_recording)
        self.stop_button.pack(pady=10)

        self.filename_entry = tk.Entry(self, width=40)
        self.filename_entry.pack(pady=10)
        self.filename_entry.insert(0, "Recording.mp4")

        self.fps_entry = tk.Entry(self, width=10)
        self.fps_entry.pack(pady=10)
        self.fps_entry.insert(0, "30")

    def select_recording_region(self):
        selector = RegionSelector(self)
        selector.mainloop()

    def start_recording(self):
        try:
            filename = self.filename_entry.get()
            fps = int(self.fps_entry.get())
            self.recorder.start_recording(filename, fps, COORDINATES)
            messagebox.showinfo("Recording Started", "Screen recording has started.")
        except (ValueError, SyntaxError):
            messagebox.showerror("Invalid Input", "Please enter valid values for the filename and FPS.")
        except ScreenRecordingInProgress:
            messagebox.showerror("Recording in Progress", "Screen recording is already in progress.")

    def pause_recording(self):
        try:
            self.recorder.pause_recording()
            messagebox.showinfo("Recording Paused", "Screen recording has been paused.")
        except NoScreenRecordingInProgress:
            messagebox.showerror("No Recording", "No screen recording is in progress.")

    def resume_recording(self):
        try:
            self.recorder.resume_recording()
            messagebox.showinfo("Recording Resumed", "Screen recording has been resumed.")
        except ScreenRecordingInProgress:
            messagebox.showerror("Recording in Progress", "Screen recording is already in progress.")

    def stop_recording(self):
        try:
            self.recorder.stop_recording()
            messagebox.showinfo("Recording Stopped", "Screen recording has stopped.")
        except NoScreenRecordingInProgress:
            messagebox.showerror("No Recording", "No screen recording is in progress.")


if __name__ == "__main__":
    app = GUIScreenRecorder()
    app.mainloop()
