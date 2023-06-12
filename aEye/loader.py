from video import Video
import boto3

def loader(bucket=  'aeye-data-bucket', prefix='input_video/'):

    video_list = []

    s3 = boto3.client('s3')
    result = s3.list_objects(Bucket = bucket, Prefix = prefix)
    for i in result["Contents"]:
        if i["Key"] == prefix:
            continue
        url = s3.generate_presigned_url( ClientMethod='get_object', Params={ 'Bucket': bucket, 'Key': key } ,ExpiresIn=5)
        video_list.append(Video(url))
        
    return video_list