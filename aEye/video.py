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
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.frame_array = []


    def set_dim(self,dim):
        self.shape = dim
        self.width = self.shape[0]
        self.height = self.shape[1]

        
    def set_frame_array(self, array):
        self.frame_array = array

    def get_frame_array(self):
        return self.frame_array

    def write_video(self,path):
        """write output video """

        fourcc = cv2.VideoWriter.fourcc(*'mp4v')
        out = cv2.VideoWriter(path, fourcc, self.fps, (self.width,self.height))

