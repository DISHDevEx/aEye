"""
Module contains the visualizer to annotate the frame with the yolo prediction.
"""

import cv2
import numpy as np

MARGIN = 10  # pixels
ROW_SIZE = 10  # pixels
FONT_SIZE = 1
FONT_THICKNESS = 1
TEXT_COLOR = (255, 0, 0)  # red

def visualize_yolo(image,detection_result) -> np.ndarray:
    """Draws bounding boxes on the input image and return it.
    Parameters
    ----------
      image: cv2 image 
          The input RGB image.
      detection_result: 
          The list of all bounding boxes entities to be visualize from yolo.

    Returns
    ---------
      image: cv2 image
          Image with bounding boxes.
    """

    shape = detection_result[0].orig_shape
    for i, _ in enumerate(detection_result[0].boxes.cls):
        # Draw bounding_box
        x,y,w,h = detection_result[0].boxes.xyxyn[i]

        start_point = int(x.item()*shape[1]), int(y.item()*shape[0])
        end_point = int(w.item()*shape[1]),  int(h.item()*shape[0])

        cv2.rectangle(image, start_point, end_point, TEXT_COLOR, 3)

        # Draw label and score
        category_name = detection_result[0].names[detection_result[0].boxes.cls[i].item()]
        probability = round(detection_result[0].boxes.conf[i].item(), 2)
        result_text = category_name + ' (' + str(probability) + ')'
        text_location = (MARGIN + int(x.item()*shape[0]),
                        MARGIN + ROW_SIZE + int(y.item()*shape[1]))
        cv2.putText(image, result_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                    FONT_SIZE, TEXT_COLOR, FONT_THICKNESS)

    return image