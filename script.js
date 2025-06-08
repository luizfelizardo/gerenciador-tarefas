const button = document.querySelector('.button-add-task');
const input = document.querySelector('.input-task');
const listaCompleta = document.querySelector('.list-tasks');

let minhaListaDeItens = [];

async function adicionarNovaTarefa() {
    const tarefa = input.value.trim();
    const dataCriacao = document.getElementById('dataCriacao').value;
    const dataVencimento = document.getElementById('dataVencimento').value;

    if (!tarefa || !dataCriacao) {
        alert("Por favor, digite uma tarefa e a data de criação.");
        return;
    }

    const data = { tarefa: tarefa, data_criacao: dataCriacao, data_vencimento: dataVencimento };
    console.log("JSON enviado:", JSON.stringify(data));
    try {
        button.disabled = true;
        input.disabled = true;
        const response = await fetch('/tarefas', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            input.value = '';
            recarregarTarefas();
        } else {
            console.error("Erro ao adicionar tarefa:", response.status, response.statusText);
            alert("Ocorreu um erro ao adicionar a tarefa. Por favor, tente novamente.");
        }
    } catch (error) {
        console.error("Erro ao adicionar tarefa:", error);
        alert("Ocorreu um erro ao adicionar a tarefa. Por favor, tente novamente.");
    } finally {
        button.disabled = false;
        input.disabled = false;
    }
}

async function mostrarTarefas() {
    if (minhaListaDeItens.length === 0) {
        listaCompleta.innerHTML = '<p>Nenhuma tarefa encontrada.</p>';
        return;
    }

    let listaHTML = '';
    minhaListaDeItens.forEach(item => {
        listaHTML += `
            <li class="task ${item.concluida ? 'done' : ''}">
                <img src="./img/checked.png" alt="check-na-tarefa" onclick="concluirTarefa(${item.id})">
                <p>${item.tarefa}</p>
                <p>Criação: ${item.data_criacao}</p>
                <p>Vencimento: ${item.data_vencimento || 'N/A'}</p>
                <img src="./img/trash.png" alt="tarefa-para-o-lixo" onclick="deletarItem(${item.id})">
            </li>
        `;
    });
    listaCompleta.innerHTML = listaHTML;
}

async function concluirTarefa(id) {
    try {
        const response = await fetch(`/tarefas/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ concluida: minhaListaDeItens.find(item => item.id === id).concluida })
        });

        if (response.ok) {
            recarregarTarefas();
        } else {
            console.error("Erro ao concluir tarefa:", response.status, response.statusText);
            alert("Ocorreu um erro ao concluir a tarefa. Por favor, tente novamente.");
        }
    } catch (error) {
        console.error("Erro ao concluir tarefa:", error);
        alert("Ocorreu um erro ao concluir a tarefa. Por favor, tente novamente.");
    }
}

async function deletarItem(id) {
    if (confirm("Deseja realmente excluir esta tarefa?")) {
        try {
            const response = await fetch(`/tarefas/${id}`, {
                method: 'DELETE'
            });

            if (response.ok) {
                recarregarTarefas();
            } else {
                console.error("Erro ao deletar tarefa:", response.status, response.statusText);
                alert("Ocorreu um erro ao deletar a tarefa. Por favor, tente novamente.");
            }
        } catch (error) {
            console.error("Erro ao deletar tarefa:", error);
            alert("Ocorreu um erro ao deletar a tarefa. Por favor, tente novamente.");
        }
    }
}

async function recarregarTarefas() {
    try {
        const response = await fetch('/tarefas');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const tarefas = await response.json();
        minhaListaDeItens = tarefas.map(tarefa => ({
            id: tarefa.id,
            tarefa: tarefa.tarefa,
            concluida: tarefa.concluida,
            data_criacao: tarefa.data_criacao,
            data_vencimento: tarefa.data_vencimento
        }));
        mostrarTarefas();
    } catch (error) {
        console.error("Erro ao recarregar tarefas:", error);
        listaCompleta.innerHTML = '<p>Não foi possível carregar as tarefas. Por favor, tente novamente mais tarde.</p>';
    }
}

recarregarTarefas();
button.addEventListener('click', adicionarNovaTarefa);