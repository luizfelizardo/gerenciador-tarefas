import sqlite3

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

def adicionar_tarefa(descricao, status, data_criacao, data_vencimento):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO tarefas (descricao, status, data_criacao, data_vencimento)
        VALUES (?, ?, ?, ?)
    """, (descricao, status, data_criacao, data_vencimento))
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

def exibir_menu():
    print("Gerenciador de Tarefas")
    print("1. Adicionar tarefa")
    print("2. Listar tarefas")
    print("3. Deletar tarefa")
    print("4. Sair")

def main():
    criar_tabela()
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            descricao = input("Descrição da tarefa: ")
            status = "pendente"
            data_criacao = input("Data de criação (AAAA-MM-DD): ")
            data_vencimento = input("Data de vencimento (AAAA-MM-DD): ")
            adicionar_tarefa(descricao, status, data_criacao, data_vencimento)
            print("Tarefa adicionada!")
        elif opcao == "2":
            tarefas = listar_tarefas()
            if tarefas:
                for tarefa in tarefas:
                    print(tarefa)
            else:
                print("Nenhuma tarefa encontrada.")
        elif opcao == "3":
            tarefas = listar_tarefas()
            if tarefas:
                print("Tarefas:")
                for tarefa in tarefas:
                    print(f"{tarefa[0]}. {tarefa[1]}")
                id_tarefa = int(input("Digite o ID da tarefa a ser deletada: "))
                deletar_tarefa(id_tarefa)
                print("Tarefa deletada!")
            else:
                print("Nenhuma tarefa encontrada.")
        elif opcao == "4":
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()