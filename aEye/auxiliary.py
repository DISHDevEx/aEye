from aEye.video import Video
import boto3
import tempfile
import os
import subprocess
import logging
from static_ffmpeg import run
from aEye.processor import Processor
ffmpeg, ffprobe = run.get_or_fetch_platform_executables_else_raise()

class Aux():

    def __init__(self):

        self._s3 = boto3.client('s3')
        self._temp_fold = tempfile.mkdtemp(dir= "")

    def load_s3(self,bucket , prefix):

        video_list = []
        result = self._s3.list_objects(Bucket = bucket, Prefix = prefix)
        for i in result["Contents"]:
            #When we request from S3 with the input parameters, the prefix folder will also pop up as a object.
            #This if-statement is to skip over the folder object since we are only interested in the video files.
            if i["Key"] == prefix:
                continue

            title = i["Key"].split(prefix)[1]
            video_list.append(Video(bucket = bucket,key= i["Key"], title = title))
        return video_list


    def load_local(self,path):
        video_list = []
        if os.path.isdir(path):
            files = os.listdir('data')
            video_list = [ Video(file=  path + i, title=i) for i in files if (i !='.ipynb_checkpoints' and i != '.gitkeep' ) ]


        else:
            dummy = path.replace('/', ' ').strip()
            title = dummy.split(' ')[-1]
            video_list.append(Video(file = path, title = title))

        return video_list

    def write(self, video_list):
        for video in video_list:
            #This if statement will skip over any untouched videos.
            if video.get_modification() != "":
                command = f"{ffmpeg} -i {video.get_presigned_url()} {video.get_modification()} {self._temp_fold}/{video.get_output_title()}"
                subprocess.run(command, shell=True)
                print(command)

    def upload_s3(self, video_list, bucket ,prefix =  'modified/'):
        s3 = boto3.client('s3')
        for video in video_list:
            if video.get_modification() != "":

                path = self._temp_fold +'/'+video.get_output_title()
                response = s3.upload_file( path, bucket, prefix  + video.get_output_title())

                #delete all file from RAM and local machine
                os.remove(path)
                #video.cleanup()

        logging.info("successfully upload the output files and remove them from local machine")
        
        print("successfully upload the output files S3 bucket: s3://aeye-data-bucket/modified/")
        print("successfully remove the output file from local machine")

    def upload(self,path):
        pass