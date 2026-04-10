// pages/insert_client.js
import { setupPhoneMask, setupCpfMask, setupCurrencyMask, setupPercentMask } from '../common/format.js';

/*
  --------------------------------------------------------------------------------------
  Função para carregar os dropdowns do backend
  --------------------------------------------------------------------------------------
*/

async function loadDropdownOptions() {
    try {
        const response = await fetch('http://localhost:5000/getInformation');
        const data = await response.json();
        
        // Preencher dropdown de educação
        const educationSelect = document.getElementById('client-education');
        if (educationSelect && data.person_education) {
            educationSelect.innerHTML = '<option value="">Selecione...</option>';
            data.person_education.forEach(edu => {
                const option = document.createElement('option');
                option.value = edu;
                option.textContent = edu;
                educationSelect.appendChild(option);
            });
        }
        
        // Preencher dropdown de moradia
        const homeOwnershipSelect = document.getElementById('client-home-ownership');
        if (homeOwnershipSelect && data.home_ownership) {
            homeOwnershipSelect.innerHTML = '<option value="">Selecione...</option>';
            data.home_ownership.forEach(ownership => {
                const option = document.createElement('option');
                option.value = ownership;
                option.textContent = ownership;
                homeOwnershipSelect.appendChild(option);
            });
        }
        
        console.log('✅ Dropdowns carregados com sucesso');
        
    } catch (error) {
        console.error('❌ Erro ao carregar dropdowns:', error);
        
        // Fallback em caso de erro
        const educationSelect = document.getElementById('client-education');
        if (educationSelect) {
            educationSelect.innerHTML = '<option value="">Erro ao carregar</option>';
        }
        const homeOwnershipSelect = document.getElementById('client-home-ownership');
        if (homeOwnershipSelect) {
            homeOwnershipSelect.innerHTML = '<option value="">Erro ao carregar</option>';
        }
    }
}

/*
  --------------------------------------------------------------------------------------
  Formulário para inserir novo cliente
  --------------------------------------------------------------------------------------
*/

export function initializeClientForm() {
    console.log('🏢 Inicializando o formulário do cliente ...');
    
    // Carregar dropdowns
    loadDropdownOptions();
    
    // Encontra o formulário
    const form = document.getElementById('client-form');
    
    if (!form) {
        console.warn('⚠️ Formulário do cliente não encontrado na página');
        return;
    }
    
    console.log('✅ Formulário do cliente encontrado, fazendo o setup...');

    // Setup das máscaras
    setupPhoneMask('client-cell-phone');        // Máscara para telefone
    setupCpfMask('client-cpf');                 // Máscara para CPF
    setupCurrencyMask('client-income');         // Máscara para renda (R$)
    
    // Setup do botão de verificar CPF
    const checkCpfBtn = document.getElementById('check-cpf-btn');
    const cpfInput = document.getElementById('client-cpf');
    
    if (checkCpfBtn && cpfInput) {
        checkCpfBtn.addEventListener('click', async function() {
            await checkCpfExists();
        });
        
        // Verificar ao sair do campo CPF (blur)
        cpfInput.addEventListener('blur', async function() {
            await checkCpfExists();
        });
    }
    
    // Lógica do formulário
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        console.log('Formulário enviado!');
        
        await newClientItem();
    });
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
    // Remove pontos de milhar
    cleaned = cleaned.replace(/\./g, '');
    // Substitui vírgula decimal por ponto
    cleaned = cleaned.replace(',', '.');
    const num = parseFloat(cleaned);
    return isNaN(num) ? null : num;
}

/*
  --------------------------------------------------------------------------------------
  Função para verificar se CPF já existe
  --------------------------------------------------------------------------------------
*/

async function checkCpfExists() {
    const cpfInput = document.getElementById('client-cpf');
    // Remove formatação para enviar apenas números
    const cpf = cpfInput?.value.replace(/\D/g, '');
    const checkResult = document.getElementById('cpf-check-result');
    
    if (!cpf) {
        if (checkResult) {
            checkResult.innerHTML = '⚠️ Digite um CPF primeiro';
            checkResult.style.color = 'orange';
        }
        return false;
    }
    
    // Validar formato do CPF (11 dígitos)
    if (cpf.length !== 11) {
        if (checkResult) {
            checkResult.innerHTML = '❌ CPF inválido. Deve conter 11 dígitos numéricos.';
            checkResult.style.color = 'red';
        }
        return false;
    }
    
    try {
        const result = await checkCpf(cpf);
        
        if (checkResult) {
            if (result.exists) {
                checkResult.innerHTML = '⚠️ CPF já cadastrado!';
                checkResult.style.color = 'red';
                return false;
            } else {
                checkResult.innerHTML = '✅ CPF disponível para cadastro';
                checkResult.style.color = 'green';
                return true;
            }
        }
        
        return !result.exists;
        
    } catch (error) {
        console.error('Erro ao verificar CPF:', error);
        if (checkResult) {
            checkResult.innerHTML = '❌ Erro ao verificar CPF. Tente novamente.';
            checkResult.style.color = 'red';
        }
        return false;
    }
}

/*
  --------------------------------------------------------------------------------------
  Função para adicionar um novo cliente
  --------------------------------------------------------------------------------------
*/

async function newClientItem() {
    // Informações Pessoais
    const cpfInput = document.getElementById('client-cpf');
    const fullNameInput = document.getElementById('client-full-name');
    const birthdateInput = document.getElementById('client-birthdate');
    const genderSelect = document.getElementById('client-gender');
    const cellPhoneInput = document.getElementById('client-cell-phone');
    
    // Informações Financeiras e Profissionais
    const educationSelect = document.getElementById('client-education');
    const incomeInput = document.getElementById('client-income');
    const professionInput = document.getElementById('client-profession');
    const empExpInput = document.getElementById('client-emp-exp');
    const creditScoreInput = document.getElementById('client-credit-score');
    const previousDefaultSelect = document.getElementById('client-previous-default');
    const homeOwnershipSelect = document.getElementById('client-home-ownership');
    
    // Remove formatação para enviar apenas números
    const clientCpf = cpfInput?.value.replace(/\D/g, '');
    const clientFullName = fullNameInput?.value.trim();
    const clientBirthdate = birthdateInput?.value.trim();
    const clientGender = genderSelect?.value;
    const clientCellPhone = cellPhoneInput?.value.replace(/\D/g, '');
    
    // Valores financeiros
    const clientEducation = educationSelect?.value;
    const clientIncomeRaw = incomeInput?.value;
    const clientProfession = professionInput?.value.trim();
    const clientEmpExp = empExpInput?.value;
    const clientCreditScore = creditScoreInput?.value;
    const clientPreviousDefault = previousDefaultSelect?.value;
    const clientHomeOwnership = homeOwnershipSelect?.value;
    
    // Extrair valor numérico da renda
    const clientIncome = extractNumericValue(clientIncomeRaw);
    
    // ============================================
    // VALIDAÇÕES - INFORMAÇÕES PESSOAIS
    // ============================================
    
    if (!clientCpf) {
        alert("Informe o CPF do cliente!");
        cpfInput?.focus();
        return;
    }
    
    if (!clientFullName) {
        alert("Informe o nome completo do cliente!");
        fullNameInput?.focus();
        return;
    }
    
    if (!clientBirthdate) {
        alert("Informe a data de nascimento do cliente!");
        birthdateInput?.focus();
        return;
    }
    
    if (!clientGender) {
        alert("Selecione o gênero do cliente!");
        genderSelect?.focus();
        return;
    }
    
    if (!clientCellPhone) {
        alert("Informe o telefone do cliente!");
        cellPhoneInput?.focus();
        return;
    }
    
    // Validar formato do CPF (11 dígitos)
    if (clientCpf.length !== 11) {
        alert("CPF inválido. Deve conter 11 dígitos numéricos.");
        cpfInput?.focus();
        return;
    }
    
    // Validar formato do telefone (mínimo 10 dígitos)
    if (clientCellPhone.length < 10 || clientCellPhone.length > 11) {
        alert("Telefone inválido. Deve conter 10 ou 11 dígitos (DDD + número).");
        cellPhoneInput?.focus();
        return;
    }
    
    // ============================================
    // VALIDAÇÕES - INFORMAÇÕES FINANCEIRAS
    // ============================================
    
    if (!clientEducation) {
        alert("Selecione o nível de educação!");
        educationSelect?.focus();
        return;
    }
    
    if (!clientIncomeRaw) {
        alert("Informe a renda anual!");
        incomeInput?.focus();
        return;
    }
    
    if (clientIncome === null || clientIncome <= 0) {
        alert("Renda anual inválida. Deve ser maior que zero.");
        incomeInput?.focus();
        return;
    }
    
    if (!clientEmpExp && clientEmpExp !== 0) {
        alert("Informe a experiência profissional (anos)!");
        empExpInput?.focus();
        return;
    }
    
    const clientEmpExpNum = parseFloat(clientEmpExp);
    if (isNaN(clientEmpExpNum) || clientEmpExpNum < 0) {
        alert("Experiência profissional inválida.");
        empExpInput?.focus();
        return;
    }
    
    if (!clientCreditScore) {
        alert("Informe a nota de crédito (score)!");
        creditScoreInput?.focus();
        return;
    }
    
    const clientCreditScoreNum = parseInt(clientCreditScore);
    if (isNaN(clientCreditScoreNum) || clientCreditScoreNum < 300 || clientCreditScoreNum > 850) {
        alert("Nota de crédito inválida. Deve estar entre 300 e 850.");
        creditScoreInput?.focus();
        return;
    }
    
    if (!clientPreviousDefault) {
        alert("Selecione se já teve empréstimo com inadimplência!");
        previousDefaultSelect?.focus();
        return;
    }
    
    if (!clientHomeOwnership) {
        alert("Selecione a situação de moradia!");
        homeOwnershipSelect?.focus();
        return;
    }
    
    // Verificar se CPF já existe antes de enviar
    const isAvailable = await checkCpfExists();
    if (!isAvailable) {
        alert("CPF já cadastrado. Não é possível realizar o cadastro.");
        return;
    }
    
    // ============================================
    // PREPARAR DADOS PARA ENVIO
    // ============================================
    
    try {
        await postClient(
            clientCpf,
            clientFullName,
            clientBirthdate,
            clientGender,
            clientCellPhone,
            clientEducation,
            clientIncome,
            clientProfession,
            clientEmpExpNum,
            clientCreditScoreNum,
            parseInt(clientPreviousDefault),
            clientHomeOwnership
        );
        
        alert("Cliente cadastrado com sucesso!");
        
        // Limpar formulário
        if (cpfInput) cpfInput.value = '';
        if (fullNameInput) fullNameInput.value = '';
        if (birthdateInput) birthdateInput.value = '';
        if (genderSelect) genderSelect.value = '';
        if (cellPhoneInput) cellPhoneInput.value = '';
        if (educationSelect) educationSelect.value = '';
        if (incomeInput) incomeInput.value = '';
        if (professionInput) professionInput.value = '';
        if (empExpInput) empExpInput.value = '';
        if (creditScoreInput) creditScoreInput.value = '';
        if (previousDefaultSelect) previousDefaultSelect.value = '';
        if (homeOwnershipSelect) homeOwnershipSelect.value = '';
        
        const checkResult = document.getElementById('cpf-check-result');
        if (checkResult) checkResult.innerHTML = '';
        
    } catch (error) {
        alert(`Erro ao cadastrar cliente: ${error.message}`);
    }
}

/*
  --------------------------------------------------------------------------------------
  Função para verificar CPF no servidor via requisição POST
  --------------------------------------------------------------------------------------
*/

const checkCpf = async (cpf) => {
    const url = 'http://localhost:5000/checkCPF';
    
    const formData = new FormData();
    formData.append('client_cpf', cpf);
    
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

/*
  --------------------------------------------------------------------------------------
  Função para adicionar novo cliente no servidor via requisição POST
  --------------------------------------------------------------------------------------
*/

const postClient = async (cpf, full_name, birthdate, gender, cellphone, 
                         education, income, profession, emp_exp, credit_score, 
                         previous_default, home_ownership) => {
    const url = 'http://localhost:5000/registerClient';
    
    const formData = new FormData();
    formData.append('client_cpf', cpf);
    formData.append('client_full_name', full_name);
    formData.append('client_birthdate', birthdate);
    formData.append('client_gender', gender);
    formData.append('client_cell_phone', cellphone);
    formData.append('client_education', education);
    formData.append('client_income', income);
    formData.append('client_profession', profession || '');
    formData.append('client_emp_exp', emp_exp);
    formData.append('client_credit_score', credit_score);
    formData.append('client_previous_default', previous_default);
    formData.append('client_home_ownership', home_ownership);
    
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