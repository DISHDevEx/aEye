import cv2
import numpy as np

MARGIN = 10  # pixels
ROW_SIZE = 10  # pixels
FONT_SIZE = 1
FONT_THICKNESS = 1
TEXT_COLOR = (255, 0, 0)  # red


def visualize(image,detection_result) -> np.ndarray:
    """Draws bounding boxes on the input image and return it.
    Args:
      image: The input RGB image.
      detection_result: The list of all "Detection" entities to be visualize.
    Returns:
      Image with bounding boxes.
    """
    for i in range(len(detection_result)):
        # Draw bounding_box
        x,y,w,h = detection_result[0].boxes.xywh[i]
        start_point = int(x.item()), int(y.item())
        end_point = int(x.item()) + int(w.item()), int(y.item()) + int(h.item())
        cv2.rectangle(image, start_point, end_point, TEXT_COLOR, 3)

        # Draw label and score
        category_name = detection_result[0].names[detection_result[0].boxes.cls[i].item()]
        probability = round(detection_result[0].boxes.conf.item(), 2)
        result_text = category_name + ' (' + str(probability) + ')'
        text_location = (MARGIN + int(x.item()),
                        MARGIN + ROW_SIZE + int(y.item()))
        cv2.putText(image, result_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                    FONT_SIZE, TEXT_COLOR, FONT_THICKNESS)

    return image