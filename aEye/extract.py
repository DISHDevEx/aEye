import json
import subprocess


def extract_metadata(filePath):
    """
    Probably the most important method, probes a video passed with a
    file path and returns a json dictionary full of metadata. Video metadata lives in
    json['streams'][0] because it is the first channel and the dictionary splits streams from error
    """
    command = f"ffprobe -hide_banner -show_streams -v error -print_format json -show_format -i '{filePath}'"
    out = subprocess.check_output(command, shell=True).decode("utf-8")
    json_data = json.loads(out)
    return json_data


def extract_frame_at_time(time, video):
    """
    Does pretty much what you think it does.
    """
    cmd = f"ffmpeg -v quiet -ss {time} -i {video.getfile()} -frames:v 1 outputs/ebt%02d.png"
    subprocess.call(cmd, shell=True)


def extract_frame_at_frame(frame, video):
    """
    Does exactly what you think it does
    """
    cmd = f"ffmpeg -v quiet -i {video.getfile()} -vf select='eq(n\,{frame})' -frames:v 1 outputs/ebf%03d.png"
    subprocess.call(cmd, shell=True)
