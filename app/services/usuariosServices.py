from app.models import db, Usuario
import bcrypt
from random import randint

def checar_funcao(funcao : str):
    if funcao == 'administrador-seguranca':
        return 2
    elif funcao == 'gerente':
        return 3
    else:
        return 4

def gerar_nome_usuario(nome : str):
    lista_nomes = nome.split()
    nome_usuario = lista_nomes[0].lower()
    if len(lista_nomes) > 1:
        nome_usuario = f"{nome_usuario}.{lista_nomes[1].lower()}"
    return nome_usuario

def gerar_senha(nome : str, funcao : str):
    lista_nomes = nome.split()
    return f"@{lista_nomes[0]}{funcao.lower()}{randint(101, 999)}"

def encriptografar_senha(senha : str):
    salt = bcrypt.gensalt()
    senha_hash = bcrypt.hashpw(senha.encode(), salt)
    return senha_hash.decode('utf-8')

def buscar_usuario_nome_usuario(nome : str):
    return Usuario.query.filter_by(nome_usuario=nome).first()

def buscar_usuario_nome(nome_completo : str):
    return Usuario.query.filter_by(nome=nome_completo).first()

def cadastrar_usuario(nome : str, nome_usuario : str, funcao : str, senha_gerada : str, permisao_cadastrar : int, permisao_editar : int, permisao_deletar : int):
    senha_encriptografada = encriptografar_senha(senha_gerada)
    id_funcao = checar_funcao(funcao)

    try:
        novo_usuario = Usuario(nome=nome, 
                            nome_usuario=nome_usuario, 
                            senha=senha_encriptografada, 
                            id_funcao=id_funcao,
                            permisao_registrar=permisao_cadastrar, 
                            permisao_editar=permisao_editar,
                            permisao_deletar=permisao_deletar)
        db.session.add(novo_usuario)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(str(e))
        return f"Erro ao cadastrar usuário: {str(e)}"
    
def atualizar_usuario(usuario_nome : str, funcao : str, permisao_cadastrar : int, permisao_editar : int, permisao_deletar : int):
    usuario = buscar_usuario_nome(usuario_nome)

    try:
        usuario.id_funcao = checar_funcao(funcao)
        usuario.permisao_registrar = permisao_cadastrar
        usuario.permisao_editar = permisao_editar
        usuario.permisao_deletar = permisao_deletar
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(str(e))
        return f"Erro ao editar usuário: {str(e)}"
    
def apagar_usuario(usuario : Usuario):
    try:
        db.session.delete(usuario)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(str(e))
        return f"Erro ao apagar usuário: {str(e)}"