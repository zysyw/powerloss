from app import app
from flask import Flask, render_template, request, flash
from app.models.line_model import LineModel

from app.views.upload import upload_bp
from app.views.import_data import import_data_bp


@app.route('/')
def index():
    return "Hello, World!"

@app.route('/line_models')
def line_models():
    line_models = LineModel.query.all()
    return render_template('line_models.html', line_models=line_models)


app.register_blueprint(upload_bp)
app.register_blueprint(import_data_bp)

if __name__ == '__main__':
    app.run(debug=True)