from ultralytics import YOLO
import boto3

class Yolo:

    def __init__(self) -> None:
        self.model = YOLO
        self.model_weight = None
        self._s3 = boto3.client('s3')
        

    def get_yolo_weight(self):
        return self.model_weight
    
    def load_model(self, local_path = 'yolov8s.pt'):

        self.model_weight = local_path
        self.model = self.model(local_path)

    def save_model(self):
        self.model.export()
        return self.model

    def train(self,data = None):
        
        self.model.train(data = data)
        

    def predict_(self, data = None):

        result = self.model.predict(data)
        return result
        