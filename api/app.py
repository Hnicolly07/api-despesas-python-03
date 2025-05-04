from flask import Flask
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from dotenv import load_dotenv
from config import DATABASE_CONFIG
from extensions import db, jwt
from blueprints.usuario.usuario import usuario_bp
from blueprints.despesa.despesa import despesa_bp
import os  # Import os module

# Carregar o arquivo .env
load_dotenv()

# Obter string de conexão da variável de ambiente
connection_string = os.getenv('DATABASE_URL')

def create_app():
    app = Flask(__name__)

    # Configura a URI do banco de dados para o SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Para evitar avisos

    app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY', 'super-secret') # Configure a chave secreta JWT


    # Inicializa o SQLAlchemy com a aplicação Flask
    db.init_app(app)
    jwt.init_app(app)

    # Reflete as tabelas do banco de dados
    with app.app_context():
        db.reflect()
        from models import reflected_models
        reflected_models(db)

    app.register_blueprint(despesa_bp)
    app.register_blueprint(usuario_bp)
    #app.register_blueprint(categoria_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)