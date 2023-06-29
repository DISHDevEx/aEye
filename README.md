# aEye

Extensible Video Processing Framework with Additional Features Continuously Deployed

### **Project Structure**

```
├──  aEye				contains vidoe class and processor class that manage from loading, processing and uploading
│   ├── processor.py
│   ├── video.py
|   ├── auxiliary.py
├──  tests				contains unit tests
│   ├── test.py
├──  data				contains a temp location for video to save before deleting and uploading to S3
├──  modified   directory for modified videos/images
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

5.5 Initalize the processor class.

```console
process = Processor()
```

How to use the processor:

To see all processing options as a user, run process.show_util()

The processor allows users to select multiple actions to apply to a video or list of videos and execute once. As a result, videos are output significantly more quickly, but 
there are some rules to ensure that everything is processed correctly! The Aux execute function returns a list of videos, meaning you can execute, upload those videos
and continue to process those same videos, but it can be run without an output cariable as well. Similarly, any CV image processing returns a video
list, but doesn't need to. For example, if the user inputs two commands that trim a video before executing, only the most recent
command will run. If the user wants to create two different trims, they will have to execute in between those two. 

Example of this below:

```console
to_process = process.add_label_trim_video_start_end(video_list_s3, 1, 9)
to_process = process.add_label_trim_num_frames(to_process, 10, 60)
output_video_list = aux.execute_label_and_write_local(to_process)
# This will only create a 60 frame long clip, not an 8 second one.

to_process = process.add_label_trim_video_start_end(video_list_s3, 1, 9)
processed = aux.execute_label_and_write_local(to_process)
processed = process.add_label_trim_num_frames(processed, 10, 60)
output_video_list = aux.execute_label_and_write_local(processed)
# This will create two videos, one from time 1 to 9, and another 60 frame clip.

```

IMAGE PROCESSING IS EXECUTED THE MOMENT IT IS CALLED! IF YOU WANT TO EXTRACT FRAMES WITH PROCESSING, YOU MUST
EXECUTE THE VIDEO PROCESSING COMMANDS FIRST WITH AUX.EXECUTE_LABEL_AND_WRITE_LOCAL(VIDEO_LIST)!!!

Example:

```console
to_process = process.add_label_change_resolution(video_list_s3, "720p")
process.cv_extract_specific_frame(to_process, 42)  # These screenshots will not be in 720p
aux.execute_label_and_write_local(to_process)
# Because the video modifications have not been executed, the images will come from the original video.

to_process = process.add_label_change_resolution(video_list_s3, "720p")
output_list = aux.execute_label_and_write_local(to_process)
process.cv_extract_specific_frame(output_list, 42)  # These screenshots WILL be in 720p!
# Because the rescale was executed, the resulting screenshot is in 720p!
```

Processor Limitations:

Because the processor works as a pipeline, frames cannot be extracted from a source that has been previously executed. 
Most importantly, ADD_LABEL_TRIM_INTO_CLIPS MUST BE EXECUTED LAST! Because this can create significantly more videos, it branches one inpput to many
outputs, which currently cannot be processed further.

Any processing creates a lot of files! If you don't want to upload these, just use:
```console
process.remove_outputs()
aux.clean()
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
