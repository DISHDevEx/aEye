import cv2
from aEye.extract import (
    extract_metadata,
    cv_extract_frame_at_time,
    extract_many_frames,
    cv_extract_specific_frame,
)
from aEye.split import *
from aEye.crop import *


class Video:
    """
    @:constructor file
        file is the path name for the file
    """

    def __init__(self, file) -> None:
        self.file = file
        self.meta_data = None
        self.cv_video = cv2.VideoCapture(file)

    def get_metadata(self):
        self.meta_data = extract_metadata(self.file)

    def get_codec(self):
        if self.meta_data is not None:
            return self.meta_data["streams"][0]["codec_name"]
        else:
            self.get_metadata()
            self.get_codec()

    def get_duration(self):
        if self.meta_data is not None:
            return self.meta_data["streams"][0]["duration"]
        else:
            self.get_metadata()
            self.get_duration()

    def get_frames(self):
        return self.cv_video.get(cv2.CAP_PROP_FPS)

    def getfile(self):
        """
        returns da file path
        """
        return self.file

    def split_by_time(self, interval, end):
        """
        time split wrapper
        """
        split_on_time(interval, end, self.file)

    def split_interval(self, interval):
        """
        Split video into interval long clips
        """
        split_on_interval(interval, self)

    def split_on_frame(self, frame):
        """
        capture everything after frome
        """
        split_on_frame(frame, self)

    def split_by_frames(self, sframe, frame_dur):
        """
        starting @ sframe, capture the next frame_dur frames
        """
        split_on_frame(sframe, frame_dur, self)

    def crop_section(self, width, height, start_x, start_y):
        """
        Crops a width x height section starting at x, y
        """
        crop_video_section(width, height, start_x, start_y, self)

    def extract_time_frame(self, time):
        """
        Grabs a frame at a given time using OpenCV (faster than FFMpeg)
        """
        cv_extract_frame_at_time(time, self.cv_video)  # need to specify for cv

    def extract_by_frame(self, frame):
        """
        Given a specific frame, extract that frame.
        """
        cv_extract_specific_frame(frame, self.cv_video)

    def extract_frames(self, start_frame, num_frames):
        """
        Extracts num_frames from start, still works using FFMpeg, need
        to test and see if openCv runs this faster.
        """
        extract_many_frames(start_frame, num_frames, self)

    def join_videos(self, video_list):
        #join_videos(video_list)
        cv_join(video_list, 25, "1920x1080")

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

    def flush_output(self):
        """
        static method to clear outputs because I get lazy
        probably a temp thing
        """
        path = "outputs"
        for f in os.listdir(path):
            os.remove(os.path.join(path, f))

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



