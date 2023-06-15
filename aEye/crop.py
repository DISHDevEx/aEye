import os
import subprocess
from static_ffmpeg import run

ffmpeg, ffprobe = run.get_or_fetch_platform_executables_else_raise()


def crop_video_section(section_width, section_height, start_x, start_y, video):
    """
    crop_video_section(width, height, x, y, video)
    Crops a Width x Height section of the video starting at pixel coordinates x, y
    and just uses the active video object to do so. Note, re-encoding is a necessary
    step for ANY filter application, so there will be noticeable processing time.
    """
    cmd = (
        f"{ffmpeg} -y -i {video.getfile()} -v quiet -filter:v 'crop={section_width}:{section_height}:{start_x}:{start_y}' "
        f"-c:a copy outputs/sectioncrop.mp4"
    )
    subprocess.call(cmd, shell=True)


def moving_crop(video):
    """
    Very basic version of what should hopefully be very important.
    Will need to pass a lot more params but right now swaprect looks like:
    =width:height:x1:y1:x2:y2:....(n,startFrame,endFrame)
    """
    script = (
        "swaprect=720:480:0:0:400:400:enable='between(n,0,100)',"
        "swaprect=720:480:0:0:500:400:enable='between(n,101,150)',"
        "swaprect=720:480:0:0:600:400:enable='between(n,151,280)',"
        "swaprect=720:480:0:0:700:300:enable='between(n,281,500)',"
        "swaprect=720:480:0:0:800:300:enable='between(n,501,750)',"
        "crop=720:480:0:0"
    )
    with open("filter_script.txt", "w") as file:
        file.write(script)
    cmd = (
        f"{ffmpeg} -y -v quiet -ss 0 -t 30 -i {video.getfile()} -filter_complex_script filter_script.txt -acodec copy "
        f"outputs/moving.mp4"
    )
    subprocess.call(cmd, shell=True)
    os.remove("filter_script.txt")
