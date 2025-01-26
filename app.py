from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from form import db, Entrada, Investimento, Gasto, criar_tabelas

app = Flask(__name__)

#configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///controle_financeiro.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
criar_tabelas(app)

#Rota principal com o dashboard
@app.route('/')
def dashboard():
    entradas = db.session.query(Entrada).all()
    investimentos = db.session.query(Investimento).all()
    gastos = db.session.query(Gasto).all()

    total_entradas = sum(e.valor for e in entradas)
    total_investimentos = sum(i.valor for i in investimentos)
    total_gastos = sum(g.valor for g in gastos)

    saldo = total_entradas - (total_gastos + total_investimentos)

    # Dados para o gráfico
    dados_grafico = {
        "labels": ["Entradas", "Investimentos", "Gastos"],
        "values": [total_entradas, total_investimentos, total_gastos]
    }

    return render_template('dashboard.html', entradas=total_entradas, investimentos=total_investimentos, gastos=total_gastos, saldo=saldo, dados_grafico=dados_grafico)

#Rota para exibir as entradas
@app.route('/entradas', methods=['GET', 'POST'])
def entradas():
    if request.method == 'POST':
        descricao = request.form('descricao')
        valor = float(request.form['valor'])
        data = datetime.strptime(request.form['data'], '%y-%m-%d')
        tipo = request.form['tipo']

        nova_entrada = Entrada(descricao=descricao, valor=valor, data=data, tipo=tipo)
        db.session.add(nova_entrada)
        db.session.commit()

        return redirect(url_for('entradas'))
    
    entradas = db.session.query(Entrada).all()
    return render_template('entrada.html', entradas=entradas)

#Rota para exibir os investimentos
@app.route('/investimentos', methods=['GET', 'POST'])
def investimentos():
    if request.method == 'POST':
        descricao = request.form['descricao']
        valor = float(request.form['valor'])
        data = datetime.strptime(request.form['data'], '%Y-%m-%d')
        tipo = request.form['tipo']
        rendimento = float(request.form['rendimento']) if request.form['rendimento'] else None

        novo_investimento = Investimento(
            descricao=descricao, valor=valor, data=data, tipo=tipo, rendimento=rendimento
        )
        db.session.add(novo_investimento)
        db.session.commit()

        return redirect(url_for('investimentos'))
    
    investimentos = db.session.query(Investimento).all()
    return render_template('investimento.html', investimentos=investimentos)

#Rota para exibir gastos
@app.route('/gastos', methods=['GET', 'POST'])
def gastos():
    if request.method == 'POST':
        descricao = request.form['descricao']
        valor = float(request.form['valor'])
        data = datetime.strptime(request.form['data'], '%Y-%m-%d')
        categoria = request.form['categoria']

        novo_gasto = Gasto(descricao=descricao, valor=valor, data=data, categoria=categoria)
        db.session.add(novo_gasto)
        db.session.commit()

        return redirect(url_for('gastos'))
    
    gastos = db.session.query(Gasto).all()
    return render_template('gastos.html', gastos=gastos)

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(port=5000,host='localhost',debug=True)