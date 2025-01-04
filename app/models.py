from app import db
from datetime import datetime

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key = True, auto_incremente = True)
    nome_usuario = db.Column(db.String, nullable = False)
    senha = db.Column(db.String, nullable = False)
    data_criacao = db.Column(db.DateTime, default = datetime.now())