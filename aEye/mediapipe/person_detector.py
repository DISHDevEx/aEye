import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import numpy as np
from visulize import visualize
BaseOptions = mp.tasks.BaseOptions
ObjectDetector = mp.tasks.vision.ObjectDetector
ObjectDetectorOptions = mp.tasks.vision.ObjectDetectorOptions
VisionRunningMode = mp.tasks.vision.RunningMode





# Check if camera opened successfully





# #
options = ObjectDetectorOptions(
    base_options=BaseOptions(model_asset_path='/Users/hamza.khokhar/Desktop/mediapipe_models/efficientdet_lite0.tflite'),
    max_results=5,
    running_mode=VisionRunningMode.VIDEO)


with ObjectDetector.create_from_options(options) as detector:
    cap = cv2.VideoCapture('/Users/hamza.khokhar/Desktop/mediapipe_models/test.mp4')
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    x = cap.get(cv2.CAP_PROP_FPS)
    if (cap.isOpened() == False):
        print("Error opening video file")

        # Read until video is completed
    frame_index = 0
    while (cap.isOpened()):

        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:
            # Display the resulting frame
            cv2.imshow('Frame', frame)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
            # Calculate the timestamp of the current frame

            print(x)
            frame_timestamp_ms = int(1000 * frame_index / x)
            print(frame_timestamp_ms)
            frame_index += 1
            #print(i)
            # Perform object detection on the video frame.
            detection_result = detector.detect_for_video(mp_image, frame_timestamp_ms)
            print(detection_result)
            image_copy = np.copy(mp_image.numpy_view())
            annotated_image = visualize(image_copy, detection_result)
            rgb_annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)

            cv2.imshow("window_name", rgb_annotated_image)
            # cv2.imwrite("window_name", rgb_annotated_image)
            cv2.waitKey(1)
        # Break the loop
        else:
            break






#







# When everything done, release
# the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()
