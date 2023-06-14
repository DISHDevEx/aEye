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
P = Processor()
```

5. Load the video from the desired bucket and folder and resize them to desired ratio

```console
P.load_and_resize(bucket = 'aeye-data-bucket', prefix = 'input_video/', x_ratio = .6, y_ratio = .5)
```

6. Upload the result to the desire bucket

```console
P.upload(bucket = 'aeye-data-bucket')
```
