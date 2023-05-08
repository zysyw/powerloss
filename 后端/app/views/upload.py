from flask import Blueprint, render_template, request, redirect, url_for, flash
from .file_uploader import FileUploader
from flask import session
from app import app,db
from sqlalchemy import MetaData, Table, create_engine, text
import csv
import pandas as pd
from ..models.line_model import LineModel

upload_bp = Blueprint('upload', __name__, url_prefix='/upload')
upload_folder = app.config['UPLOAD_FOLDER']
allowed_extensions = app.config['ALLOWED_EXTENSIONS']
file_uploader = FileUploader(app,upload_folder,allowed_extensions)

@upload_bp.route('/', methods=['GET', 'POST']) 
def upload_csv():
    data = None
    table_names = get_all_table_names()
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
    column_mapping = {
        '导线型号': 'model',
        '电阻(Ω/km)': 'unit_resistance',
        '电抗(Ω/km)': 'unit_reactance',
        # 添加其他映射，如果有的话
    }
    if filepath:
        # 执行导入操作
        df = pd.read_csv(filepath)

        # 对列名进行映射
        df = df.rename(columns=column_mapping)

        # 将数据导入数据库，选择覆盖或追加方式
        df.to_sql(table_name, db.engine, if_exists='replace', index=True, index_label='id')

        flash('File imported into ' +  table_name +' successfully!', 'success')
    else:
        flash('Please upload file before importing file.', 'warn')
        pass
    return redirect(url_for('upload.upload_csv'))

# 获取所有表名
def get_all_table_names():
    meta = MetaData()
    meta.reflect(bind=db.engine)
    table_names = [table for table in meta.tables]
    return table_names    
