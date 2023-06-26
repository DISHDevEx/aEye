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
from aEye.auxiliary import Aux
```

4. Initalize the auxiliary class.

```console
aux = Aux()
```

5. Load the video from the desired bucket and folder.

```console
video_list_s3 = aux.load_s3(bucket = 'aeye-data-bucket', prefix = 'input_video/')
```

5. Initalize the processor class.

```console
process = Processor()
```

6. Use the processor to add trim labels the videos.

```console
trimmed_s3 = process.add_label_trimming_start_duration(video_list_s3,0,5)
```

7. Use the processor to add resize labels to the trimmed videos.

```console
res_trimmed_s3 = process.add_label_resizing_by_ratio(trimmed_s3,.5,.5)
```

8. Use auxiliary class to execute and write the videos with resized and trimmed labels.

```console
aux.execute_label_and_write_to(res_trimmed_s3)
```

9. Upload the result to the desire bucket.

```console
aux.upload_s3(res_trimmed_s3, bucket = 'aeye-data-bucket')
```

10. Clean up the temp folder.

```console
aux.clean_temp()
```

The following steps are to load and write locally.

11. Load video files from data/ folder

```console
video_list_local = aux.load_local('data/')
```

11. Add Trim label for the local video files.

```console
trimmed_local = process.add_label_trimming_start_duration(video_list_local,0,5)
```

12 Execute all labels and write the output to data/ folder.

```console
aux.execute_label_and_write_to(trimmed_local,'data/')
```
