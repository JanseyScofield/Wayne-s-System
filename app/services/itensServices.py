from app.models import db, Item

def checar_categoria_item(categoria : str):
    if categoria == 'insumos-quimicos':
        return 1
    elif categoria == 'veiculos':
        return 2
    elif categoria == 'equipamento-protecao':
        return 3
    else:
        return 4

def registrar_item(nome : str, categoria : str, descricao : str, quantidade : int):
    id_categoria = checar_categoria_item(categoria)

    try:
        novo_item = Item(nome=nome,
                        id_categoria=id_categoria,
                        descricao=descricao,
                        quantidade=quantidade)
        db.session.add(novo_item)
        db.session.commit()
        print('Esta batendo aqui')
    except Exception as e:
        db.session.rollback()
        return f"Erro ao cadastrar item: {str(e)}"

def buscar_item_id(id : int):
    return Item.query.filter_by(id=id)

def apagar_item(item : Item):
    try:
        db.session.delete(item)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return f"Erro ao apagar item: {str(e)}"