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

4. Initalize the auxiliary class

```console
aux = Aux()
```

5. Load the video from the desired bucket and folder

```console
video_list = aux.load_s3(bucket = 'aeye-data-bucket', prefix = 'input_video/')
```

5. Initalize the processor class

```console
process = Processor()
```

6. Use the processor to trim the videos

```console
trimmed = process.trimmed_from_for(video_list,0,5)
```

7. Use the processor to resize the trimmed videos

```console
res_trimmed = process.resize_by_ratio(trimmed,.5,.5)
```

8 Use auxiliary class to write the resized and trimmed video

```console
aux.write(res_trimmed)
```

6. Upload the result to the desire bucket

```console
process.upload(bucket = 'aeye-data-bucket')
```
