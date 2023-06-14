import boto3
import os
import cv2
import logging
from aEye.video import Video

class Processor:

    """
    This Processor is the class that works act a pipeline to load, process, and upload all video from S3 bucket

    """
    def __init__(self) -> None:
        self.video_list = []
        self.pipeline = ['ffmpeg']

    
    def load(self, bucket=  'aeye-data-bucket', prefix='input_video/'):
        """
        This function will load the video data from S3 and save them 
        into a list of video class. 

        input:
            bucket: STRING
                this is the bucket name
            prefix: STRING
                this is the folder in the bucket
        """

        s3 = boto3.client('s3')
        result = s3.list_objects(Bucket = bucket, Prefix = prefix)

        for i in result["Contents"]:

            if i["Key"] == prefix:
                continue

            title = i["Key"].split(prefix)[1]
            #in order to convert video file from S3 to cv2 video class, we need its url
            url = s3.generate_presigned_url( ClientMethod='get_object', Params={ 'Bucket': bucket, 'Key': i["Key"] } ,ExpiresIn=5)
            self.video_list.append(Video(url, title))

        logging.info(f"Successfully loaded video data from {bucket}")
        logging.info(f"There are total of {len(self.video_list)} video files")

        print(f"Successfully loaded video data from {bucket}")
        print(f"There are total of {len(self.video_list)} video files")


    def resize_by_ratio(self, x_ratio = .8, y_ratio = .8):
        """
        this method will resize the current video by multiplying 
        the current x and y by the input x_ratio 

        input: 
            x_ratio: FLOAT
                the ratio for x/width value
            y_ratio: FLOAT
                the ratio for y/height value

            
        both has to be non negative and non zero value

        currently version also write the resized video

        """

        #go to each video to apply resizing
        for video in self.video_list:

            new_width = int(video.width * x_ratio )
            new_height = int(video.height * y_ratio )
            dim = (new_width, new_height)
            
            fourcc = cv2.VideoWriter.fourcc(*'mp4v')
            out = cv2.VideoWriter('data/out_put_' +video.title, fourcc, 30.0, dim)
            
            #loop to each frames to resize
            while True:
                _ ,image = video.cap.read()

                if image is None:
                    break

                resized = cv2.resize(image , dim, interpolation = cv2.INTER_AREA)
                out.write(resized)

            out.release()
            video.cleanup()


            #video.set_dim(dim)
        logging.info(f"successfully resized all video by ratio of {x_ratio} and {y_ratio}" )
        print(f"successfully resized all video by ratio of {x_ratio} and {y_ratio}" )

    def load_and_resize(self, bucket=  'aeye-data-bucket', prefix='input_video/', x_ratio = .8, y_ratio = .8):

        self.load(bucket,prefix)
        self.resize_by_ratio(x_ratio,y_ratio)

    def upload(self, bucket=  'aeye-data-bucket'):
        """
        this method will push all video output to the S3 bucket

        input:
            bucket: STRING
            the desired bucket name
        
        """

        s3 = boto3.client('s3')
        for video in self.video_list:

            path = 'data/out_put_' + video.title
            response = s3.upload_file( path, bucket,  path)

            #delete all file from RAM and local machine
            os.remove(path)
            video.cleanup()

        logging.info("successfully upload the output files and remove them from local machine")
        print("successfully upload the output files and remove them from local machine")





