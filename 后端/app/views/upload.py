from flask import Blueprint, render_template, request, redirect, url_for, flash
from .file_uploader import FileUploader
from app import app  
import csv

upload_bp = Blueprint('upload', __name__, url_prefix='/upload/')
upload_folder = app.config['UPLOAD_FOLDER']
allowed_extensions = app.config['ALLOWED_EXTENSIONS']
file_uploader = FileUploader(app,upload_folder,allowed_extensions)

@upload_bp.route('/', methods=['GET', 'POST']) 
def upload():
    data = None
    if request.method == 'POST':
        file = request.files['file']
        filepath = file_uploader.save_file(file)
        if filepath:
            flash('File uploaded successfully.', 'success')
            # 读取 CSV 文件内容
            with open(filepath, 'r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                data = [row for row in reader]
        else:
            flash('Failed to upload file. Please try again.', 'error')
    return render_template('upload.html', data=data)
