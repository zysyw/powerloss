from flask import Blueprint, render_template, request, session
from app import app
from .get_mappings import get_head_mappings,get_all_element_names
import pandas as pd
import pickle
import json
from ..circuit.OpendssElementFactory import ElementFactory
from ..circuit.line import Line
from ..circuit.linecode import Linecode

edit_table_bp = Blueprint('edit_table', __name__, url_prefix='/edit_table')
opendss_dict = {}
table_name = ''

@edit_table_bp.route('/') 
def select_table():
    global opendss_dict,table_name
    
    opendss_filepath = session.get('opendss_filepath', [])
    
    if opendss_filepath:        
        #
        with open(opendss_filepath, 'rb') as f:
            opendss_dict = pickle.load(f)
    else:
        opendss_dict = {}
    
    return render_template('edit_table.html', table_names=get_all_element_names(), current_table = table_name)

@edit_table_bp.route('/edit_element', methods=['POST'])
def edit_element():
    global opendss_dict,table_name
    table_name = request.form.get('table_name')
    
    if not opendss_dict:
        opendss_element =  {}
    else:        
        opendss_element = json.dumps(opendss_dict[table_name].to_dict('records'))
    
    return render_template('edit_element.html', opendss_element = opendss_element, table_names = get_all_element_names(), current_table = table_name)

@edit_table_bp.route('/save_table', methods=['POST'])
def save_table():
    global opendss_dict,table_name
    opendss_filepath = session.get('opendss_filepath', [])
    opendss_element = request.get_json()
    
    #保存回缓存文件
    if opendss_filepath:        
        opendss_dict[table_name] = pd.DataFrame(opendss_element)        
        with open(opendss_filepath, 'wb') as f:
            pickle.dump(opendss_dict, f)
    
    return render_template('edit_element.html', opendss_element = opendss_element, table_names = get_all_element_names(), current_table = table_name)

@edit_table_bp.route('/import', methods=['POST'])
def excel2opendss():
    global opendss_dict,table_name
    
    opendss_element_obj = ElementFactory.create_opendss_element(table_name, opendss_dict[table_name])
    if opendss_element_obj.check():
        opendss_scipots = opendss_element_obj.convert()
    print(opendss_scipots)
    opendss_element = json.dumps(opendss_dict[table_name].to_dict('records'))
    return render_template('edit_element.html', opendss_element = opendss_element, table_names = get_all_element_names(), current_table = table_name)