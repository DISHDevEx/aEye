from ultralytics import YOLO
import cv2

class CV():

    def __init__(self) -> None:

        self.model = YOLO
        self.yolo_weight = None
        
    
    def load_yolo_weight(self, weight = 'yolov8s.pt'):
        self.yolo_weight = weight
        self.model(self.yolo_weight)

    def get_yolo_weight(self):
        return self.yolo_weight
    
    def load_model(self, model = None, bucket = None , prefix = None):
        if not model and bucket:
            "load from s3"
        else:
            'load from local'

    def save_model(self):
        "save"
        return self.model



    def train(self,data, parameter):
        result = self.model.train(data = data, parameter = parameter)

    def predict(self, data):
        if 'video':
            'do video'
            pass

        elif 'frame':
            'do frame'
            pass


        