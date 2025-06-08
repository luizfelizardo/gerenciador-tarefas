from flask import Flask, redirect, request, render_template, url_for
import sqlite3

app = Flask(__name__)

def conectar_banco():
    return sqlite3.connect("tarefas.db")

def criar_tabela():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL,
            status TEXT NOT NULL,
            data_criacao TEXT NOT NULL,
            observacao TEXT
        )
    """)
    conexao.commit()
    conexao.close()

def adicionar_tarefa(descricao, status, data_criacao, observacao):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO tarefas (descricao, status, data_criacao, observacao)
        VALUES (?, ?, ?, ?)
    """, (descricao, status, data_criacao, observacao))
    conexao.commit()
    conexao.close()

def listar_tarefas():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM tarefas")
    tarefas = cursor.fetchall()
    conexao.close()
    return tarefas

def deletar_tarefa(id):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM tarefas WHERE id = ?", (id,))
    conexao.commit()
    conexao.close()

def marcar_concluida(id):
    try:
        conexao = conectar_banco()
        cursor = conexao.cursor()
        cursor.execute("UPDATE tarefas SET status = 'concluida' WHERE id = ?", (id,))
        conexao.commit()
        conexao.close()
    except sqlite3.Error as e:
        print(f"Erro ao marcar tarefa como concluída: {e}")
        
criar_tabela()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        descricao = request.form['descricao']
        data_criacao = request.form['data_criacao']
        observacao = request.form['observacao']
        adicionar_tarefa(descricao, 'pendente', data_criacao, observacao)
        return redirect(url_for('index'))
    tarefas = listar_tarefas()
    return render_template('index.html', tarefas=tarefas)

@app.route('/deletar/<int:id>')
def deletar(id):
    deletar_tarefa(id)
    return redirect(url_for('index'))

@app.route('/concluir/<int:id>')
def concluir(id):
    marcar_concluida(id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)