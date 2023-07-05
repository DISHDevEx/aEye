from ultralytics import YOLO
import cv2

class yolo():

    def __init__(self) -> None:

        self.model = YOLO
        self.yolo_weight = 'yolov8s.pt'
        
    
    def load_yolo_weight(self, weight = 'yolov8s.pt'):
        self.yolo_weight = weight
        self.model(self.yolo_weight)

    def get_yolo_weight(self):
        return self.yolo_weight
    
    def load_model(self, local_model = None, bucket = None , prefix = None):
        if not local_model and bucket:
            "load from s3"
        else:
            'load from local'

    def save_model(self):
        "save"
        return self.model

    def upload(self,bucket = None , prefix = None):
        'upload to s3'


    def train(self,data, parameter):

        self.model.train(data = data, parameter = parameter)

    def predict(self, data):
        self.model.predict(data, save = True)
        