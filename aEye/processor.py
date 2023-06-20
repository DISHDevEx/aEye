"""
Module contains the Processor class that, loads, uploads, and facilitates all video processcing features.

"""

import boto3
import os
import cv2
import logging
from aEye.video import Video
import subprocess
from static_ffmpeg import run
ffmpeg, ffprobe = run.get_or_fetch_platform_executables_else_raise()

class Processor:

    """
    Processor is the class that works act a pipeline to load, process, and upload all video from S3 bucket.

    Attributes
    ----------
        video_list: list
            A list to append the Video classes.

        _s3: botocore.client.S3
            An internal variable to talk to S3.


    Methods
    -------
        load(bucket, prefix) -> list[Video]:
            Loads in video files as Video classes into a list from S3.


        resize_by_ratio(x_ratio, y_ratio) -> None:
            Resize video by multiplying width by the ratio.

        load_and_resize(bucket, prefix, x_ratio, y_ratio) -> None:
            Load in video files and resize by the x and y ratio.

        upload(bucket) -> None:
            Upload the modified video to S3.

        split_on_time(start, end) -> None:
            Given start and end times in seconds, modified a trimmed down version of
            the video to the modified file.

        split_on_interval(interval) -> None:
            Splits the video into X second clips, sends all these clips to output
            folder.
            *Note this should be done LAST for any multiprocessing

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

        moving_crop() -> None:
            Can pass coordinates to move a cropped section while the video plays. Don't use it right now please...

        cv_extract_frame_at_time(time) -> None:
            Uses openCV cap to pull the frame at a given time. Can use floats for this, will pick the
            closest applicable frame if need be.

        cv_extract_specific_frame(frame) -> None:
            Pulls a specific frame from the video. Nice.

        extract_many_frames(start_frame, num_frames) -> None:
            Given a start frame, extract the next num_frames to output folder. Outputs are in PNG form.

        resize_by_ratio(x_ratio, y_ratio) -> None:
            Given a ratio between 0 < x < 1, resize the video to that dimension
    """

    def __init__(self) -> None:
        self.video_list = []
        self._s3 = boto3.client('s3')

    def get_video_list(self):
        return self.video_list

    def load(self, bucket=  'aeye-data-bucket', prefix='input_video/'):
        """
        This method will load the video files from S3 and save them
        into a list of video classes.

         Parameters
        ----------
            bucket: string
                The bucket name to path into S3 to get the video files.
            prefix: string
                The folder name where the video files belong in the S3 bucket.

        Returns
        -------
            video_list: list
                The list of all video files loaded from S3 bucket.
        """

        result = self._s3.list_objects(Bucket = bucket, Prefix = prefix)

        for i in result["Contents"]:



            #When we request from S3 with the input parameters, the prefix folder will also pop up as a object.
            #This if-statement is to skip over the folder object since we are only interested in the video files.
            if i["Key"] == prefix:
                continue

            title = i["Key"].split(prefix)[1]
            #In order to convert video file from S3 to cv2 video class, we need its url.
            url = self._s3.generate_presigned_url( ClientMethod='get_object', Params={ 'Bucket': bucket, 'Key': i["Key"] }, ExpiresIn=100000)
            self.video_list.append(Video(url, title))

        logging.info(f"Successfully loaded video data from {bucket}")
        logging.info(f"There are total of {len(self.video_list)} video files")

        return self.video_list


    def resize_by_ratio(self, x_ratio = .8, y_ratio = .8) -> None:
        """
        This method will resize the video by multiplying the width by x_ratio and height by y_ratio.
        Both values have to be non negative and non zero value.

        Parameters
        ----------
            x_ratio: float
                The ratio for x/width value.
            y_ratio: float
                The ratio for y/height value.


        """

        #This will loop to the list of videos to apply the resizing feature.
        for video in self.video_list:

            new_width = int(video.width * x_ratio )
            new_height = int(video.height * y_ratio )
            dim = (new_width, new_height)

            fourcc = cv2.VideoWriter.fourcc(*'mp4v')
            out = cv2.VideoWriter('modified/out_put_' +video.title, fourcc, 30.0, dim)

            #This loops to each frame of a video and resizes the current dimension to the new dimension.
            while True:
                _ ,image = video.cap.read()

                if image is None:
                    break

                resized = cv2.resize(image , dim, interpolation = cv2.INTER_AREA)
                out.write(resized)

            out.release()
            video.cleanup()

        logging.info(f"successfully resized all video by ratio of {x_ratio} and {y_ratio}" )

    def load_and_resize(self, bucket=  'aeye-data-bucket', prefix='input_video/', x_ratio = .8, y_ratio = .8) -> None:
        """
        This method will call on load() and resize_by_ratio() methods to load and resize by the input parameters.
        Both values have to be non negative and non zero value.

        Parameters
        ----------
            bucket: string
                The bucket name to path into S3 to get the video files.
            prefix: string
                The folder name where the video files belong in the S3 bucket.

            x_ratio: float
                The ratio for x/width value.
            y_ratio: float
                The ratio for y/height value.
        """


        self.load(bucket,prefix)
        self.resize_by_ratio(x_ratio,y_ratio)

    def upload(self, bucket=  'aeye-data-bucket') -> None:
        """
        This method will push all modified videos to the S3 bucket and delete all video files from local machine.

        Parameters
        ----------
            bucket: string
                The bucket name/location to upload on S3.
        """


        for video in self.video_list:

            path = 'modified/output_' + video.title
            response = self._s3.upload_file( path, bucket,  path)

            #This will delete all file from RAM and local machine.
            os.remove(path)
            video.cleanup()

        logging.info("successfully upload the output files and remove them from local machine")

        print("successfully upload the output files S3 bucket: s3://aeye-data-bucket/modified/")
        print("successfully remove the output file from local machine")


    def split_on_time(self, start, end):
        """
        split_on_time(start, end, file)
        This method can be used to extract a clip based on a given start and end point in seconds.
        *Error checking and minute conversion would probably be good...
        Returns
        -------
        None, but creates trimmed video in output folder
        """
        for video in self.video_list:
            duration = end - start
            cmd = f"{ffmpeg} -y -ss {start} -i '{video.getfile()}' -v quiet -t {duration} -c copy " \
                  f"modified/split_on_time_" + video.title
            subprocess.call(cmd, shell=True)

    def split_on_interval(self, interval):
        """
        split_on_time(interval, file)
        This method splits a video into *interval* second long clips, but for any remainder
        the last clip will be truncated. For example: A 43 second long video with a 10 second interval
        will produce 5 modified: 4 ten second clips, and one three second long one, rather than filling with
        black space. *Probably can be changed if need be but idk why you'd want that?
        Returns
        -------
        None, but creates interval second long videos in output folder
        """
        for video in self.video_list:
            cmd = (
                f"{ffmpeg} -y -i '{video.getfile()}' -c copy -map 0 -segment_time {interval} "
                f"-f segment -reset_timestamps 1 modified/interval_split%02d.mp4"
            )
            print(cmd)
            subprocess.call(cmd, shell=True)

    def split_on_frame(self, frame):
        """
        split_on_frame(frame, video)
        Given a passed frame, this method will create a video starting at that specific
        frame and running all the way until the end. Again, might not be the stupidest idea to
        add in some safety/edge case stuff here
        Returns
        -------
        None, but creates trimmed video in output folder
        """
        for video in self.video_list:
            fps = float(video.get_frames()) / float(video.get_duration())
            time_stamp = frame / fps
            cmd = f"{ffmpeg} -y -ss {time_stamp} -i '{video.getfile()}' -v quiet -c:v libx264 -c:a aac" \
                  f" modified/split_on_frame.mp4"
            subprocess.call(cmd, shell=True)

    def split_num_frames(self, start_frame, num_frames):
        """
        split_num_frames(start, duration, video_object)
        Given a passed frame (start), and a duration, which in this instance is the number of
        frames to crop to, it will send a cropped video to the output folder.
        *Could change num_frames to a time duration to make more sense to a human user but like
        just use split_on_time???
        Returns
        -------
        None, but creates trimmed video in output folder
        """
        for video in self.video_list:
            fps = float(video.get_frames()) / float(video.get_duration())
            time_stamp = start_frame / fps
            cmd = (
                f"{ffmpeg} -y -ss {str(time_stamp)} -i '{video.getfile()}' -v quiet -c:v libx264 -frames:v {num_frames}"
                f" modified/frames_{start_frame}_to{(start_frame + num_frames)}.mp4"
            )
            logging.info("Encoding ", num_frames, " from ", start_frame)
            subprocess.call(cmd, shell=True)

    def crop_video_section(self, section_width, section_height, start_x, start_y):
        """
        crop_video_section(width, height, x, y, video)
        Crops a Width x Height section of the video starting at pixel coordinates x, y
        and just uses the active video object to do so. Note, re-encoding is a necessary
        step for ANY filter application, so there will be noticeable processing time.
        Returns
        -------
        None, but creates cropped video in output folder
        """
        for video in self.video_list:
            cmd = (
                f"{ffmpeg} -y -i '{video.getfile()}' -v quiet -filter:v 'crop={section_width}:{section_height}:{start_x}:{start_y}' "
                f"-c:a copy modified/section_crop.mp4"
            )
            subprocess.call(cmd, shell=True)

    def moving_crop(self):
        """
        Very basic version of what should hopefully be very important.
        Will need to pass a lot more params but right now swaprect looks like:
        =width:height:x1:y1:x2:y2:....(n,startFrame,endFrame)
        *** HARDCODED FOR NOW, MAY REPLACE W OPENCV MASK SO IM NOT GONNA WORK ON IT UNTIL I KNOW
        Returns
        -------
        None, but creates cropped video in output folder
        """
        for video in self.video_list:
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
                f"{ffmpeg} -y -v quiet -ss 0 -t 30 -i '{video.getfile()}' -filter_complex_script filter_script.txt -acodec copy "
                f"modified/moving_crop.mp4"
            )
            subprocess.call(cmd, shell=True)
            os.remove("filter_script.txt")

    def cv_extract_frame_at_time(self, time):
        """
        Img extraction that takes less than half as long as the FFMpeg version
        Returns
        -------
        None, but frame grabbed is displayed in output folder
        """
        for video in self.video_list:
            cv_video = video.cv_video
            fps = cv_video.get(cv2.CAP_PROP_FPS)
            frame_id = int(fps * time)
            cv_video.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
            ret, frame = cv_video.read()
            cv2.imwrite("modified/cv2frame_at_time.png", frame)

    def cv_extract_specific_frame(self, frame):
        """
        OpenCv method to grab a single frame (very cool)
        Returns
        -------
        None, but frame grabbed is displayed in output folder
        """
        for video in self.video_list:
            cv_video = video.cv_video
            cv_video.set(cv2.CAP_PROP_POS_FRAMES, frame)
            ret, output = cv_video.read()
            cv2.imwrite("modified/cv2specific_frame.png", output)

    def extract_many_frames(self, start_frame, num_frames):
        """
        Given a starting frame, extract the next num_frames from the video, and store the resulting
        collection of frames in the output folder. USE THIS SPARINGLY!!!! Has the potential to create like
        a million images, only use this when you REALLY need a lot of frames or a specific set of frames.
        Returns
        -------
        None, but frames are displayed in output folder
        """
        for video in self.video_list:
            cmd = f"{ffmpeg} -i '{video.getfile()}' -vf select='eq(n\,{start_frame})' -frames:v {num_frames} " \
                  f"modified/extract_many_frames%02d.png"
            subprocess.call(cmd, shell=True)


    def cleanup(self) -> None:
        """
        This method will release the current view of video object from RAM.
        """
        self.capture.release()



