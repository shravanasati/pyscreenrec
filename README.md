# pyscreenrec

*pyscreenrec* is a small and cross-platform python library to record screen.

[![Downloads](https://pepy.tech/badge/pyscreenrec)](https://pepy.tech/project/pyscreenrec)

<br>

## Installation
Install on Windows: 
`pip install pyscreenrec`

Install on Linux/macOS: 
`pip3 install pyscreenrec`

<br>

## Example usage
``` python
>>> import pyscreenrec
>>> recorder = pyscreenrec.ScreenRecorder()

>>> # to start recording
>>> recorder.start_recording("recording.mp4") # 'recording.mp4' is the name of the output video file, may also contain full path like 'C:/Users/<user>/Videos/video.mp4'

>>> # to pause recording
>>> recorder.pause_recording()

>>> # to resume recording
>>> recorder.resume_recording()

>>> # to stop recording
>>> recorder.stop_recording()
```

The `stop_recording` saves the video and deletes all screenshots used in the session. So calling
the `stop_recording` method is necessary when `start_recording` is called.


<br>

## Known limitations
*pyscreenrec* is yet not able to:
- capture the system sound during screen recording
- capture only a certain part of the screen

<br>

## Change Log
Changes made in the latest version (*v0.2*) are:
- Introduced two new methods: `pause_recording` and `resume_recording` which can be used to pause and resume screen recording respectively.
- The `timeout` argument of the `start_recording` method is deprecated due to it miscellaneous behavior and clash with ability to pause and resume screen recording.
- The screen recording output video is now saved and the screenshots are deleted by `stop_recording` method.

View [CHANGELOG](CHANGELOG) for more details.

<br>

## Contribution
Pull requests are welcome. If you want to make a major change, open an issue first to discuss about the change.

For further details, view [CONTRIBUTING.md](CONTRIBUTING.md).