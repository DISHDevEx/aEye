"""
Module contains the Processor class that, loads, uploads, and facilitates all video processcing features.

"""

import boto3
import os
import cv2
import logging
from aEye.video import Video
from static_ffmpeg import run
import math
import subprocess
import tempfile

ffmpeg, ffprobe = run.get_or_fetch_platform_executables_else_raise()

class Processor:

    """
    Processor is the class that works as a labeler that tags and adds ffmpeg modification to video object.

    Methods
    -------

        resize_by_ratio(x_ratio, y_ratio,target) -> None:
            Add modification of resizing video by multiplying width by the ratio to video.

        trimmed_from_for(start, duration, target) -> None:
            Add modification of trimming video from start input for duration of seconds to video.

    """
    def __init__(self) -> None:
        self.video_list = []

        self._s3 = boto3.client('s3')

    def __init__(self) -> None:
        pass



    def add_label_resizing_by_ratio(self,video_list, x_ratio = .8, y_ratio = .8):
        """
        This method will add resizing modification to all target the video that will be multiplying the 
        width by x_ratio and height by y_ratio.
        Both values have to be non negative and non zero value.

        Parameters
        ----------
            video_list: list
                The list of desired videos that the users want to process.
            x_ratio: float
                The ratio for x/width value.
            y_ratio: float
                The ratio for y/height value.

        Returns
        ---------
            video_list: list
                The list of video that contains the resize modification.
            
        """


        #go to each video and add the resizing ffmpeg modification
        for video in video_list:

            video.get_meta_data()
            new_width = int(video.meta_data['width'] * x_ratio )
            new_height = int(video.meta_data['height'] * y_ratio )

            video.add_modification(f"-vf scale={math.ceil(new_width/2)*2}:{math.ceil(new_height/2)*2},setsar=1:1 ")

        logging.info(f"successfully added resizing mod to all video by ratio of {x_ratio} and {y_ratio}")
    
        return video_list
        
    def add_label_trimming_from_for(self,video_list, start, duration):
        """
        This method will add the trim modification with desired parameters to the video list.
        Parameters
        ----------
            video_list: list
                The list of desired videos that the users want to process.

            start: float
                The start time to trim the video from.

            duration: float
                The duration of time in seconds to trim the start of video. 

        Returns
        ---------
            video_list: list
                The list of video that contains the trim modification.
            
        """


        #generate the desired target list of videos to add modification
        #add the trim ffmpeg modification to all desired videos
        for video in video_list:
            video.add_modification(f"-ss {start} -t {duration} ")

        logging.info(f"successfully added trimming mod from {start} for {duration} seconds" )

        return video_list



    


