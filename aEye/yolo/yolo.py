from ultralytics import YOLO
import boto3

class Yolo:

    def __init__(self) -> None:
        self.model = YOLO
        self.model_weight = None


    def get_yolo_weight(self):
        return self.model_weight
    

    def train(self,data = None):
        
        self.model.train(data = data)
        

    def predict_(self, data = None):

        result = self.model.predict(data)
        return result
        