from ultralytics import YOLO
import cv2
import os
import boto3

class Yolo():

    def __init__(self) -> None:

        self.model = YOLO
        self.model_weight = None
        self._s3 = boto3.client('s3')
        

    def get_yolo_weight(self):
        return self.model_weight
    
    def load_model(self, local_path = None, bucket = None , key = None):
        if not local_path and bucket:
            s3_model = self._s3.get_object( Bucket = bucket, Key = key)
            self.model_weight = s3_model['Body']
            self.model = self.model(s3_model['Body'])

        else:
            self.model_weight = local_path
            self.model = self.model(local_path)

    def save_model(self):
        "save"
        return self.model

    def upload_model_s3(self,bucket = None , prefix = None):
        'upload to s3'


    def train(self,data = None,  **parameter):
        
        self.model.train(data = data , **parameter)
        

    def predict_(self, data = None,  **parameter):

        result = self.model.predict(data, **parameter)
        return result
        
