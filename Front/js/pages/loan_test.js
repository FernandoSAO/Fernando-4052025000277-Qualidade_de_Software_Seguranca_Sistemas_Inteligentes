// pages/loan_test.js
import { 
    setupCpfMask, 
    setupCurrencyMask, 
    setupPercentMask 
} from '../common/format.js';

/*
  --------------------------------------------------------------------------------------
  Função para carregar os dropdowns do backend
  --------------------------------------------------------------------------------------
*/

async function loadDropdownOptions() {
    try {
        const response = await fetch('http://localhost:5000/getInformation');
        const data = await response.json();
        
        // Preencher dropdown de intenção de empréstimo
        const loanIntentSelect = document.getElementById('loan_intent');
        if (loanIntentSelect && data.loan_intent) {
            loanIntentSelect.innerHTML = '<option value="">Selecione...</option>';
            data.loan_intent.forEach(intent => {
                const option = document.createElement('option');
                option.value = intent;
                option.textContent = intent;
                loanIntentSelect.appendChild(option);
            });
        }
        
        console.log('✅ Dropdowns carregados com sucesso');
        
    } catch (error) {
        console.error('❌ Erro ao carregar dropdowns:', error);
    }
}

/*
  --------------------------------------------------------------------------------------
  Função para verificar se CPF existe no banco
  --------------------------------------------------------------------------------------
*/

async function checkCpfExists(cpf) {
    const cleanCpf = cpf.replace(/\D/g, '');
    
    if (cleanCpf.length !== 11) {
        return { exists: false, valid: false, message: 'CPF inválido' };
    }
    
    try {
        const formData = new FormData();
        formData.append('client_cpf', cleanCpf);
        
        const response = await fetch('http://localhost:5000/checkCPF', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        return {
            exists: data.exists,
            valid: true,
            message: data.exists ? 'CPF já cadastrado' : 'CPF disponível'
        };
        
    } catch (error) {
        console.error('Erro ao verificar CPF:', error);
        return { exists: false, valid: false, message: 'Erro na verificação' };
    }
}

/*
  --------------------------------------------------------------------------------------
  Função para extrair valor numérico de campos formatados
  --------------------------------------------------------------------------------------
*/

function extractNumericValue(formattedValue) {
    if (!formattedValue) return null;
    // Remove o símbolo R$ e espaços
    let cleaned = formattedValue.replace('R$', '').trim();
    // Remove o símbolo % se existir
    cleaned = cleaned.replace('%', '');
    // Remove pontos de milhar
    cleaned = cleaned.replace(/\./g, '');
    // Substitui vírgula decimal por ponto
    cleaned = cleaned.replace(',', '.');
    const num = parseFloat(cleaned);
    return isNaN(num) ? null : num;
}

/*
  --------------------------------------------------------------------------------------
  Inicialização do formulário de empréstimo
  --------------------------------------------------------------------------------------
*/

export function initializeLoanForm() {
    console.log('🏢 Inicializando o formulário do empréstimo ...');
    
    // Carregar dropdowns
    loadDropdownOptions();
    
    // Encontra o formulário
    const form = document.getElementById('credit-analysis-form');
    
    if (!form) {
        console.warn('⚠️ Formulário do empréstimo não encontrado na página');
        return;
    }
    
    console.log('✅ Formulário do empréstimo encontrado, fazendo o setup...');
    
    // Aplicar máscaras
    setupCpfMask('client_cpf');                    // CPF
    setupCurrencyMask('loan_amnt');                // Valor do Empréstimo
    setupPercentMask('loan_int_rate');             // Taxa de Juros (%)
    setupPercentMask('loan_percent_income');       // Percentual da Renda
    
    // Setup do CPF check
    const cpfInput = document.getElementById('client_cpf');
    const checkCpfBtn = document.getElementById('check-cpf-btn');
    const cpfResult = document.getElementById('cpf-check-result');
    
    if (checkCpfBtn && cpfInput) {
        checkCpfBtn.addEventListener('click', async () => {
            const cpf = cpfInput.value.trim();
            if (!cpf) {
                if (cpfResult) {
                    cpfResult.innerHTML = '⚠️ Digite um CPF';
                    cpfResult.style.color = 'orange';
                }
                return;
            }
            
            const result = await checkCpfExists(cpf);
            
            if (cpfResult) {
                if (result.valid) {
                    if (result.exists) {
                        cpfResult.innerHTML = '✅ CPF encontrado! Você pode prosseguir.';
                        cpfResult.style.color = 'green';
                    } else {
                        cpfResult.innerHTML = '❌ CPF não cadastrado. Cadastre-se primeiro.';
                        cpfResult.style.color = 'red';
                    }
                } else {
                    cpfResult.innerHTML = `❌ ${result.message}`;
                    cpfResult.style.color = 'red';
                }
            }
        });
        
        // Verificar ao sair do campo
        cpfInput.addEventListener('blur', async () => {
            const cpf = cpfInput.value.trim();
            if (cpf && cpf.replace(/\D/g, '').length === 11) {
                const result = await checkCpfExists(cpf);
                if (cpfResult && !result.exists) {
                    cpfResult.innerHTML = '❌ CPF não cadastrado. Cadastre-se primeiro.';
                    cpfResult.style.color = 'red';
                }
            }
        });
    }
    
    // Lógica do formulário
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        console.log('Formulário enviado!');
        
        await newLoanItem();
    });
}

/*
  --------------------------------------------------------------------------------------
  Função para adicionar um novo empréstimo
  --------------------------------------------------------------------------------------
*/

async function newLoanItem() {
    // Obter valores do formulário
    const clientCpfRaw = document.getElementById("client_cpf")?.value;
    const loanAmntRaw = document.getElementById("loan_amnt")?.value;
    const loanIntRateRaw = document.getElementById("loan_int_rate")?.value;
    const loanPercentIncomeRaw = document.getElementById("loan_percent_income")?.value;
    const cbPersonCredHistLength = document.getElementById("cb_person_cred_hist_length")?.value;
    const loanIntent = document.getElementById("loan_intent")?.value;

    // ============================================
    // VALIDAÇÕES
    // ============================================
    
    // CPF
    if (!clientCpfRaw) {
        alert("Informe o CPF do cliente!");
        document.getElementById("client_cpf")?.focus();
        return;
    }
    const cleanCpf = clientCpfRaw.replace(/\D/g, '');
    if (cleanCpf.length !== 11) {
        alert("CPF inválido. Deve conter 11 dígitos numéricos.");
        document.getElementById("client_cpf")?.focus();
        return;
    }
    
    // Verificar se CPF existe antes de enviar
    const cpfCheck = await checkCpfExists(clientCpfRaw);
    if (!cpfCheck.exists) {
        alert("CPF não cadastrado. Por favor, cadastre-se primeiro na página de Cadastro de Cliente.");
        document.getElementById("client_cpf")?.focus();
        return;
    }
    
    // Valor do Empréstimo
    if (!loanAmntRaw) {
        alert("Informe o valor solicitado do empréstimo!");
        document.getElementById("loan_amnt")?.focus();
        return;
    }
    const loanAmnt = extractNumericValue(loanAmntRaw);
    if (isNaN(loanAmnt) || loanAmnt <= 0) {
        alert("Valor do empréstimo inválido. Deve ser maior que zero.");
        document.getElementById("loan_amnt")?.focus();
        return;
    }
    
    // Taxa de Juros
    if (!loanIntRateRaw) {
        alert("Informe a taxa de juros do empréstimo!");
        document.getElementById("loan_int_rate")?.focus();
        return;
    }
    const loanIntRate = extractNumericValue(loanIntRateRaw);
    if (isNaN(loanIntRate) || loanIntRate < 0) {
        alert("Taxa de juros inválida.");
        document.getElementById("loan_int_rate")?.focus();
        return;
    }
    
    // Percentual da Renda
    if (!loanPercentIncomeRaw) {
        alert("Informe o percentual da renda comprometido!");
        document.getElementById("loan_percent_income")?.focus();
        return;
    }
    const loanPercentIncome = extractNumericValue(loanPercentIncomeRaw);
    if (isNaN(loanPercentIncome) || loanPercentIncome < 0 || loanPercentIncome > 100) {
        alert("Percentual da renda inválido. Deve estar entre 0 e 100.");
        document.getElementById("loan_percent_income")?.focus();
        return;
    }
    
    // Histórico de Crédito
    if (!cbPersonCredHistLength) {
        alert("Informe o tempo de histórico de crédito (anos)!");
        document.getElementById("cb_person_cred_hist_length")?.focus();
        return;
    }
    const cbPersonCredHistLengthNum = parseInt(cbPersonCredHistLength);
    if (isNaN(cbPersonCredHistLengthNum) || cbPersonCredHistLengthNum < 0) {
        alert("Histórico de crédito inválido.");
        document.getElementById("cb_person_cred_hist_length")?.focus();
        return;
    }
    
    // Objetivo do Empréstimo
    if (!loanIntent) {
        alert("Selecione o objetivo do empréstimo!");
        document.getElementById("loan_intent")?.focus();
        return;
    }

    // ============================================
    // PREPARAR FORM DATA PARA ENVIO
    // ============================================
    
    const formData = new FormData();
    formData.append('client_cpf', cleanCpf);
    formData.append('loan_amnt', loanAmnt);
    formData.append('loan_int_rate', loanIntRate);
    formData.append('loan_percent_income', loanPercentIncome / 100);  // Converter para decimal (0-1)
    formData.append('cb_person_cred_hist_length', cbPersonCredHistLengthNum);
    formData.append('loan_intent', loanIntent);

    console.log('📤 Enviando FormData:');
    for (let [key, value] of formData.entries()) {
        console.log(`   ${key}: ${value}`);
    }

    try {
        const result = await postLoan(formData);
        
        // Mostrar resultado da análise
        const status = result.approved ? "APROVADO ✅" : "NEGADO ❌";
        const message = `
            ========================================
            RESULTADO DA ANÁLISE DE CRÉDITO
            ========================================
            
            Resultado: ${status}
            
            ${result.message}
            ========================================
        `;
        alert(message);
        
        // Limpar formulário após sucesso
        document.getElementById("credit-analysis-form")?.reset();
        const cpfResult = document.getElementById('cpf-check-result');
        if (cpfResult) cpfResult.innerHTML = '';
        
    } catch (error) {
        console.error('❌ Erro ao registrar empréstimo:', error);
        alert(`Erro ao registrar empréstimo: ${error.message}`);
    }
}

/*
  --------------------------------------------------------------------------------------
  Função para adicionar novo empréstimo no servidor via requisição POST
  --------------------------------------------------------------------------------------
*/

const postLoan = async (formData) => {
    const url = 'http://localhost:5000/registerLoanData';

    const response = await fetch(url, {
        method: 'POST',
        body: formData
    });

    let data = null;

    try {
        data = await response.json();
    } catch {
        data = null;
    }

    if (!response.ok) {
        const backendMessage = data?.message || `${response.status} ${response.statusText}`;
        throw new Error(backendMessage);
    }

    return data;
}