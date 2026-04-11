# Front-end de Aprovação de Empréstimo

**Dataset:** https://www.kaggle.com/datasets/taweilo/loan-approval-classification-data

---

## Sobre o Projeto

Este front-end é responsável pela interface de interação com o sistema de análise de crédito. Ele consome a API backend para permitir o cadastro de clientes, simulação de empréstimos e visualização de histórico.

A aplicação foi desenvolvida utilizando apenas tecnologias nativas da web, sem uso de bibliotecas externas.

---

## Funcionalidades

* Obter informações para preenchimento de campos dropdown

  * Endpoint: `/getInformation`
  * Método: GET

* Cadastro de clientes no banco de dados

  * Endpoint: `/registerClient`
  * Método: POST

* Verificação de CPF já cadastrado

  * Endpoint: `/checkCPF`
  * Método: POST

* Simulação e registro de empréstimos com análise do modelo de Machine Learning

  * Endpoint: `/registerLoanData`
  * Método: POST

* Consulta ao histórico de empréstimos realizados

  * Endpoint: `/getLoanHistory`
  * Método: GET

* Remoção de registros de empréstimos

  * Endpoint: `/deleteLoan`
  * Método: DELETE

---

## Tecnologias Utilizadas

* HTML5
* CSS3
* JavaScript (ES6+)
* Fetch API (comunicação com o backend)

---

## Estrutura do Projeto

```bash
Front/
├── index.html          # Página principal
├── components/         # Componentes HTML (header e sidebar)
├── css/                # Arquivos de estilo
├── js/                 # Scripts JavaScript
└── pages/              # Páginas adicionais
```

---

## Como Executar

Este projeto não utiliza servidor próprio. Para evitar problemas com CORS e requisições locais, é necessário rodar um servidor estático.

### Opção recomendada (VS Code)

Utilize a extensão **Live Server**:

1. Instale a extensão "Live Server" no VS Code
2. Clique com o botão direito no arquivo `index.html`
3. Selecione **"Open with Live Server"**

---

### Alternativa com Python

```bash
python -m http.server 5500
```

Acesse no navegador:

```
http://localhost:5500
```

---

## Observações

* O backend deve estar em execução para que o front-end funcione corretamente
* As requisições são feitas via Fetch API diretamente para a API Flask
* Não há uso de frameworks ou bibliotecas externas

---

## Autor - Fernando Oliveira

Projeto desenvolvido para fins acadêmicos (PUC-RJ)
