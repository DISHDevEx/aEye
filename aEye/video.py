"""
Module contains the Video class that stores and represents video files as objects.

"""
import cv2
impoty boto3
import numpy as np


s3 = boto3.client('s3')
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

    def __init__(self, bucket , key,  title = None ) -> None:
        

        '''
        self.meta_data = 'insert by James'

        self.capture = cv2.VideoCapture(file)

        _ , self.image = self.capture.read()
        self.shape = self.image.shape
        self.width = self.shape[0]
        self.height = self.shape[1]

        self.title = title
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
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.frame_array = []
        '''
        self.bucket = bucket
        self.key = key
        self.title = title
        self.meta_data = None
        self.modification = ''
 
            
    def write_video(self,path):

        """
        This method will write the video into local machine

        input:
            path: STRING
            the desired for video file to be at
        
        """

        fourcc = cv2.VideoWriter.fourcc(*'mp4v')
        out = cv2.VideoWriter(path, fourcc, self.fps, (self.width,self.height))

    def cleanup(self):
        """
        This method will release the current view of video object from RAM
        """
        self.cap.release()

    def update(self,file, title):
        self.file = file
        self.cap = cv2.VideoCapture(file)
        self.title = title
    
    
    def get_meta_data(self):
        self.meta_data = [1000,400]


    def get_presigned_url(self):
        url = s3.generate_presigned_url( ClientMethod='get_object', Params={ 'Bucket': self.bucket, 'Key': self.key} ,ExpiresIn=60)
        return url
    
    def add_mod(self, mod):
        self.modification += mod

    def reset_mod(self):
        self.modification = ''

    def get_modification(self):
        return self.modification
    
    def get_output_title(self):
        result = ''
        if '-r' in self.modification:
            result += "resized"
        return result + self.title