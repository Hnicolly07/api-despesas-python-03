from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db, jwt
import models

despesa_bp = Blueprint('despesa', __name__)


@despesa_bp.route('/despesa', methods=['POST'])
#@jwt_required()
def criardespesa():
    try:
        nova_despesa = request.get_json()

        if not nova_despesa:
            return jsonify(msg='Dados Insuficientes'), 400

        despesa = models.Despesa(
            descricao = nova_despesa['descricao'],
            valor = nova_despesa['valor'],
            id_categoria = nova_despesa['id_categoria'],
            id_usuario = nova_despesa['id_usuario']
            )
        
        # Adiciona a nova despesa ao banco
        db.session.add(despesa)
        db.session.commit()
        db.session.refresh(despesa)

        despesas_list = []
        despesas_list.append({
            'id': despesa.id,
            'descrição': despesa.descricao,
            'valor': despesa.valor,
            'data': despesa.data.isoformat(),
            'id_categoria': despesa.id_categoria,
            'id_usuário': despesa.id_usuario
        })
        
        return make_response(jsonify(msg='Despesa Cadastrada Com Sucesso!', data=despesas_list)),201
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao cadastrar despesa: {str(e)}")
        return jsonify(msg='Erro ao cadastrar despesa'), 500

# <int:id> para tornar dinâmico, se colocar apenas /id ele entende como str
@despesa_bp.route('/despesa/<int:id>', methods=['PUT'])
#@jwt_required()
def atualizar(id):
   try:
    despesa_atualizar = models.Despesa.query.get(id)
    if not despesa_atualizar:
        return jsonify(msg='Despesa Não Encontrada!'), 404
    
    dados = request.get_json()
    if 'descricao' in dados:
        despesa_atualizar.descricao = dados['descricao']
    if 'valor' in dados:
        despesa_atualizar.valor = dados['valor']
    if 'id_categoria' in dados:
        despesa_atualizar.id_categoria = dados['id_categoria']
    
    db.session.commit()

    despesas_list = []
    despesas_list.append({
        'id': despesa_atualizar.id,
        'descrição': despesa_atualizar.descricao,
        'valor': despesa_atualizar.valor,
        'data': despesa_atualizar.data.isoformat(),
        'id_categoria': despesa_atualizar.id_categoria,
        'id_usuário': despesa_atualizar.id_usuario
    })
    return make_response(jsonify(msg='Despesa Atualizada Com Sucesso!', data=despesas_list)), 200
   except Exception as e:
       db.session.rollback()
       print(f"Erro ao atualizar despesa: {str(e)}")
       return jsonify(msg='Erro ao atualizar despesa'), 500

@despesa_bp.route('/despesa')
#@jwt_required()
def listar():
   # Falta a opção de filtrar por categoria, valor e data e integrar com usuário
    try:
        #id_usuario = get_jwt_identity()

        despesas = models.Despesa.query.all() # retorna uma lista de objetos

        despesas_list = []
        for despesa in despesas:
            despesas_list.append({
            'id': despesa.id,
            'descrição': despesa.descricao,
            'valor': despesa.valor,
            'data': despesa.data.isoformat(),
            'id_categoria': despesa.id_categoria,
            'id_usuário': despesa.id_usuario 
        })
        return make_response(jsonify(despesas_list), 200)
    except Exception as e:
        print(f"Erro ao cadastrar despesa: {str(e)}")
        return jsonify(msg='Erro ao cacadastrar despesa'), 500
    

@despesa_bp.route('/despesa/<int:id>', methods=['DELETE'])
#@jwt_required()
def deletar(id):
    try:
        despesa_deletar = models.Despesa.query.get(id)
        if not despesa_deletar:
            return jsonify(msg='Despesa Não Encontrada'), 404
        db.session.delete(despesa_deletar)
        db.session.commit()
        return jsonify(msg='Despesa deletada com sucesso'), 200
    except Exception as e:
       db.session.rollback()
       print(f"Erro ao deletar despesa: {str(e)}")
       return jsonify(msg='Erro ao deletar despesa'), 500