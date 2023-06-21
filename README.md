# aEye

Extensible Video Processing Framework with Additional Features Continuously Deployed

### **Project Structure**

```
├──  aEye				contains vidoe class and processor class that manage from loading, processing and uploading
│   ├── processor.py
│   ├── video.py
├──  tests				contains unit tests
│   ├── test.py
├──  data				contains a temp location for video to save before deleting and uploading to S3
```

### **inital project setup**

1. clone/pull this repo to local machine

```console
git clone https://github.com/DISHDevEx/aEye.git
```

2. Install the necessary requirements

```console
!pip install -r requirements.txt
```

3. Run below to import in jyputer-notebook

```console
import boto3
import cv2
from aEye.video import Video
from aEye.processor import Processor
```

4. Initalize the processor class

```console
process = Processor()
```

5. Load the video from the desired bucket and folder and resize them to desired ratio

```console
process.load_and_resize(bucket = 'aeye-data-bucket', prefix = 'input_video/', x_ratio = .6, y_ratio = .5)
# To load without resizing:
process.load(bucket = 'aeye-data-bucket', prefix = 'input_video/')
```

6. Use the Processor to perform operations on video objects

```console
#NOTE: All methods currently process every video in the video list; multiprocessing is on the horizon
process.trim_video_from_to(2, 6)                  #Trims video from 2s to 6s
process.cv_extract_specific_frame(42)             #Extracts 42nd frame as a .PNG
process.blur_video(10,2)                          #Applies a Gaussian blur of strength 10 two times *Takes a while
process.crop_video_section(100, 50, 100, 100)     #Creates a 100x100 pixel cropped portion starting at (100,50)
process.split_num_frames(42, 60)                  #Creates a video starting at frame 42 which is 60 frames long 
process.trim_into_clips(4.5)                      #Splits the video into 4.5 second long clips 
process.split_on_frame(69)                        #Splits video from frame 69 to end 
process.cv_extract_frame_at_time(2.344)           #Extracts the frame CLOSEST to 2.344s as a PNG
process.extract_many_frames(3, 5)                 #Starting at frame 3, extracts 5 subsequent frames
```
Running this in Jupyter Notebook will create a LOT of files in the local modified folder! This is meant to illustrate functionality.

8. Upload the result to the desire bucket

```console
process.upload(bucket = 'aeye-data-bucket')
```
