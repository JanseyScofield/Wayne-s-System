from app import db
from datetime import datetime

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key = True, auto_incremente = True)
    nome_usuario = db.Column(db.String, nullable = False)
    senha = db.Column(db.String, nullable = False)
    data_criacao = db.Column(db.DateTime, default = datetime.now())
    id_funcao = db.Column(db.Integer, nullable = False)
    permisao_mansao = db.Column(db.Integer, nullable = False)
    permisao_indutria = db.Column(db.Integer, nullable = False)
    permisao_batcaverna = db.Column(db.Integer, nullable = False)


class Funcao(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    descricao = db.Column(db.String, nullable = False)
