import boto3
import cv2
from aEye.video import Video
from aEye.auxiliary import Aux
from aEye.labeler import Labeler
from aEye.extractor import Extractor

def handler(event, context):
    print("Running aEye lambda test!")
    aux = Aux()
    video_list = aux.load_s3(bucket = 'aeye-data-bucket', prefix = 'input_video/')
    label = Labeler()
    extract = Extractor()
    print("Videos and Util loaded")
    label.change_resolution(video_list, '720p')
    label.change_fps(video_list, 10)
    out = aux.execute_label_and_write_local(video_list[1], '/tmp/')
    print("Videos executed")
    aux.upload_s3(out, bucket='aeye-data-bucket', prefix='modified/')
    retval = "Videos Uploaded!"
    return retval
