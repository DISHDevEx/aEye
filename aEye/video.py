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
    Video class that encapsulates all necessary video information.
    Also contains some useful utility like the ability to grab frames, process
    video clips, trim them down, crop, etc.
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


        add_label(self, mod) -> None:
            Add ffmpeg label to video object.

        reset_label() -> None:
            Reset and remove all labels.

        get_label(self) -> string:
            Get ffmpeg label from video objects.
        
    """


    def __init__(self,file = None, bucket = None  , key = None,  title = None ) -> None:
        self.file = file
        self.bucket = bucket
        self.key = key
        self.title = title
        self.meta_data = None
        self.label = ''
 
    def __repr__(self):
        """    title: string
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
        
    def extract_metadata(self):
        """
        Probably the most important method, probes a video passed with a
        file path and returns a json dictionary full of metadata. Video metadata lives in
        json['streams'][0] because it is the first channel and the dictionary splits streams from error
        Returns
        -------
        String of JSON Dictionary full of video metadata
        """
        if self.meta_data is None:
            command = f"{ffprobe} -hide_banner -show_streams -v error -print_format json -show_format -i '{self.file}'"
            out = subprocess.check_output(command, shell=True).decode("utf-8")
            json_data = json.loads(out)
            self.meta_data = json_data
            return json_data

    def get_codec(self):
        """
        Returns the video codec as a string.
        """
        if self.meta_data is not None:
            return self.meta_data["streams"][0]["codec_name"]
        else:
            self.meta_data = self.get_metadata()
            return self.meta_data["streams"][0]["codec_name"]

    def get_duration(self):
        """
        Returns the video duration as a string.
        """
        if self.meta_data is not None:
            return self.meta_data["streams"][0]["duration"]
        else:
            self.meta_data = self.get_metadata()
            return self.meta_data["streams"][0]["duration"]

    def get_num_frames(self):
        """
        Returns # of frames in video as a string.
        """
        if self.meta_data is not None:
            return self.meta_data["streams"][0]["nb_frames"]
        else:
            self.meta_data = self.extract_metadata()
            return self.meta_data["streams"][0]["nb_frames"]

    def get_file(self):
        """
        Returns the file path as a string.
        """
        return self.file

    def get_width(self):
        """
        Returns the pixel width of the video associated with the current video object.
        """
        if self.meta_data is not None:
            return self.meta_data["streams"][0]["width"]
        else:
            self.meta_data = self.extract_metadata()
            return self.meta_data["streams"][0]["width"]

    def get_height(self):
        """
        Returns the pixel height of the video associated with the current video object.
        """
        if self.meta_data is not None:
            return self.meta_data["streams"][0]["height"]
        else:
            self.meta_data = self.extract_metadata()
            return self.meta_data["streams"][0]["height"]

    
    def __bool__(self):
        """
        This method will check whether the video file can be readed properly.
        
        Returns
        ---------
            condition: boolean
                Boolean state of whether the video can be readed properly.
        
        """
        return cv2.VideoCapture(self.get_presigned_url(time = 2)).read()[0]


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
    
    def add_label(self, label):
        """
        This method will add ffmpeg label to the video.
        """
        self.label += label

    def reset_label(self):
        """
        This method will reset all ffmpeg label to empty.
        """

        self.label = ''

    def get_label(self):
        """
        This method will return the all ffmpeg label from the video.
        """
        return self.label
    
    def get_output_title(self):
        """
        This method will create the output title for video so the users can know all the labels that happen to the video.
        (I have a better implementation of this, it will be in the next pr after james adds all of the features.)

        Returns
        ---------
            result: string
                The output title of video.
        """

        result = ''
        if 'scale' in self.label:
            result += "resized_"
        if '-ss' in self.label:
            result += "trimmed_"
        return result + self.title

