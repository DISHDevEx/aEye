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

5.5 Temporary Processing Util:

To automatically execute processor commands. This will be changed once tags can be added to all processing util
```console
process.trim_video_start_end(2, 6)              # Creates a video from 2s to 6s
process.cv_extract_specific_frame(42)           # Grabs frame 42
process.blur_video(11,2)                        # Applies blur level 11 twice
process.crop_video_section(100, 50, 100, 100)   # Creates a 100x100 crop at (100,50)
process.split_num_frames(23, 60)                # Creates a 60 frame long clip starting at frame 23
rocess.trim_into_clips(8)                       # Trims Video into 8 second clips
process.split_on_frame(69)                      # Creates a video from the 69th frame to the end
process.cv_extract_frame_at_time(2.344)         # Extracts the closest frame to 2.344
process.extract_many_frames(3, 5)               # Extracts 5 subsequent frames from 3
```
This will output a lot of files! If you don't want to write and upload these, just use
```console
process.clear_outputs()
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
aux.execute_label_and_write_local(res_trimmed_s3)
```

9. Upload the result to the desire bucket.

```console
aux.upload_s3(res_trimmed_s3, bucket = 'aeye-data-bucket')
```

10. Clean up the temp folder.

```console
aux.clean()
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
aux.execute_label_and_write_local(trimmed_local,'data/')
```
