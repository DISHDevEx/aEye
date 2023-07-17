"""
Module contains the pipeline to faciliate and  apply a yolo model to predict frame by frame by using cv2.
This pipeline will call visualize_yolo to visualize the result from the prediction.
"""

from .visualize import visualize_yolo
import cv2

import boto3
import os 

def pipeline(input_video,  model, output_video ):

    cap = cv2.VideoCapture(input_video)
    x = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video, fourcc, x, (frame_width, frame_height))
    
    result = []

    while (cap.isOpened()):

        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:
            # change the channel in the format that yolo accepts
            im2 = frame[..., ::-1]

            # Perform object detection on the video frame.
            detection_result = model.predict_(im2, verbose = False, save=False, save_txt = False, device = 'cpu')
            result.append(detection_result)

            copy_image = frame.copy()
            
            annotated_image = visualize_yolo(copy_image, detection_result)
            out.write(annotated_image)

        # Break the loop
        else:
            break
    # When everything done, release
    # the video capture object
    cap.release()
    out.release()

    return result



def downloadDirectoryFroms3(bucketName, remoteDirectoryName):
    s3_resource = boto3.resource('s3')
    bucket = s3_resource.Bucket(bucketName) 
    for obj in bucket.objects.filter(Prefix = remoteDirectoryName):
        if not os.path.exists(os.path.dirname(obj.key)):
            os.makedirs(os.path.dirname(obj.key))
        bucket.download_file(obj.key, obj.key) # save to same path