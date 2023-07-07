import logging
from static_ffmpeg import run
import math

ffmpeg, ffprobe = run.get_or_fetch_platform_executables_else_raise()


class Labeler:
    """
    The Labler class works by applying "labels" to a Video object. These labels are
    FFmpeg commands that will be executed upon the Aux.execute_label_and_write_local command.
    If two simple labels of the same type (trim for example) are applied, only the most recent
    label will be run. This does not apply for multiple video_filter applications, as those are
    turned into a complex filter and applied sequentially.

    Methods
    -------

    resize_by_ratio(video_list, x_ratio, y_ratio) -> List[Video]:
        Given a ratio from 0 to 1, the video will be resized by that ratio. This uses
        the original dimensions to resize

    change_resolution(video_list, resolution) -> List[Video]:
        Takes a list and a "typical" resolution label like 720p or 360p and resizes the
        video to common aspect ratios.

    trim_video_start_end(video_list, start, end) -> List[Video]:
        Given start and end times in seconds, modified a trimmed down version of
        the video to the modified file.

    trim_into_clips(video_list, interval) -> List[Video]:
        Splits the video into X second clips, sends all these clips to output
        folder.
        *will re-encode

    split_on_frame(video_list, frame) -> List[Video]:
        Given a specific frame, start the video there, removes any preceding frames.
        *will re-encode

    split_num_frames(video_list, start_frame, num_frames) -> List[Video]:
        Given a start frame and the amount of frames that a user wants to copy, splits the video to all of the frames
        within that frame range.
        *will re-encode

    crop_video_section(video_list, width, height, start_x, start_y) -> List[Video]:
        Create a width x height crop of the input video starting at pixel values start_x, start_y and sends the
        smaller video to the modified file.

    blur_video(video_list, blur_level, blur_steps) -> List[Video]:
        Adds the blur_level amount of blur blur_steps amount of times to a video.
        *will re-encode
    """

    def __init__(self) -> None:
        print("---aEye Video Label Maker v0---")
        pass

    def resize_by_ratio(self, video_list, x_ratio=.8, y_ratio=.8):
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
            video.extract_metadata()
            new_width = int(video.get_width() * x_ratio)
            new_height = int(video.get_height() * y_ratio)

            video.add_label(f"-vf scale={math.ceil(new_width / 2) * 2}:{math.ceil(new_height / 2) * 2},setsar=1:1 ")

        logging.info(f"successfully added resizing mod to all video by ratio of {x_ratio} and {y_ratio}")

        return video_list

    def trim_video_start_end(self, video_list, start, end):
        """
        Given a start time (start) and end time (end) in seconds, this will return a clip
        from start-end time stamps. *Note this works with b frames, there may be slight time offsets as a result

        Parameters
        -------

        video_list : List[Video]
            List of all video objects loaded for processing.

        start      : Integer
            Start time in seconds for the cropped video to begin at

        end        : Integer
            End time in seconds for where the clip should end.

        Returns
        -------

        List of videos with labels applied to it
        """
        for video in video_list:
            duration = end - start
            video.add_label(f"-ss {start} -t {duration} ")
            video.add_output_title(f"trimmed_{start}_to_{end}_")
            logging.info(f"Created a sub-video from {start} to {end}")
        return video_list

    def change_resolution(self, video_list, desired_resolution):
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
                video.add_label("-c:v libx264 -preset slow -crf 21 ")
                video.complex_filter.append(f"scale={width_height[0]}x{width_height[1]}:flags=lanczos")
                video.add_output_title(f"resized_{width_height[0]}x{width_height[1]}_")

            logging.info(f"successfully added resize label for desired_resolution")

        except:
            logging.error(
                "Error: Sorry you did not pick one of the sizes: 1080p,720p,480p,360p,240p as desired_resolution"
            )

        return video_list

    def trim_into_clips(self, video_list, interval):
        """
        This method splits a video into *interval* second long clips, but for any remainder
        the last clip will be truncated. Interval should be in seconds! For example: A 43 second long video with a
        10 second interval will produce 5 modified: 4 ten second clips, and one three second long one, rather
        than filling with black space.

        Parameters
        -------

        video_list : List[Video]
            List of all video objects loaded for processing.

        interval   : Float
            The clip interval in seconds. Note, this will not be 100% accurate, as it will split on
            he nearest frame its possible to split on.

        Returns
        -------

        List of Video objects with labels applied.
        """
        for video in video_list:
            video.add_label(
                f" -map 0 -c:a aac -vsync vfr -reset_timestamps 1 -segment_time {interval} -g {interval} -sc_threshold 0 -force_key_frames 'expr:gte(t,n_forced*{interval})' -f segment ")
            video.add_output_title(f"trimmed_{interval}_clips_")
            logging.info(f"Video has been trimmed into {interval} second long clips!")
        return video_list

    def trim_on_frame(self, video_list, frame):
        """
        Given a frame, this method will create a video starting at that specific
        frame and running all the way until the end. Note: Depending on encoding, it can be
        difficult to get the exact frame if it isn't an I/P/B frame.

        Parameters
        -------

        video_list : List[Video]
            List of all video objects loaded for processing.

        frame      : Integer
            The frame on which the output video will begin on.

        Returns
        -------

        List of Video Objects with trim labels applied
        """
        for video in video_list:
            fps = float(video.get_num_frames()) / float(video.get_duration())
            time_stamp = frame / fps
            video.add_label(f"-ss {time_stamp} ")
            video.add_output_title(f"trimmed_on_frame_{frame}_")
            logging.info(f"Split video at frame {frame}")
        return video_list

    def trim_num_frames(self, video_list, start_frame, num_frames):
        """
        Given a passed frame (start_Frame), and a duration (num_frames), which in this instance is the number of
        frames to crop to, it will send a cropped video to the output folder.

        Parameters
        -------

        video_list  : List[Video]
            List of all video objects loaded for processing.

        start_frame : Integer
            This is the frame that the clip will begin at. Sometimes it will not be possible to get the
            exact start frame, but if this is the case, it will get the closest without truncating the video.

        num_frames  : Integer
            This is the number of frames that will be in the clip. For example, if num_frames is 60
            and the video FPS is 30, this will create a two second clip.

        Returns
        -------

        List of Video Objects with trim labels
        """
        for video in video_list:
            fps = float(video.get_num_frames()) / float(video.get_duration())
            time_stamp = start_frame / fps
            logging.info(f"Encoding {num_frames} from {start_frame}")
            video.add_output_title(f"trim_frames_{start_frame}_to_{start_frame + num_frames}_")
            video.add_label(f"-ss {str(time_stamp)} -frames:v {num_frames} ")
        return video_list

    def crop_video_section(self, video_list, start_x, start_y, section_width, section_height):
        """
        Crops a section_width x section_height grab of the video starting at pixel coordinates start_x, start_y
        and just uses the active video object to do so. Note, re-encoding is a necessary
        step for ANY filter application, so there will be noticeable processing time.

        Parameters
        -------

        video_list     : List[Video]
            List of all video objects loaded for processing.

        start_x        : Integer
            The pixel x coordinate for where the crop frame should originate.

        start_y        : Integer
            The pixel y coordinate for where the crop frame should originate.

        section_width  : Integer
            Width in pixels for the cropped section.

        section_height : Integer
            Height in pixels for the cropped section

        Returns
        -------

        A list of Video objects with labels applied
        """
        for video in video_list:
            video.complex_filter.append(f"crop={section_width}:{section_height}:{start_x}:{start_y} ")
            video.add_output_title(f"cropped_{section_width}x{section_height}_")
            logging.info(f"Created a {section_width}x{section_height} crop at ({start_x},{start_y})")
        return video_list

    def blur_video(self, video_list, blur_level, blur_steps=1):
        """
        Create a Gaussian blur, with the blur_level being the sigma level for the blur, with the
        blur_steps being the amount of times that sigma level is applied to the video. Ex. 6, 2 applies a level 6 blur
        to the video twice. More steps = more blending. Upper limit to steps is 6, default is 1; unsure
        what the upper limit of the sigma is.

        Parameters
        -------

        video_list [List] : List[Video]
            List of all video objects loaded for processing.

        blur_level [int]  : Integer
            Integer level to determine the strength of a blur applied. Higher strength is more blur.

        blur_steps [int]  : Integer
            Integer amount of times blur level is applied. 1-6, with each step being a reapplication of
             the original filter level. Good practice is to have a low blur applied with multiple steps
             to create a "frosty" blur rather than a pixelated blur.

        Returns
        -------

        List of videos with the blur label applied
        """
        for video in video_list:
            video.complex_filter.append(f"gblur=sigma={blur_level}:steps={blur_steps} ")
            video.add_output_title(f"blurred_{blur_level}x{blur_steps}_")
            logging.info(f"Created a blur of strength {blur_level} and applied it {blur_steps} times")
        return video_list
