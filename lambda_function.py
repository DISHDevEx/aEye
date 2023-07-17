from aEye import object_detection
import sys
import boto3
import os

# input_video_path = os.environ.get('input_video_path')
# output_video_path = os.environ.get('output_video_path')


def handler(event, context):

    print('Empty lambda')

    return 'Hello from AWS Lambda using Python' + sys.version + '!'
