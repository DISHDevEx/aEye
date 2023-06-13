"""
Module contains the Video class that stores and represents video files as objects.

"""
import cv2
import numpy as np

class Video:
    """
<<<<<<< HEAD
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


=======
    @:constructor file, title
        file is the path name for the video file,
        title is the title of the video if given
>>>>>>> 4b229f3 (add more comments)
    """

    def __init__(self,file , title = None ) -> None:
        self.file = file
        self.meta_data = 'insert by James'

<<<<<<< HEAD
        self.capture = cv2.VideoCapture(file)

        _ , self.image = self.capture.read()
=======
        self.cap = cv2.VideoCapture(file)
        _ , self.image = self.cap.read()
>>>>>>> 4b229f3 (add more comments)
        self.shape = self.image.shape
        self.width = self.shape[0]
        self.height = self.shape[1]

        self.title = title
<<<<<<< HEAD
        self.fps = self.capture.get(cv2.CAP_PROP_FPS)

            
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
=======
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.frame_array = []


    def set_dim(self,dim):
        self.shape = dim
        self.width = self.shape[0]
        self.height = self.shape[1]

        
    def set_frame_array(self, array):
        self.frame_array = array

    def get_frame_array(self):
        return self.frame_array

    def write_video(self,path):
        """write output video """
>>>>>>> 18f9ed4 (modified processor into a class)

        fourcc = cv2.VideoWriter.fourcc(*'mp4v')
        out = cv2.VideoWriter(path, fourcc, self.fps, (self.width,self.height))

