from fileinput import filename
from importlib.resources import path
import os
import shutil
import urllib.request
from app import app
from flask import Flask, request, redirect, jsonify, render_template
from werkzeug.utils import secure_filename
from flask import send_file
import subprocess
from pathlib import Path

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
	#get app path
	app_path = os.path.dirname(os.path.abspath(__file__))
	download_path = os.path.join(app_path, app.config['UPLOAD_FOLDER'])
	#zip all files
	zip_file = shutil.make_archive(base_name='AllUploadedImages', format='zip', base_dir=os.chdir(app_path), root_dir=os.chdir(download_path))
	return send_file(os.path.join(app_path, app.config['UPLOAD_FOLDER'], zip_file), as_attachment=True)
#import ImageClip


#route for build video with ffmpeg
@app.route('/build', methods=['GET'])
def build():
	fps = 25
	#upload folder full path
	app_path = os.path.dirname(os.path.abspath(__file__))
	download_path = os.path.join(app_path, app.config['UPLOAD_FOLDER'])

	
	for i in range(1, 2+1):
		#input directory
		input_file = (os.path.join(str(Path(__file__).parent), '{:02d}.png'.format(i)))
		input_file2 =(os.path.join(str(Path(__file__).parent), ''))
		
		#create video from png files in upload folder with ffmpeg and sent to html page
		#subprocess.call(['ffmpeg', '-framerate', str(fps), '-i', input_file, '-c:v', 'libx264', '-r', '30', '-pix_fmt', 'yuv420p','output.mp4'])
		my_frame = 3
		subprocess.call([
			'ffmpeg',
			'-r', '10',
			'-i', '%03d.png' % my_frame,
			'-r', 'ntsc',
			'movie%03d.mpg' % my_frame,
		])
		#return send_file(os.path.join(app_path, app.config['UPLOAD_FOLDER'], 'output.mp4'), as_attachment=True)
		return render_template('video.html', user_image = 'output.mp4')
	
		
		#return render_template('video.html', video=video)
		return send_file(os.path.join(app_path, app.config['UPLOAD_FOLDER'], 'video.mp4'), as_attachment=True)
	
	
	



if __name__ == "__main__":
    #app.run()
    app.run(host='0.0.0.0', port=5000, debug=True)



#subprocess.call(['ffmpeg', '-framerate', str(fps), '-i', 'uploads/%d.jpg', '-c:v', 'libx264', '-r', '30', '-pix_fmt', 'yuv420p', 'output.mp4'])
#		subprocess.call(['ffmpeg', '-framerate', str(fps), '-i', os.chdir(input_file) , '-c:v', 'libx264', '-profile:v', 'high', '-crf', '20', '-pix_fmt', 'yuv420p', 'output.mp4'])
