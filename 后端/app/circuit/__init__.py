import opendssdirect as dss
import os

# 获取脚本所在的目录
scripts_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)),'opendss_scripts')
# 预先为电路配置好带电压源的110kV主变
master_file = 'Redirect ' + os.path.join(scripts_dir, 'master.dss')

dss.Text.Command(master_file)

if __name__ == '__main__':
    print(dss.Transformers.Count())