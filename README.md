# aEye

Extensible Video Processing Framework with Additional Features Continuously Deployed

### **Project Structure**

```
├──  aEye				contains video class and processor class that manage from loading, processing and uploading
│   ├── processor.py
│   ├── video.py
|   ├── auxiliary.py
├──  tests				contains unit tests
│   ├── test.py
├──  data				contains a temp location for video to save before deleting and uploading to S3

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

To see all processing options as a user, run the following:
```console
process.show_util()
```

The processor provides multiple actions that can be applied to a video or a list of videos. Each action takes a video or list of videos as its first parameter and returns a modified video or list of videos. 
To chain multiple processing labels together, you can pass the output of one process as the input for the next process.

Example:
```console
# Trimming the video from 1 second to 9 seconds
to_process = process.add_label_trim_video_start_end(video_list_s3, 1, 9)

# Trimming the resulting video to 60 frames
to_process = process.add_label_trim_num_frames(to_process, 10, 60)

# Execute the processing labels and write the processed videos locally
output_video_list = aux.execute_label_and_write_local(to_process)

# Note: This example will create a 60-frame long clip, not an 8-second one.
```

If you want to create two different trims, you will need to execute the processing in between those two operations:

```console

to_process = process.add_label_trim_video_start_end(video_list_s3, 1, 9)
processed = aux.execute_label_and_write_local(to_process)
processed = process.add_label_trim_num_frames(processed, 10, 60)
output_video_list = aux.execute_label_and_write_local(processed)
# This will create two videos, one from time 1 to 9, and another 60 frame clip.

```


Important note: Image processing is executed the moment it is called! If you want to extract frames with processing, you must execute the video processing commands first using aux.execute_label_and_write_local(video_list).

Keep in mind that processor modifications are not applied until the aux.execute_label_and_write_local(list) command is performed. Any image extraction that happens prior to an execution will not have any modifications applied. 
The framework allows frames to be extracted at any point while processing, but if there are pending processor modifications, a warning will be raised, and the resulting images will come from the original source. 
The execution order affects frame capture.

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

Please note the following limitations of the processor:

Frames cannot be extracted from a source that has been previously executed in the processor pipeline.
The ADD_LABEL_TRIM_INTO_CLIPS operation must be executed last. It creates multiple output videos from a single input, and these outputs cannot be processed further.
Here's an example of using the processor utility to downsize, crop, and trim a video:


```console
to_process = process.add_label_trim_video_start_end(video_list_s3, 1, 9)              #Trims from 1s to 9s
to_process = process.add_label_change_resolution(to_process, "720p")                  #Converts to 720p
final_video_list = process.add_label_crop_video_section(to_process, 0, 0, 150, 100)   #Creates a 150x100 crop at (0,0)
```

Below is a list of all current processor utility:

```console
---------------VIDEO UTILITY----------------
"add_label_resizing_by_ratio(video_list, x_ratio, y_ratio,target) -> Add label of resizing video by multiplying width by the ratio to video."

"add_label_change_resolution(video_list, desired_res) -> Pass in a common resolution (ex '720p') and re-encode videos to that res!"

"add_label_trim_video_start_end(video_list, start, end) -> Given start and end times in seconds, modified a trimmed down version of the video to the modified file."

"add_label_trim_into_clips(video_list, interval) -> Splits the video into X second clips, sends all these clips to output folder."

"add_label_split_on_frame(video_list, frame) -> Given a specific frame, start the video there, removes any preceding frames."

"add_label_split_num_frames(video_list, start_frame, num_frames) -> Given a start frame and the amount of frames that a user wants "
                                                                "to copy, splits the video to all of the frames within that frame range."

"add_label_crop_video_section(video_list, width, height, start_x, start_y) -> Create a width x height crop of the input video starting at pixel values"
                                                                              "start_x, start_y and sends the smaller video to the modified file."

"add_label_blur_video(video_list, blur_level, blur_steps) -> Adds the blur_level amount of blur blur_steps amount of times to a video."

---------------IMAGE UTILITY-----------------
"cv_extract_frame_at_time(video_list, time) -> Uses openCV cap to pull the frame at a given time. Can use floats for this, will pick the closest applicable frame if need be."

"cv_extract_specific_frame(video_list, frame) -> Pulls a specific frame from the video."

"cv_extract_many_frames(video_list, start_frame, num_frames) -> Given a start frame, extract the next num_frames to output folder. Outputs are in PNG form."
```

8. Use auxiliary class to execute and write the videos with processor labels.

```console
aux.execute_label_and_write_local(final_video_list)
```

9. Processing can create a lot of files! After processing, if you don't want to upload the generated files, you can use the following command to clean up:
```console
aux.clean()
```

10. Finally, you can upload the processed videos to the desired bucket using the upload_s3 function:

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

trimmed_local = process.add_label_trim_on_frame(video_list_local, 501)
```

14. Execute all labels and write the output to data/ folder.

```console
aux.execute_label_and_write_local(trimmed_local,'data/')
```
