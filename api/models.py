from extensions import db 

# Modelo Usuario
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<Usuario {self.nome}>'

    def json(self):
        return {'id': self.id, 'nome': self.nome, 'email': self.email, 'senha': self.senha}
    
# Tabelas refletidas com db.reflect()
def reflected_models(db):
    global Despesa, Categoria
    class Despesa(db.Model):
        __table__ = db.metadata.tables['despesa']
    class Categoria(db.Model):
        __table__ = db.metadata.tables['categoria']