"""
Module contains the Video class that stores and represents video files as objects.

"""
import cv2
import os
import json
import subprocess
from static_ffmpeg import run

ffmpeg, ffprobe = run.get_or_fetch_platform_executables_else_raise()
import boto3

s3 = boto3.client("s3")


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

    -------

        __repr__() -> string:
            A native python method to represent the Video class.

        __eq__() -> string:
            A native python method to add comparison functionality.

        __bool__() -> boolean:
            A native python method to see whether video can be readed properly.

        cleanup() -> None:
            Clean up memory from cv2 video capture.

        get_meta_data() -> None:
            Retrieve the meta data from video.

        get_presigned_url(time) -> string:
            Retrieve the url for video file from S3 bucket.

        add_label(self, mod) -> None:
            Add ffmpeg label to video object.

        reset_label() -> None:
            Reset and remove all labels.

        get_label(self) -> string:
            Get ffmpeg label from video objects.
           
        get_codec -> str:
            Returns the video codec.
            
        get_duration -> str:
            Returns video duration in seconds, but does so as a string.
            
        get_frames -> str:
            Returns the amount of frames in the video as a string (via OpenCV).

    """

    def __init__(self, file=None, bucket=None, key=None, title=None) -> None:
        self.file = file
        self.bucket = bucket
        self.key = key
        self.title = title
        self.meta_data = None
        self.label = ''
        self.out = ''
        self.out_title = ''


    def __repr__(self):
        """
        This method will implement the video title name as object representation.

        Returns
        ---------
            title: string
                The title of video file.

        """
        return self.title

    def __eq__(self, target):
        """
        This method will implement comparison functionality for video.
        This will compare between video's title.

        Returns
        ---------
            comparison: boolean
                Boolean state of whether the target's title is same self's title.


        """

        return self.title == target

    def __bool__(self):
        """
        This method will check whether the video file can be readed properly.

        Returns
        ---------
            condition: boolean
                Boolean state of whether the video can be readed properly.

        """
        return cv2.VideoCapture(self.get_presigned_url(time=2)).read()[0]

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
            fp = None
            if self.file is None:
                fp = self.get_presigned_url()
            elif self.out is not None:
                fp = self.out
            else:
                fp = self.file
            command = f"{ffprobe} -hide_banner -show_streams -v error -print_format json -show_format -i {fp}"
            out = subprocess.check_output(command, shell=True).decode("utf-8")
            json_data = json.loads(out)
            self.meta_data = json_data
            return json_data

    def get_codec(self):
        """
        Returns the video codec as a string.
        """
        if self.meta_data is not None:
            return self.meta_data["streams"][0]["codec_name"]
        else:
            self.meta_data = self.get_metadata()
            return self.meta_data["streams"][0]["codec_name"]


    def get_duration(self):
        """
        Returns the video duration as a string.
        """
        if self.meta_data is not None:
            return self.meta_data["streams"][0]["duration"]
        else:
            self.meta_data = self.get_metadata()
            return self.meta_data["streams"][0]["duration"]

    def get_num_frames(self):
        """
        Returns # of frames in video as a string.
        """
        if self.meta_data is not None:
            return self.meta_data["streams"][0]["nb_frames"]
        else:
            self.meta_data = self.extract_metadata()
            return self.meta_data["streams"][0]["nb_frames"]

    def get_file(self):
        """
        Returns the file path as a string.
        """
        if self.file is None:
            return self.get_presigned_url()
        else:
            return self.file

    def get_width(self):
        """
        Returns the pixel width of the video associated with the current video object.
        """
        if self.meta_data is not None:
            return self.meta_data["streams"][0]["width"]
        else:
            self.meta_data = self.extract_metadata()
            return self.meta_data["streams"][0]["width"]

    def get_height(self):
        """
        Returns the pixel height of the video associated with the current video object.
        """
        if self.meta_data is not None:
            return self.meta_data["streams"][0]["height"]
        else:
            self.meta_data = self.extract_metadata()
            return self.meta_data["streams"][0]["height"]

    def cleanup(self) -> None:
        """
        This method will release the current view of video object from RAM.
        """
        self.capture.release()


    def get_presigned_url(self, time=60):
        """
        This method will return the presigned url of video file from S3.
        If the video file is from local machine then it will return the local path of the video file.

        Returns
        ---------
            url: string
                The presigned url or file path of the video file.

        """

        if self.file is None:

            url = s3.generate_presigned_url(
                ClientMethod="get_object",
                Params={"Bucket": self.bucket, "Key": self.key},
                ExpiresIn=time,
            )
            return f"'{url}'"
        return self.file

    def add_label(self, label):
        """
        This method will add ffmpeg label to the video.
        """
        self.label += label

    def add_output_title(self, title):
        """
        Appends the output title to name videos correctly 
        """
        self.out_title += title

    def reset_label(self):
        """
        This method will reset all ffmpeg label to empty.
        """

        self.label = ""

    def get_label(self):
        """
        This method will return the all ffmpeg label from the video.
        """
        return self.label

    def set_output(self, new_out):
        """
        Sets the output to the old video title string 
        """
        self.out = new_out


    def get_output_title(self):
        """
        This method will create the output title for video so the users can know all the labels that happen to the video.
        (I have a better implementation of this, it will be in the next pr after james adds all of the features.)

        Returns
        ---------
            result: string
                The output title of video.
        """

        result = ""
        if "scale" in self.label:
            result += "resized_"

        if "-ss" in self.label:
            result += "trimmed_"
        if 'crop' in self.label:
            result += "cropped_"
        if 'blur' in self.label:
            result += "blurred_"
        if '-f segment' in self.label:
            out = self.title.split('.')
            out[0] += "_%02d."
            out = "".join(out)
            self.title = out
        self.out = result + self.title
        return self.out_title + self.title

