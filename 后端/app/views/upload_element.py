from flask import Blueprint, render_template, request, redirect, url_for, flash,jsonify
from .file_uploader import FileUploader
from app import app, opendss_dict
import os
import json
import pandas as pd

upload_bp = Blueprint('upload', __name__, url_prefix='/upload')
upload_folder = app.config['UPLOAD_FOLDER']
allowed_extensions = app.config['ALLOWED_EXTENSIONS']
file_uploader = FileUploader(app,upload_folder,allowed_extensions)

@upload_bp.route('/', methods=['GET', 'POST']) 
def upload_csv():
    upload_object_counts = {}
    upload_object_types_count = 0
    global_object_counts = {}
    global_object_types_count = 0
    return_message={}
    if request.method == 'POST':
        file = request.files['file']
        filepath = file_uploader.save_file(file)
        if filepath:
            # 读取 excel 文件内容
            excel_dict = pd.read_excel(filepath, sheet_name=None)
            #把excel文件的列名称更改为opendss对象名称，如“导线型号”->“LineModel"
            mapping = get_head_mappings()
            for object_name, df in excel_dict.items():
                if object_name in mapping:
                    df.rename(columns=mapping[object_name], inplace=True)
            # 计算本次上传的统计信息
            upload_object_counts = {name: len(df) for name, df in excel_dict.items()}
            upload_object_types_count = len(excel_dict)
            # 更新全局字典并计算总的统计信息
            opendss_dict.update(excel_dict)
            global_object_counts = {name: len(df) for name, df in opendss_dict.items()}
            global_object_types_count = len(opendss_dict)
            #
            # return_message={'message': 'File uploaded successfully.'}
        else:
            upload_object_counts = {}
            upload_object_types_count = 0
            global_object_counts = {}
            global_object_types_count = 0
            #
            # return_message={'message': 'Failed to upload file. Please try again.'}
    return render_template('upload.html', 
                           upload_object_counts=upload_object_counts, 
                           upload_object_types_count=upload_object_types_count, 
                           global_object_counts=global_object_counts, 
                           global_object_types_count=global_object_types_count, 
                           json_message=return_message)

@upload_bp.route('/import', methods=['POST'])
def csv2database():
    table_data = request.get_json()

    table_name = table_data['table_name']
    data = table_data['data']

    if data:
        # 执行导入操作
        df = pd.DataFrame(data)
        print(df)

        # 对列名进行映射
        #df = df.rename(columns=get_head_mappings()[table_name])

        return jsonify(message='File imported into ' +  table_name +' successfully!')
    else:
        return jsonify(message='Please upload file before importing file.')

# 获取所有表名
def get_head_mappings():
    # 获取当前模块文件所在的目录
    current_dir = os.path.dirname(os.path.realpath(__file__))
    # 构造配置文件的路径
    head_mapping_file = os.path.join(current_dir, 'csv_head_mapping.json')

    with open(head_mapping_file, 'r', encoding='utf-8') as f:
        head_mappings = json.load(f)

    return head_mappings

def get_all_element_names():
    #从头映射字典中的值集合中获取元件的类名称，因为所有的元件都需要做列名称映射
    return get_head_mappings().keys()