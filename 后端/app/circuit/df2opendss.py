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

def create_scripts_from_df(df, element_type):
    
    # 读取配置文件
    config = load_config()
    
    dss_scripts = []
    required_columns = get_required_columns_from_config(config, element_type)
    
    if set(required_columns).issubset(df.columns):
        for _, row in df.iterrows():
            # 检查当前行的必需列是否全部不为空
            if not row[required_columns].isnull().any():
                # 格式化并添加到dss_scripts中
                dss_scripts.append(config[element_type].format(**row.to_dict()))
            else:
                # 触发一个错误
                raise ValueError('Row with index {} has null value(s) in required column(s)'.format(_))
    else:
        missing_columns = set(required_columns) - set(df.columns)
        raise ValueError('Missing required column(s): {}'.format(', '.join(missing_columns)))

    return dss_scripts

def get_required_columns_from_config(config, element_type):
    # 从配置文件中获取对应元件的模板字符串
    template_str = config.get(element_type)

    if template_str is None:
        raise ValueError(f"Unsupported component type {element_type}")

    # 使用正则表达式查找模板字符串中的占位符
    required_columns = re.findall(r'\{(.*?)\}', template_str)

    return required_columns

if __name__ == '__main__':

    dss_lines = create_scripts_from_df(df_lines, 'LINE')
    # 打印转换后的脚本语句
    for line in dss_lines:
        print(line)
