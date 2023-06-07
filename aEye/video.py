class Video:
    def __init__(self,file,name:str, codec: str, width: int, height: int, duration: float, frames: int) -> None:
        self.file = file
        self.meta_data = 'insert by James'
        self.name = name
        self.codec = codec
        self.width = int(width)
        self.height = int(height)
        self.duration = float(duration)
        self.frames = int(frames)
        self.fps = self.frames / self.duration

    def getSize(self):
        print("Video Resolution:", self.width, 'x', self.height)

    def getVideoDetails(self):
        print("Metadata for video: " + self.name)
        self.getSize()
        print("Encoding Format:", self.codec, "Duration (s):", self.duration, "with a total of", self.frames,
              "frames! (" + str(self.fps) + " FPS)")

