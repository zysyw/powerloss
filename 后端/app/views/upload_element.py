from flask import Blueprint, render_template, request, redirect, url_for, flash
from .file_uploader import FileUploader
from flask import session
from app import app
import csv
import os
import json
import pandas as pd

upload_bp = Blueprint('upload', __name__, url_prefix='/upload')
upload_folder = app.config['UPLOAD_FOLDER']
allowed_extensions = app.config['ALLOWED_EXTENSIONS']
file_uploader = FileUploader(app,upload_folder,allowed_extensions)

@upload_bp.route('/', methods=['GET', 'POST']) 
def upload_csv():
    data = None
    table_names = get_all_element_names()
    if request.method == 'POST':
        file = request.files['file']
        filepath = file_uploader.save_file(file)
        if filepath:
            flash('File uploaded successfully.', 'success')
            session['file_path'] = filepath
            # 读取 CSV 文件内容
            with open(filepath, 'r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                data = [row for row in reader]
        else:
            flash('Failed to upload file. Please try again.', 'error')
    return render_template('upload.html', data=data, table_names=table_names)

@upload_bp.route('/import', methods=['POST'])
def csv2database():
    filepath = session.get('file_path', None)
    table_name = request.form.get('table_name')

    if filepath:
        # 执行导入操作
        df = pd.read_csv(filepath)

        # 对列名进行映射
        df = df.rename(columns=get_head_mappings()[table_name])

        flash('File imported into ' +  table_name +' successfully!', 'success')
    else:
        flash('Please upload file before importing file.', 'warn')
        pass
    return redirect(url_for('upload.upload_csv'))

# 获取所有表名
def get_head_mappings():
    # 获取当前模块文件所在的目录
    current_dir = os.path.dirname(os.path.realpath(__file__))
    # 构造配置文件的路径
    head_mapping_file = os.path.join(current_dir, 'csv_head_mapping.json')

    with open(head_mapping_file, 'r') as f:
        head_mappings = json.load(f)

    return head_mappings

def get_all_element_names():
    #从头映射字典中的键值集合中获取元件的类名称，因为所有的元件都需要做列名称映射
    return json.loads(get_head_mappings()).keys()