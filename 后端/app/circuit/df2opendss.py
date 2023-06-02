import pandas as pd
import json
import re
import os

# 示例数据
data = {
    'LineName': ['Line1', 'Line2', 'Line3'],
    'Bus1': ['Bus1', 'Bus2', 'Bus3'],
    'Bus2': ['Bus2', 'Bus3', 'Bus4'],
    'Length': [10, 20, 30],
    'Linecode': ['16', '16', '16']
}

df_lines = pd.DataFrame(data)

def load_config():
    # 获取当前模块文件所在的目录
    current_dir = os.path.dirname(os.path.realpath(__file__))
    # 构造配置文件的路径
    config_file = os.path.join(current_dir, 'opendss_config.json')

    with open(config_file, 'r') as f:
        config = json.load(f)

    return config

def create_scripts_from_df(df, component_type):
    
    # 读取配置文件
    config = load_config()
    
    dss_scripts = []
    required_columns = get_required_columns_from_config(config, component_type)
    if set(required_columns).issubset(df.columns):
        for _, row in df.iterrows():
            dss_scripts.append(config[component_type].format(**row.to_dict()))
    else:
        missing_columns = set(required_columns) - set(df.columns)
        print("DataFrame 缺少以下列：", missing_columns)
    

    return dss_scripts

def get_required_columns_from_config(config, component_type):
    # 从配置文件中获取对应元件的模板字符串
    template_str = config.get(component_type)

    if template_str is None:
        raise ValueError(f"Unsupported component type {component_type}")

    # 使用正则表达式查找模板字符串中的占位符
    required_columns = re.findall(r'\{(.*?)\}', template_str)

    return required_columns

if __name__ == '__main__':
    import os
    print(os.path.dirname(os.path.realpath(__file__)))
    dss_lines = create_scripts_from_df(df_lines, 'LINE')
    # 打印转换后的脚本语句
    for line in dss_lines:
        print(line)
