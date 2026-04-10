# tests/fixtures/test_data.py
from datetime import date


class MockClient:
    """Cliente simulado (não usa banco) - compatível com model.Client"""
    def __init__(self, cpf, name, birthdate, gender, education, 
                 income=50000, emp_exp=5, credit_score=700, 
                 previous_default=0, home_ownership="Rent", 
                 cell_phone="11999999999", profession=None):
        self.client_cpf = cpf
        self.client_full_name = name
        self.client_birthdate = birthdate
        self.client_gender = gender
        self.client_education = education
        self.client_cell_phone = cell_phone
        self.client_income = income
        self.client_profession = profession
        self.client_emp_exp = emp_exp
        self.client_credit_score = credit_score
        self.client_previous_default = previous_default
        self.client_home_ownership = home_ownership


class MockLoanData:
    """Dados de empréstimo simulados (não usa banco) - compatível com model.LoanData"""
    def __init__(self, **kwargs):
        self.loan_id = kwargs.get('loan_id', 1)
        self.client_cpf = kwargs.get('client_cpf', '12345678901')
        self.loan_amnt = kwargs.get('loan_amnt', 10000)
        self.loan_intent = kwargs.get('loan_intent', 'Personal')
        self.loan_int_rate = kwargs.get('loan_int_rate', 10.5)
        self.loan_percent_income = kwargs.get('loan_percent_income', 0.20)
        self.cb_person_cred_hist_length = kwargs.get('cb_person_cred_hist_length', 5)
        self.loan_status = None
        self.expected = kwargs.get('expected', None)


def get_training_data():
    """
    Retorna dados que simulam o dataset de treino original
    
    REGRA DE NEGÓCIO:
    - Clientes com previous_default = 1 são NEGADOS (1) independentemente de outros fatores
    - Clientes sem default são avaliados pelo modelo baseado em renda e score
    
    Baseado no modelo treinado:
    - APROVADO (0): renda > 500k E score > 650 E previous_default = 0
    - NEGADO (1): caso contrário
    """
    
    # ============================================
    # CLIENTES
    # ============================================
    
    clients = [
        # Cliente Bom - Renda alta, Score alto, SEM default → APROVADO (0)
        MockClient(
            cpf="11111111111", name="Cliente Bom", 
            birthdate=date(1990, 5, 15), gender="male", education="Bachelor",
            income=600000, emp_exp=8, credit_score=670, previous_default=0, 
            home_ownership="Own"
        ),
        # Cliente Excelente - Renda muito alta, Score alto, SEM default → APROVADO (0)
        MockClient(
            cpf="44444444444", name="Cliente Excelente", 
            birthdate=date(1980, 1, 1), gender="female", education="Master",
            income=1957180, emp_exp=15, credit_score=684, previous_default=0, 
            home_ownership="Own"
        ),
        # Cliente Regular - Renda média, Score médio, SEM default → NEGADO (1)
        MockClient(
            cpf="22222222222", name="Cliente Regular", 
            birthdate=date(1985, 8, 20), gender="female", education="High School",
            income=122820, emp_exp=5, credit_score=504, previous_default=0, 
            home_ownership="Rent"
        ),
        # Cliente Risco - Renda baixa, Score baixo, SEM default → NEGADO (1)
        MockClient(
            cpf="55555555555", name="Cliente Risco Medio", 
            birthdate=date(1990, 6, 25), gender="male", education="Associate",
            income=80000, emp_exp=3, credit_score=520, previous_default=0, 
            home_ownership="Rent"
        ),
        # Cliente COM Default - será NEGADO por regra de negócio (1)
        MockClient(
            cpf="66666666666", name="Cliente Com Default", 
            birthdate=date(1990, 5, 15), gender="male", education="Bachelor",
            income=1000000, emp_exp=10, credit_score=800, previous_default=1, 
            home_ownership="Own"
        ),
    ]
    
    # ============================================
    # EMPRÉSTIMOS
    # ============================================
    
    loans = [
        # APROVADOS (expected = 0) - apenas para clientes sem default com boas características
        MockLoanData(
            client_cpf="11111111111", loan_amnt=50000, loan_intent="Education",
            loan_int_rate=8.5, loan_percent_income=0.083, cb_person_cred_hist_length=10,
            expected=0  # APROVADO
        ),
        MockLoanData(
            client_cpf="44444444444", loan_amnt=100000, loan_intent="Venture",
            loan_int_rate=6.5, loan_percent_income=0.051, cb_person_cred_hist_length=15,
            expected=0  # APROVADO
        ),
        
        # NEGADOS (expected = 1) - para clientes sem default com características ruins
        MockLoanData(
            client_cpf="22222222222", loan_amnt=25000, loan_intent="Personal",
            loan_int_rate=10.5, loan_percent_income=0.20, cb_person_cred_hist_length=5,
            expected=1  # NEGADO
        ),
        MockLoanData(
            client_cpf="55555555555", loan_amnt=35000, loan_intent="Personal",
            loan_int_rate=12.0, loan_percent_income=0.44, cb_person_cred_hist_length=3,
            expected=1  # NEGADO
        ),
        
        # NEGADOS (expected = 1) - para clientes COM default (regra de negócio)
        MockLoanData(
            client_cpf="66666666666", loan_amnt=10000, loan_intent="Education",
            loan_int_rate=5.0, loan_percent_income=0.01, cb_person_cred_hist_length=10,
            expected=1  # NEGADO
        ),
    ]
    
    return clients, loans


def get_test_cases():
    """
    Cria casos de teste combinando clientes e empréstimos
    """
    clients, loans = get_training_data()
    
    test_cases = []
    for i, client in enumerate(clients):
        for j, loan in enumerate(loans):
            # Determinar resultado esperado baseado na regra de negócio
            if client.client_previous_default == 1:
                expected = 1  # NEGADO por regra de negócio (1 = NEGADO)
            else:
                expected = loan.expected  # Usa o expected do empréstimo
            
            test_cases.append({
                'id': f"case_{i}_{j}",
                'client': client,
                'loan': loan,
                'expected': expected
            })
    
    return test_cases