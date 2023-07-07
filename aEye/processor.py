"""
Module contains the Processor class that facilitates all video processcing features by adding ffmpeg labels to the videos.

"""

import logging
from static_ffmpeg import run
import math


#ffmpeg, ffprobe = run.get_or_fetch_platform_executables_else_raise()


class Processor:

    """
    Processor is the class that works as a labeler that tags and adds ffmpeg label to video object.

    Methods
    -------

        add_label_resizing_by_ratio(x_ratio, y_ratio,target) -> None:
            Add label of resizing video by multiplying width by the ratio to video.

        add_label_trimming_start_duration(start, duration, target) -> None:
            Add label of trimming video from start input for duration of seconds to video.

    """


    def __init__(self) -> None:
        pass

    def add_label_resizing_by_ratio(self, video_list, x_ratio=0.8, y_ratio=0.8):
        """
        This method will add resizing label to all target the video that will be multiplying the
        width by x_ratio and height by y_ratio.
        Both values have to be non negative and non zero value.

        Parameters
        ----------
            video_list: list
                The list of desired videos that the users want to process.
            x_ratio: float
                The ratio for x/width value.
            y_ratio: float
                The ratio for y/height value.

        Returns
        ---------
            video_list: list
                The list of video that contains the resize label.

        """

        # Go to each video and add the resizing ffmpeg label.
        for video in video_list:
            video.get_meta_data()
            new_width = int(video.meta_data["width"] * x_ratio)
            new_height = int(video.meta_data["height"] * y_ratio)

            video.add_label(
                f"-vf scale={math.ceil(new_width/2)*2}:{math.ceil(new_height/2)*2},setsar=1:1 "
            )

        logging.info(
            f"successfully added resizing lebl to all video by ratio of {x_ratio} and {y_ratio}"
        )

        return video_list

    def add_label_trimming_start_duration(self, video_list, start, duration):
        """
        This method will add the trim label with desired parameters to the video list.

        Parameters
        ----------
            video_list: list
                The list of desired videos that the users want to process.

            start: float
                The start time to trim the video from.

            duration: float
                The duration of time in seconds to trim the start of video.

        Returns
        ---------
            video_list: list
                The list of video that contains the trim label.

        """

        # Generate the desired target list of videos to add label.
        # Add the trim ffmpeg label to all desired videos.
        for video in video_list:
            video.add_label(f"-ss {start} -t {duration} ")

        logging.info(
            f"successfully added trimming label from {start} for {duration} seconds"
        )

        return video_list

    def add_label_change_resolution(self, video_list, desired_resolution):
        """
        Add the label for resizing a video according to desired resolution.
        Height is what determines: 420p, 720p, etc.
        Function will automatically select the correct width based off popular sizing.

        Parameters
        ----------
            video_list: list
                The list of desired videos that the users want to process.

            desired_resolution: string
                The desired resolution for the videos. Values: 1080p,720p,480p,360p,240p

        Returns
        ---------
            video_list: list
                The list of video that contains the trim label.

        """

        popular_resolutions = {
            "1080p": [1920, 1080],
            "720p": [1280, 720],
            "480p": [640, 480],
            "360p": [480, 360],
            "240p": [426, 240],
        }

        try:
            width_height = popular_resolutions[desired_resolution]

            # Generate the desired target list of videos to add label.
            # Add the scale ffmpeg label to all desired videos.
            for video in video_list:
                video.add_label(
                    f"-vf scale={width_height[0]}x{width_height[1]}:flags=lanczos -c:v libx264 -preset slow -crf 21"
                )

            logging.info(f"successfully added resize label for desired_resolution")

        except:
            logging.error(
                "Error: Sorry you did not pick one of the sizes: 1080p,720p,480p,360p,240p as desired_resolution"
            )

        return video_list
