

# Import packages
import os
import argparse
import cv2
import numpy as np
import sys
import glob
import importlib.util
from time import sleep
from picamera import PiCamera
from pymongo import MongoClient
from base64 import b64encode
from datetime import datetime


# host machine ip and mongodb port
DATABASE_DOMAIN = '192.168.1.54'
DATABASE_PORT = 27017

# these values will be updated at bottom of image recognition system
ROOM_ID = 1
backpack_prob = 0.0
suitcase_prob = 0.0
laptop_prob = 0.0
cellphone_prob = 0.0
umbrella_prob = 0.0

# creat db entry
def createEntry(imageData, captureTime):
    dbEntry = {"dateTime": captureTime, 
               "roomID": ROOM_ID, 
               "backpackProb": backpack_prob,
               "suitcaseProb":suitcase_prob, 
               "laptopProb":laptop_prob, 
               "cellphoneProb":cellphone_prob, 
               "umbrellaProb":umbrella_prob, 
               "image":b64encode(imageData)}
    return dbEntry

# connect to server
try:
    print("[+] Connecting to mongoDB server @ {}:{}".format(DATABASE_DOMAIN, DATABASE_PORT))
    mongo_client = MongoClient("mongodb://{}:{}".format(DATABASE_DOMAIN, DATABASE_PORT))
    print("[+] Connected")
except:
    print("[-] Connection failed")
    exit(0)

# authenticate database
try:
    rPiDatabase = mongo_client.rPiData
    print("[+] Authenticating to rPiData database...")
    rPiDatabase.authenticate(name='rPiCamNode', password='G7q1D^3Bh3Ql')
    print("[+] Successfully Authenticated")
except:
    print("[-] Authentication failed")
    exit(0)

# switch to correct collection
try:
    print("[+] Switching to camNodeResults collection...")
    camNodeResultsCollection = rPiDatabase.camNodeResults
    print("[+] Successfully switched")
except:
    print("[-] Switch failed")

# camera setup
camera = PiCamera()

# Define and parse input arguments
parser = argparse.ArgumentParser()
parser.add_argument('--modeldir', help='Folder the .tflite file is located in',
                    required=True)
parser.add_argument('--graph', help='Name of the .tflite file, if different than detect.tflite',
                    default='detect.tflite')
parser.add_argument('--labels', help='Name of the labelmap file, if different than labelmap.txt',
                    default='labelmap.txt')
parser.add_argument('--threshold', help='Minimum confidence threshold for displaying detected objects',
                    default=0.45)
parser.add_argument('--image', help='Name of the single image to perform detection on. To run detection on multiple images, use --imagedir',
                    default=None)
parser.add_argument('--imagedir', help='Name of the folder containing images to perform detection on. Folder must contain only images.',
                    default=None)
parser.add_argument('--edgetpu', help='Use Coral Edge TPU Accelerator to speed up detection',
                    action='store_true')

args = parser.parse_args()

MODEL_NAME = args.modeldir
GRAPH_NAME = args.graph
LABELMAP_NAME = args.labels
min_conf_threshold = float(args.threshold)
use_TPU = args.edgetpu

# Parse input image name and directory. 
IM_NAME = args.image
IM_DIR = args.imagedir

'''
# If both an image AND a folder are specified, throw an error
if (IM_NAME and IM_DIR):
    print('Error! Please only use the --image argument or the --imagedir argument, not both. Issue "python TFLite_detection_image.py -h" for help.')
    sys.exit()
'''




# If neither an image or a folder are specified, default to using 'curImg.jpg' for image name
if (not IM_NAME and not IM_DIR):
    IM_NAME = 'curImg.jpg'

# Import TensorFlow libraries
# If tflite_runtime is installed, import interpreter from tflite_runtime, else import from regular tensorflow
# If using Coral Edge TPU, import the load_delegate library
pkg = importlib.util.find_spec('tflite_runtime')
if pkg:
    from tflite_runtime.interpreter import Interpreter
    if use_TPU:
        from tflite_runtime.interpreter import load_delegate
else:
    from tensorflow.lite.python.interpreter import Interpreter
    if use_TPU:
        from tensorflow.lite.python.interpreter import load_delegate
'''
# If using Edge TPU, assign filename for Edge TPU model
if use_TPU:
    # If user has specified the name of the .tflite file, use that name, otherwise use default 'edgetpu.tflite'
    if (GRAPH_NAME == 'detect.tflite'):
        GRAPH_NAME = 'edgetpu.tflite'
'''

# Get path to current working directory
CWD_PATH = os.getcwd()
'''
# Define path to images and grab all image filenames
if IM_DIR:
    PATH_TO_IMAGES = os.path.join(CWD_PATH,IM_DIR)
    images = glob.glob(PATH_TO_IMAGES + '/*')

if IM_NAME:
    PATH_TO_IMAGES = os.path.join(CWD_PATH,IM_NAME)
    images = glob.glob(PATH_TO_IMAGES)
'''
# Path to .tflite file, which contains the model that is used for object detection
PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,GRAPH_NAME)

# Path to label map file
PATH_TO_LABELS = os.path.join(CWD_PATH,MODEL_NAME,LABELMAP_NAME)

# Load the label map
with open(PATH_TO_LABELS, 'r') as f:
    labels = [line.strip() for line in f.readlines()]

# Have to do a weird fix for label map if using the COCO "starter model" from
# https://www.tensorflow.org/lite/models/object_detection/overview
# First label is '???', which has to be removed.
if labels[0] == '???':
    del(labels[0])

# Load the Tensorflow Lite model.

# If using Edge TPU, use special load_delegate argument
if use_TPU:
    interpreter = Interpreter(model_path=PATH_TO_CKPT,
                              experimental_delegates=[load_delegate('libedgetpu.so.1.0')])
    print(PATH_TO_CKPT)
else:
    interpreter = Interpreter(model_path=PATH_TO_CKPT)

interpreter.allocate_tensors()

# Get model details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]

floating_model = (input_details[0]['dtype'] == np.float32)

input_mean = 127.5
input_std = 127.5

# Loop over every image and perform detection
'''for image_path in images:'''

####################### CLARK ADDITION 1 ###############
while True:

    camera.capture('curImg.jpg')
    image = "curImg.jpg"
####################### CLARK ADDITION 1 END ###########

    # Load image and resize to expected shape [1xHxWx3]
    '''image = cv2.imread(image_path)'''
    image = cv2.imread(image) # replaced line above
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    imH, imW, _ = image.shape 
    image_resized = cv2.resize(image_rgb, (width, height))
    input_data = np.expand_dims(image_resized, axis=0)

    # Normalize pixel values if using a floating model (i.e. if model is non-quantized)
    if floating_model:
        input_data = (np.float32(input_data) - input_mean) / input_std

    # Perform the actual detection by running the model with the image as input
    interpreter.set_tensor(input_details[0]['index'],input_data)
    interpreter.invoke()

    # Retrieve detection results
    boxes = interpreter.get_tensor(output_details[0]['index'])[0] # Bounding box coordinates of detected objects
    classes = interpreter.get_tensor(output_details[1]['index'])[0] # Class index of detected objects
    scores = interpreter.get_tensor(output_details[2]['index'])[0] # Confidence of detected objects
    #num = interpreter.get_tensor(output_details[3]['index'])[0]  # Total number of detected objects (inaccurate and not needed)

    ########## CLARK CHANGE ###############

    objectList = []
    ########## END CLARK CHANGE ##########


    # Loop over all detections and draw detection box if confidence is above minimum threshold
    for i in range(len(scores)):
        if ((scores[i] > min_conf_threshold) and (scores[i] <= 1.0)):

            # Get bounding box coordinates and draw box
            # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
            ymin = int(max(1,(boxes[i][0] * imH)))
            xmin = int(max(1,(boxes[i][1] * imW)))
            ymax = int(min(imH,(boxes[i][2] * imH)))
            xmax = int(min(imW,(boxes[i][3] * imW)))
            
            cv2.rectangle(image, (xmin,ymin), (xmax,ymax), (10, 255, 0), 2)

            # Draw label
            object_name = labels[int(classes[i])] # Look up object name from "labels" array using class index

            ########## CLARK CHANGE ###############
            objectList.append(object_name)
            ########## CLARK CHANGE ###############
            


            label = '%s: %d%%' % (object_name, int(scores[i]*100)) # Example: 'person: 72%'
            labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2) # Get font size
            label_ymin = max(ymin, labelSize[1] + 10) # Make sure not to draw label too close to top of window
            cv2.rectangle(image, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0], label_ymin+baseLine-10), (255, 255, 255), cv2.FILLED) # Draw white box to put label text in
            cv2.putText(image, label, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2) # Draw label text

    # CLARK CHANGE 8Feb2020 ############################
    # rescaling the image 
    scale_percent = 70
    new_width = int(image.shape[1] * scale_percent / 100)
    new_height = int(image.shape[0] * scale_percent / 100)
    dim = (new_width, new_height)

    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    ### END CLARK CHANGE 8Feb2020 #####################

    ########## CLARK CHANGE ###############
    backpack_prob = 1.0 if "backpack" in objectList else 0.0
    suitcase_prob = 1.0 if "suitcase" in objectList else 0.0
    laptop_prob = 1.0 if "laptop" in objectList else 0.0
    cellphone_prob = 1.0 if "cell phone" in objectList else 0.0
    umbrella_prob = 1.0 if "umbrella" in objectList else 0.0
    
    # save and convert image to b64
    saveDate = datetime.now()
    cv2.imwrite('images/{}.jpg'.format(saveDate), resized)
    with open('images/{}.jpg'.format(saveDate), mode='rb') as ourImage: 
        imageContent = ourImage.read()
        ourImage.close()
    
    # add to db
    entry = createEntry(imageContent)
    camNodeResultsCollection.insert_one(entry, saveDate)
    print("[+] Entry made for picutre @ {}".format(saveDate))
    
    ########## CLARK CHANGE ###############


    # All the results have been drawn on the image, now display the image
    cv2.imshow('Object detector', resized)

    # Clean up
    cv2.waitKey(3000)
    cv2.destroyAllWindows()

    # now that we have used the image, delete it to save storage space
    os.remove('images/{}.jpg'.format(saveDate))
    '''
    # Press any key to continue to next image, or press 'q' to quit
    if cv2.waitKey(0) == ord('q'):
        break
    '''
    # sleep 2 sec to give db time to receive last entry
    sleep(2)


