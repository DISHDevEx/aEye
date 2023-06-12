import cv2
import numpy as np
import os

class Video:
    """
    @:constructor file
        file is the path name for the file
    """

    def __init__(self,file , title = None ) -> None:
        """name:str, codec: str, width: int, height: int, duration: float, frames: int"""
        self.file = file
        self.meta_data = 'insert by James'
        #self.codec = codec
        #self.width = int(width)
        #self.height = int(height)
        #self.duration = float(duration)
        #self.frames = int(frames)
        #self.fps = self.frames / self.duration
        #self.meta_data = 'insert by James'
        self.cap = cv2.VideoCapture(file)
        _ , self.image = self.cap.read()
        self.shape = self.image.shape
        self.width = self.shape[0]
        self.height = self.shape[1]
        self.title = title


    def resize_by_ratio(self, x_ratio, y_ratio):
        """
        this method will resize the current video by multiplying 
        the current x and y by the input x_ratio 

        input: FLOAT
        non negative and non zero value

        """

        

        new_width = int(self.width * x_ratio )
        new_height = int(self.height * y_ratio )
        dim = (new_width, new_height)

        fourcc = cv2.VideoWriter.fourcc(*'mp4v')
        out = cv2.VideoWriter('data/output.mp4', fourcc, 30.0, dim)
        
        while True:
            _ ,image = self.cap.read()
            if image is None:
                break
            resized = cv2.resize(image , dim, interpolation = cv2.INTER_AREA)
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

    def write_video(self,path):
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
    data = Video("data/sample1.mp4")
    data.resize_by_ratio(.8,.8)
    print(len(data.frame_array))
    print(data.fps)