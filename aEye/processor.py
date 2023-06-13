import boto3
import os
from aEye.video import Video

class Processor:

    """
    
    """
    def __init__(self) -> None:
        self.video_list = []

    

    def loader(self, bucket=  'aeye-data-bucket', prefix='input_video/'):
        """
        This function will load the video data from S3 and save them 
        into a list of video class. 

        input:
        bucket is the bucket name
        prefix is the folder in the bucket

        """

        s3 = boto3.client('s3')
        result = s3.list_objects(Bucket = bucket, Prefix = prefix)

        for i in result["Contents"]:
            if i["Key"] == prefix:
                continue
            title = i["Key"].split(prefix)[1]

            #in order to convert video file from S3 to cv2 video class, we need its url
            url = s3.generate_presigned_url( ClientMethod='get_object', Params={ 'Bucket': bucket, 'Key': i["Key"] } ,ExpiresIn=5)
            self.video_list.append(Video(url, title))

        print("Successfully loaded video data from " + bucket)
        print("There are total of " + len(self.video_list) + " video files")


    def resize_by_ratio(self, x_ratio, y_ratio):
        """
        this method will resize the current video by multiplying 
        the current x and y by the input x_ratio 
        input: FLOAT
        non negative and non zero value

        """

        #convert ratio into actual dimension 
        new_width = int(self.width * x_ratio )
        new_height = int(self.height * y_ratio )
        dim = (new_width, new_height)

        for video in self.video_list:
            frame_list = video.get_frame_array()
            temp = []


            for frame in frame_list:
                resized = cv2.resize(frame , dim, interpolation = cv2.INTER_AREA)
                temp.append(resized)
            
            video.set_frame_array(temp)
            video.set_dim(dim)


    def upload(self, bucket=  'aeye-data-bucket'):
        s3 = boto3.client('s3')

        for video in self.video_list:
            path = 'data/out_put_' + video.title

            video.write_video(path)
            response = s3.upload_file( path, bucket,  path)
            os.remove(path)






