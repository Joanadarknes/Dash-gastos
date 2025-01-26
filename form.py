from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#tabela para entradas
class Entrada(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    data = db.Column(db.Date, nullable=False)
    tipo = db.Column(db.String(50), nullable=False) #Exemplo salário, bônus

#tabela de investimentos
class Investimento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    data = db.Column(db.Date, nullable=False)
    tipo = db.Column(db.String(50), nullable=False) #poupança,ações
    rendimento = db.Column(db.Float, nullable=False) #Rendimento estimado

#Tabela de gastos
class Gasto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    data = db.Column(db.Date, nullable=False)
    Categoria = db.Column(db.String(50), nullable=False) #Alimentação, Transporte

def criar_tabelas(app):
    with app.app_context():
        db.create_all()
