import cv2
import sys
import os

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

	print ("Found {0} faces".format(len(faces)))
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

def cropImage(left, top, height, width, image):

	# Crop image to most prominent face or centred rectangle using numpy truncation
	imageCropped = image[top:top+height, left:left+width]

	return imageCropped

def scaleImage(STANDARD_HEIGHT, STANDARD_WIDTH, imageCropped):

	# Scale to standard size
	imageScaled = cv2.resize(imageCropped, (STANDARD_WIDTH, STANDARD_HEIGHT))

	return imageScaled

def saveFile(name, image):

	classpath = os.path.join("./static/faces/processed_images/classifier_images", name).replace(os.sep, "/")
	neurpath = os.path.join("./static/faces/processed_images/neural_images", name).replace(os.sep, "/")

	if cv2.imwrite(classpath, image) and cv2.imwrite(neurpath, image):
		print("Image saved successfully")
	else:
		print("Failed to save image")

def cropAndScale(imagePath, classifier):

	# Define cascade
	HAARpath = "haarcascade_frontalface_default.xml"
	LBPpath = "./venv/Lib/site-packages/cv2/data/lbpcascade_frontalface.xml"
	LBP2path = "./venv/Lib/site-packages/cv2/data/lbpcascade_frontalface_improved.xml"
	if classifier == 1:
		faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + HAARpath)
	elif classifier == 2:
		faceCascade = cv2.CascadeClassifier(LBPpath)
	else:
		faceCascade = cv2.CascadeClassifier(LBP2path)
	
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

	imageCropped = image[top:top+height, left:left+width]
	imageScaled = scaleImage(STANDARD_HEIGHT, STANDARD_WIDTH, imageCropped)

	return imageScaled