"""
Module contains the pipeline to faciliate and  apply a yolo model to predict frame by frame by using cv2.
This pipeline will call visualize_yolo to visualize the result from the prediction.
"""

from .visualize import visualize_yolo
import cv2

def pipeline(input_video,  model, output_video ):
    cap = cv2.VideoCapture(input_video)
    frame_index = 0
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
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
            # Display the resulting frame
            im2 = frame[..., ::-1]

            # Calculate the timestamp of the current frame
            frame_timestamp_ms = int(1000 * frame_index / x)
            frame_index += 1
            # Perform object detection on the video frame.
            
            
            detection_result = model.predict_(im2,save_to_json = False,  verbose = False, save=False, save_txt = False)
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
