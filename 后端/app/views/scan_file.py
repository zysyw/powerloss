import pandas as pd
from .get_mappings import get_name_mapping, get_head_mapping

def scan_file(opendss_dict):
    
    scan_records = pd.DataFrame([], columns=['name_mapping', 'attribute_mapping', 'col_missing', 'data_missing'])

    # 对opendss_dict中的key按elements_name_mapping的设置进行修改，并记录修改记录
    new_opendss_dict = {}
    for sheet_name, df in opendss_dict.items():

        # 记录
        name_mapped_records = []
        attribute_mapped_records = []
        col_missing_records = []
        data_missing_records = []

        element_name = get_name_mapping(sheet_name)
        if element_name:
            # 对df进行检查和修改列名
            element_attribute_mapping = get_head_mapping(element_name)
            if element_attribute_mapping:
                for old_col, new_col in element_attribute_mapping.items():
                    if old_col in df.columns:
                        df.rename(columns={old_col: new_col}, inplace=True)
                        attribute_mapped_records.append(f'列 {old_col} 对应属性 {new_col} ')
                        # 查找该列中缺失数据的行
                        missing_rows = df[df[new_col].isna()].index.tolist()
                        if missing_rows:
                            data_missing_records.append(f'列 {old_col} 中 {missing_rows} 行缺失数据')
                    else:
                        col_missing_records.append(f'缺失列 {old_col} ')
            new_opendss_dict[element_name] = df
            name_mapped_records = [f'页面 {sheet_name} 对应opendss对象 {element_name} ']
        else:
            new_opendss_dict[sheet_name] = df
            name_mapped_records = [f'页面 {sheet_name} 无对应opendss对象']
            attribute_mapped_records = []
            col_missing_records = []
            data_missing_records = []
        new_row = {'name_mapping':name_mapped_records, 'attribute_mapping':attribute_mapped_records, 'col_missing':col_missing_records, 'data_missing':data_missing_records}
        #增加一条记录
        scan_records.loc[len(scan_records)] = new_row    
    
    opendss_dict = new_opendss_dict

    return (opendss_dict, scan_records)
