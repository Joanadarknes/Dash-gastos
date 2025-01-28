from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from form import db, Entrada, Investimento, Gasto, criar_tabelas
import io
import base64
import matplotlib.pyplot as plt
import numpy as np

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

    total_entradas = sum(e.valor for e in entradas) or 0
    total_investimentos = sum(i.valor for i in investimentos) or 0
    total_gastos = sum(g.valor for g in gastos) or 0

    saldo = total_entradas - (total_gastos + total_investimentos)

    # Verificação de valores NaN
    total_entradas = total_entradas if not np.isnan(total_entradas) else 0
    total_investimentos = total_investimentos if not np.isnan(total_investimentos) else 0
    total_gastos = total_gastos if not np.isnan(total_gastos) else 0

    # Gerar gráfico
    labels = ["Entradas", "Investimentos", "Gastos"]
    values = [total_entradas, total_investimentos, total_gastos]

    # Verificação para evitar todos os valores serem zero
    if all(v == 0 for v in values):
        values = [1, 1, 1]  # Para garantir que o gráfico não falhe

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Para que o gráfico fique circular

    # Salvar o gráfico em um objeto BytesIO
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close(fig)  # Fechar a figura para liberar memória

    return render_template('dashboard.html', 
                           entradas=total_entradas, 
                           investimentos=total_investimentos, 
                           gastos=total_gastos, 
                           saldo=saldo, 
                           img_data=img_base64)



#Rota para Entradas
@app.route('/entradas', methods=['GET', 'POST'])
def entradas():
    if request.method == 'POST':
        descricao = request.form.get('descricao')
        valor = float(request.form['valor'])
        data = datetime.strptime(request.form['data'], '%Y-%m-%d')
        tipo = request.form.get['tipo']

        nova_entrada = Entrada(descricao=descricao, valor=valor, data=data, tipo=tipo)
        db.session.add(nova_entrada)
        db.session.commit()

        return redirect(url_for('entradas'))
    
    entradas = db.session.query(Entrada).all()
    return render_template('entradas.html', entradas=entradas)

@app.route('/entradas/editar/<int:id>', methods=['GET', 'POST'])
def editar_entrada(id):
    entrada = db.session.query(Entrada).get(id)
    if request.method == 'POST':
        entrada.descricao = request.form['descricao']
        entrada.valor = float(request.form['valor'])
        entrada.data = datetime.strptime(request.form['data'], '%Y-%m-%d')
        entrada.tipo = request.form['tipo']

        db.session.commit()
        return redirect(url_for('entradas'))

    return render_template('editar_entrada.html', entrada=entrada)

@app.route('/entradas/deletar/<int:id>')
def deletar_entrada(id):
    entrada = db.session.query(Entrada).get(id)
    db.session.delete(entrada)
    db.session.commit()
    return redirect(url_for('entradas'))


#Rota para investimentos
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
    return render_template('investimentos.html', investimentos=investimentos)

@app.route('/investimentos/editar/<int:id>', methods=['GET', 'POST'])
def editar_investimento(id):
    investimento = db.session.query(Investimento).get(id)
    if request.method == 'POST':
        investimento.descricao = request.form['descricao']
        investimento.valor = float(request.form['valor'])
        investimento.data = datetime.strptime(request.form['data'], '%Y-%m-%d')
        investimento.tipo = request.form['tipo']
        investimento.rendimento = float(request.form['rendimento']) if request.form['rendimento'] else None

        db.session.commit()
        return redirect(url_for('investimentos'))
    
    return render_template('editar_investimento.html', investimento=investimento)

@app.route('/investimentos/deletar/<int:id>')
def deletar_investimento(id):
    investimento = db.session.query(Investimento).get(id)
    db.session.delete(investimento)
    db.session.commit()
    return redirect(url_for('investimentos'))


#Rota para gastos
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

@app.route('/gastos/editar/<int:id>', methods=['GET', 'POST'])
def editar_gastos(id):
    gasto = db.session.query(Gasto).get(id)
    if request.method == 'POST':
        gasto.descricao = request.form['descricao']
        gasto.valor = float(request.form['valor'])
        gasto.data = datetime.strptime(request.form['data'], '%Y-%m-%d')
        gasto.categoria = request.form['categoria']

        db.session.commit()
        return redirect(url_for('gastos'))
    
    return render_template('editar_gasto.html', gasto=gasto)

@app.route('/gastos/deletar/<int:id>')
def deletar_gastos(id):
    gasto = db.session.query(Gasto).get(id)
    db.session.delete(gasto)
    db.session.commit()
    return redirect(url_for('gastos'))

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(port=5000,host='localhost',debug=True)