import os
import sys
import boto3
from aEye import object_detection
from aEye import pipeline
from aEye import Yolo
import subprocess
import time
from aEye import Video
import urllib.parse

import static_ffmpeg
import os

static_ffmpeg.add_paths()
os.system("ffmpeg -i var/task/test_video.mp4  -ss 0 -t 2  video.mp4 ")



def handler(event, context):

    print('Loading function')

    s3_client = boto3.client('s3')

    yolo_model = Yolo()
    yolo_model.load_model_weight('yolov8n.pt')

    mp_yolo = os.path.basename("efficientdet_lite0.tflite")


    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    try:
        video = Video(bucket=bucket, key=key)

        yolo_output_video = os.path.join("/tmp", os.path.basename('yolo_' + video.get_title()))
        mp_output_video = os.path.join("/tmp", os.path.basename('mp_' + video.get_title()))


        object_detection(mp_yolo, video.get_presigned_url(), mp_output_video)
        pipeline(video.get_presigned_url(), yolo_model, yolo_output_video)

        s3_client.upload_file(yolo_output_video, "leto-dish", f"object_detection/yolo_{video.get_title()}")
        s3_client.upload_file(mp_output_video, "leto-dish", f"object_detection/mp_{video.get_title()}")
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e


    return 'Hello from AWS Lambda using Python' + sys.version + '!'
