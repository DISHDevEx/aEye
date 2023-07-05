from aEye import object_detection
import sys
import boto3
import os

# input_video_path = os.environ.get('input_video_path')
# output_video_path = os.environ.get('output_video_path')




def handler(event, context):

    print('Loading function')

    s3_client = boto3.client('s3')
    input_video = os.path.join("/tmp", os.path.basename("Untitled.mp4"))
    output_video = os.path.join("/tmp", os.path.basename("output_video.mp4"))

    s3_client.download_file("leto-dish", "original-videos/random-videos/Untitled.mp4", input_video)

    object_detection(os.path.basename("efficientdet_lite0.tflite"), input_video, output_video)

    s3_client.upload_file(output_video, "leto-dish", "object_detection/sample.mp4")

    return 'Hello from AWS Lambda using Python' + sys.version + '!'
