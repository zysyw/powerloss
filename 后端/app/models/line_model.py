# models/line_model.py
from app import db

class LineModel(db.Model):

    __tablename__ = 'line_models'

    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(100), nullable=False)
    unit_resistance = db.Column(db.Float, nullable=False)
    unit_reactance = db.Column(db.Float, nullable=False)

    def __init__(self, model, unit_resistance, unit_reactance):
        self.model = model
        self.unit_resistance = unit_resistance
        self.unit_reactance = unit_reactance
