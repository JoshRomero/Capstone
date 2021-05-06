import os
import argparse
import cv2
import numpy as np
import sys
import glob
import importlib.util
from time import sleep
from picamera import PiCamera
from datetime import datetime
import requests
from base64 import b64encode
import json
#-------------------------------------------NETWORK STUFF------------------------------------------
def getIdToken():
    user = open(os.environ['CURR_USER'], "r")
    jsonUser = json.loads(user.read())
    
    return jsonUser["idToken"]

def getUID():
    user = open(os.environ['CURR_USER'], "r")
    jsonUser = json.loads(user.read())
    
    try:
        userID = jsonUser["userId"]
    except:
        userId = jsonUser["localId"]
    
    return userId

def getRoomID():
    room = open(os.environ['ROOM_ID'], "r")
    jsonRoom = json.loads(room.read())
    
    return jsonRoom["roomID"]

items = {"laptopProb": 0.0, "cellphoneProb": 0.0, "remoteProb": 0.0, "handbagProb": 0.0, "bookProb": 0.0 }
def createEntry(captureTime):
    dbEntry = {"userID": getUID(),
               "dateTime": captureTime,
               "roomID": getRoomID(), 
               "remoteProb": items["remoteProb"],
               "laptopProb": items["laptopProb"],
               "cellphoneProb": items["cellphoneProb"],
               "handbagProb": items["handbagProb"],
               "bookProb": items["bookProb"],
    }
    
    print(dbEntry)
    
    return dbEntry
#------------------------------------END NETWORK STUFF------------------------------------------------------



#----------------------------------------CNN STUFF----------------------------------------------
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

# Get path to current working directory
CWD_PATH = "/home/pi/tflite1/"

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

####################### CLARK ADDITION 1 ###############
camera = PiCamera()
while True:

	camera.capture('/home/pi/tflite1/curImg.jpg')
	saveDate = datetime.now()
	print("[+] Picture captured at the dateTime: {}".format(saveDate))
	image = "curImg.jpg"
####################### CLARK ADDITION 1 END ###########

    # Load image and resize to expected shape [1xHxWx3]
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
	items["remoteProb"] = 1.0 if "remote" in objectList else 0.0
	items["handbagProb"] = 1.0 if "handbag" in objectList else 0.0
	items["laptopProb"] = 1.0 if "laptop" in objectList else 0.0
	items["cellphoneProb"] = 1.0 if "cell phone" in objectList else 0.0
	items["bookProb"] = 1.0 if "book" in objectList else 0.0        

	# save and convert image to b64
	cv2.imwrite('/home/pi/tflite1/images/{}.jpg'.format(saveDate), resized)

	#with open('images/{}.jpg'.format(saveDate), mode='rb') as ourImage: 
	 	# imageContent = ourImage.read()
	 	# ourImage.close()

	# add to db
	entry = createEntry(user["localId"], saveDate)
	file = {"image": open('/home/pi/tflite1/images/{}.jpg'.format(saveDate), 'rb')}

	# send post request to server to insert image and related data
	header = {"Authorization": getIdToken()}
	url = "https://objectfinder.tech/pidata"
	r = requests.post(url, files=file, data=entry, headers=header)
	print("[+] Entry made for picture @ {}".format(datetime))

	########## CLARK CHANGE ###############


	# All the results have been drawn on the image, now display the image
	cv2.imshow('Object detector', resized)

	# Clean up
	cv2.waitKey(3000)
	cv2.destroyAllWindows()
 
	# now that we have used the image, delete it to save storage space
	os.remove('images/{}.jpg'.format(saveDate))
 
	statusFile = open(os.environ['CURR_STATUS'], "r")
	jsonStatusFile = json.loads(statusFile.read())
	if(jsonStatusFile['status'] != 'ACTIVE'):
		break

	# sleep 2 sec to give db time to receive last entry
	sleep(2)
#----------------------------------------END CNN STUFF-----------------------------------------------------

            

	

            
