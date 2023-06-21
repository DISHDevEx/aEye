"""
Module contains the Video class that stores and represents video files as objects.

"""
import cv2
import boto3
import subprocess
import json
import numpy as np
from static_ffmpeg import run
ffmpeg, ffprobe = run.get_or_fetch_platform_executables_else_raise()
s3 = boto3.client("s3")
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
        self.bucket = bucket
        self.key = key
        self.title = title
        self.meta_data = None
        self.modification = ''
 
    def __repr__(self):
        """
        This method will implement the video title name as object representation.
        
        Returns
        ---------
            The title of video file.
            
        """
        return self.title
    
    def __eq__(self, target):
        return self.title == target
    
    

    def cleanup(self):
        """
        This method will release the current view of video object from RAM
        """
        self.cap.release()

    
    
    def get_meta_data(self):

        if self.meta_data is None:
            cmd = f"{ffprobe} -hide_banner -show_streams -v error -print_format json -show_format -i '{self.get_presigned_url()}'"
            out = subprocess.check_output(cmd, shell=True)
            out = json.loads(out)
            self.meta_data = out['streams'][0]
            
        return self.meta_data



    def get_presigned_url(self, time = 60):
        url = s3.generate_presigned_url( ClientMethod='get_object', Params={ 'Bucket': self.bucket, 'Key': self.key} ,ExpiresIn=time)
        return url
    
    def add_mod(self, mod):
        self.modification += mod

    def reset_mod(self):

        self.modification = ''

    def get_modification(self):
        return self.modification
    
    def get_output_title(self):
        result = 'modified/'
        if 'scale' in self.modification:
            result += "resized_"
        if '-ss' in self.modification:
            result += "trimmed_"
        return result + self.title