"""
Module contains the Yolo class that is a wrapper class for the yolov8 model from ultralytics. 
For more information, please refer to https://docs.ultralytics.com/modes/
This class will tweak some methods and their outputs from the original model to match our framework.
"""


from ultralytics import YOLO
import boto3

class Yolo:

    def __init__(self) -> None:
        """
        Yolo stands for 'You only look once'. This class is just a wrapper for the yolov8 model.
        

        Attributes
        ----------
        model: YOLO
            The yolo model imported from ultralytics
        model_weight: str
            The path to the model weight.

        Methods
        ----------
        get_model_weight -> str:
            A getter for the yolo weight.
        load_model_weight -> None:
            Load in model weight locally.
        train -> None:
            Train the model based on the input.
        
        predict_ -> list of result value.
            Predict data based on the current model and input

        """

        self.model = YOLO
        self.model_weight = None
        

    def get_model_weight(self):
        """
        This method will return the path of model weight

        Parameters
        ----------

        Returns
        ----------
        The path of the model weight
        """

        return self.model_weight
    
    def load_model_weight(self, local_path = 'yolov8s.pt'):
        """
        This method will load in from local path and set the model weight.
        By default this function will load in the 2nd smallest pretrained model from ultralytics.
        If 'yolov8s.pt' doesn't exist in your local machine, ultralytics will download the weight 'yolov8s.pt' to the local machine.
        
        ##################################
        This must be called at least once in the beginning to set the weight into model before running .train_ or .predict_

        ##################################

        Parameters
        ----------
            local_path: str
                The local path of the model weight.
                

        Returns
        ----------
        None
        """

        self.model_weight = local_path
        self.model = self.model(local_path)


    def train_(self,data = None, **parameter):
        """
        This method will train the model based on the parameter and the given dataset.
        The structure of the dataset has to be fit the ultralics framework. 
        The best and easiest way to obtain a valid dataset is to used https://universe.roboflow.com/

        Please also refer to training_parameter_input.py for the entire list of all possible **parameter can take in
        and how to use this method properly!


        Parameters
        ----------
            data: str
                The data can be a yaml file or zip file.
                The config in the yaml file and zip file have to match the ultralytics requirement.

            **parameter: dict of argument
                An unpacked the dict of argument that are native from ultralics framework
                

        Returns
        ----------
        None
        """
        
        self.model.train(data = data , **parameter)
        

    def predict_(self, data = None, **parameter):
        """
        This method will predict the model based on the parameter and the given data.
        
        The data can be inputted with many format; it can be a video, an image and even a list of images.
        It can also take in an entire directory path
        Please refer to https://docs.ultralytics.com/modes/predict/#inference-sources 
        for the full list of valid sources, videos, and images format.

        Please also refer to prediction_parameter_input.py for the entire list of all possible **parameter can take in
        and how to use this method properly!

        Parameters
        ----------
            data: str
                The path of the desired data.

            **parameter: dict of argument
                An unpacked  dict of argument that are native from ultralics framework


        Returns
        ----------
            A list of Result object
        """

        result = self.model.predict(data, **parameter)
        return result
    

    