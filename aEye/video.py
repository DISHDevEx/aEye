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
    split_on_time(start, end) -> None:
        Given start and end times in seconds, outputs a trimmed down version of
        the video to the outputs file.
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
        smaller video to the outputs file.
    moving_crop() -> None:
        Can pass coordinates to move a cropped section while the video plays. Don't use it rn tho pls
    cv_extract_frame_at_time(time) -> None:
        Uses openCV cap to pull the frame at a given time. Can use floats for this, will pick the
        closest applicable frame if need be.
    cv_extract_specific_frame(frame) -> None:
        Pulls a specific frame from the video. Nice.
    extract_many_frames(start_frame, num_frames) -> None:
        Given a start frame, extract the next num_frames to output folder. Sent as PNGs
    resize_by_ratio(x_ratio, y_ratio) -> None:
        Given a ratio between 0 < x < 1, resize the video to that dimension

    """

    def __init__(self, file) -> None:
        self.file = file
        self.meta_data = None
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
        command = f"{ffprobe} -hide_banner -show_streams -v error -print_format json -show_format -i '{self.getfile()}'"
        out = subprocess.check_output(command, shell=True).decode("utf-8")
        json_data = json.loads(out)
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

    def get_frames(self):
        """
        Returns # of frames in video as a string
        """
        if self.meta_data is not None:
            return self.meta_data["streams"][0]["nb_frames"]
        else:
            self.meta_data = self.extract_metadata()
            return self.meta_data["streams"][0]["nb_frames"]

    def getfile(self):
        """
        Returns the file path as a string
        """
        return self.file

    def split_on_time(self, start, end):
        """
        split_on_time(start, end, file)
        This method can be used to extract a clip based on a given start and end point in seconds.
        *Error checking and minute conversion would probably be good...
        Returns
        -------
        None, but creates trimmed video in output folder
        """
        duration = end - start
        cmd = f"{ffmpeg} -y -ss {start} -i {self.getfile()} -v quiet -t {duration} -c copy outputs/timesplit.mp4"
        subprocess.call(cmd, shell=True)

    def split_on_interval(self, interval):
        """
        split_on_time(interval, file)
        This method splits a video into *interval* second long clips, but for any remainder
        the last clip will be truncated. For example: A 43 second long video with a 10 second interval
        will produce 5 outputs: 4 ten second clips, and one three second long one, rather than filling with
        black space. *Probably can be changed if need be but idk why you'd want that?
        Returns
        -------
        None, but creates interval second long videos in output folder
        """
        cmd = (
            f"{ffmpeg} -y -i {self.getfile()} -c copy -v quiet -map 0 -segment_time {interval} "
            f"-f segment -reset_timestamps 1 outputs/output%02d.mp4"
        )
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
        fps = float(self.get_frames()) / float(self.get_duration())
        time_stamp = frame / fps
        cmd = f"{ffmpeg} -y -ss {time_stamp} -i {self.getfile()} -v quiet -c:v libx264 -c:a aac outputs/splitonframe.mp4"
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
        fps = float(self.get_frames()) / float(self.get_duration())
        time_stamp = start_frame / fps
        cmd = (
            f"{ffmpeg} -y -ss {str(time_stamp)} -i {self.getfile()} -v quiet -c:v libx264 -frames:v {num_frames}"
            f" outputs/frames_{start_frame}_to{(start_frame+num_frames)}.mp4"
        )
        print("Encoding ", num_frames, " from ", start_frame)
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
        cmd = (
            f"{ffmpeg} -y -i {self.getfile()} -v quiet -filter:v 'crop={section_width}:{section_height}:{start_x}:{start_y}' "
            f"-c:a copy outputs/sectioncrop.mp4"
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
            f"{ffmpeg} -y -v quiet -ss 0 -t 30 -i {self.getfile()} -filter_complex_script filter_script.txt -acodec copy "
            f"outputs/moving.mp4"
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
        cv_video = self.cv_video
        fps = cv_video.get(cv2.CAP_PROP_FPS)
        frame_id = int(fps * time)
        cv_video.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
        ret, frame = cv_video.read()
        cv2.imwrite("outputs/cv2Frame.png", frame)

    def cv_extract_specific_frame(self, frame):
        """
        OpenCv method to grab a single frame (very cool)
        Returns
        -------
        None, but frame grabbed is displayed in output folder
        """
        cv_video = self.cv_video
        cv_video.set(cv2.CAP_PROP_POS_FRAMES, frame)
        ret, output = cv_video.read()
        cv2.imwrite("outputs/cv2specific.png", output)

    def extract_many_frames(self, start_frame, num_frames):
        """
        Given a starting frame, extract the next num_frames from the video, and store the resulting
        collection of frames in the output folder. USE THIS SPARINGLY!!!! Has the potential to create like
        a million images, only use this when you REALLY need a lot of frames or a specific set of frames.
        Returns
        -------
        None, but frames are displayed in output folder
        """
        cmd = f"{ffmpeg} -i {self.getfile()} -vf select='eq(n\,{start_frame})' -frames:v {num_frames} outputs/emf%02d.png"
        subprocess.call(cmd, shell=True)

    def resize_by_ratio(self, x_ratio, y_ratio):
        """
        this method will resize the current video by multiplying
        the current x and y by the input x_ratio

        input: FLOAT
        non negative and non zero value

        """

        new_width = int(self.width * x_ratio)
        new_height = int(self.height * y_ratio)
        dim = (new_width, new_height)

        fourcc = cv2.VideoWriter.fourcc(*"mp4v")
        out = cv2.VideoWriter("data/output.mp4", fourcc, 30.0, dim)

        while True:
            _, image = self.cap.read()
            if image is None:
                break
            resized = cv2.resize(image, (400, 400), interpolation=cv2.INTER_AREA)
            self.frame_array.append(resized)
            out.write(resized)
        out.release()
        self.cap.release()

    ##############################################
    #  TESTING FUNCTIONS BELOW, WORK IN PROGRESS #
    ##############################################

    def flush_output(self):
        """
        static method to clear outputs because I get lazy
        probably a temp thing
        """
        path = "outputs"
        for f in os.listdir(path):
            os.remove(os.path.join(path, f))

    def join_videos(self, video_list):
        """
        WIP sorta works but is so slow it doesn't really work
        """
        cmd = ""
        inputs = ""
        mapping = ""
        streams = 0
        to_write = ""
        far_cmd = 'scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2[v0]; [v0]'
        for video in video_list:
            video.get_metadata()
            to_write += f"file '{video.getfile()}'\n"
            inputs += "-i " + video.getfile() + " "
            mapping += f"[{streams}:v]{far_cmd} [{streams}:a] "
            streams += 1
            far_cmd = ''
        cmd = f"{ffmpeg} {inputs}-y -filter_complex '{mapping}concat=n={streams}:v=1:a=1 [v] [a]' " \
              f"-map '[v]' -map '[a]' outputs/joined.mp4"
        print(cmd)
        subprocess.call(cmd, shell=True)

    def cv_join(self, videos_list, fps, resolution):
        """
        WIP doesnt work
        """
        new_video = cv2.VideoWriter("new_video.mp4", cv2.VideoWriter_fourcc(*"MPEG"), fps, resolution)

        for video in videos_list:
            cur_v = cv2.VideoCapture(video)
            while cur_v.isOpened():
                r, frame = cur_v.read()
                if not r:
                    break
                new_video.write(frame)
        new_video.release()

    def cmd_multi_test(self):
        """
        Tests multiple commands, just gonna leave it here to figure it out for
        real later
        """
        cmds = [
            f"ffmpeg -y -i {self.getfile()} -v quiet -filter:v 'crop={600}:{400}:{1000}:{200}' "
            f"-c:a copy outputs/domore.mp4",
            f"ffmpeg -y -ss {15} -i outputs/domore.mp4 -v quiet -t {10} "
            f"-c copy outputs/timesplit.mp4",
        ]
        for cmd in cmds:
            subprocess.call(cmd, shell=True)
        print("Done, output timesplit should also be cropped")
