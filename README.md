# pyscreenrec

*pyscreenrec* is a small and cross-platform python library for recording screen.

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
>>> recorder.start_recording("recording.mp4", 10) 
>>> # 'recording.mp4' is the name of the output video file, may also contain full path like 'C:/Users/<user>/Videos/video.mp4'
>>> # the second parameter(10) is the FPS. You can specify the FPS for the screen recording using the second parameter. It must not be greater than 60.

>>> # to pause recording
>>> recorder.pause_recording()

>>> # to resume recording
>>> recorder.resume_recording()

>>> # to stop recording
>>> recorder.stop_recording()
```

The `stop_recording` saves the video and deletes all screenshots used in the session. 
So calling the `stop_recording` method is necessary when `start_recording` is called.


<br>

## Known limitations
*pyscreenrec* is yet not able to:
- capture the system sound during screen recording
- capture only a certain part of the screen

<br>

## Change Log
Changes made in the latest version (*v0.3*) are:
- Manually set FPS for the screen recording, by an extra `fps` argument in `start_recording` method.
- Introduced a one more exception class named `InvalidFPS`.
- Minor bug fixes.

View [CHANGELOG](https://github.com/Shravan-1908/pyscreenrec/blob/master/CHANGELOG) for more details.

<br>

## Contribution
Pull requests are welcome. If you want to make a major change, open an issue first to discuss about the change.

For further details, view [CONTRIBUTING.md](https://github.com/Shravan-1908/pyscreenrec/blob/master/CONTRIBUTING.md).