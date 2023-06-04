from flask import Blueprint, render_template, request, redirect, url_for, flash,session
from app import app,db
from sqlalchemy import MetaData, Table, create_engine, text
from ..models.line_model import LineModel

edit_table_bp = Blueprint('edit_table', __name__, url_prefix='/edit_table')

@edit_table_bp.route('/') 
def select_table():
    table_names = get_all_table_names()
    return render_template('edit_table.html', records=None, table_names=table_names)

@edit_table_bp.route('/edit', methods=['POST'])
def edit_table():
    table_names = get_all_table_names()
    table_name = request.form.get('table_name')
    # 获取模型类引用
    model_class = globals()[table_name]
    # 查询该模型的所有记录
    records = model_class.query.all()
    #转成字典，方便序列化
    records_dicts = [record.to_dict() for record in records]
    
    return render_template('edit_table.html', records=records_dicts, table_names=table_names)

# 获取所有表名
def get_all_table_names():
    meta = MetaData()
    meta.reflect(bind=db.engine)
    table_names = [table for table in meta.tables]
    return table_names 