import subprocess


def crop_video_section(section_width, section_height, start_x, start_y, video):
    """
    crop_video_section(width, height, x, y, video)
    Crops a Width x Height section of the video starting at pixel coordinates x, y
    and just uses the active video object to do so. Note, re-encoding is a necessary
    step for ANY filter application, so there will be noticeable processing time.
    """
    cmd = f"ffmpeg -y -i {video.getfile()} -v quiet -filter:v 'crop={section_width}:{section_height}:{start_x}:{start_y}' " \
          f"-c:a copy outputs/sectioncrop.mp4"
    subprocess.call(cmd, shell=True)
