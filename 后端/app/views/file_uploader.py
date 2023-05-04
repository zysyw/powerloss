import os
from werkzeug.utils import secure_filename

class FileUploader:
    def __init__(self, app, upload_folder='uploads', allowed_extensions=None):
        self.app = app
        self.upload_folder = upload_folder
        self.allowed_extensions = allowed_extensions
        self.app.config['UPLOAD_FOLDER'] = self.upload_folder

    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.allowed_extensions

    def save_file(self, file):
        if file and self.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(self.app.config['UPLOAD_FOLDER'], filename)
            # 输出绝对路径
            absolute_path = os.path.abspath(filepath)
            print(f'文件将保存到：{absolute_path}')
            ##
            file.save(filepath)
            return filepath
        return None
