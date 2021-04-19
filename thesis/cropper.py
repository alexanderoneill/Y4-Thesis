import cv2
import sys
import os
import numpy as np

# Scan through image for faces
def detectFaces(gray, cascade):
	
	# v----------v CODE ADAPTED FROM REALPYTHON.COM v---------v
	faces = cascade.detectMultiScale(
	
		gray,
		scaleFactor = 1.1,
		minNeighbors = 5,
		minSize = (30, 30),
		flags = cv2.CASCADE_SCALE_IMAGE

	)
	# ^----------^ CODE ADAPTED FROM REALPYTHON.COM ^---------^
	
	return faces

# Find largest face
def findLargestFace(faces):

	facesDict = {}
	face = 0
	
	# Build dictionary of faces in image, finding the area of the rectangle
	for (left, top, width, height) in faces:
	
		area = width * height

		facesDict[face] = [left, top, width, height, area]

		face += 1
	
	# Find the rectangle with the largest area
	largestArea = 0
	for face in facesDict:
		if facesDict[face][4] > largestArea:
			largestArea = facesDict[face][4]
			largestFace = facesDict[face]

	bigleft, bigtop, bigwidth, bigheight = largestFace[0], largestFace[1], largestFace[2], largestFace[3]

	return (bigleft, bigtop, bigwidth, bigheight)

# If no faces are detected, crop to a region 25% the size of the full image, centred on the centre of the image
def defaultRectangle(gray):

	fullheight, fullwidth = gray.shape

	if fullheight < 30 or fullwidth < 30:
		return(0, 0, fullheight, fullwidth)
	
	# Find centre coords
	verticalCentre = (fullheight // 2)
	horizontalCentre = (fullwidth // 2)

	# Find scaled size of cropped area
	height = int((fullheight / 100) * 25)
	width = int((fullwidth / 100) * 25)

	# Find scaled coords of cropped area
	left = horizontalCentre - (width // 2)
	top = verticalCentre - (height // 2)

	return (left, top, height, width)

def scaleImage(STANDARD_HEIGHT, STANDARD_WIDTH, imageCropped):

	# Scale to standard size
	imageScaled = cv2.resize(imageCropped, (STANDARD_WIDTH, STANDARD_HEIGHT))

	return imageScaled

def saveFile(name, image1, image2):

	classpath = os.path.join("./static/faces/processed_images/classifier_images", name).replace(os.sep, "/")
	neurpath = os.path.join("./static/faces/processed_images/neural_images", name).replace(os.sep, "/")

	if cv2.imwrite(classpath, image1) and cv2.imwrite(neurpath, image2):
		print("Image saved successfully")
	else:
		print("Failed to save image")

def cascadeCrop(imagePath, cascade):

	faceCascade = cv2.CascadeClassifier(cascade)
	
	# Convert image to grayscale for facial detection
	image = cv2.imread(imagePath)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	STANDARD_WIDTH = 600
	STANDARD_HEIGHT = 335

	# Find all faces
	faces = detectFaces(gray, faceCascade)

	# If no faces have been found, use default rectangle
	if len(faces) == 0:
		left, top, height, width = defaultRectangle(gray)
	else: # If faces were found, use largest face
		left, top, height, width = findLargestFace(faces)

	# Crop and scale image to standard dimensions
	imageCropped = image[top:top+height, left:left+width]
	imageScaled = scaleImage(STANDARD_HEIGHT, STANDARD_WIDTH, imageCropped)

	return imageScaled

def deepCrop(imagePath, protoPath, modelPath, givenConfidence):

	# Define CAFFE model and image to use, as well as some variables we will use later
	caffeNet = cv2.dnn.readNetFromCaffe(protoPath, modelPath)
	image = cv2.imread(imagePath)
	(h, w) = image.shape[:2]
	facesDict = {}
	highestConfidence = 0

	STANDARD_WIDTH = 600
	STANDARD_HEIGHT = 335

	# Preprocess image data
	blob = cv2.dnn.blobFromImage(image, 1.0, (30, 30), (104.0, 177.0, 123.0))
	caffeNet.setInput(blob)
	detections = caffeNet.forward()

	# Loop through all detected faces
	for i in range(0, detections.shape[2]):
		confidence = detections[0, 0, i, 2]

		# If detected face exceeds confidence threshold
		if confidence >= (int(givenConfidence)/100):

			# Define bounding box around face
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")

			# Append detected face to dictionary of high-confidence detections
			facesDict[i] = [box, confidence]

	# If there are suitable detections (i.e faces detected)
	if len(facesDict) > 0:
	
		# Loop through all detected faces that match or exceed confidence threshold
		for face in facesDict:

			# Bubble sort faces by confidence level
			if facesDict[face][1] > highestConfidence:
				highestConfidence = facesDict[face][1]
				mostProbableFace = facesDict[face]

		# Get bounding box dimensions of face detection with highest confidence
		left, top, width, height = int(mostProbableFace[0][0]), int(mostProbableFace[0][1]), int(mostProbableFace[0][2]), int(mostProbableFace[0][3])

	else:

		# Use default rectangle for cropping values
		left, top, width, height = defaultRectangle(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))	

	# Crop and scale image using derived dimensions
	imageCropped = image[top:top+height, left:left+width]
	imageScaled = scaleImage(STANDARD_HEIGHT, STANDARD_WIDTH, imageCropped)

	return imageScaled

def determineMethod(imagePath, method, givenCofidence):

	# Define method paths
	HAARpath = "./venv/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml"
	LBPpath = "./venv/Lib/site-packages/cv2/data/lbpcascade_frontalface.xml"
	LBP2path = "./venv/Lib/site-packages/cv2/data/lbpcascade_frontalface_improved.xml"
	CAFFEProtoPath = "deploy.prototxt.txt"
	CAFFEModelPath = "res10_300x300_ssd_iter_140000.caffemodel"

	# Define method
	if method == 1:
		return (cascadeCrop(imagePath, HAARpath))
	elif method == 2:
		return (cascadeCrop(imagePath, LBPpath))
	elif method == 3:
		return (cascadeCrop(imagePath, LBP2path))
	else:
		return (deepCrop(imagePath, CAFFEProtoPath, CAFFEModelPath, givenCofidence))