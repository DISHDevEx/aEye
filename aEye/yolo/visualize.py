import cv2
import numpy as np

MARGIN = 10  # pixels
ROW_SIZE = 10  # pixels
FONT_SIZE = 1
FONT_THICKNESS = 1
TEXT_COLOR = (255, 0, 0)  # red


def visualize(
    image,
    detection_result
) -> np.ndarray:
  """Draws bounding boxes on the input image and return it.
  Args:
    image: The input RGB image.
    detection_result: The list of all "Detection" entities to be visualize.
  Returns:
    Image with bounding boxes.
  """
  for detection in detection_result:
    # Draw bounding_box
    x,y,w,h = detection.boxes.xywh[0]
    start_point = x.item(), y.item()
    end_point = x.item() + w.item(), y.item() + h.item()
    cv2.rectangle(image, start_point, end_point, TEXT_COLOR, 3)

    # Draw label and score
    category_name = detection.names[detection.boxes.cls.item()]
    probability = round(detection.boxes.conf.item(), 2)
    result_text = category_name + ' (' + str(probability) + ')'
    text_location = (MARGIN + x.item(),
                     MARGIN + ROW_SIZE + y.item())
    cv2.putText(image, result_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                FONT_SIZE, TEXT_COLOR, FONT_THICKNESS)

  return image