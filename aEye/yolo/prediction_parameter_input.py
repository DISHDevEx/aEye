"""
Module contains the default prediction parameter for yolov8 model. 

The vaule in this function can be modified and be used directly as paramater in the .predict_ method in the Yolo class.
Example: 
    p = prediction_parameter_input()
    yolo.predict_( data = some_data , **p )

    
.predict_ can also take a small subsets of the diction as arguments below.
Example:
    yolo.predict_( data = some_data, conf = 0.5, save = True)

    
.predict_ can also take a diction of the small subsets.
Example:
    p = {'conf' : 0.50, 'show' : True}
    yolo.predict_( data = some_data, **p)

Please follow the syntax/format of inputting argument above!
"""
def prediction_parameter_input():
    parameter = {
        'conf' : 0.25,	            #object confidence threshold for detection
        'iou'  : 0.7,	            #intersection over union (IoU) threshold for NMS
        'half' : False,	            #use half precision (FP16)
        'device' : None,	        #device to run on, i.e. cuda device=0/1/2/3 or device=cpu
        'show' : False,	            #show results if possible
        'save' : False,	            #save images with results
        'save_txt' : False,	        #save results as .txt file
        'save_conf' : False,        #save results with confidence scores
        'save_crop' : False,        #save cropped images with results
        'hide_labels' : False,      #hide labels
        'hide_conf' : False,        #hide confidence scores
        'max_det' : 300,            #maximum number of detections per image
        'vid_stride' : False,       #video frame-rate stride
        'line_width' : None,        #The line width of the bounding boxes. If None, it is scaled to the image size.
        'visualize' : False,        #visualize model features
        'augment' : False,          #apply image augmentation to prediction sources
        'agnostic_nms' : False,     #class-agnostic NMS
        'retina_masks' : False,     #use high-resolution segmentation masks
        'classes' : None,           #filter results by class, i.e. class=0, or class=[0,2,3]
        'boxes' : True,	            #Show boxes in segmentation predictions
    }
    return parameter