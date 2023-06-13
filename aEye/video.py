import ast
import cv2
import subprocess


class Video:
    """
    @:constructor file
        file is the path name for the file
    """

    def __init__(self, file) -> None:
        """name:str, codec: str, width: int, height: int, duration: float, frames: int"""
        self.file = file
        self.meta_data = subprocess.run(["python", "/Users/James.Fagan/Desktop/git/aEye/aEye/extractmd.py"],
                                        capture_output=True, text=True).stdout
        self.codec = (ast.literal_eval(self.meta_data)['streams'][0]['codec_name'])
        self.duration = (ast.literal_eval(self.meta_data)["streams"][0]['duration'])
        self.frames = ast.literal_eval(self.meta_data)["streams"][0]['nb_frames']
        self.cap = cv2.VideoCapture(file)
        _, self.image = self.cap.read()
        self.shape = self.image.shape
        self.width = self.shape[0]
        self.height = self.shape[1]
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.frame_array = []
        self.split_interval = 0

    def getfile(self):
        return self.file

    def splitclips(self, interval):
        self.split_interval = interval
        exec(open("/Users/James.Fagan/Desktop/git/aEye/aEye/split.py").read())

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
    data.splitclips(12)
    # data.resize_by_ratio(.8,.8)
    # print(len(data.frame_array))
    # print(data.fps)