"""
Module contains the Video class that stores and represents video files as objects.

"""
import cv2
import boto3
import subprocess
import json
from static_ffmpeg import run

#Please comment this out when setting up a docker image.
#This will fail when we use the docker image in the lambda function on AWS.
#ffmpeg, ffprobe = run.get_or_fetch_platform_executables_else_raise()

s3 = boto3.client("s3")

class Video:
    """
    Video class stores all relevant informations from video file.

    Attributes
    ----------
        file: string
            The path/file name of the video.

        title: string
            The title that represents the video file.

        bucket: string
            The name of the bucket that video exists in.


        key: string
            The key that associates with the video file.





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

    """

    def __init__(self, file=None, bucket=None, key=None, title=None) -> None:
        self.file = file
        self.bucket = bucket
        self.key = key
        self.title = title
        self.meta_data = None
        self.label = ""

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

    def get_meta_data(self):
        """
        This method will run ffprobe to cmd and return the meta data of the video.

        Returns
        ---------
            meta_data: dictionary
                The dictionary of meta data.

        """
        if self.meta_data is None:
            cmd = f"{ffprobe} -hide_banner -show_streams -v error -print_format json -show_format -i {self.get_presigned_url()}"
            out = subprocess.check_output(cmd, shell=True)
            out = json.loads(out)
            self.meta_data = out

        return self.meta_data

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
        return result + self.title
