import os
import json

# 获取映射配置
def get_mappings(mappingfile):
    # 获取当前模块文件所在的目录
    current_dir = os.path.dirname(os.path.realpath(__file__))
    # 构造配置文件的路径
    mapping_file_path = os.path.join(current_dir, mappingfile)

    with open(mapping_file_path, 'r', encoding='utf-8') as f:
        mappings = json.load(f)

    return mappings

# 获取对象名称映射配置
def get_name_mappings():
    return get_mappings('elements_name_mapping.json')

def get_name_mapping(sheet_name):
    mappings = get_mappings('elements_name_mapping.json')
    if sheet_name in mappings.keys():
        return mappings[sheet_name]
    else:
        return []

#获取属性映射配置
def get_head_mappings():
    return get_mappings('elements_head_mapping.json')

def get_head_mapping(attr_name):
    mappings = get_mappings('elements_head_mapping.json')
    if attr_name in mappings.keys():
        return mappings[attr_name]
    else:
        return []

def get_all_element_names():
    #从头映射字典中的值集合中获取元件的类名称，因为所有的元件都需要做列名称映射
    return get_head_mappings().keys()