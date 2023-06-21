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

ffmpeg, ffprobe = run.get_or_fetch_platform_executables_else_raise()

class Processor:

    """
    Processor is the class that works act a pipeline to load, process, and upload all video from S3 bucket.

    Attributes
    ----------
        video_list: list
            A list to append the Video classes.

        _s3: botocore.client.S3
            An internal variable to talk to S3.


    Methods
    -------
        load(bucket, prefix) -> list[Video]:
            Loads in video files as Video classes into a list from S3.


        resize_by_ratio(x_ratio, y_ratio) -> None:
            Resize video by multiplying width by the ratio.

        load_and_resize(bucket, prefix, x_ratio, y_ratio) -> None:
            Load in video files and resize by the x and y ratio.

        upload(bucket) -> None:
            Upload the modified video to S3.
   
    """
    def __init__(self) -> None:
        self.video_list = []

        self._s3 = boto3.client('s3')

    def __init__(self) -> None:
        self.video_list = []
        self._s3 = boto3.client('s3')

    
    def load(self, bucket=  'aeye-data-bucket', prefix='input_video/'):
        """
        This method will load the video files from S3 and save them 
        into a list of video classes. 

         Parameters
        ----------
            bucket: string
                The bucket name to path into S3 to get the video files.
            prefix: string
                The folder name where the video files belong in the S3 bucket.

        Returns
        -------
            video_list: list
                The list of all video files loaded from S3 bucket.
        """

        result = self._s3.list_objects(Bucket = bucket, Prefix = prefix)

        for i in result["Contents"]:


                       
            #When we request from S3 with the input parameters, the prefix folder will also pop up as a object.
            #This if-statement is to skip over the folder object since we are only interested in the video files.
            if i["Key"] == prefix:
                continue

            title = i["Key"].split(prefix)[1]

            self.video_list.append(Video(bucket, i["Key"], title))



        logging.info(f"Successfully loaded video data from {bucket}")
        logging.info(f"There are total of {len(self.video_list)} video files")

        return self.video_list


    def resize_by_ratio(self, x_ratio = .8, y_ratio = .8, target = "all"):
        """
        This method will resize the video by multiplying the width by x_ratio and height by y_ratio.
        Both values have to be non negative and non zero value.

        Parameters
        ----------
            x_ratio: float
                The ratio for x/width value.
            y_ratio: float
                The ratio for y/height value.

        
        """
        target_list = self.target_list(target)

        #go to each video to apply resizing
        for video in target_list:

            video.get_meta_data()
            new_width = int(video.meta_data['width'] * x_ratio )
            new_height = int(video.meta_data['height'] * y_ratio )

            video.add_modification(f"-vf scale={math.ceil(new_width/2)*2}:{math.ceil(new_height/2)*2},setsar=1:1 ")

        logging.info(f"successfully resized all video by ratio of {x_ratio} and {y_ratio}" )
        
    def trimmed_from_for(self,start, duration, target = "all"):

        target_list = self.target_list(target)

        for video in target_list:

            video.add_modification(f"-ss {start} -t {duration} ")
        print(f"Trimming from {start} for {duration} seconds" )


    def load_and_resize(self, bucket=  'aeye-data-bucket', prefix='input_video/', x_ratio = .8, y_ratio = .8) -> None:
        """
        This method will call on load() and resize_by_ratio() methods to load and resize by the input parameters.
        Both values have to be non negative and non zero value.

        Parameters
        ----------
            bucket: string
                The bucket name to path into S3 to get the video files.
            prefix: string
                The folder name where the video files belong in the S3 bucket.

            x_ratio: float
                The ratio for x/width value.
            y_ratio: float
                The ratio for y/height value.
        """


        self.load(bucket,prefix)
        self.resize_by_ratio(x_ratio,y_ratio)

    

    def upload(self, bucket=  'aeye-data-bucket'):
        """
        This method will push all modified videos to the S3 bucket and delete all video files from local machine.

        Parameters
        ----------
            bucket: string
                The bucket name/location to upload on S3.
        """


        for video in self.video_list:

            path = 'modified/output_' + video.title
            response = self._s3.upload_file( path, bucket,  path)

            #This will delete all file from RAM and local machine.
            os.remove(path)
            #video.cleanup()

        logging.info("successfully upload the output files and remove them from local machine")

        print("successfully upload the output files S3 bucket: s3://aeye-data-bucket/modified/")
        print("successfully remove the output file from local machine")

    def target_list(self, target):
        
        if target != 'all':
            result = [ i for i in self.video_list if i in target]
            return result
        return self.video_list

    def execute(self):
        
        for video in self.video_list:
            command = f"{ffmpeg} -i '{video.get_presigned_url()}' " + video.get_modification() + video.get_output_title()
            subprocess.run(command, shell=True)
            print(command)



