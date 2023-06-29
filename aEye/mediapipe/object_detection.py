import mediapipe as mp
<<<<<<< HEAD
import cv2
import numpy as np
from .visulize import visualize

def object_detection(model_path, input_video, output_video):
    """
    Given a specific model and video, it will initiate the model and will
    scan through the video frame by frame adding the bounding boxes to the output video.
    Uses the visualize function to apply bounding boxes once the area for it is calculated

    Parameters
    ----------
    model_path  : string
        Path of the model weight (mediapipe specific).
    input_video : string
        The path to the video to object detect.
    output_video: string
        The path for video output.

    Returns
    ----------
    Doesn't return anything, but it does write a video to the output folder with
    the bounding boxes and weights applied.
    """
=======
from mediapipe.tasks import python
import cv2
import numpy as np
<<<<<<<< HEAD:aEye/mediapipe/person_detector.py
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
========
from .visulize import visualize

def object_detection(model_path, input_video, output_video):
>>>>>>> 186cdeb (pushing for Docker work)
    BaseOptions = mp.tasks.BaseOptions
    ObjectDetector = mp.tasks.vision.ObjectDetector
    ObjectDetectorOptions = mp.tasks.vision.ObjectDetectorOptions
    VisionRunningMode = mp.tasks.vision.RunningMode
<<<<<<< HEAD
    # Media Pipe Init, necessary for setup
=======

>>>>>>> 186cdeb (pushing for Docker work)

    # Check if camera opened successfully
    options = ObjectDetectorOptions(
        base_options=BaseOptions(model_asset_path=model_path),
        max_results=5,
        running_mode=VisionRunningMode.VIDEO)

<<<<<<< HEAD
    # Opens the model, parses frame by frame and applies model
=======
>>>>>>> 186cdeb (pushing for Docker work)
    with ObjectDetector.create_from_options(options) as detector:
        cap = cv2.VideoCapture(input_video)
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        x = cap.get(cv2.CAP_PROP_FPS)
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_video, fourcc, x, (frame_width, frame_height))
        if cap.isOpened() == False:
            print("Error opening video file")
<<<<<<< HEAD

        # Read until video is completed
        frame_index = 0
        # While the video still has frames, apply the model to get the bounding box
        while (cap.isOpened()):

            # Capture frame-by-frame
            ret, frame = cap.read()
            if ret == True:
                # Display the resulting frame
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
                # Calculate the timestamp of the current frame
                frame_timestamp_ms = int(1000 * frame_index / x)
                frame_index += 1
                # Perform object detection on the video frame.
                detection_result = detector.detect_for_video(mp_image, frame_timestamp_ms)
                image_copy = np.copy(mp_image.numpy_view())
                annotated_image = visualize(image_copy, detection_result)  #Adds Bounding box to img
                out.write(annotated_image)

            # Break the loop
            else:
                break
    # When everything done, release
    # the video capture object
    cap.release()
    out.release()
=======
>>>>>>>> 186cdeb (pushing for Docker work):aEye/mediapipe/object_detection.py

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
>>>>>>> 186cdeb (pushing for Docker work)
