import subprocess
from multipledispatch import dispatch

'''
Split Class:    Contains all utility to split up/trim video, both by time and by frame
                All method docs describe in further detail what they're supposed to do, and
                all videos are sent to the outputs folder. 
                *This was done bc only RAW Video can be moved via stdout, and I don't wanna pipe
                 400 gigs of video ya dig?
'''


@dispatch(int, str)
def split_on_time(interval, file):
    """
    split_on_time(interval, file)
    This method splits a video into *interval* second long clips, but for any remainder
    the last clip will be truncated. For example: A 43 second long video with a 10 second interval
    will produce 5 outputs: 4 ten second clips, and one three second long one, rather than filling with
    black space. *Probably can be changed if need be but idk why you'd want that?
    """
    cmd = 'ffmpeg -i ' + file + ' -c copy -v quiet -map 0 -segment_time ' + str(interval) + \
          ' -f segment -reset_timestamps 1 outputs/output%03d.mp4'
    subprocess.call(cmd, shell=True)


@dispatch(int, int, str)
def split_on_time(start, end, file):
    """
    split_on_time(start, end, file)
    This method can be used to extract a clip based on a given start and end point in seconds.
    *Error checking and minute conversion would probably be good...
    """
    duration = end - start
    cmd = f'ffmpeg -y -ss {start} -i {file} -v quiet -t {duration} -c copy outputs/timesplit.mp4'
    subprocess.call(cmd, shell=True)


@dispatch(int, object)
def split_on_frame(frame, video):
    """
    split_on_frame(frame, video)
    Given a passed frame, this method will create a video starting at that specific
    frame and running all the way until the end. Again, might not be the stupidest idea to
    add in some safety/edgecase stuff here
    """
    fps = (float(video.get_frames()) / float(video.get_duration()))
    time_stamp = frame / fps
    cmd = "ffmpeg -y -ss " + str(
        time_stamp) + " -i " + video.file + " -v quiet -c:v libx264 -c:a aac outputs/frameCrop.mp4"
    subprocess.call(cmd, shell=True)
    # pipe_string = "-ss " + str(time_stamp) + " -i " + video.file + " -v quiet -c:v libx264 -c:a aac"
    # return pipe_string


@dispatch(int, int, object)
def split_on_frame(start_frame, num_frames, video):
    """
    split_on_frame(start, duration, video_object)
    Given a passed frame (start), and a duration, which in this instance is the number of
    frames to crop to, it will send a cropped video to the output folder.
    *Could change num_frames to a time duration to make more sense to a human user but like
    just use split_on_time???
    """
    fps = (float(video.get_frames()) / float(video.get_duration()))
    time_stamp = start_frame / fps
    cmd = f"ffmpeg -y -ss {str(time_stamp)} -i {video.getfile()} -v quiet -c:v libx264 -frames:v {num_frames} outputs/extract.mp4"
    print("Encoding ", num_frames, " from ", start_frame)
    subprocess.call(cmd, shell=True)
