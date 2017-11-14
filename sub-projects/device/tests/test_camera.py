# NOTE: this file must be in the same directory as screenstream.py to run
from screenstream import WebCamStream
import cv2
from time import sleep

video_stream = WebCamStream()
video_stream.start()

while True:
    frame = video_stream.read() # read a frame from the stream
    cv2.imshow('img', frame)  # display the frame in a window
    if cv2.waitKey(1) == ord('q'):  # must follow imshow, wait for keypress
        break  # stop if 'q' is pressed

video_stream.stop()
cv2.destroyAllWindows()
