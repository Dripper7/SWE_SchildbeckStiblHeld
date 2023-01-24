from fileinput import filename
from importlib.resources import path
import os
import shutil
from app import app
from flask import Flask, request, redirect, jsonify, render_template
from werkzeug.utils import secure_filename
from flask import send_file
from pathlib import Path
import cv2

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

#check File type 
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#route for index
@app.route('/')
def index():
	return render_template('index.html')

#route for templates/download-multiple.html
@app.route('/templates/download-multiple.html')
def download_multiple():
	return render_template('download-multiple.html')

#route for templates/upload-multiple.html
@app.route('/templates/upload-multiple.html')
def upload_multiple():
	return render_template('upload-multiple.html')

#route for templates/upload-multiple.html
@app.route('/templates/playvideo.html')
def play_video():
	return render_template('playvideo.html')

#multiple files upload 
@app.route('/multiple-files-upload', methods=['POST'])
def upload_file():
	# check if the post request has the file part
	if 'files[]' not in request.files:
		resp = jsonify({'message' : 'No file part in the request'})
		resp.status_code = 400
		return resp
	
	files = request.files.getlist('files[]')

	errors = {}
	success = False
	
	for file in files:		
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			#get app path
			app_path = os.path.dirname(os.path.abspath(__file__))
			#apppath + filename
			file.save(os.path.join(app_path, app.config['UPLOAD_FOLDER'], filename))
			success = True
		else:
			errors[file.filename] = 'File type is not allowed'
	
	if success and errors:
		errors['message'] = 'File(s) successfully uploaded'
		resp = jsonify(errors)
		resp.status_code = 206
		return resp
	if success:
		resp = jsonify({'message' : 'Files successfully uploaded'})
		resp.status_code = 201
		return resp
	else:
		resp = jsonify(errors)
		resp.status_code = 400
		return resp

@app.route('/multiple-files-download', methods=['GET'])
def download_file():
	#zip all files and save the zipped file into zips directory
	shutil.make_archive('zips/AllImages', 'zip', 'uploads')
	return send_file(os.path.join('zips\\', 'AllImages.zip'), as_attachment=True)


#build route that takes a name as input in a api call
@app.route('/build', methods=['POST'])
def GetName():
	#check if the post request has the file part
    if 'name' not in request.form:
        resp = jsonify({'message' : 'No name part in the request'})
        resp.status_code = 400
        return resp
    #call build function with name
    return build(request.form['name'])

#play route to playVideo by name
@app.route('/play', methods=['POST'])
def PlayVideo():
	#check if the post request has the file part
    if 'name' not in request.form:
        resp = jsonify({'message' : 'No name part in the request'})
        resp.status_code = 400
        return resp
    #call build function with name
    return play(request.form['name'])
	
def play(videoName):
	#load video
    cap = cv2.VideoCapture('videos/' + videoName + '.avi')
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret==True:
            # Display the resulting frame
            cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

    return 'Video played'

def build(videoName):
	# Define the codec and create VideoWriter object avi output with 4 fps and 4 sek length
	fourcc = cv2.VideoWriter_fourcc(*'XVID')
	out = cv2.VideoWriter('videos/' + videoName + '.avi',fourcc, 1.0, (28,28))
	
	# Load images
	image_folder = 'uploads'
	images = [img for img in os.listdir(image_folder) if img.endswith(".png")]

	for image in images:
		frame = cv2.imread(os.path.join(image_folder, image))
		print(image)
		out.write(frame)
	
	#save video in uploads folder
	
	
	# Release everything if job is finished
	out.release()
	
	#send file
	return send_file('videos/' + videoName + '.avi', as_attachment=True)
	



if __name__ == "__main__":
    #app.run()
    app.run(host='0.0.0.0', port=5000, debug=True)


