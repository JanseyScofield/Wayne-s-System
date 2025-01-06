from app import app
from app import db
from app.models import Usuario
from flask import render_template, request, redirect, url_for, session

@app.route('/login', methods = ["GET", "POST"])
def tela_login():
    erro = None

    if request.method == 'POST':
        usuario = Usuario.query.filter_by(nome_usuario=request.form.get('usuario')).first()
        if usuario:
            if usuario.senha == request.form.get('senha'): 
                session['usuario_logado'] = {
                    'id' : usuario.id,
                    'nome' : usuario.nome,
                    'funcao' : usuario.id_funcao,
                    'mansao' : usuario.permisao_mansao,
                    'industira' : usuario.permisao_industria,
                    'batcaverna' : usuario.permisao_batcaverna
                }
                return  redirect(url_for('home'))
        erro = 'Credencias inválidas, digite novamente.'          
        
    return render_template('login.html', erro = erro)

@app.route('/home', methods = ['GET'])
def home():
    context = {
        'nome' : session['usuario_logado']['nome']
    }

    return render_template('home.html', context=context)