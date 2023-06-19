"""
Module contains the Video class that stores and represents video files as objects.

"""
import cv2
import numpy as np

class Video:
    """
    Video class stores all relevant informations from video file.

    Attributes
    ----------
        file: string
            The path/file name of the video.

        title: string
            The title that represents the video file.

        capture: cv2.VideoCapture
            The video capture of the video file from cv2 package.

        image: numpy.ndarray
            The representaion of first frame of video file as numpy ndarray.

        width: int
            The width value of the video file.

        height: int
            The height value of the video file.
        
        fps: int
            The fps of the video file.


    Methods
    -------
    
        __repr__() -> string:
            A native python method to represent the Video class.

        cleanup() -> None:
            Clean up memory from cv2 video capture.


    """

    def __init__(self,file , title = None ) -> None:
        self.file = file
        self.meta_data = 'insert by James'

        self.capture = cv2.VideoCapture(file)

        _ , self.image = self.cap.read()
        self.shape = self.image.shape
        self.width = self.shape[0]
        self.height = self.shape[1]

        self.title = title
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)

            
    def __repr__(self):
        """
        This method will implement the video title name as object representation.
        
        Returns
        ---------
            The title of video file.
            
        """
        return self.title
            

    def cleanup(self) -> None:
        """
        This method will release the current view of video object from RAM.
        """
        self.capture.release()

