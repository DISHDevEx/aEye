import cv2
import numpy as np

def calculate_psnr(original_video, compressed_video):
    input_cap = cv2.VideoCapture(original_video)
    output_cap = cv2.VideoCapture(compressed_video)

    frame_count = min(int(input_cap.get(cv2.CAP_PROP_FRAME_COUNT)), int(output_cap.get(cv2.CAP_PROP_FRAME_COUNT)))
    total_psnr = 0

    for _ in range(frame_count):
        ret1, input_frame = input_cap.read()
        ret2, output_frame = output_cap.read()

        if not ret1 or not ret2:
            break

        psnr = calculate_psnr_frame(input_frame, output_frame)
        total_psnr += psnr

    input_cap.release()
    output_cap.release()

    mean_psnr = total_psnr / frame_count
    return mean_psnr

def calculate_psnr_frame(original_frame, compressed_frame):
    mse = np.mean((original_frame - compressed_frame) ** 2)
    max_pixel_value = np.max(original_frame)
    psnr = 10 * np.log10((max_pixel_value ** 2) / mse)
    return psnr
