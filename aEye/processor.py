"""
Module contains the Processor class that, loads, uploads, and facilitates all video processcing features.

"""

import boto3
import os
import cv2
import logging
from aEye.video import Video
from static_ffmpeg import run
import math
import subprocess
import tempfile
import shutil

ffmpeg, ffprobe = run.get_or_fetch_platform_executables_else_raise()


class Processor:
    """
    Processor is the class that works as a labeler that tags and adds ffmpeg label to video object.

    Methods
    -------

        add_label_resizing_by_ratio(x_ratio, y_ratio,target) -> None:
            Add label of resizing video by multiplying width by the ratio to video.

        add_label_trimming_start_duration(start, duration, target) -> None:
            Add label of trimming video from start input for duration of seconds to video.

        load_and_resize(bucket, prefix, x_ratio, y_ratio) -> None:
            Load in video files and resize by the x and y ratio.

        upload(bucket) -> None:
            Upload the modified video to S3.

        trim_video_start_end(start, end) -> None:
            Given start and end times in seconds, modified a trimmed down version of
            the video to the modified file.

        trim_into_clips(interval) -> None:
            Splits the video into X second clips, sends all these clips to output
            folder.
            *will re-encode

        split_on_frame(frame) -> None:
            Given a specific frame, start the video there, removes any preceding frames.
            *will re-encode

        split_num_frames(start_frame, num_frames) -> None:
            Given a start frame and the amount of frames that a user wants to copy, splits the video to all of the frames
            within that frame range.
            *will re-encode

        crop_video_section(width, height, start_x, start_y) -> None:
            Create a width x height crop of the input video starting at pixel values start_x, start_y and sends the
            smaller video to the modified file.

        cv_extract_frame_at_time(time) -> None:
            Uses openCV cap to pull the frame at a given time. Can use floats for this, will pick the
            closest applicable frame if need be.

        cv_extract_specific_frame(frame) -> None:
            Pulls a specific frame from the video. Nice.

        extract_many_frames(start_frame, num_frames) -> None:
            Given a start frame, extract the next num_frames to output folder. Outputs are in PNG form.

        blur_video(blur_level, blur_steps) -> None:
            Adds the blur_level amount of blur blur_steps amount of times to a video.

        clear_outputs() -> None:
            Deletes all files in the hardcoded directory for output videos (modified)


    """

    def __init__(self) -> None:
        pass

    def add_label_resizing_by_ratio(self, video_list, x_ratio=.8, y_ratio=.8):
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

        logging.info(f"successfully added trimming mod from {start} for {duration} seconds")

        return video_list

    def trim_video_start_end(self, video_list, start, end):
        """
        Given a start time (start) and end time (end) in seconds, this will return a clip
        from start-end time stamps. *Note this works with b frames, there may be slight time offsets as a result

        Parameters
        -------
        video_list : List of all video objects loaded for processing.
        start      : Start time in seconds for the cropped video to begin at
        end        : End time in seconds for where the clip should end.

        Returns
        -------
        None, but creates trimmed video in output folder
        """
        for video in video_list:
            duration = end - start
            cmd = f"{ffmpeg} -y -ss {start} -i '{video.get_file()}' -v quiet -t {duration} -c copy " \
                  f"modified/output_trim_video_start_{start}_end_{end}_{video.title}"
            subprocess.call(cmd, shell=True)
            logging.info(f"Created a sub-video from {start} to {end}")

    def trim_into_clips(self, video_list, interval):
        """
        This method splits a video into *interval* second long clips, but for any remainder
        the last clip will be truncated. Interval should be in seconds! For example: A 43 second long video with a
        10 second interval will produce 5 modified: 4 ten second clips, and one three second long one, rather
        than filling with black space.

        Parameters
        -------
        video_list : List of all video objects loaded for processing.
        interval   : The clip interval in seconds. Note, this will not be 100% accurate, as it will split on
                     the nearest frame its possible to split on.

        Returns
        -------
        None, but creates interval second long videos in output folder
        """
        for video in video_list:
            cmd = (
                f"{ffmpeg} -y -i '{video.get_file()}' -c:v libx264 -map 0 -segment_time {interval} "
                f"-f segment -reset_timestamps 1 -break_non_keyframes 1 "
                f"modified/output_trim_into_{interval}s_clips_%02d_{video.title}"
            )
            subprocess.call(cmd, shell=True)
            logging.info(f"Video has been trimmed into {interval} second long clips!")

    def split_on_frame(self, video_list, frame):
        """
        Given a frame, this method will create a video starting at that specific
        frame and running all the way until the end. Again, might not be the stupidest idea to
        add in some safety/edge case stuff here

        Parameters
        -------
        video_list : List of all video objects loaded for processing.
        frame      : The frame on which the output video will begin on.

        Returns
        -------
        None, but creates trimmed video in output folder
        """
        for video in video_list:
            fps = float(video.get_num_frames()) / float(video.get_duration())
            time_stamp = frame / fps
            cmd = f"{ffmpeg} -y -ss {time_stamp} -i '{video.get_file()}' -v quiet -c:v libx264 -c:a aac" \
                  f" modified/output_split_on_frame_{frame}_{video.title}"
            subprocess.call(cmd, shell=True)
            logging.info(f"Split video at frame {frame}")

    def split_num_frames(self, video_list, start_frame, num_frames):
        """
        Given a passed frame (start_Frame), and a duration (num_frames), which in this instance is the number of
        frames to crop to, it will send a cropped video to the output folder.

        Parameters
        -------
        video_list  : List of all video objects loaded for processing.
        start_frame : This is the frame that the clip will begin at. Sometimes it will not be possible to get the
                      exact start frame, but if this is the case, it will get the closest without truncating the video.
        num_frames  : This is the number of frames that will be in the clip. For example, if num_frames is 60
                      and the video FPS is 30, this will create a two second clip.

        Returns
        -------
        None, but creates trimmed video in output folder
        """
        for video in video_list:
            fps = float(video.get_num_frames()) / float(video.get_duration())
            time_stamp = start_frame / fps
            cmd = (
                f"{ffmpeg} -y -ss {str(time_stamp)} -i '{video.get_file()}' -v quiet -c:v libx264 -frames:v {num_frames}"
                f" modified/output_split_num_frames_{start_frame}_to_{(start_frame + num_frames)}_{video.title}"
            )
            logging.info(f"Encoding {num_frames} from {start_frame}")
            subprocess.call(cmd, shell=True)

    def crop_video_section(self, video_list, start_x, start_y, section_width, section_height):
        """
        Crops a section_width x section_height grab of the video starting at pixel coordinates start_x, start_y
        and just uses the active video object to do so. Note, re-encoding is a necessary
        step for ANY filter application, so there will be noticeable processing time.

        Parameters
        -------
        video_list     : List of all video objects loaded for processing.
        start_x        :The pixel x coordinate for where the crop frame should originate.
        start_y        :The pixel y coordinate for where the crop frame should originate.
        section_width  :Width in pixels for the cropped section.
        section_height :Height in pixels for the cropped section

        Returns
        -------
        None, but creates cropped video in output folder
        """
        for video in video_list:
            cmd = (
                f"{ffmpeg} -y -i '{video.get_file()}' -v quiet -filter:v 'crop={section_width}:{section_height}:{start_x}:{start_y}' "
                f"-c:a copy modified/output_crop_video_{section_width}x{section_height}_section_{video.title}"
            )
            subprocess.call(cmd, shell=True)
            logging.info(f"Created a {section_width}x{section_height} crop at ({start_x},{start_y})")

    def cv_extract_frame_at_time(self, video_list, time):
        """
        Given a time in seconds, this will extract the closest frame.
        Img extraction that takes less than half as long as the FFMpeg version.

        Parameters
        -------
        video_list : List of all video objects loaded for processing.
        time       : Time in seconds to extract frame. Can be a float for higher degree of specificity

        Returns
        -------
        None, but frame grabbed is displayed in output folder
        """
        for video in video_list:
            cv_video = video.capture
            fps = cv_video.get(cv2.CAP_PROP_FPS)
            frame_id = int(fps * time)
            cv_video.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
            ret, frame = cv_video.read()
            actual_title = os.path.splitext(video.title)[0]
            cv2.imwrite(f"modified/output_cv_extract_frame_at_time_{time}_{actual_title}.png", frame)
            logging.info(f"Extracted frame at time {time}")

    def cv_extract_specific_frame(self, video_list, frame):
        """
        OpenCv method to grab a single frame as a PNG. Passed argument frame is the frame that
        will be extracted. (No decimals please)

        Parameters
        -------
        video_list : List of all video objects loaded for processing.
        frame      : The frame number to be saved as a PNG

        Returns
        -------
        None, but frame grabbed is displayed in output folder
        """
        for video in video_list:
            cv_video = video.capture
            cv_video.set(cv2.CAP_PROP_POS_FRAMES, frame)
            ret, output = cv_video.read()
            actual_title = os.path.splitext(video.title)[0]
            cv2.imwrite(f"modified/output_cv_extract_specific_frame_{frame}_{actual_title}.png", output)
            logging.info(f"Frame #{frame} extracted ")

    def extract_many_frames(self, video_list, start_frame, num_frames):
        """
        Given a start_frame, extract the next num_frames from the video, and store the resulting
        collection of frames in the output folder. num_Frames is the number of frames to be returned
        Has the potential to create like a million images, only use this when you REALLY need a lot
        of frames or a specific set of frames.

        Parameters
        -------
        video_list  : List of all video objects loaded for processing.
        start_frame : Number of the frame at which to start all the frame grabs.
        num_frames  : Number of frames to extract. THIS IS THE AMOUNT OF IMAGES PER VIDEO YOU WANT
                      UNLESS YOU NEED A TON OF CONTIGUOUS FRAMES, DO NOT SET THIS TO A HIGH NUMBER.

        Returns
        -------
        None, but frames are displayed in output folder
        """
        for video in video_list:
            vid_obj = video.capture
            actual_title = os.path.splitext(video.title)[0]
            for x in range(num_frames):
                ret, frame = vid_obj.read()
                fn = f"modified/output_extract_many_frames_{start_frame}_{num_frames}_{actual_title}_{x}.png"
                cv2.imwrite(fn, frame)
            logging.info(f"Extracted {num_frames} from video, saved as PNG's")

    def blur_video(self, video_list, blur_level, blur_steps=1):
        """
        Create a Gaussian blur, with the blur_level being the sigma level for the blur, with the
        blur_steps being the amount of times that sigma level is applied to the video. Ex. 6, 2 applies a level 6 blur
        to the video twice. More steps = more blending. Upper limit to steps is 6, default is 1; unsure
        what the upper limit of the sigma is.

        Parameters
        -------
        video_list : List of all video objects loaded for processing.
        blur_level : Integer level to determine the strength of a blur applied. Higher strength is more blur.
        blur_steps : Integer amount of times blur level is applied. 1-6, with each step being a reapplication of
                     the original filter level. Good practice is to have a low blur applied with multiple steps
                     to create a "frosty" blur rather than a pixelated blur.

        Returns
        -------
        None, outputs new videos to modified folder
        """
        for video in video_list:
            output = f"modified/output_blur_{blur_level}_video_{video.title}"
            cmd = f"{ffmpeg} -i '{video.get_file()}' -vf 'gblur=sigma={blur_level}:steps={blur_steps}' -c:a copy " \
                  f"{output}"
            subprocess.call(cmd, shell=True)
            logging.info(f"Created a blur of strength {blur_level} and applied it {blur_steps} times")

    def remove_outputs(self):
        """
        Removes all files in the output folder. Useful for testing/debugging.

        Parameters
        -------

        Returns
        -------
        Empties the directory videos output to.
        """
        dir = 'modified'
        for files in os.listdir(dir):
            path = os.path.join(dir, files)
            try:
                shutil.rmtree(path)
            except OSError:
                os.remove(path)
