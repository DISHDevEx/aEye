import mediapipe as mp
from mediapipe.tasks import python
import cv2
import numpy as np
from .visulize import visualize

def object_detection(model_path, input_video, output_video):
    BaseOptions = mp.tasks.BaseOptions
    ObjectDetector = mp.tasks.vision.ObjectDetector
    ObjectDetectorOptions = mp.tasks.vision.ObjectDetectorOptions
    VisionRunningMode = mp.tasks.vision.RunningMode


    # Check if camera opened successfully
    options = ObjectDetectorOptions(
        base_options=BaseOptions(model_asset_path=model_path),
        max_results=5,
        running_mode=VisionRunningMode.VIDEO)

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

        # Read until video is completed
        frame_index = 0
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
                annotated_image = visualize(image_copy, detection_result)
                #rgb_annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR)


                out.write(annotated_image)
                #cv2.imshow("window_name", annotated_image)
                #cv2.waitKey(1)
            # Break the loop
            else:
                break

    # When everything done, release
    # the video capture object
    cap.release()
    out.release()
    # Closes all the frames
    #cv2.destroyAllWindows()
