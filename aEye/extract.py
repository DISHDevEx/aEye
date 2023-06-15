import json
import subprocess
from static_ffmpeg import run
import cv2

ffmpeg, ffprobe = run.get_or_fetch_platform_executables_else_raise()


def extract_metadata(filePath):
    """
    Probably the most important method, probes a video passed with a
    file path and returns a json dictionary full of metadata. Video metadata lives in
    json['streams'][0] because it is the first channel and the dictionary splits streams from error
    """
    command = f"{ffprobe} -hide_banner -show_streams -v error -print_format json -show_format -i '{filePath}'"
    out = subprocess.check_output(command, shell=True).decode("utf-8")
    json_data = json.loads(out)
    return json_data


def extract_frame_at_time(xtime, video):
    """
    Does pretty much what you think it does.
    """
    cmd = f"{ffmpeg} -v quiet -ss {xtime} -i {video.getfile()} -frames:v 1 outputs/ebt%02d.png"
    subprocess.call(cmd, shell=True)


def extract_frame_at_frame(frame, video):
    """
    Does exactly what you think it does
    """
    cmd = f"{ffmpeg} -v quiet -i {video.getfile()} -vf select='eq(n\,{frame})' -frames:v 1 outputs/ebf%03d.png"
    subprocess.call(cmd, shell=True)


def extract_many_frames(start_frame, num_frames, video):
    cmd = f"{ffmpeg} -i {video.getfile()} -vf select='eq(n\,{start_frame})' -frames:v {num_frames} outputs/emf%02d.png"
    subprocess.call(cmd, shell=True)


def cv_extract_frame_at_time(time, cv_video):
    """
    Img extraction that takes less than half as long as the FFMpeg version
    """
    fps = cv_video.get(cv2.CAP_PROP_FPS)
    frame_id = int(fps * time)
    cv_video.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
    ret, frame = cv_video.read()
    cv2.imwrite("outputs/cv2Frame.png", frame)


def cv_extract_specific_frame(frame, cv_video):
    cv_video.set(cv2.CAP_PROP_POS_FRAMES, frame)
    ret, output = cv_video.read()
    cv2.imwrite("outputs/cv2specific.png", output)
