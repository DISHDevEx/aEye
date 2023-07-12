import os
import sys
import boto3
from aEye import object_detection
from aEye import pipeline
from aEye import Yolo
import ffmpeg
import subprocess


# input_video_path = os.environ.get('input_video_path')
# output_video_path = os.environ.get('output_video_path')
def reduce_resolution(input_file, output_file):
    """
    Reduces the resolution of a video by 10 times.
    input_file: Path to the input video file.
    output_file: Path to save the output video file.
    """
    ffmpeg_cmd = [
    'ffmpeg',
    '-i', input_file,
    '-vf', 'scale=iw/3.16227766:ih/3.16227766',
    output_file
    ]
    subprocess.run(ffmpeg_cmd)

# Example usage



def handler(event, context):

    print('Loading function')

    s3_client = boto3.client('s3')
    input_video = os.path.join("/tmp", os.path.basename("Untitled.mp4"))
    mp_output_video = os.path.join("/tmp", os.path.basename("mp_output_video.mp4"))
    #yolo_output_video = os.path.join("/tmp", os.path.basename("yolo_output_video.mp4"))

    s3_client.download_file("leto-dish", "original-videos/random-videos/demo_10_second_clip.mp4", input_video)

    object_detection(os.path.basename("efficientdet_lite0.tflite"), input_video, mp_output_video)

    #model = Yolo()
    #model.load_model_weight('yolov8s.pt')

    #pipeline(input_video, model, yolo_output_video)

    s3_client.upload_file(mp_output_video, "leto-dish", "object_detection/mp_sample.mp4")
    #s3_client.upload_file(yolo_output_video, "leto-dish", "object_detection/yolo_sample.mp4")

    reduceout = os.path.join("/tmp", os.path.basename("reduce_out.mp4"))

    reduce_resolution(input_video, reduceout)

    s3_client.upload_file(reduceout, "leto-dish", "object_detection/out_sample.mp4")

    return 'Hello from AWS Lambda using Python' + sys.version + '!'
