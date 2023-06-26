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
            The name of the bucket that video exists in.


        key: string
            The key that associates with the video file.





    Methods
    -------
    
        __repr__() -> string:
            A native python method to represent the Video class.

        __eq__() -> string:
            A native python method to add comparison functionality.

        __bool__() -> boolean:
            A native python method to see whether video can be readed properly.

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

        set_output_location(self) -> None:
            Set output file location for video objects.
            
        get_output_location(self) -> string:
            Get output file location from video objects.

        
    """


    def __init__(self,file = None, bucket = None  , key = None,  title = None ) -> None:
        self.file = file
        self.bucket = bucket
        self.key = key
        self.title = title
        self.meta_data = None
        self.modification = ''
        self.output_location = None
 
    def __repr__(self):
        """
        This method will implement the video title name as object representation.
        
        Returns
        ---------
            title: string
                The title of video file.
            
        """
        return self.title
    
    def __eq__(self, target):
        """
        This method will implement comparison functionality for video.
        This will compare between video's title.

        Returns
        ---------
            comparison: boolean
                Boolean state of whether the target's title is same self's title.
            

        """

        return self.title == target
    
    def __bool__(self):
        """
        This method will check whether the video file can be readed properly.
        
        Returns
        ---------
            condition: boolean
                Boolean state of whether the video can be readed properly.
        
        """
        return cv2.VideoCapture(self.get_presigned_url(time = 2)).read()[0]
    


    def get_meta_data(self):
        """
        This method will run ffprobe to cmd and return the meta data of the video.

        Returns
        ---------
            meta_data: dictionary
                The dictionary of meta data.

        """
        if self.meta_data is None:
            cmd = f"{ffprobe} -hide_banner -show_streams -v error -print_format json -show_format -i {self.get_presigned_url()}"
            out = subprocess.check_output(cmd, shell=True)
            out = json.loads(out)
            self.meta_data = out['streams'][0]
            
        return self.meta_data



    def get_presigned_url(self, time = 60):
        """
        This method will return the presigned url of video file from S3. 
        If the video file is from local machine then it will return the local path of the video file.

        Returns
        ---------
            url: string
                The presigned url or file path of the video file.

        """

        if self.file is None:
            url = s3.generate_presigned_url( ClientMethod='get_object', Params={ 'Bucket': self.bucket, 'Key': self.key} ,ExpiresIn=time)
            return f"'{url}'"
        return self.file
    
    def add_modification(self, mod):
        """
        This method will add ffmpeg modification to the video.
        """
        self.modification += mod

    def reset_modification(self):
        """
        This method will reset all ffmpeg modification to empty.
        """

        self.modification = ''

    def get_modification(self):
        """
        This method will return the all ffmpeg modification from the video.
        """
        return self.modification
    
    def get_output_title(self):
        """
        This method will create the output title for video so the users can know all the modifications that happen to the video.
        (I have a better implementation of this, it will be in the next pr after james adds all of the features.)

        Returns
        ---------
            result: string
                The output title of video.
        """

        result = ''
        if 'scale' in self.modification:
            result += "resized_"
        if '-ss' in self.modification:
            result += "trimmed_"
        return result + self.title


    def set_output_location(self, path):
        """
        This method is a setter for where the output video will be located.
        """
        self.output_location = path

    def get_output_location(self):
        """
        This method is a get for where the output video is located.
        Returns
        ---------
            result: string
                The output location of the video file.
        """

        return self.output_location



            


