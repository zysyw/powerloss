DEBUG = True
MYSQL_HOST = '81.68.100.223' # or '127.0.0.1'
MYSQL_USER = 'Administer'
MYSQL_PASSWORD = 'Ss_123456'
MYSQL_DATABASE = 'powerloss'

SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}'
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = '123456'

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'xlsx'}
OPENDSS_FILEPATH = './uploads/opendss_dict.pkl'