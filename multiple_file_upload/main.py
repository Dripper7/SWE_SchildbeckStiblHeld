from fileinput import filename
from importlib.resources import path
import os
import shutil
import urllib.request
from app import app
from flask import Flask, request, redirect, jsonify, render_template
from werkzeug.utils import secure_filename
from flask import send_file


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

#check File type 
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#upload image
@app.route('/')  # GET, for browser, gui will be provided to user
def upload_image():
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
	#delete_zip_files()
	#get all files in uploads
	files = os.listdir(os.path.join(app_path, app.config['UPLOAD_FOLDER']))
	#download_path
	download_path = os.path.join(app_path, app.config['UPLOAD_FOLDER'])
	#get all files in uploads
	files = os.listdir(download_path)
	#zip all files
	#zip_file = shutil.make_archive(base_name='AllUploadedImages', format='zip', base_dir=app_path, root_dir=os.chdir(download_path))
	#create zip file at app path with contents from download path
	zip_file = shutil.make_archive(base_name='AllUploadedImages', format='zip', base_dir=os.chdir(app_path), root_dir=os.chdir(download_path))
	#move zip file from download path to app path
	#download zip file and delete zip file on server when download is finished
	return send_file(os.path.join(app_path, app.config['UPLOAD_FOLDER'], zip_file), as_attachment=True)


def delete_zip_files():
	#get app path
    app_path = os.path.dirname(os.path.abspath(__file__))
    #get all files in uploads
    files = os.listdir(os.path.join(app_path, app.config['UPLOAD_FOLDER']))
    #delete all zip files in upload folder
    for file in files:
        if file.endswith('.zip'):
            os.remove(os.path.join(app_path, file))
    return jsonify({'message' : 'Zip files successfully deleted'})


    
if __name__ == "__main__":
    #app.run()
    app.run(host='0.0.0.0', port=5000, debug=True)

