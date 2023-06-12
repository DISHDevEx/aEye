import cv2
import numpy as np
import os

class Video:
    """
    @:constructor file, title
        file is the path name for the video file,
        title is the title of the video if given
    """

    def __init__(self,file , title = None ) -> None:
        self.file = file
        self.meta_data = 'insert by James'

        self.cap = cv2.VideoCapture(file)
        _ , self.image = self.cap.read()
        self.shape = self.image.shape
        self.width = self.shape[0]
        self.height = self.shape[1]
        self.title = title
        self.frame_array = None


    def resize_by_ratio(self, x_ratio, y_ratio):
        """
        this method will resize the current video by multiplying 
        the current x and y by the input x_ratio 

        input: FLOAT
        non negative and non zero value

        """

        #convert ratio into actual dimension 
        new_width = int(self.width * x_ratio )
        new_height = int(self.height * y_ratio )
        dim = (new_width, new_height)

        #using cv2 encode the saved video as mp4
        fourcc = cv2.VideoWriter.fourcc(*'mp4v')
        out = cv2.VideoWriter('data/out_put' +self.title, fourcc, 30.0, dim)

        #loop through each frame and resizing it by on the parameter ratio
        #right now, this function also writes the new video (I will update and change it later)
        while True:
            _ ,image = self.cap.read()
            #if there is no more frames, break from this loop
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

