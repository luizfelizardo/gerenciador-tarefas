import os
import sqlite3
from flask import Flask, redirect, request, render_template, url_for
import click

app = Flask(__name__)

# --- PARA O DEPLOY NO RENDER (PLANO GRATUITO SEM PERSISTÊNCIA) ---
# Coloca o DB na raiz do diretório de trabalho do Render.
# Os dados NÃO SERÃO persistentes entre deploys ou reinícios.
DATABASE = 'tarefas.db' 

# PARA DESENVOLVIMENTO LOCAL, VOCÊ TAMBÉM PODE USAR ESTA LINHA.
# Se você já configurou localmente para 'tarefas.db', não precisa mudar.

# Função para obter uma conexão com o banco de dados
def conectar_banco():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# NOVO: Comando CLI para inicializar o banco de dados
@app.cli.command('init-db')
def init_db_command():
    """Cria as tabelas do banco de dados."""
    
    # --- REMOVA OU COMENTE AS 3 LINHAS ABAIXO ---
    # db_dir = os.path.dirname(DATABASE)
    # if db_dir: 
    #     os.makedirs(db_dir, exist_ok=True)
    # ---------------------------------------------
    
    # Apenas conecte e crie a tabela. O sqlite3.connect() criará o arquivo tarefas.db
    # na raiz do projeto se ele não existir.
    conn = conectar_banco()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL,
            status TEXT NOT NULL,
            data_criacao TEXT NOT NULL,
            observacao TEXT
        )
    """)
    conn.commit()
    conn.close()
    click.echo('Banco de dados inicializado.')

# Função para adicionar uma nova tarefa
def adicionar_tarefa(descricao, status, data_criacao, observacao):
    conn = conectar_banco()
    conn.execute("""
        INSERT INTO tarefas (descricao, status, data_criacao, observacao)
        VALUES (?, ?, ?, ?)
    """, (descricao, status, data_criacao, observacao))
    conn.commit()
    conn.close()

# Função para listar todas as tarefas
def listar_tarefas():
    conn = conectar_banco()
    tarefas = conn.execute("SELECT * FROM tarefas ORDER BY id DESC").fetchall()
    conn.close()
    return tarefas

# Função para deletar uma tarefa por ID
def deletar_tarefa(id_tarefa):
    conn = conectar_banco()
    conn.execute("DELETE FROM tarefas WHERE id = ?", (id_tarefa,))
    conn.commit()
    conn.close()

# Função para marcar uma tarefa como concluída
def marcar_concluida(id_tarefa):
    try:
        conn = conectar_banco()
        conn.execute("UPDATE tarefas SET status = 'concluida' WHERE id = ?", (id_tarefa,))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Erro ao marcar tarefa como concluída: {e}")

# --- Rotas da Aplicação ---

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

@app.route('/deletar/<int:id_tarefa>')
def deletar(id_tarefa):
    deletar_tarefa(id_tarefa)
    return redirect(url_for('index'))

@app.route('/concluir/<int:id_tarefa>')
def concluir(id_tarefa):
    marcar_concluida(id_tarefa)
    return redirect(url_for('index'))

# --- Início da Aplicação Flask ---
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)