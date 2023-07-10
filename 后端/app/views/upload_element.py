from flask import Blueprint, render_template, request, session
from .file_uploader import FileUploader
from app import app
import pandas as pd
import json
from .scan_file import scan_file
import pickle

upload_bp = Blueprint('upload', __name__, url_prefix='/upload')
upload_folder = app.config['UPLOAD_FOLDER']
allowed_extensions = app.config['ALLOWED_EXTENSIONS']
file_uploader = FileUploader(app,upload_folder,allowed_extensions)

@upload_bp.route('/', methods=['GET', 'POST']) 
def upload_excel():

    display_json = json.dumps({})
    session['opendss_filepath'] = ''

    if request.method == 'POST':

        file = request.files['file']
        filepath = file_uploader.save_file(file)

        if filepath:
            # 读取 excel 文件内容
            opendss_dict = pd.read_excel(filepath, sheet_name=None)

            # 扫描文件，修改名称和属性
            opendss_dict, scan_records = scan_file(opendss_dict)
            scan_records = scan_records.applymap(lambda x: '\\n'.join(x) if isinstance(x, list) else x)
            display_json = json.dumps(scan_records.to_dict('records'))

            # opendss_dict写入文件，向session写入文件路径，向其他路由提供扫描后的文件
            col_missing_not_empty = any(scan_records['col_missing'].apply(lambda x: any(x) if isinstance(x, list) else False))
            data_missing_not_empty = any(scan_records['data_missing'].apply(lambda x: any(x) if isinstance(x, list) else False))
            if not (col_missing_not_empty or data_missing_not_empty):
                opendss_filepath = app.config['OPENDSS_FILEPATH']
                with open(opendss_filepath, 'wb') as f:
                    pickle.dump(opendss_dict, f)
                session['opendss_filepath'] = opendss_filepath

        else:
            display_json = json.dumps({})
            session['opendss_filepath'] = ''

    return render_template('upload.html',  display_json = display_json)