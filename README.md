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

### **Inital project setup**

1. clone/pull this repo to local machine

```console
git clone https://github.com/DISHDevEx/aEye.git
```

2. Run the following command to create the wheel file

```console
python setup.py bdist_wheel --version <VERSION_NUMBER>
```
**NOTE**: the ***<VERSION_NUMBER>*** only effects your local build.  You can use any version number you like.  This can be helpful in testing prior to submitting a pull request.  Alternatively, you can eclude the ***--version <VERSION_NUMBER>*** flag and the .whl file name will output as ***aEye-_VERSION_PLACEHOLDER_-py3-none-any.whl***

3. Install the necessary requirements

```console
!pip install -r requirements.txt
```

4. Run below to import in jyputer-notebook

```console
import boto3
import cv2
from aEye.video import Video
from aEye.processor import Processor
from aEye.auxiliary import Aux
```

5. Initalize the auxiliary class.

```console
aux = Aux()
```

6. Load the video from the desired bucket and folder.

```console
video_list_s3 = aux.load_s3(bucket = 'aeye-data-bucket', prefix = 'input_video/')
```


7. Initalize the processor class.

```console
process = Processor()
```


How to use the processor:

To see all processing options as a user, run process.show_util()

All processing utilities take a video or list of videos as their first parameter, and return a video or list of videos. Essentially, adding multiple processing labels
to a video or video list should see the output of one process being used as the input for the next process. 

The processor allows users to select multiple actions to apply to a video or list of videos and execute once. As a result, videos are output significantly more quickly, but 
there are some rules to ensure that everything is processed correctly! The Aux execute_label_and_write_local function, which is used to execute a series of processor labels on a list of videos
also returns a list of videos. This means you can process videos, execute, upload those videos and continue to process them! 
The order of input matters, and one execution cycle should ideally avoid performing the same type of operation, as the older one is ignored. (For example, 
if you try to trim a video length twice, the video will be trimmed according to the most recently applied process.)
If the user wants to create two different trims, they will have to execute in between those two. 

Example:
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

Again, because processor modifications are not applied until the aux.execute_label_and_write_local(list) command is performed, any image extraction that
happens prior to an execution will not have any of the modifications applied. The framework will always allow frames to be extracted, but if there
are pending processor modifications, a warning will be raised for the user. The following shows how execution order affects frame capture.

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
Most importantly, ADD_LABEL_TRIM_INTO_CLIPS MUST BE EXECUTED LAST! Because this can create significantly more videos, it branches one input to many
outputs, which currently cannot be processed further.

Below is an example of processor utility to downsize, crop, and trim a video:


```console
to_process = process.add_label_trim_video_start_end(video_list_s3, 1, 9)              #Trims from 1s to 9s
to_process = process.add_label_change_resolution(to_process, "720p")                  #Converts to 720p
final_video_list = process.add_label_crop_video_section(to_process, 0, 0, 150, 100)   #Creates a 150x100 crop at (0,0)
```

8. Use auxiliary class to execute and write the videos with processor labels.

```console
aux.execute_label_and_write_local(final_video_list)
```

9. Any processing creates a lot of files! If you don't want to upload these, just use:
```console
aux.clean()
```

10. Upload the result to the desire bucket.

```console
aux.upload_s3(res_trimmed_s3, bucket = 'aeye-data-bucket')
```

11. Clean up the temp folder.

```console
aux.clean()
```

The following steps are to load and write locally.

12. Load video files from data/ folder

```console
video_list_local = aux.load_local('data/')
```

13. Add Trim label for the local video files.


```console

trimmed_local = process.add_label_trimming_start_duration(video_list_local,0,5)
```

14. Execute all labels and write the output to data/ folder.

```console
aux.execute_label_and_write_local(trimmed_local,'data/')
```
