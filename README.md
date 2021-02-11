# pyscreenrec

*pyscreenrec* is a small and cross-platform python library to record screen.

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

>>> # to stop recording
>>> recorder.stop_recording()
```

The `start_recording` method takes care of all video-saving, screenshot-deleting tasks. You needn't do anything else than just start or stop recording.

You can also pass optional `timeout` argument to `start_recording` method. <br>
When timeout is argument is passed you dont need to execute `stop_recording` method. <br>
The recording will automatically stop after the given `timeout` (in seconds) argument. <br>

``` python
>>> recorder.start_recording("recording.mp4", 10)
>>> # The recording will automatically stop after 10 seconds.
```

<br>

## Known limitations
*pyscreenrec* is not able to:
- capture the system sound during screen recording
- capture only a certain part of the screen

<br>

## Contribution
Pull requests are welcome. If you want to make a major change, open an issue first to discuss about the change.