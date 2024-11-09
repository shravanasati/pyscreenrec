# pyscreenrec

*pyscreenrec* is a small and cross-platform python library for recording screen.


![PyPI Downloads](https://static.pepy.tech/badge/pyscreenrec)

<br>

## Installation
Install on Windows: 
`pip install -U pyscreenrec`

Install on Linux/macOS: 
`pip3 install -U pyscreenrec`

<br>

## Example usage


``` python
>>> import pyscreenrec
>>> recorder = pyscreenrec.ScreenRecorder()

>>> # to start recording
>>> recorder.start_recording("recording.mp4", 30, {
	"mon": 1,
	"left": 100,
	"top": 100,
	"width": 1000,
	"height": 1000
}) 
>>> # 'recording.mp4' is the name of the output video file, may also contain full path like 'C:/Users/<user>/Videos/video.mp4'
>>> # the second parameter is the FPS for the recording
>>> # the third parameter (optional) is the monitor and the dimensions that needs to be recorded,
# here we're capturing the first monitor, 100px from left, 100px from right, and then 1000px each in resp. axes
# refer https://python-mss.readthedocs.io/examples.html#part-of-the-screen-of-the-2nd-monitor for more information


>>> # to pause recording
>>> recorder.pause_recording()

>>> # to resume recording
>>> recorder.resume_recording()

>>> # to stop recording
>>> recorder.stop_recording()
```

> Take a look at the example GUI screen recorder [here](examples/gui_recorder.py) for more information.

Keep in mind that the `start_recording` method is non-blocking, it will start a thread in the background to capture the screenshots.


The `stop_recording` saves the video. So calling the `stop_recording` method is necessary when `start_recording` is called.

You'd ideally need some sort of a timeout or a callback to call the `stop_recording` function after `start_recording`, to give the program some time to capture the screen.

If a screen recording session is already running, calling the `start_recording` and `resume_recording` methods raises a `ScreenRecodingInProgress` warning.

Similarly, if a screen recording session is not running, calling the `stop_recording` and `pause_recording` methods raises a `NoScreenRecodingInProgress` warning.


<br>

## Known limitations

*pyscreenrec* is not able to:
- capture the system sound during screen recording

<br>

## Change Log

Changes made in the latest version (*v0.6*) are:

- Write screenshots directly to the video stream instead of the disk.
- Delegate image writing to a separate thread.
- Use mss library instead of pyscreeze for capturing screenshots.
- Capture a part of the screen.
- Performance improvements.
- Internal refactors.



View [CHANGELOG](https://github.com/shravanasati/pyscreenrec/blob/master/CHANGELOG) for more details.

<br>

## Contribution

Pull requests are welcome. If you want to make a major change, open an issue first to discuss about the change.

For further details, view [CONTRIBUTING.md](https://github.com/shravanasati/pyscreenrec/blob/master/CONTRIBUTING.md).