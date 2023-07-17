"""
Module contains the pipeline to faciliate and apply a yolo model to predict frame by frame by using cv2.
This pipeline will call visualize_yolo to visualize the result from the prediction.
"""

from .visualize import visualize_yolo
import cv2

def pipeline(input_video,  model, output_video ):

    '''  
    This functions opens the video frame by frame and applies yolo model to each frame.
    
    Parameters
    ----------
        input_video: string
            The path for the video file or its presigned url if video is in s3. 

        model: YOLO
            The desired yolo model with its weight.

        output_video: string
            The path name 
    Returns
    ---------
        None
    '''

    cap = cv2.VideoCapture(input_video)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video, fourcc, fps, (frame_width, frame_height))
    
    while (cap.isOpened()):

        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:
            # change the channel in the format that yolo accepts
            im2 = frame[..., ::-1]

            # Perform object detection on the video frame.
            detection_result = model.predict_(im2, verbose = False, save=False, save_txt = False)

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


