from app import db
from datetime import datetime

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    nome = db.Column(db.String(255), nullable = False)
    nome_usuario = db.Column(db.String(50), nullable = False)
    senha = db.Column(db.String(30), nullable = False)
    data_criacao = db.Column(db.DateTime, default = datetime.now())
    id_funcao = db.Column(db.Integer, nullable = False)
    permisao_mansao = db.Column(db.Integer, nullable = False)
    permisao_industria = db.Column(db.Integer, nullable = False)
    permisao_batcaverna = db.Column(db.Integer, nullable = False)

class Funcao(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    descricao = db.Column(db.String, nullable = False)
