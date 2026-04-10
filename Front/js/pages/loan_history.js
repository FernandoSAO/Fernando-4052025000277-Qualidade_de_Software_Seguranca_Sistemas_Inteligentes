// pages/loan_history.js

/*
  --------------------------------------------------------------------------------------
  Página de Histórico de Empréstimos
  --------------------------------------------------------------------------------------
*/

export function initializeLoanHistory() {
    console.log('📋 Inicializando página de histórico de empréstimos...');
    
    // Carregar os dados da tabela
    loadLoanHistory();
}

/*
  --------------------------------------------------------------------------------------
  Função para carregar o histórico de empréstimos do backend
  --------------------------------------------------------------------------------------
*/

async function loadLoanHistory() {
    const tbody = document.getElementById('loan-history-body');
    const messageDiv = document.getElementById('loan-history-message');
    
    if (!tbody) return;
    
    // Mostrar loading
    tbody.innerHTML = '<tr><td colspan="6" style="text-align: center;">⌛ Carregando dados...</td></tr>';
    
    try {
        const response = await fetch('http://localhost:5000/getLoanHistory', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        
        if (!data.loans || data.loans.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" style="text-align: center;">📭 Nenhum empréstimo encontrado.</td></tr>';
            return;
        }
        
        // Preencher a tabela
        renderLoanTable(data.loans);
        
    } catch (error) {
        console.error('❌ Erro ao carregar histórico:', error);
        tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; color: #e74c3c;">❌ Erro ao carregar dados. Tente novamente.</td></tr>';
        
        if (messageDiv) {
            messageDiv.textContent = 'Erro ao carregar histórico de empréstimos.';
            messageDiv.className = 'message error';
            messageDiv.style.display = 'block';
            setTimeout(() => {
                messageDiv.style.display = 'none';
            }, 5000);
        }
    }
}

/*
  --------------------------------------------------------------------------------------
  Função para renderizar a tabela de empréstimos
  --------------------------------------------------------------------------------------
*/

function renderLoanTable(loans) {
    const tbody = document.getElementById('loan-history-body');
    if (!tbody) return;
    
    tbody.innerHTML = '';
    
    loans.forEach(loan => {
        const row = document.createElement('tr');
        
        // ID do Empréstimo
        const idCell = document.createElement('td');
        idCell.textContent = loan.loan_id || '-';
        row.appendChild(idCell);
        
        // Data
        const dateCell = document.createElement('td');
        const date = loan.insertion_date || loan.date || loan.created_at;
        if (date) {
            const formattedDate = new Date(date).toLocaleDateString('pt-BR');
            dateCell.textContent = formattedDate;
        } else {
            dateCell.textContent = '-';
        }
        row.appendChild(dateCell);
        
        // CPF do Cliente
        const cpfCell = document.createElement('td');
        const cpf = loan.client_cpf || loan.cpf;
        if (cpf) {
            // Formata CPF: XXX.XXX.XXX-XX
            cpfCell.textContent = formatCpf(cpf);
        } else {
            cpfCell.textContent = '-';
        }
        row.appendChild(cpfCell);
        
        // Valor do Empréstimo
        const amountCell = document.createElement('td');
        const amount = loan.loan_amnt || loan.amount;
        if (amount) {
            amountCell.textContent = formatCurrency(amount);
        } else {
            amountCell.textContent = '-';
        }
        row.appendChild(amountCell);
        
        // Status
        const statusCell = document.createElement('td');
        const status = loan.loan_status;
        if (status === 0 || status === '0') {
            statusCell.innerHTML = '<span class="status-approved">✅ Aprovado</span>';
        } else if (status === 1 || status === '1') {
            statusCell.innerHTML = '<span class="status-rejected">❌ Negado</span>';
        } else {
            statusCell.innerHTML = '<span class="status-pending">⏳ Pendente</span>';
        }
        row.appendChild(statusCell);
        
        // Ações (botão remover)
        const actionsCell = document.createElement('td');
        const deleteBtn = document.createElement('button');
        deleteBtn.textContent = '🗑️ Remover';
        deleteBtn.className = 'delete-btn';
        deleteBtn.title = 'Remover este empréstimo';
        deleteBtn.onclick = async () => {
            if (confirm(`Tem certeza que deseja remover o empréstimo ID ${loan.loan_id}?`)) {
                await deleteLoan(loan.loan_id);
            }
        };
        actionsCell.appendChild(deleteBtn);
        row.appendChild(actionsCell);
        
        tbody.appendChild(row);
    });
}

/*
  --------------------------------------------------------------------------------------
  Função para formatar CPF
  --------------------------------------------------------------------------------------
*/

function formatCpf(cpf) {
    const cleanCpf = cpf.replace(/\D/g, '');
    if (cleanCpf.length !== 11) return cpf;
    return cleanCpf.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
}

/*
  --------------------------------------------------------------------------------------
  Função para formatar valor monetário
  --------------------------------------------------------------------------------------
*/

function formatCurrency(value) {
    const num = parseFloat(value);
    if (isNaN(num)) return 'R$ 0,00';
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(num);
}

/*
  --------------------------------------------------------------------------------------
  Função para remover um empréstimo
  --------------------------------------------------------------------------------------
*/

async function deleteLoan(loanId) {
    if (!loanId) {
        alert('ID do empréstimo não informado.');
        return;
    }
    
    try {
        const formData = new FormData();
        formData.append('loan_id', loanId);
        
        const response = await fetch('http://localhost:5000/deleteLoan', {
            method: 'DELETE',
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.message || `${response.status} ${response.statusText}`);
        }
        
        alert('✅ Empréstimo removido com sucesso!');
        
        // Recarregar a tabela
        loadLoanHistory();
        
    } catch (error) {
        console.error('❌ Erro ao remover empréstimo:', error);
        alert(`Erro ao remover empréstimo: ${error.message}`);
    }
}