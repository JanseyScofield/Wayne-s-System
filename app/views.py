from app import app
from app import db
from app.models import Usuario
from app.services import usuariosServices
from flask import render_template, request, redirect, url_for, session, flash
import bcrypt

@app.route('/login', methods = ['GET', 'POST'])
def tela_login():
    erro = None
    session.clear()
    # Usuario mestre atual : jansey.scofield  senha: @Janseyadministrador-seguranca696
    if request.method == 'POST':
        usuario = usuariosServices.buscar_usuario_nome_usuario(request.form.get('usuario'))
        if usuario:
            if bcrypt.checkpw(request.form.get('senha').encode(), usuario.senha.encode()): 
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
        if request.form.get('nome-funcionario') == '':
            erro = 'Digite um nome para o novo usuário.'
            flash(erro, 'erro')
            return redirect(url_for('registrar_funcionario'))
        funcionario = usuariosServices.buscar_usuario_nome(request.form.get('nome-funcionario'))
        if funcionario:
            erro = 'Já existe funcionário com esse nome.'
            flash(erro, 'erro')
            return redirect(url_for('registrar_funcionario'))
    
        nome_usuario = usuariosServices.gerar_nome_usuario(request.form.get('nome-funcionario'))
        senha_gerada = usuariosServices.gerar_senha(request.form.get('nome-funcionario'), request.form.get('funcao-funcionario'))

        try:
            permisao_registrar = request.form.get('permisao-registrar')
            if permisao_registrar == None:
                permisao_registrar = 0
            else:
                permisao_registrar = 1

            permisao_editar = request.form.get('permisao-editar')
            if permisao_editar == None:
                permisao_editar = 0
            else:
                permisao_editar = 1

            permisao_deletar = request.form.get('permisao-deletar')
            if permisao_deletar == None:
                permisao_deletar = 0
            else:
                permisao_deletar = 1

            usuariosServices.cadastrar_usuario(request.form.get('nome-funcionario'), 
                                            nome_usuario, 
                                            request.form.get('funcao-funcionario'),
                                            senha_gerada,
                                            permisao_registrar,
                                            permisao_editar,
                                            permisao_deletar)
        except Exception as e:
            erro = str(e)
            flash(erro, 'erro')
            return redirect(url_for('registrar_funcionario'))
        else:
            flash(f'Usuário: {nome_usuario} | Senha: {senha_gerada}', 'sucesso')
            return redirect(url_for('registrar_funcionario'))
    
@app.route('/funcionarios/visualizar', methods = ['GET'])
def visualizar_funcionario():
    if not session:
        return redirect(url_for('tela_login'))
    usuarios =  Usuario.query.all()
    return render_template('funcionarios/visualizar_funcionarios.html', usuarios=usuarios, qtd_funcionarios=len(usuarios))

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
