import boto3
import os
def process(list_video, operator = '-r' , x = .8, y=.8 ):
    s3 = boto3.client('s3')
    for video in list_video:
        if operator == '-r':
            video.resize_by_ratio(x,y)
            
            object_name = os.path.basename("data/out_put" + video.title)

            response = s3.upload_file("data/out_put" + video.title, 'aeye-data-bucket', "data/out_put" + video.title)
            

