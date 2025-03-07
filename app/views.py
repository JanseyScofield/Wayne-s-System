from app import app
from app import db
from app.models import Usuario, Item
from app.services import usuariosServices, itensServices
from flask import render_template, request, redirect, url_for, session, flash
import bcrypt

@app.route('/login', methods = ['GET', 'POST'])
def tela_login():
    erro = None
    session.clear()
    # Usuario mestre atual para realizar testes: bruce.wayne senha : @Bruceadministrador-seguranca571
    
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

# Região dos endpoints de funcionários

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

@app.route('/funcionarios/apagar', methods = ['GET', 'POST'])
def remover_funcionario():
    if not session:
        return redirect(url_for('tela_login'))
    if request.method == 'GET':
        return render_template('funcionarios/apagar_funcionario.html')
    if request.method == 'POST':
        if request.form.get('nome-funcionario') == '':
            flash('Digite o nome de um funcionário.', 'erro')
            return redirect(url_for('remover_funcionario'))
        funcionario = usuariosServices.buscar_usuario_nome(request.form.get('nome-funcionario'))
        if request.form.get('nome-funcionario') == session['usuario_logado']['nome']:
            flash('Você não pode se apagar do sistema!', 'erro')
            return redirect(url_for('remover_funcionario'))
        if funcionario:
            try:
                usuariosServices.apagar_usuario(funcionario)
                flash('Funcionário apagado com sucesso!', 'sucesso')
                return redirect(url_for('remover_funcionario'))
            except Exception as e:
                flash(str(e), 'erro')
                return redirect(url_for('remover_funcionario'))
        else:
            flash('Funcionário não encontrado. Digite outro.', 'erro')
            return redirect(url_for('remover_funcionario'))
        

@app.route('/funcionarios/buscar', methods=['GET','POST'])
def buscar_funcionario():
    if not session:
        return redirect(url_for('tela_login'))
    if request.method ==  'GET':
        return render_template('funcionarios/buscar_funcionario.html')
    nome_funcionario = request.form.get('nome-funcionario')
    if not nome_funcionario:
        flash('Por favor, digite o nome do funcionário.', 'erro')
        return redirect(url_for('buscar_funcionario'))

    funcionario = usuariosServices.buscar_usuario_nome(nome_funcionario)
    if funcionario:
        return render_template('funcionarios/editar_funcionario.html', funcionario=funcionario)
    else:
        flash('Funcionário não encontrado. Digite outro nome.', 'erro')
        return redirect(url_for('buscar_funcionario'))


@app.route('/funcionarios/editar', methods=['POST'])
def editar_funcionario():
    if not session:
        return redirect(url_for('tela_login'))

    funcionario_nome = request.form.get('funcionario')
    funcao_funcionario = request.form.get('funcao-funcionario')
    permisao_registrar = 1 if request.form.get('permisao-registrar') else 0
    permisao_editar = 1 if request.form.get('permisao-editar') else 0
    permisao_deletar = 1 if request.form.get('permisao-deletar') else 0

    try:
        usuariosServices.atualizar_usuario(
            funcionario_nome,
            funcao_funcionario,
            permisao_registrar,
            permisao_editar,
            permisao_deletar
        )
        flash('Funcionário editado com sucesso!', 'sucesso')
        return redirect(url_for('buscar_funcionario'))
    except Exception as e:
        flash(f'Erro ao atualizar funcionário: {str(e)}', 'erro')
        return redirect(url_for('buscar_funcionario'))

# Fim região funcionários

# Região dos endpoints de iventário

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

    return render_template('inventario/modulo_inventario.html', context=context)

@app.route('/inventario/registrar', methods = ['GET', 'POST'])
def registrar_item():
    if not session:
        return redirect(url_for('tela_login'))
    if request.method == 'GET':
        return render_template('inventario/registrar_item.html')
    if request.method == 'POST':
        if request.form.get('nome-item') == '':
            flash('Digite algum nome para o item.', 'erro')
            return redirect(url_for('registrar_item'))
        if request.form.get('quantidade-item') == '':
            flash('Informe alguma quantidade para o item.', 'erro')
            return redirect(url_for('registrar_item'))
        quantidade_item = int(request.form.get('quantidade-item'))
        
        try:
            itensServices.registrar_item(request.form.get('nome-item'),
                                        request.form.get('categoria-item'),
                                        request.form.get('descricao-item'),
                                        quantidade_item)
            flash('Item cadastrado com sucesso!', 'sucesso')
            return redirect(url_for('registrar_item'))
        except Exception as e:
            flash(f'Erro ao cadastrar item: {str(e)}', 'erro')
            return redirect(url_for('registrar_item'))
        
@app.route('/inventario/visualizar', methods=['GET'])
def visualizar_itens():
    if not session:
        return redirect(url_for('tela_login'))
    itens = Item.query.all()
    qtd_itens_distintos = len(itens)
    return render_template('inventario/visualizar_itens.html', itens=itens, qtd_itens_distintos=qtd_itens_distintos)

@app.route('/inventario/apagar', methods = ['GET', 'POST'])
def remover_item():
    if not session:
        return redirect(url_for('tela_login'))
    if request.method == 'GET':
        return render_template('inventario/apagar_item.html')
    if request.method == 'POST':
        if request.form.get('codigo-item') == '':
            flash('Digite o código de um item.', 'erro')
            return redirect(url_for('remover_item'))
        
        codigo_item = int(request.form.get('codigo-item'))
        item = itensServices.buscar_item_id(codigo_item)
        if item:
            try:
                itensServices.apagar_item(item)
                flash('Item apagado com sucesso!', 'sucesso')
                return redirect(url_for('remover_item'))
            except Exception as e:
                flash(str(e), 'erro')
                return redirect(url_for('remover_item'))
        else:
            flash('Item não encontrado. Digite outro código.', 'erro')
            return redirect(url_for('remover_item'))
        
@app.route('/inventario/buscar', methods=['GET','POST'])
def buscar_item():
    if not session:
        return redirect(url_for('tela_login'))
    if request.method ==  'GET':
        return render_template('inventario/buscar_item.html')
    codigo_item = request.form.get('codigo-item')
    if not codigo_item:
        flash('Por favor, digite o código do item.', 'erro')
        return redirect(url_for('buscar_item'))

    item = itensServices.buscar_item_id(int(codigo_item))
    if item:
        return render_template('inventario/editar_item.html', item=item)
    else:
        flash('Item não encontrado. Digite outro código.', 'erro')
        return redirect(url_for('buscar_item'))
    
@app.route('/inventario/editar', methods=['POST'])
def editar_item():
    if not session:
        return redirect(url_for('tela_login'))

    codigo_item = int(request.form.get('item'))
    categoria = request.form.get('categoria-item')
    quantidade = request.form.get('quantidade-item')
    descricao = request.form.get('descricao-item')

    try:
        itensServices.atualizar_item(
            codigo_item,
            categoria,
            quantidade,
            descricao,
        )
        flash('Item editado com sucesso!', 'sucesso')
        return redirect(url_for('buscar_item'))
    except Exception as e:
        flash(f'Erro ao atualizar item: {str(e)}', 'erro')
        return redirect(url_for('buscar_item'))
    
#Fim região endpoints inventário