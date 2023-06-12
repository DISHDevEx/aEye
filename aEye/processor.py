import boto3
import os

def process(list_video, operator = '-r' , x = .8, y=.8 ):
    """
    This function takes a list of video and apply the desired processing/features based on the prompted operator

    right now, it is just hardcore for 1 simple operator

    input:
    list_video is the list of video object
    operator is the argument for desired operator
    x, y is the parameter for the operator, which implement *args/**kwargs later
    """

    s3 = boto3.client('s3')
    for video in list_video:
        if operator == '-r':
            video.resize_by_ratio(x,y)

            #write in s3
            response = s3.upload_file("data/out_put" + video.title, 'aeye-data-bucket', "data/out_put" + video.title)
            

