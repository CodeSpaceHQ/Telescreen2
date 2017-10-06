from cv2 import VideoCapture
from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread


class PiCameraVideoStream(object):
    """
    A class that handles threaded video streaming through a PiCamera.
    based on imutils library for python: https://github.com/jrosebr1/imutils
    """

    def __init__(self, resolution, framerate):
        """
        Initialize an object that controls a video
        stream from a PiCamera on a separate thread.
        Args:
          resolution: the desired resoluiton of each frame in the stream
          framerate: the desired framerate of the video stream
        """
        self.camera = PiCamera()  # get picamera object
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.rawCapture = PiRGBArray(self.camera,
                                     size=resolution)  # get RGB array from the camera
        # continuously capture and store as an array in stream
        self.stream = self.camera.capture_continuous(self.rawCapture,
                                                     format="bgr",
                                                     use_video_port=True)

        self.frame = None  # current frame
        self.stopped = False

    def start(self):
        """
        Start the video stream on a separate daemon thread.
        """
        thread = Thread(target=self.update, args=())
        thread.daemon = True
        thread.start()
        return self

    def update(self):
        """
        Continuously update the stream with each frame
        until stopped.
        """
        for frame in self.stream:
            self.frame = frame.array
            self.rawCapture.truncate(0)

            if self.stopped:
                self.stream.close()
                self.rawCapture.close()
                self.camera.close()
                return

    def read(self):
        """
        Read the current frame in the video stream.
        Returns:
          The most recent frame captured
        """
        return self.frame

    def stop(self):
        """
        Stop the video stream.
        """
        self.stopped = True


class WebCamVideoStream(object):
    """
    A class that handles threaded video streaming through a USB webcam.
    based on imutils library for python: https://github.com/jrosebr1/imutils

    """

    def __init__(self, src=0):
        """
        Initialize an object that controls a video
        stream from a USB Webcam on a separate thread.
        Args:
          src: the source for the USB webcam, 0 is the default camera
        """
        self.stream = VideoCapture(src)  # initialize video source
        self.grabbed, self.frame = self.stream.read()  # grab initial frame
        self.stopped = False

    def start(self):
        """
        Start the video stream on a separate daemon thread.
        """
        thread = Thread(target=self.update, args=())  # create new thread
        thread.daemon = True  # set thread to daemon
        thread.start()  # start thread
        return self

    def update(self):
        """
        Continuously update the stream with the most recent frame
        until stopped.
        """
        while not self.stopped:
            self.grabbed, self.frame = self.stream.read()

    def read(self):
        """
        Read the current frame in the video stream.
        Returns:
          The most recent frame captured
        """
        return self.frame

    def stop(self):
        """
        Stop the video stream.
        """
        self.stopped = True


class ScreenStream(object):
    
    def __init__(self, src=0, usePiCamera=False, FPS=32, resolution=(400,400)):
        """
        Initialize a video stream from a PiCamera or a USB Webcam (default)
        based on imutils library for python: https://github.com/jrosebr1/imutils

        Args:
          src: the source for the webcam (default camera is 0)
          usePiCamera: boolean of whether to use PiCamera
          FPS: framerate of the PiCamera
          resolution: resolution of the PiCamera
        """
        self.usePiCamera= usePiCamera  # dfault to use USB webcam
        self.FPS = FPS  # frames per second
        self.resolution = resolution
        
        if usePiCamera:  # set up picamera using helper class
            self.stream = PiCameraVideoStream(resolution=resolution,
                                              framerate=FPS)
        else:  # set up webcam using helper class
            self.stream = WebCamVideoStream(src=src)
            
    def start(self):
        """
        Start the corresponding stream
        """
        return self.stream.start()
    
    def update(self):
        """
        Update the frame for the corresponding stream
        """
        return self.stream.update()
    
    def read(self):
        """
        Read a frame in the corresponding stream
        """
        return self.stream.read()
    
    def stop(self):
        """
        Stop the corresponding stream
        """
        return self.stream.stop()