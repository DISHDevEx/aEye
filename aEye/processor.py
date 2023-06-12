def process(list_video, operator = '-r' , x = .8, y=/8 ):
    for video in list_video:
        if operator == '-r':
            video.resize_by_ratio(x,y)
            

