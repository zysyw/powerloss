from flask import Blueprint
import os

import_data_bp = Blueprint('import_data', __name__, url_prefix='/import_data/')

@import_data_bp.route('/')
def import_data():
    return 'Data imported successfully.'