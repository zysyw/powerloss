import opendssdirect as dss
import os

# 获取脚本所在的目录
scripts_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)),'scripts')
# 预先为电路配置好带电压源的110kV主变
master_file = os.path.join(scripts_dir, 'master.dss')

dss.Text.Command('Redirect ' & master_file)