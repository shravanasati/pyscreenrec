import mss
import cv2
import numpy as np

with mss.mss() as sct:
    mon = sct.monitors[0]
    video = cv2.VideoWriter(
        "test.mp4", cv2.VideoWriter_fourcc(*"mp4v"), 30, (mon["width"], mon["height"])
    )

    for frame in range(300):
        img = np.array(sct.grab(mon))
        video.write(cv2.cvtColor(img, cv2.COLOR_BGRA2BGR))

    video.release()
