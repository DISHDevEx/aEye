import cv2
import numpy as np
import subprocess
import json
import ffmpy

'''
Method:     extractMetaData(fileName):
Purpose:    Pass in a video path (for now) to extract the metadata of the video. This then
            creates a video object for processing.
For Later:  Purpose is the encapsulation of videos, create a way to ez-import videos rather than file path
            and also potentially come back to add in more critical data additions 
            temp: /Users/James.Fagan/Documents/artloop3.mp4
'''
def extractMetaData(fileName):
    print("Extracting MetaData From Passed Video File")

    probe = ffmpy.FFprobe(executable='./ffprobe',
                          inputs={fileName: None},
                          global_options=['-v', 'error',
                                          '-print_format', 'json',
                                          '-show_format', '-show_streams']
                          ).run(stdout=subprocess.PIPE)
    meta = json.loads(probe[0].decode('utf-8'))

    vidStream = meta['streams'][0]

    currentCodec = vidStream['codec_name']
    videoWidth = vidStream['width']
    videoHeight = vidStream['height']
    videoDuration = vidStream['duration']
    videoFrameCount = vidStream[
        'nb_frames']  # MD For frames may not always be accurate; if this becomes an issue nb_read_frame param can help (probably)

    vidObject = Video(fileName, currentCodec, videoWidth, videoHeight, videoDuration, videoFrameCount, meta)
    vidObject.getVideoDetails()

    print("Total # of streams:", len(meta['streams']))
    return vidObject


class Video:
    """
    @:constructor file
        file is the path name for the file
    """

    def __init__(self,file, codec: str, width: int, height: int, duration: float, frames: int, metadata: dict) -> None:
        self.file = file
        self.meta_data = metadata
        self.codec = codec
        self.width = int(width)
        self.height = int(height)
        self.duration = float(duration)
        self.frames = int(frames)
        self.fps = self.frames / self.duration
        self.cap = cv2.VideoCapture(file)
        if self.cap is None:
            print("Error opening video stream or file")


    def trimbytime(self):
        '''
        trim by time wrapper function, basically just asks the users to input time constraints for cropping
        giving them an end time. A little bit of early onset error checking, poor inputs dont cause crashes anymore!
        '''
        print("Current Video Duration is",self.duration,"\nPlease enter constraints to split video by:")
        starttime = input("Cropped Video Starts At: ")
        endtime = input("Cropped Video Ends At:")
        print(starttime,endtime)
        if float(starttime) in range(0, int(self.duration)) and float(endtime) in range(0, int(self.duration)) and float(starttime) <= float(endtime):
            self.fftrim(starttime, endtime)
        else:
            print("Unable to crop video with given times : "+starttime+"-"+endtime+"\nPlease ensure that these fall within the logical constraints!")

    def fftrim(self,start,end):
        '''
        *Hopefully* a reusable method to crop down any video with some quick FFMpeg processing
        '''
        ff = ffmpy.FFmpeg(executable='./ffmpeg',
                          inputs={self.file: "-y -hide_banner -v quiet -ss "+str(start)+" -to "+str(end)},  # Lots of these tags just make it look nicer
                          outputs={"cropped.mp4": "-c copy"}
        )
        ff.run()


    def resize(self, x_ratio, y_ratio):
        """
        this method will resize the current video by multiplying 
        the current x and y by the input x_ratio 

        input: FLOAT
        non negative and non zero value

        """
        width = int(self.cap.shape[1] * x_ratio / 100)
        height = int(self.cap.shape[0] * y_ratio / 100)
        dim = (width, height)
        self.cap = cv2.resize(self.cap , dim, interpolation = cv2.INTER_AREA)

    def extract_time_frame(self):
        """
        this method will extract frames with time
        """
        print("The Vide")

    def extract_index_frame(self):
        """
        this method will extract frames with index
        """


    def getSize(self):
        print("Video Resolution:", self.width, 'x', self.height)

    def getVideoDetails(self):
        print("Metadata for video: " + self.file)
        self.getSize()
        print("Encoding Format:", self.codec, "Duration (s):", self.duration, "with a total of", self.frames, "frames! (" + str(self.fps) + " FPS)")




if __name__ == '__main__':
    #filename = input("Enter a file Path for a video:")
    filename = '/Users/James.Fagan/Documents/artloop3.mp4'
    vidObj = extractMetaData(filename)
    vidObj.trimbytime()
