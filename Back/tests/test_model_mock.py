# tests/test_model_mock.py
import pytest
import sys
import os
from datetime import date

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.loan_predictor import get_predictor
from tests.fixtures.test_data import MockClient, MockLoanData, get_test_cases


class TestModelWithMockData:
    """Testes do modelo usando dados mock (sem banco)"""
    
    @pytest.fixture(scope="class")
    def predictor(self):
        """Carrega o modelo real"""
        return get_predictor()
    
    @pytest.fixture
    def test_cases(self):
        """Retorna os casos de teste do arquivo fixtures"""
        return get_test_cases()
    
    # ============================================
    # TESTES BÁSICOS
    # ============================================
    
    def test_model_loads(self, predictor):
        """Testa se o modelo carrega corretamente"""
        assert predictor is not None
        assert predictor.model is not None
        assert predictor.scaler is not None
        print(f"\n✅ Modelo carregado: {predictor.model_info['algorithm']}")
        print(f"   Score CV: {predictor.model_info['score_cv']}")
    
    # ============================================
    # TESTES DA REGRA DE NEGÓCIO
    # ============================================
    
    def test_business_rule_previous_default_rejected(self, predictor):
        """
        Testa a regra de negócio: cliente com default anterior deve ser NEGADO (1)
        independentemente dos outros fatores
        """
        client = MockClient(
            cpf="66666666666", name="Cliente Com Default",
            birthdate=date(1990, 5, 15), gender="male", education="Bachelor",
            income=1000000, emp_exp=10, credit_score=800, previous_default=1,
            home_ownership="Own"
        )
        
        loan = MockLoanData(
            client_cpf="66666666666", loan_amnt=10000, loan_intent="Education",
            loan_int_rate=5.0, loan_percent_income=0.01, cb_person_cred_hist_length=10
        )
        
        prediction = predictor.predict(client, loan)
        
        # Regra de negócio: default anterior = NEGADO (1)
        assert prediction == 1, f"Esperado NEGADO (1), obtido {prediction}"
        print(f"   ✅ Cliente com default anterior: pred={prediction} (NEGADO por regra de negócio)")
    
    # ============================================
    # TESTES COM CENÁRIOS ESPECÍFICOS
    # ============================================
    
    def test_predict_with_good_client(self, predictor):
        """Testa predição com cliente bom (deve ser APROVADO = 0)"""
        client = MockClient(
            cpf="11111111111", name="Cliente Bom",
            birthdate=date(1990, 5, 15), gender="male", education="Bachelor",
            income=600000, emp_exp=12, credit_score=700, previous_default=0,
            home_ownership="Own"
        )
        
        loan = MockLoanData(
            client_cpf="11111111111", loan_amnt=20000, loan_intent="Education",
            loan_int_rate=10.5, loan_percent_income=0.033, cb_person_cred_hist_length=10
        )
        
        prediction = predictor.predict(client, loan)
        
        # Cliente bom deve ser APROVADO (0)
        assert prediction == 0, f"Esperado APROVADO (0), obtido {prediction}"
        print(f"   Predição: {prediction} (APROVADO)")
    
    def test_predict_with_risky_client(self, predictor):
        """Testa predição com cliente de risco (deve ser NEGADO = 1)"""
        client = MockClient(
            cpf="55555555555", name="Cliente Risco",
            birthdate=date(1995, 3, 10), gender="male", education="High School",
            income=30000, emp_exp=2, credit_score=450, previous_default=0,
            home_ownership="Rent"
        )
        
        loan = MockLoanData(
            client_cpf="55555555555", loan_amnt=50000, loan_intent="Medical",
            loan_int_rate=18.0, loan_percent_income=1.67, cb_person_cred_hist_length=2
        )
        
        prediction = predictor.predict(client, loan)
        
        # Cliente de risco deve ser NEGADO (1)
        assert prediction == 1, f"Esperado NEGADO (1), obtido {prediction}"
        print(f"   Predição: {prediction} (NEGADO)")
    
    def test_predict_returns_consistent_results(self, predictor):
        """Testa consistência da predição (mesmo input = mesmo output)"""
        client = MockClient(
            cpf="22222222222", name="Cliente Regular",
            birthdate=date(1985, 8, 20), gender="female", education="High School",
            income=122820, emp_exp=5, credit_score=504, previous_default=0,
            home_ownership="Rent"
        )
        
        loan = MockLoanData(
            client_cpf="22222222222", loan_amnt=25000, loan_intent="Personal",
            loan_int_rate=10.5, loan_percent_income=0.20, cb_person_cred_hist_length=5
        )
        
        pred1 = predictor.predict(client, loan)
        pred2 = predictor.predict(client, loan)
        
        assert pred1 == pred2
    
    # ============================================
    # TESTES COM MÚLTIPLOS CENÁRIOS
    # ============================================
    
    def test_predict_with_multiple_scenarios(self, predictor, test_cases):
        """Testa predições em múltiplos cenários (apenas verifica se retorna 0 ou 1)"""
        
        for case in test_cases:
            client = case['client']
            loan = case['loan']
            
            prediction = predictor.predict(client, loan)
            
            # Apenas verifica se retorna 0 ou 1
            assert prediction in [0, 1], f"Predição inválida: {prediction}"
            
            print(f"   Caso {case['id']}: pred={prediction}")
    
    def test_predict_with_excellent_client(self, predictor):
        """Testa predição com cliente excelente (deve ser APROVADO = 0)"""
        client = MockClient(
            cpf="44444444444", name="Cliente Excelente",
            birthdate=date(1980, 1, 1), gender="female", education="Master",
            income=1957180, emp_exp=15, credit_score=684, previous_default=0,
            home_ownership="Own"
        )
        
        loan = MockLoanData(
            client_cpf="44444444444", loan_amnt=100000, loan_intent="Venture",
            loan_int_rate=6.5, loan_percent_income=0.051, cb_person_cred_hist_length=15
        )
        
        prediction = predictor.predict(client, loan)
        
        # Cliente excelente deve ser APROVADO (0)
        assert prediction == 0, f"Esperado APROVADO (0), obtido {prediction}"
        print(f"   Predição: {prediction} (APROVADO)")
    
    def test_predict_with_high_debt_ratio(self, predictor):
        """Testa predição com alto percentual de renda comprometido (deve ser NEGADO = 1)"""
        client = MockClient(
            cpf="22222222222", name="Cliente Regular",
            birthdate=date(1985, 8, 20), gender="female", education="High School",
            income=122820, emp_exp=5, credit_score=504, previous_default=0,
            home_ownership="Rent"
        )
        
        loan = MockLoanData(
            client_cpf="22222222222", loan_amnt=45000, loan_intent="Personal",
            loan_int_rate=12.0, loan_percent_income=0.37, cb_person_cred_hist_length=5
        )
        
        prediction = predictor.predict(client, loan)
        
        # Alto percentual de renda comprometido deve ser NEGADO (1)
        assert prediction == 1, f"Esperado NEGADO (1), obtido {prediction}"
        print(f"   Predição: {prediction} (NEGADO - alto percentual de renda)")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])