# Back-end de Análise de Crédito para Empréstimos com Machine Learning

**Dataset:** [Loan Approval Classification Dataset](https://www.kaggle.com/datasets/taweilo/loan-approval-classification-data)

---

## 📋 Funcionalidades da API

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| **GET** | `/getInformation` | Obtém informações para preenchimento de campos dropdown (educação, moradia, objetivo do empréstimo) |
| **POST** | `/registerClient` | Inclui um novo cliente no banco de dados |
| **POST** | `/checkCPF` | Verifica se um CPF já está cadastrado na tabela de clientes |
| **POST** | `/registerLoanData` | Registra um pedido de empréstimo e retorna a análise de aprovação usando o modelo de ML treinado |
| **GET** | `/getLoanHistory` | Retorna o histórico de todos os testes de empréstimo realizados |
| **DELETE** | `/deleteLoan` | Remove um teste de empréstimo a partir do seu ID |

---

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.10** (versão específica necessária para compatibilidade)
- **Flask** - Microframework web para a API
- **SQLite** - Banco de dados relacional
- **SQLAlchemy** - ORM para interação com o banco
- **Pydantic** - Validação de dados
- **Joblib** - Carregamento do modelo de ML treinado

### Machine Learning (Modelo Exportado)
- **Scikit-learn** - Modelo CART (Decision Tree)
- **Pandas / NumPy** - Manipulação de dados
- **MinMaxScaler** - Normalização dos dados

### Testes
- **Pytest** - Framework para testes unitários e de integração
- **Pytest-cov** - Relatório de cobertura de testes

---

## 🚀 Como Executar o Projeto

### Pré-requisitos

- **Python 3.10** (versão obrigatória - o projeto pode não funcionar com outras versões do Python)
- `pip` (gerenciador de pacotes do Python)

### Verificando a versão do Python

```bash
python --version
# Deve mostrar: Python 3.10.x
Se você não tiver o Python 3.10 instalado:

Windows: Baixe em python.org/downloads/release/python-31011/

Linux: sudo apt install python3.10

macOS: brew install python@3.10

Passo a passo para execução
1. Acessar o diretório do backend

bash
cd Sprint\ 4/MVP/Back
2. Criar o ambiente virtual

bash
# Windows
py -3.10 -m venv venv

# Linux/macOS
python3.10 -m venv venv

# Ou se o Python 3.10 for o padrão
python -m venv venv
3. Ativar o ambiente virtual

Sistema	Comando
Windows (PowerShell)	.\venv\Scripts\activate
Windows (CMD)	venv\Scripts\activate.bat
Linux/macOS	source venv/bin/activate
Após ativação, você verá (venv) no início da linha do terminal.

4. Verificar se o ambiente está ativo

bash
python --version
# Deve mostrar: Python 3.10.x
5. Instalar as dependências

bash
pip install -r requirements.txt
6. Executar a API

bash
# Modo normal (sem reload)
flask run --host 0.0.0.0 --port 5000

# Modo desenvolvimento (com reload automático - recomendado)
flask run --host 0.0.0.0 --port 5000 --reload
O parâmetro --reload faz o servidor reiniciar automaticamente sempre que você modificar algum arquivo do código fonte.

7. Verificar se a API está funcionando

Abra o navegador e acesse: http://localhost:5000/openapi/swagger

🧪 Executando os Testes
bash
# Executar todos os testes
pytest tests/ -v

# Executar testes específicos
pytest tests/test_model_accuracy.py -v
pytest tests/test_model_mock.py -v

# Executar com relatório de cobertura
pytest tests/ -v --cov=services --cov-report=term

# Executar com relatório HTML de cobertura
pytest tests/ -v --cov=services --cov-report=html
📁 Estrutura do Backend
bash
Back/
├── app.py                  # Arquivo principal da aplicação Flask
├── model/                  # Modelos SQLAlchemy (Client, LoanData)
│   ├── base.py             # Base declarativa do SQLAlchemy
│   ├── client.py           # Modelo Client
│   └── loan_data.py        # Modelo LoanData
├── schemas.py              # Schemas Pydantic para validação
├── services/               # Lógica de negócio
│   └── loan_predictor.py   # Predictor do modelo de ML
├── ml_model/               # Modelo de ML treinado
│   ├── modelo_completo_cart.pkl   # Modelo serializado
│   └── modelo_metadata.json       # Metadados do modelo
├── database/               # Banco de dados SQLite (criado automaticamente)
│   └── db.sqlite3
├── tests/                  # Testes unitários e de integração
│   ├── fixtures/           # Dados de teste
│   ├── test_conversions.py # Testes de conversão
│   ├── test_model_accuracy.py # Testes de acurácia
│   ├── test_model_import.py    # Testes de importação
│   └── test_model_mock.py      # Testes com dados mock
├── requirements.txt        # Dependências do projeto
└── .gitignore              # Arquivos ignorados pelo Git