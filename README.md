# aEye

Extensible Video Processing Framework with Additional Features Continuously Deployed

### **Project Structure**

```
├──  aEye				contains vidoe class and processor class that manage from loading, processing and uploading
│   ├── processor.py
│   ├── video.py
│   ├── auxiliary.py 
│   ├── mediapipe
│      ├── object_detection.py
│      ├── visualize.py 
├──  runner_notebooks
│   ├── leto-demo.ipynb
├──  tests				contains unit tests
│   ├── test_get_meta_data.py
│   ├── conftest.py
│   ├── test_data
│      ├── test_video.mp4
├── lambda_function.py
├── setup.py 
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

8. Use the processor to add trim labels the videos.

```console
trimmed_s3 = process.add_label_trimming_start_duration(video_list_s3,0,5)
```

9. Use the processor to add resize labels to the trimmed videos.

```console
res_trimmed_s3 = process.add_label_resizing_by_ratio(trimmed_s3,.5,.5)
```

10. Use auxiliary class to execute and write the videos with resized and trimmed labels.

```console
aux.execute_label_and_write_local(res_trimmed_s3)
```

11. Upload the result to the desire bucket.

```console
aux.upload_s3(res_trimmed_s3, bucket = 'aeye-data-bucket')
```

12. Clean up the temp folder.

```console
aux.clean()
```

The following steps are to load and write locally.

13. Load video files from data/ folder

```console
video_list_local = aux.load_local('data/')
```

14. Add Trim label for the local video files.

```console
trimmed_local = process.add_label_trimming_start_duration(video_list_local,0,5)
```

15. Execute all labels and write the output to data/ folder.

```console
aux.execute_label_and_write_local(trimmed_local,'data/')
```

### **Docker Image Setup**
The docker image is built automatically via github workflow action on every pull request. 
The rough sequence is below:

    1) The workflow action will build a wheel file based on setup.py,
    2) Then it will create a docker image based on the dockerfile.
    3) Finally it will push the image to ECR (currently, this will be loaded in ECR: Leto).

Please refer to mp-to-ecr.yml to get the exact sequences of the github workflow action, the dockerfile for the exact content in the docker image and setup.py for the exact built version.

### **Lambda Function**
Please refer to lambda_function.py for the logic of the lambda function. 
