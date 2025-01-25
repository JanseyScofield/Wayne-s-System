from app import app
from app import db
from app.models import Usuario
from app.services import usuariosServices
from flask import render_template, request, redirect, url_for, session

@app.route('/login', methods = ['GET', 'POST'])
def tela_login():
    erro = None
    session.clear()
    
    if request.method == 'POST':
        usuario = usuariosServices.buscar_usuario_nome_usuario(request.form.get('usuario'))
        if usuario:
            if usuario.senha == request.form.get('senha'): 
                session['usuario_logado'] = {
                    'id' : usuario.id,
                    'nome' : usuario.nome,
                    'funcao' : usuario.id_funcao,
                    'registrar' : usuario.permisao_registrar,
                    'editar' : usuario.permisao_editar,
                    'deletar' : usuario.permisao_deletar
                }
                return  redirect(url_for('home'))
        erro = 'Credenciais inválidas, digite novamente.'          
        
    return render_template('login.html', erro = erro)

@app.route('/home', methods = ['GET'])
def home():
    if not session:
        return redirect(url_for('tela_login'))
    context = {
        'nome' : session['usuario_logado']['nome']
    }

    return render_template('home.html', context=context)

@app.route('/funcionarios', methods = ['GET'])
def funcionarios():
    if not session:
        return redirect(url_for('tela_login'))
    context = {
        'nome' : session['usuario_logado']['nome'],
        'permisao_registrar' : session['usuario_logado']['registrar'],
        'permisao_editar' : session['usuario_logado']['editar'],
        'permisao_deletar' : session['usuario_logado']['deletar']
    }

    return render_template('funcionarios/modulo_funcionarios.html', context=context)

@app.route('/funcionarios/registrar', methods = ['GET', 'POST'])
def registrar_funcionario():
    if not session:
        return redirect(url_for('tela_login'))
    erro = None
    if request.method == "GET":
        return render_template('funcionarios/registrar_funcionario.html')
    if request.method == "POST":
        funcionario = usuariosServices.buscar_usuario_nome(request.form.get('nome-funcionario'))
        if funcionario:
            erro = 'Já existe funcionário com esse nome.'
            return redirect(url_for('registrar_funcionario', erro=erro))
        
        nome_usuario = usuariosServices.gerar_nome_usuario(request.form.get('nome-funcionario'))
        senha_gerada = usuariosServices.gerar_senha(request.form.get('nome-funcionario'), request.form('funcao-funcionario'))

        try:
            usuariosServices.cadastrar_usuario(request.form.get('nome-funcionario'), 
                                            nome_usuario, 
                                            request.form('funcao-funcionario'),
                                            senha_gerada,
                                            request.form('permisao-registrar'),
                                            request.form('permisao-editar'),
                                            request.form('permisao-deletar'))
        except Exception as e:
            erro = str(e)
            return redirect(url_for('registrar_funcionario', erro=erro))
        else:
            context = {
                'mensagem' :'Usuário cadastrado com sucesso!',
                'nome_usuario' : nome_usuario,
                'senha' : senha_gerada
            }

            return redirect(url_for('funcionarios', context=context))
        
        


@app.route('/funcionarios/visualizar', methods = ['GET'])
def visualizar_funcionario():
    if not session:
        return redirect(url_for('tela_login'))
    return render_template('funcionarios/visualizar_funcionarios.html')

@app.route('/funcionarios/visualizar/unico', methods = ['GET'])
def visualizar_unico_funcionario():
    if not session:
        return redirect(url_for('tela_login'))
    return render_template('funcionarios/visualizar_unico_funcionario.html')

@app.route('/funcionarios/remover', methods = ['GET'])
def remover_funcionario():
    if not session:
        return redirect(url_for('tela_login'))
    return render_template('funcionarios/apagar_funcionario.html')

@app.route('/funcionarios/editar', methods = ['GET'])
def editar_funcionario():
    if not session:
        return redirect(url_for('tela_login'))
    return render_template('funcionarios/editar_funcionario.html')

@app.route('/inventario', methods = ['GET'])
def inventario():
    if not session:
        return redirect(url_for('tela_login'))
    context = {
        'nome' : session['usuario_logado']['nome'],
        'permisao_registrar' : session['usuario_logado']['registrar'],
        'permisao_editar' : session['usuario_logado']['editar'],
        'permisao_deletar' : session['usuario_logado']['deletar']
    }

    return render_template('iventario/modulo_inventario.html', context=context)
