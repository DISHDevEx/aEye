import time
from aEye import object_detection
import sys
import json
import urllib.parse
import boto3
import os
#print(os.getcwd())
print(os.system('ls'))
print(os.getcwd())
print("imported")
models = ["/Users/pierce.lovesee/Desktop/mediapipe/models/efficientdet_lite0_float16.tflite",
          "/Users/pierce.lovesee/Desktop/mediapipe/models/efficientdet_lite0_float32.tflite",
          "/Users/pierce.lovesee/Desktop/mediapipe/models/efficientdet_lite0int8.tflite"]
# input_video_path = os.environ.get('input_video_path')
# output_video_path = os.environ.get('output_video_path')

# model_file = open('efficientdet_lite0.tflite', "rb")
# model_data = model_file.read()
# model_file.close()
print("read successfully")

def handler(event, context):
    print('Loading function')
    #os.chdir('/tmp')
    print(os.system('ls'))
    s3_client = boto3.client('s3')
    input_video = os.path.join("/tmp", os.path.basename("Untitled.mp4"))
    output_video = os.path.join("/tmp", os.path.basename("Untitled.mp4"))
    # input_video_path = "s3://leto-dish/original-videos/random-videos/Untitled.mp4"
    # output_video_path = "s3://leto-dish/object_detection/sample.mp4"
    s3_client.download_file("leto-dish", "original-videos/random-videos/Untitled.mp4", input_video)

    object_detection(f"var/task/" + os.path.basename("efficientdet_lite0.tflite"), input_video, "tmp/output_video.mp4")

    s3_client.upload_file("tmp/output_video.mp4",
                          "leto-dish", "object_detection/sample.mp4")





    # print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    # bucket = event['Records'][0]['s3']['bucket']['name']
    # key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    # try:
    #     response = s3.get_object(Bucket=bucket, Key=key)
    #     print("CONTENT TYPE: " + response['ContentType'])
    #     return response['ContentType']
    # except Exception as e:
    #     print(e)
    #     print(
    #         'Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(
    #             key, bucket))
    #     raise e

    return 'Hello from AWS Lambda using Python' + sys.version + '!'


#
#
# for model in models:
#     model_name = model.split('/')[-1]
#     output_path= "/Users/pierce.lovesee/Desktop/mediapipe/output_video/" + model_name + '.mp4'
#     t1 = time.time()
#     object_detection(model, "/Users/pierce.lovesee/Desktop/mediapipe/input_video/Untitled.mp4", output_path)
#     print(str(time.time() - t1) + " --- " + model_name)
