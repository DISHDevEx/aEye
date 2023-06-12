from aEye.video import Video
import boto3

def loader(bucket=  'aeye-data-bucket', prefix='input_video/'):
    """
    This function will load the video data from S3 and save them 
    into a list of video class. 

    input:
    bucket is the bucket name
    prefix is the folder in the bucket

    output:
    a list of video classes
    """

    video_list = []
    s3 = boto3.client('s3')
    result = s3.list_objects(Bucket = bucket, Prefix = prefix)

    for i in result["Contents"]:
        if i["Key"] == prefix:
            continue
        title = i["Key"].split(prefix)[1]

        #in order to convert video file from S3 to cv2 video class, we need its url
        url = s3.generate_presigned_url( ClientMethod='get_object', Params={ 'Bucket': bucket, 'Key': i["Key"] } ,ExpiresIn=5)
        video_list.append(Video(url, title))

    return video_list