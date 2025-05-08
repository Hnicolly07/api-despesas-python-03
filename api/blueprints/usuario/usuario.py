from flask import Flask, Blueprint, jsonify, render_template, request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from passlib.hash import bcrypt
from extensions import db
from models import Usuario
import logging


usuario_bp = Blueprint('usuario', __name__)

#Login
@usuario_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        nome = request.json.get('nome')
        senha = request.json.get('senha')
        if not nome or not senha:
            return jsonify({'msg': 'nome e senha são obrigatórios'}), 400

            # Buscar o usuário no banco de dados pelo username
        user = Usuario.query.filter_by(nome=nome).first()

        if not user:
            return jsonify({'msg': 'Usuário não existe'}), 401

            # Verificar se a senha fornecida corresponde ao hash armazenado no banco de dados
        if bcrypt.verify(senha, user.senha):
            access_token = create_access_token(identity=str(user.id))
            return jsonify(access_token=access_token), 200
                #return render_template('sucesso.html')
        else:
                #return render_template('falha.html')
            return jsonify({'msg': 'Senha incorreta'}), 401

     # Criar usuário
@usuario_bp.route('/usuario', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        nome = data['nome']
        email = data['email']
        senha = data['senha']

            # Hashear a senha            
        hashed_password_str = bcrypt.hash(senha)
            
        new_user = Usuario(nome=nome, email=email, senha=hashed_password_str)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'user created'}), 201
    except KeyError as e:
        db.session.rollback()
        logging.error(f"Erro ao criar usuário (dados ausentes): {e}")
        return jsonify({'message': f'missing data: {e}'}), 400
    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao criar usuário: {e}")
        return jsonify({'message': 'error creating user'}), 500
           
# ESTE TRECHO NÃO ESTÁ FUNCIONANDO AINDA
@usuario_bp.route('/protegido', methods=['GET'])
@jwt_required()
def protegido():
    current_user = get_jwt_identity()
    return render_template('sucesso.html')
        # return jsonify(logado_como=current_user), 200

    # Lista todos os usuários
@usuario_bp.route('/usuario', methods=['GET'])
def get_users():
    try:
        users = Usuario.query.all()
        return jsonify([usuario.json() for usuario in users]), 200
    except Exception as e:
        logging.error(f"Erro ao obter usuários: {e}")
        return jsonify({'message': 'error getting users'}), 500

    # Atualizar
@usuario_bp.route("/usuario/<int:id>", methods=["PUT"])
def update_usuario(id):
    usuario_objeto = Usuario.query.filter_by(id=id).first()
    if usuario_objeto:
        body = request.get_json()
        if body:
            try:
                if 'nome' in body:
                    usuario_objeto.nome = body['nome']
                if 'email' in body:
                    usuario_objeto.email = body['email']
                if 'senha' in body:
                    usuario_objeto.senha = body['senha']
                    usuario_objeto.senha = bcrypt.hash(body['senha'])

                db.session.commit()
                return jsonify({'message': 'usuario updated successfully', 'usuario': usuario_objeto.json()}), 200
            except Exception as e:
                print('Erro', e)
                db.session.rollback()
                return jsonify({'message': 'error updating user'}), 400
        else:
            return jsonify({'message': 'request body is empty'}), 400
    return jsonify({'message': 'user not found'}), 404

    # Deletar
@usuario_bp.route("/usuario/<int:id>", methods=["DELETE"])
def deleta_usuario(id):
    usuario_objeto = Usuario.query.filter_by(id=id).first()
    if usuario_objeto:
        try:
            db.session.delete(usuario_objeto)
            db.session.commit()
            return jsonify({'message': 'usuario deleted successfully'}), 200
        except Exception as e:
            print('Erro', e)
            db.session.rollback()  # Em caso de erro, desfaz as alterações na sessão
            return jsonify({'message': 'error deleting user'}), 400
    return jsonify({'message': 'user not found'}), 404