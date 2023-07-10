from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

#opendss_dict = {}            #保存opendss线路计算所需的各类对象，主要用于从文件导入数据、在线编辑数据
#opendss_scripts = []         #保存opendss线路计算所需的脚本语句，从opendss_dict转化而来

from app import routes