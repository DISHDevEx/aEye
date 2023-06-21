"""
Module contains the Video class that stores and represents video files as objects.

"""
import cv2
import os
import json
import subprocess
from static_ffmpeg import run

ffmpeg, ffprobe = run.get_or_fetch_platform_executables_else_raise()


class Video:
    """
    Video class that encapsulates all necessary video information.
    Also contains some useful utility like the ability to grab frames, process
    video clips, trim them down, crop, etc.
    Attributes
    ----------
    file: str
        path of the video file associated with the object
    meta_data: str
        JSON dictionary of video metadata, typically streams[0] is the video metadata
    cv_video: cv2.VideoCapture
        OpenCV video object, used for any openCV processing
    ----------
    Methods
    ----------
    extract_metadata -> str:
        Collects the metadata from all video sources and separates the streams
        Necessary for basically any processing, but still has to be set (none by default)
    get_codec -> str:
        Returns the video codec
    get_duration -> str:
        Returns video duration in seconds, but does so as a string
    get_frames -> str:
        Returns the amount of frames in the video as a string (via OpenCV)
    getfile -> str:
        Returns video file path

    """

    def __init__(self, file, title = None) -> None:
        self.file = file
        self.meta_data = None
        self.title = title
        self.cv_video = cv2.VideoCapture(file)

    def extract_metadata(self):
        """
        Probably the most important method, probes a video passed with a
        file path and returns a json dictionary full of metadata. Video metadata lives in
        json['streams'][0] because it is the first channel and the dictionary splits streams from error
        Returns
        -------
        String of JSON Dictionary full of video metadata
        """
        if self.meta_data is None:
            command = f"{ffprobe} -hide_banner -show_streams -v error -print_format json -show_format -i '{self.getfile()}'"
            out = subprocess.check_output(command, shell=True).decode("utf-8")
            json_data = json.loads(out)
            self.meta_data = json_data
            return json_data

    def get_codec(self):
        """
        Returns the video codec as a string
        """
        if self.meta_data is not None:
            return self.meta_data["streams"][0]["codec_name"]
        else:
            self.meta_data = self.get_metadata()
            return self.meta_data["streams"][0]["codec_name"]

    def get_duration(self):
        """
        Returns the video duration as a string
        """
        if self.meta_data is not None:
            return self.meta_data["streams"][0]["duration"]
        else:
            self.meta_data = self.get_metadata()
            return self.meta_data["streams"][0]["duration"]

    def get_num_frames(self):
        """
        Returns # of frames in video as a string
        """
        if self.meta_data is not None:
            return self.meta_data["streams"][0]["nb_frames"]
        else:
            self.meta_data = self.extract_metadata()
            return self.meta_data["streams"][0]["nb_frames"]

    def get_file(self):
        """
        Returns the file path as a string
        """
        return self.file

