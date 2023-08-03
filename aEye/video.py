"""
Module contains the Video class that stores and represents video files as objects.

"""
import cv2
import subprocess
import json
import boto3
from static_ffmpeg import run

s3 = boto3.client("s3")


class Video:
    """
    Video class that encapsulates all necessary video information.
    Also contains some useful utility like the ability to grab frames, process
    video clips, trim them down, crop, etc.
    Attributes
    ----------
    file    : str
        path of the video file associated with the object

    bucket  : str
        JSON dictionary of video metadata, typically streams[0] is the video metadata

    key     : str
        Essentially this is the s3 absolute location of the file

    title   : str
        Title for the output video to build upon

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

    get_file -> str:
        Returns video file path

    get_title -> str:
        Returns video title

    get_width -> str:
        Returns video width as a string

    get_height -> str:
        Returns video height as a string

    get_presigned_url -> str:
        Returns the presigned AWS bucket URL, which acts as the file location for
        videos uploaded via S3

    add_label -> None:
        Adds a passed label to the current video object

    reset_label -> None:
        Sets the video label to an empty string

    add_output_title -> None:
        Adds the passed string to the output title so it can be informative

    create_complex_filter -> None:
        Creates a sequential exection label for modifications that use -vf tag. This
        way multiple -vf filters can be applied to the same video


    """

    def __init__(self, file=None, bucket=None, key=None, title=None) -> None:
        self.file = file
        self.bucket = bucket
        self.key = key
        self.title = title
        self.path = None
        self.meta_data = None
        self.label = ''
        self.complex_filter = []
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
        ---------
            meta_data: dictionary
                The dictionary of metadata for all streams.

        """
        ffmpeg, probe_path = run.get_or_fetch_platform_executables_else_raise()
        if self.meta_data is None:
            fp = None
            if self.file is None:
                fp = self.get_presigned_url()
            elif self.out is not '':
                fp = self.out
            else:
                fp = self.file
            command = f"{probe_path} -hide_banner -show_streams -v error -print_format json -show_format -i {fp}"
            out = subprocess.check_output(command, shell=True).decode("utf-8")
            json_data = json.loads(out)
            self.meta_data = json_data
            return json_data

    def get_codec(self):
        """
        Gets the codec of the current video

        Parameters
        ----------

        Returns
        ----------

        Video codec as a string
        """
        if self.meta_data is not None:
            return self.meta_data["streams"][0]["codec_name"]
        else:
            self.meta_data = self.extract_metadata()
            return self.meta_data["streams"][0]["codec_name"]

    def get_duration(self):
        """
        Gets the current video duration

        Parameters
        ----------

        Returns
        ----------

        The video duration as a STRING. Convert to float before processing if needed
        """
        if self.meta_data is not None:
            return self.meta_data["streams"][0]["duration"]
        else:
            self.meta_data = self.extract_metadata()
            return self.meta_data["streams"][0]["duration"]

    def get_num_frames(self):
        """
        Gets teh number of B-frames in the video

        Parameters
        ----------

        Returns
        ----------

        Returns the number of frames in the current video as a string
        """
        if self.meta_data is not None:
            return self.meta_data["streams"][0]["nb_frames"]
        else:
            self.meta_data = self.extract_metadata()
            return self.meta_data["streams"][0]["nb_frames"]

    def get_file(self):
        """
        Current file path/s3 bucket location

        Parameters
        ----------

        Returns
        ----------

        String of the location of the video file, whether thats a local path or S3 url
        """
        if self.file is None:
            return self.get_presigned_url()
        else:
            return self.file

    def get_width(self):
        """
        Get the pixel width of a video

        Parameters
        ----------

        Returns
        ----------

        Returns the current video's width as a string
        """
        if self.meta_data is not None:
            return self.meta_data["streams"][0]["width"]
        else:
            self.meta_data = self.extract_metadata()
            return self.meta_data["streams"][0]["width"]

    def get_height(self):
        """
        Get the pixel height of a video

        Parameters
        ----------

        Returns
        ----------

        Returns the current video's height as a string
        """
        if self.meta_data is not None:
            return self.meta_data["streams"][0]["height"]
        else:
            self.meta_data = self.extract_metadata()
            return self.meta_data["streams"][0]["height"]

    def cleanup(self) -> None:
        """
        Removes current CV Frame capture

        Parameters
        ----------

        Returns
        ----------

        """
        self.capture.release()

    def get_presigned_url(self, time=600):
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

        Parameters
        ----------
        label : string
            The label is the FFmpeg mod to add to the video

        Returns
        ----------

        None, but updates the current video label
        """
        self.label += label

    def add_output_title(self, title):
        """
        This method will create a name for the output file.

        Parameters
        ----------
        title : string
            Current video title, added to the final output to keep file names useful

        Returns
        ----------

        None, but updates the current video output title
        """
        self.out_title += title

    def reset_label(self):
        """
        This method will reset all ffmpeg label to empty.

        Parameters
        ----------

        Returns
        ----------

        None, but updates the current video label
        """

        self.label = ''

    def get_label(self):
        """
        This method will return the all ffmpeg label from the video.

        Parameters
        ----------

        Returns
        ----------

        String representation of the label
        """
        return self.label

    def set_output(self, new_out):
        """
        This method will set the current video's output

        Parameters
        ----------
        new_out : string
            Usually a path to a file that has been processed in case further processing is needed

        Returns
        ----------

        None, but updates the current video output
        """
        self.out = new_out

    def create_complex_filter(self, video):
        """
        This method is used for creating a complex video filter. This is any overlay that would
        necessitate a re-encoding of the video (ex. Resizing, Blur, Crop, etc) and encapsulates it all as
        one filter with many steps that way all of the filter applications can be completed. Once the complex
        filter is created, it is added to the label. *Has to be final part of label. Already does that so order
        doesn't matter, but if you mess with some stuff and it stops working, that might be why

        Parameters
        ----------
        video: video with VF process(es) like crop or blur

        Returns
        ----------
        Nothing, but the video label is appended with the completed complex filter
        """
        filter_steps = video.complex_filter
        filter_str = " -filter_complex '"
        end = len(filter_steps)
        for i in range(len(filter_steps)):
            filter_str += f"[{i}]{filter_steps[i]}[{i + 1}];"
        filter_str = filter_str.strip(";")
        filter_str += f"' -map [{end}] "
        video.add_label(filter_str)

    def get_output_title(self):
        """
        This method will create the output title for video so the users can know all the labels that happen to the video.
        (I have a better implementation of this, it will be in the next pr after james adds all of the features.)

        Returns
        ---------
            result: string
                The output title of video.
        """

        result = ''
        if '-f segment' in self.label:
            out = self.title.split('.')
            out[0] += "_%02d."
            out = "".join(out)
            self.title = out
        if 'rawvideo' in self.label:
            out = self.title.split('.')
            out[1] = '.yuv'
            out = "".join(out)
            self.title = out
        self.out = result + self.title
        return self.out_title + self.title

    def get_title(self):
        """
        This method will return the video's title.
        This will also create the video title based on its key from s3

        Returns
        ----------
            title: string
                The video's title.
        """

        if not self.title and self.key:
            self.title = self.key.split('/')[-1]
        return self.title
