from app import app
from flask import Flask, render_template
from app.models.line_model import LineModel

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/line_models')
def line_models():
    line_models = LineModel.query.all()
    return render_template('line_models.html', line_models=line_models)

if __name__ == '__main__':
    app.run(debug=True)