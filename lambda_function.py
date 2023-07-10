from aEye import object_detection
import sys
import boto3
import os
from aEye import pipeline
from aEye import Yolo

# input_video_path = os.environ.get('input_video_path')
# output_video_path = os.environ.get('output_video_path')


def handler(event, context):

    print('Loading function')

    s3_client = boto3.client('s3')
    input_video = os.path.join("/tmp", os.path.basename("Untitled.mp4"))
    mp_output_video = os.path.join("/tmp", os.path.basename("mp_output_video.mp4"))
    yolo_output_video = os.path.join("/tmp", os.path.basename("yolo_output_video.mp4"))

    s3_client.download_file("leto-dish", "original-videos/random-videos/Untitled.mp4", input_video)

    object_detection(os.path.basename("efficientdet_lite0.tflite"), input_video, mp_output_video)

    model = Yolo()
    model.load_model('yolov8s.pt')

    pipeline(input_video, model, yolo_output_video)

    s3_client.upload_file(mp_output_video, "leto-dish", "object_detection/mp_sample.mp4")
    s3_client.upload_file(yolo_output_video, "leto-dish", "object_detection/yolo_sample.mp4")

    return 'Hello from AWS Lambda using Python' + sys.version + '!'
