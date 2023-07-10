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

    def upload_model_s3(self,bucket = None , prefix = None):
        'upload to s3'


    def train(self,data = None,  **parameter):
        
        self.model.train(data = data , **parameter)
        

    def predict_(self, data = None,  **parameter):

        result = self.model.predict(data, **parameter)
        return result
        