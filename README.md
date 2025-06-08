# Gerenciador de Tarefas

Um aplicativo web simples para gerenciar suas tarefas diárias, permitindo adicionar, marcar como concluídas e excluir itens. Desenvolvido com Flask (Python) e utilizando SQLite como banco de dados.

## 🚀 Funcionalidades

* **Adicionar Tarefas:** Insira uma descrição, data de criação e observações para novas tarefas.
* **Listar Tarefas:** Visualize todas as tarefas cadastradas.
* **Marcar como Concluída:** Altere o status de uma tarefa para "concluída" (ou remova-a, dependendo da implementação).
* **Excluir Tarefas:** Remova tarefas que não são mais necessárias.
* **Design Responsivo:** Interface limpa e intuitiva, com ícones para as ações.
* **Destaque de Status:** A palavra "pendente" para tarefas em aberto é destacada para fácil visualização.

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python 3, Flask
* **Banco de Dados:** SQLite3
* **Frontend:** HTML5, CSS3
* **Ícones:** Font Awesome 6

## 📂 Estrutura do Projeto

Assista ao vídeo: 
https://github.com/user-attachments/assets/d8323e6f-8daf-41c7-987d-8567f20519b6

## ⚙️ Como Executar Localmente

Para rodar este projeto em sua máquina local, siga os passos abaixo:

### Pré-requisitos

* Python 3.x
* Pip (gerenciador de pacotes do Python)

### Instalação

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/luizfelizardo/gerenciador-tarefas.git](https://github.com/luizfelizardo/gerenciador-tarefas.git)
    cd gerenciador-tarefas
    ```

2.  **Crie e ative um ambiente virtual:**
    É altamente recomendado usar um ambiente virtual para isolar as dependências do projeto.
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # No Linux/macOS
    # venv\Scripts\activate   # No Windows (PowerShell)
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Crie o banco de dados (se ainda não existir):**
    O `app.py` está configurado para criar o banco de dados `tarefas.db` e a tabela `tarefas` na primeira execução, se eles não existirem.

### Execução

1.  **Inicie a aplicação Flask:**
    Com o ambiente virtual ativado, execute:
    ```bash
    python app.py
    ```
2.  **Acesse no navegador:**
    Abra seu navegador e acesse `http://127.0.0.1:5000/` (ou a porta que o Flask indicar no terminal).

## ☁️ Deploy no Render.com

Este projeto foi configurado para deploy fácil no [Render.com](https://render.com/), que oferece um plano gratuito generoso e suporte a SQLite persistente.

### Pré-requisitos para o Deploy

* Conta no [Render.com](https://render.com/)
* Projeto no GitHub (ou GitLab/Bitbucket)

### Configuração no Render

1.  **Certifique-se de que seu código está atualizado no GitHub.**

2.  **Acesse o Render.com** e crie um novo "Web Service".

3.  **Conecte seu repositório GitHub** e selecione o `gerenciador-tarefas`.

4.  **Configure as seguintes opções:**
    * **Name:** `gerenciador-tarefas` (ou o nome que preferir)
    * **Region:** Escolha a mais próxima de você (ex: `Oregon (US West)` ou `Frankfurt (EU Central)`)
    * **Branch:** `master` (ou `main`, dependendo da sua branch principal)
    * **Root Directory:** (Deixe em branco)
    * **Runtime:** `Python 3`
    * **Build Command:** `pip install -r requirements.txt`
    * **Start Command:** `python app.py`
    * **Instance Type:** `Free`

5.  **Ajuste para persistência do SQLite (importante):**
    No seu `app.py`, o caminho do banco de dados deve ser configurado para usar o diretório persistente do Render (`/var/data`):
    ```python
    import os
    # ...
    DATABASE = os.path.join('/var/data', 'tarefas.db')
    # ...
    # No app.py, adicione isso para garantir a criação do DB na primeira execução
    @app.before_first_request
    def setup_database():
        os.makedirs('/var/data', exist_ok=True)
        if not os.path.exists(DATABASE):
            # Função para criar o banco de dados e a tabela 'tarefas'
            conn = sqlite3.connect(DATABASE)
            conn.execute('''
                CREATE TABLE IF NOT EXISTS tarefas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    descricao TEXT NOT NULL,
                    data_criacao TEXT NOT NULL,
                    observacao TEXT
                );
            ''')
            conn.commit()
            conn.close()
    ```

6.  **Crie o Web Service.** O Render fará o deploy e fornecerá uma URL pública quando estiver pronto.

## 🤝 Contribuição

Contribuições são bem-vindas! Se você tiver sugestões ou encontrar algum bug, sinta-se à vontade para abrir uma *issue* ou enviar um *pull request*.



---