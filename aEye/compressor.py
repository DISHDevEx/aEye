import boto3
import subprocess
import ffmpeg
from pathlib import Path


class Compressor:

    def change_video_to_grayscale(input_video):
        input_file_name = Path(input_video).stem
        print(input_file_name)
        output_file = "{}_grayscale_video.mp4".format(input_file_name)
        ffmpeg.input(input_video).output(output_file, vf="format=gray").run()
        return output_file

    def change_video_resolution(input_video,k):
        input_file_name = Path(input_video).stem
        resolution_factor = k
        output_file = "{}_reduced_resolution_video_{}x.mp4".format(input_file_name,resolution_factor)
        """
        Reduces the resolution of a video to 640p .
        input_file: Path to the input video file.
        output_file: Path to save the output video file.
        """
        ffmpeg_cmd = [
            'ffmpeg',
            '-i', input_video,
            '-vf', f'scale=iw/{k}:ih/{k}',
            output_file
        ]

        subprocess.run(ffmpeg_cmd)
        return output_file

    def convert_to_grayscale_with_640p(input_video):
        input_file_name = Path(input_video).stem
        output_file = "{}_grayscale_video_640p.mp4".format(input_file_name)
        ffmpeg_cmd = [
            'ffmpeg',
            '-i', input_video,
            '-vf', 'scale=640:-1,format=gray',
            output_file
        ]
        subprocess.run(ffmpeg_cmd)