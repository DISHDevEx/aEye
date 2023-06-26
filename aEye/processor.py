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
    Processor is the class that works act a pipeline to load, process, and upload all video from S3 bucket.

    Attributes
    ----------
        video_list: list
            A list to append the Video classes.

        _s3: botocore.client.S3
            An internal variable to talk to S3.

        __temp_fold: string
            An internal variable for temp folder path


    Methods
    -------
        load(bucket, prefix) -> list[Video]:
            Loads in video files as Video classes into a list from S3.


        resize_by_ratio(x_ratio, y_ratio,target) -> None:
            Add modification of resizing video by multiplying width by the ratio to video

        load_and_resize(bucket, prefix, x_ratio, y_ratio) -> None:
            Load in video files and resize by the x and y ratio.

        trimmed_from_for(start, duration, target) -> None:
            Add modification of trimming video from start input for duration of seconds to video

        upload(bucket) -> None:
            Upload the modified video to S3.

        target_list(target) -> List:
            Generate a desired list of video based on the target parameter.

        execute() -> None:
            Execute and run the video's modifications and write the video to temp folder.

        clean_temp() -> None:
            Clean up the temp folder.
    """
    def __init__(self) -> None:
        self.video_list = []

        self._s3 = boto3.client('s3')

    def __init__(self) -> None:
        self.video_list = []
        self._s3 = boto3.client('s3')
        self._temp_fold = tempfile.mkdtemp(dir= "")

    
    def load(self, local_path = None, bucket=  'aeye-data-bucket', prefix='input_video/') -> list:
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


        if local_path is None:
            result = self._s3.list_objects(Bucket = bucket, Prefix = prefix)

            for i in result["Contents"]:


                        
                #When we request from S3 with the input parameters, the prefix folder will also pop up as a object.
                #This if-statement is to skip over the folder object since we are only interested in the video files.
                if i["Key"] == prefix:
                    continue

                title = i["Key"].split(prefix)[1]

                self.video_list.append(Video(bucket = bucket,key= i["Key"], title = title))

            logging.info(f"Successfully loaded video data from {bucket}")
            logging.info(f"There are total of {len(self.video_list)} video files")

        
        elif os.path.isdir(local_path):
            files = os.listdir('data')
            self.video_list = [ Video(file=  local_path + i, title=i) for i in files if (i !='.ipynb_checkpoints' and i != '.gitkeep' ) ]


        else:
            dummy = local_path.replace('/', ' ').strip()
            title = dummy.split(' ')[-1]
            self.video_list.append(Video(file = local_path, title = title))

        return self.video_list


    def resize_by_ratio(self, x_ratio = .8, y_ratio = .8, target = ["*"]):
        """
<<<<<<< HEAD
        This method will resize the video by multiplying the width by x_ratio and height by y_ratio.
=======
        This method will add resizing modification to all target the video that will be multiplying the 
        width by x_ratio and height by y_ratio.
>>>>>>> c48b381 (stashing temp dosstring)
        Both values have to be non negative and non zero value.

        Parameters
        ----------
            x_ratio: float
                The ratio for x/width value.
            y_ratio: float
                The ratio for y/height value.
<<<<<<< HEAD
=======
            target: list
                The list of desired videos that the users want to process.
>>>>>>> c48b381 (stashing temp dosstring)

        
        """

        #generate the desired target list of videos to add modification
        target_list = self.target_list(target)

<<<<<<< HEAD
        #This will loop to the list of videos to apply the resizing feature. 
        for video in self.video_list:
=======
        #go to each video and add the resizing ffmpeg modification
        for video in target_list:
>>>>>>> c48b381 (stashing temp dosstring)

            video.get_meta_data()
            new_width = int(video.meta_data['width'] * x_ratio )
            new_height = int(video.meta_data['height'] * y_ratio )

            video.add_modification(f"-vf scale={math.ceil(new_width/2)*2}:{math.ceil(new_height/2)*2},setsar=1:1 ")

        logging.info(f"successfully added resizing mod to all video by ratio of {x_ratio} and {y_ratio}")
        
    def trimmed_from_for(self,start, duration, target = ["*"]):
        """
        This method will push all modified videos to the S3 bucket and delete all video files from local machine.

        Parameters
        ----------
            start: float
                The start time to trim the video from.

            duration: float
                The duration of time in seconds to trim the start of video. 

            target: list
                The list of desired videos that the users want to process.
        """

        #generate the desired target list of videos to add modification
        target_list = self.target_list(target)

        #add the trim ffmpeg modification to all desired videos
        for video in target_list:
            video.add_modification(f"-ss {start} -t {duration} ")

        logging.info(f"successfully added trimming mod from {start} for {duration} seconds" )


    def load_and_resize(self, bucket=  'aeye-data-bucket', prefix='input_video/', x_ratio = .8, y_ratio = .8, target = ["*"]):
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
            target: list
                The list of desired videos that the users want to process.
        """

        self.load(bucket = bucket,prefix = prefix)
        self.resize_by_ratio(x_ratio,y_ratio, target = target)

    def upload(self, bucket=  'aeye-data-bucket') -> None:
        """
        This method will push all modified videos to the S3 bucket and delete all video files from local temp folder.

        Parameters
        ----------
            bucket: string
                The bucket name/location to upload on S3.
        """


        for video in self.video_list:
            if video.get_modification() != "":

                path = self._temp_fold +'/'+video.get_output_title()
                response = s3.upload_file( path, bucket, 'modified/' + video.get_output_title())

                #delete all file from RAM and local machine
                os.remove(path)
                #video.cleanup()

        logging.info("successfully upload the output files and remove them from local machine")

        print("successfully upload the output files S3 bucket: s3://aeye-data-bucket/modified/")
        print("successfully remove the output file from local machine")

    def target_list(self, target):

        """
        This method will get all desired videos from the video list. 

        Parameters
        ----------
            target: list
                The list of desired videos that the users want to process.

        Returns
        -------
            video_list: list
                The list of desired video from the video list.
        """

        if target != ["*"]:
            video_list = [ i for i in self.video_list if i in target]
            return video_list
        
        return self.video_list

    def execute(self):

        """
        This method will execute and write new videos based on all videos that contain ffmpeg modifications. 
        """
        
        for video in self.video_list:
            #This if statement will skip over any untouched videos.
            if video.get_modification() != "":
                command = f"{ffmpeg} -i {video.get_presigned_url()} {video.get_modification()} {self._temp_fold}/{video.get_output_title()}"
                subprocess.run(command, shell=True)
                print(command)

    def clean_temp(self):
        """
        This method will delete the temp folder from local machine. 
        """
        os.rmdir(self._temp_fold)


