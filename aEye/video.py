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

        bucket: string
            

        key: string




    Methods
    -------
    
        __repr__() -> string:
            A native python method to represent the Video class.

        __eq__() -> string:
            A native python method to add comparison functionality

        cleanup() -> None:
            Clean up memory from cv2 video capture.

        get_meta_data() -> None:
            Retrieve the meta data from video.

        get_presigned_url(time) -> string:
            Retrieve the url for video file from S3 bucket. 

        add_modification(self, mod) -> None:
            Add ffmpeg modification to video object.

        reset_modification() -> None:
            Reset and remove all modifications.

        get_modification(self) -> string:
            Get ffmpeg modification from video objects.

        
    """


    def __init__(self,file = None, bucket = None  , key = None,  title = None ) -> None:
        self.file = file
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
            cmd = f"{ffprobe} -hide_banner -show_streams -v error -print_format json -show_format -i {self.get_presigned_url()}"
            out = subprocess.check_output(cmd, shell=True)
            out = json.loads(out)
            self.meta_data = out['streams'][0]
            
        return self.meta_data



    def get_presigned_url(self, time = 60):
        if self.file is None:

            url = s3.generate_presigned_url( ClientMethod='get_object', Params={ 'Bucket': self.bucket, 'Key': self.key} ,ExpiresIn=time)
            return f"'{url}'"
        return self.file
    
    def add_mod(self, mod):
        self.modification += mod

    def reset_modification(self):

        self.modification = ''

    def get_modification(self):
        return self.modification
    
    def get_output_title(self):
        result = ''
        if 'scale' in self.modification:
            result += "resized_"
        if '-ss' in self.modification:
            result += "trimmed_"
        return result + self.title