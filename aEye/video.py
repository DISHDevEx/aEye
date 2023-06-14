import os
import cv2
from extractmd import MetaData
from split import *


class Video:
    """
    @:constructor file
        file is the path name for the file
    """

    def __init__(self, file) -> None:
        """name:str, codec: str, width: int, height: int, duration: float, frames: int"""
        self.file = file
        self.meta_data = None

    def get_metadata(self):
        self.meta_data = MetaData.extract_metadata(self.file)

    def get_codec(self):
        return self.meta_data['streams'][0]['codec_name']

    def get_duration(self):
        return self.meta_data['streams'][0]['duration']

    def get_frames(self):
        return self.meta_data['streams'][0]['nb_frames']

    def getfile(self):
        """
        returns da file path
        """
        return self.file

    def split_by_time(self, interval, end=None):
        """
        sets the split interval of the object so it
        can be accessed by the subprocess it sends it
        down to
        """
        if (end is None):
            split_on_time(interval, self.file)
        else:
            split_on_time(interval, end, self.file)

    def split_by_frame(self, sframe, frame_dur=None):
        """
        Basically just a wrapper func for split stuff
        """
        if frame_dur is None:
            split_on_frame(sframe, self)
        else:
            split_on_frame(sframe, frame_dur, self)

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

        fourcc = cv2.VideoWriter.fourcc(*'mp4v')
        out = cv2.VideoWriter('data/output.mp4', fourcc, 30.0, dim)

        while True:
            _, image = self.cap.read()
            if image is None:
                break
            resized = cv2.resize(image, (400, 400), interpolation=cv2.INTER_AREA)
            self.frame_array.append(resized)
            out.write(resized)
        out.release()
        self.cap.release()

    def extract_time_frame(self):
        """
        this method will extract frames with time
        """

    def extract_index_frame(self):
        """
        this method will extract frames with index
        """

    def write_video(self, path):
        """write output video """

    def flush_output(self):
        path = 'outputs'
        for f in os.listdir(path):
            os.remove(os.path.join(path, f))


if __name__ == "__main__":
    print('@@')
    data = Video("/Users/James.Fagan/Documents/longvid.mp4")
    data.get_metadata()
    data.split_by_time(10, 12)
    # data.resize_by_ratio(.8,.8)
    # print(len(data.frame_array))
    # print(data.fps)
