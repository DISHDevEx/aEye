import ast
import cv2
import subprocess
from extractmd import extract_metadata
from split import split_on_time

class Video:
    """
    @:constructor file
        file is the path name for the file
    """

    def __init__(self, file) -> None:
        """name:str, codec: str, width: int, height: int, duration: float, frames: int"""
        self.file = file
        self.meta_data = None
        self.cap = cv2.VideoCapture(file)
        _, self.image = self.cap.read()
        self.shape = self.image.shape
        self.width = self.shape[0]
        self.height = self.shape[1]
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.frame_array = []
        self.split_interval = 0


    def get_metadata(self):
        self.meta_data = extract_metadata(self.file)
        print(self.meta_data)

    def get_codec(self):
        return self.meta_data['streams'][0]['codec_name']

    def get_duration(self):
        return self.meta_data['streams'][0]['duration']

    def getfile(self):
        """
        returns da file path
        """
        return self.file

    def split_clips(self, interval):
        """
        sets the split interval of the object so it
        can be accessed by the subprocess it sends it
        down to
        """
        self.split_interval = interval
        exec(open("/Users/James.Fagan/Desktop/git/aEye/aEye/split.py").read())
        split_on_time(interval,self.file)
        # stdout.PIPE this shit into something useful !!!!

    def pipe_test(self):
        cmd = "cat test | ffprobe -i pipe:0"
        out = subprocess.check_output(cmd, shell=True)
        print("NO WAY THIS WORKS YET: ",out)



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

    """
    def getSize(self):
        print("Video Resolution:", self.width, 'x', self.height)

    def getVideoDetails(self):
        print("Metadata for video: " + self.name)
        self.getSize()
        print("Encoding Format:", self.codec, "Duration (s):", self.duration, "with a total of", self.frames,
              "frames! (" + str(self.fps) + " FPS)")   
    """


if __name__ == "__main__":
    print('@@')
    data = Video("/Users/James.Fagan/Documents/longvid.mp4")
    data.get_metadata()
    data.split_clips(10)
    #data.pipe_test()
    # data.resize_by_ratio(.8,.8)
    # print(len(data.frame_array))
    # print(data.fps)