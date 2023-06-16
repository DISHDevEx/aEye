import subprocess
from static_ffmpeg import run

ffmpeg, ffprobe = run.get_or_fetch_platform_executables_else_raise()
"""
Split:    Contains all utility to split up/trim video, both by time and by frame
                All method docs describe in further detail what they're supposed to do, and
                all videos are sent to the outputs folder. 
"""


def split_on_interval(interval, video):
    """
    split_on_time(interval, file)
    This method splits a video into *interval* second long clips, but for any remainder
    the last clip will be truncated. For example: A 43 second long video with a 10 second interval
    will produce 5 outputs: 4 ten second clips, and one three second long one, rather than filling with
    black space. *Probably can be changed if need be but idk why you'd want that?
    """
    cmd = (
        f"{ffmpeg} -y -i {video.getfile()} -c copy -v quiet -map 0 -segment_time {interval} "
        f"-f segment -reset_timestamps 1 outputs/output%02d.mp4"
    )
    subprocess.call(cmd, shell=True)


def split_on_time(start, end, file):
    """
    split_on_time(start, end, file)
    This method can be used to extract a clip based on a given start and end point in seconds.
    *Error checking and minute conversion would probably be good...
    """
    duration = end - start
    cmd = f"{ffmpeg} -y -ss {start} -i {file} -v quiet -t {duration} -c copy outputs/timesplit.mp4"
    subprocess.call(cmd, shell=True)


def split_on_frame(frame, video):
    """
    split_on_frame(frame, video)
    Given a passed frame, this method will create a video starting at that specific
    frame and running all the way until the end. Again, might not be the stupidest idea to
    add in some safety/edge case stuff here
    """
    fps = float(video.get_frames()) / float(video.get_duration())
    time_stamp = frame / fps
    cmd = f"{ffmpeg} -y -ss {time_stamp} -i {video.getfile()} -v quiet -c:v libx264 -c:a aac outputs/splitonframe.mp4"
    subprocess.call(cmd, shell=True)


def split_num_frames(start_frame, num_frames, video):
    """
    split_num_frames(start, duration, video_object)
    Given a passed frame (start), and a duration, which in this instance is the number of
    frames to crop to, it will send a cropped video to the output folder.
    *Could change num_frames to a time duration to make more sense to a human user but like
    just use split_on_time???
    """
    fps = float(video.get_frames()) / float(video.get_duration())
    time_stamp = start_frame / fps
    cmd = (
        f"{ffmpeg} -y -ss {str(time_stamp)} -i {video.getfile()} -v quiet -c:v libx264 -frames:v {num_frames}"
        f" outputs/extract.mp4"
    )
    print("Encoding ", num_frames, " from ", start_frame)
    subprocess.call(cmd, shell=True)
