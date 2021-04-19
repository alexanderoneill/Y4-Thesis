from flask import Flask, jsonify, make_response, request, render_template, redirect
from werkzeug.utils import secure_filename # For sanitising input filenames
import os
import cropper # For processing images
import uuid # For uniquely identifying and linking user sessions and submitted images

# I have learned that this is NOT how you're supposed to use Flask oops, sorry!

app = Flask(__name__)

# Config values
app.config["IMAGE_UPLOADS"] = "./static/faces/user_images" # Default directory for uploaded images
app.config["MAX_CONTENT_LENGTH"] = 50 * (1024 ** 2) # Max filesize for uploaded images (50MB)
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "BMP"]

def validateFilename(filename):

	# If object is not a file with an extension
	if not "." in filename: 
		
		return False

	extension = filename.rsplit(".", 1)[1]

	# If permissible filetype
	if extension.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]: 
		
		return True
	
	else:
		
		return False

@app.route("/", methods=["GET", "POST"])
def upload_image():

	if request.method == "POST":
		
		# If the user has submitted a file
		if request.files: 

			image = request.files["image"]

			# If the file has no name
			if image.filename == "": 
				
				print("No filename")
				
				# Return user to page they came from
				return redirect(request.url) 

			# If valid filename
			if validateFilename(image.filename):
				
				# Sanitise filename, and define path to save image to, then save the image
				filename = secure_filename(image.filename) 
				imagepath = ((os.path.join(app.config["IMAGE_UPLOADS"], filename))).replace(os.sep, "/")
				image.save(imagepath)

				# Get value of first dropdown
				firstoption = request.form["firstmethod"]
				if firstoption == "haar":
					firstmethod = 1
				elif firstoption == "lbp":
					firstmethod = 2
				elif firstoption == "lbp2":
					firstmethod = 3
				elif firstoption == "caffe":
					firstmethod = 4
				
				# Get value of second dropdown
				secondoption = request.form["secondmethod"]
				if secondoption == "haar":
					secondmethod = 1
				elif secondoption == "lbp":
					secondmethod = 2
				elif secondoption == "lbp2":
					secondmethod = 3
				elif secondoption == "caffe":
					secondmethod = 4

				givenConfidence = request.form["confidence"]

				# Run face detection and cropper for first image, generate unique identifier for processed image
				imageCropped = cropper.determineMethod(imagepath, firstmethod, givenConfidence)
				secondImageCropped = cropper.determineMethod(imagepath, secondmethod, givenConfidence)
				imageID = str(uuid.uuid4().hex)
				
				# Generate filename for processed image, save processed image
				cropfilename = imageID + "." + filename.rsplit(".")[1]
				cropper.saveFile(cropfilename, imageCropped, secondImageCropped)

				# Redirect user to page that will give them a cookie
				return redirect(request.url + "/" + cropfilename) 

			else:

				print("That file extension is not allowed")
				
				return redirect(request.url)

	return render_template("public/upload_image.html")

@app.route("/<imageID>")
def setCookie(imageID):

	# Redirect user to domain root page and give them a cookie that associates their
	# session with the image they submitted
	response = make_response(redirect("/"))
	response.set_cookie("IID", imageID, 60 * 5)

	return response

if __name__ == "__main__":
	
	app.run(debug=True)