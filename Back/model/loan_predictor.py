# services/loan_predictor.py
import joblib
import numpy as np
from datetime import date
from typing import Dict, Tuple
import os

class LoanPredictor:
    """Handles loan prediction using the trained model"""
    
    def __init__(self, model_path: str = None):
        """
        Load the trained model and scaler
        """
        if model_path is None:
            base_dir = os.path.dirname(os.path.dirname(__file__))
            model_path = os.path.join(base_dir, 'ml_model', 'modelo_completo_cart.pkl')
        
        self.model_package = joblib.load(model_path)
        self.model = self.model_package['model']
        self.scaler = self.model_package['scaler']
        self.feature_columns = self.model_package['preprocessing']['feature_names']
        self.model_info = self.model_package['model_info']
        
        print(f"✅ Modelo carregado: {self.model_info['algorithm']}")
        print(f"   Score CV: {self.model_info['score_cv']}")
        print(f"   Features esperadas: {len(self.feature_columns)}")
    
    def calculate_age(self, birthdate: date) -> int:
        """Calculate age from birthdate"""
        today = date.today()
        age = today.year - birthdate.year
        if (today.month, today.day) < (birthdate.month, birthdate.day):
            age -= 1
        return age
    
    def encode_gender(self, gender: str) -> int:
        """Encode gender: female = 0, male = 1"""
        gender_lower = gender.lower()
        if gender_lower in ['male', 'masculino']:
            return 1
        return 0
    
    def encode_education(self, education: str) -> list:
        """One-hot encode education level"""
        mapping = {
            "Associate": [1, 0, 0, 0, 0],
            "Bachelor": [0, 1, 0, 0, 0],
            "Doctorate": [0, 0, 1, 0, 0],
            "High School": [0, 0, 0, 1, 0],
            "Master": [0, 0, 0, 0, 1]
        }
        return mapping.get(education, [0, 0, 0, 0, 0])
    
    def encode_home_ownership(self, home_ownership: str) -> list:
        """One-hot encode home ownership"""
        mapping = {
            "Mortage": [1, 0, 0, 0],
            "Other": [0, 1, 0, 0],
            "Own": [0, 0, 1, 0],
            "Rent": [0, 0, 0, 1]
        }
        return mapping.get(home_ownership, [0, 0, 0, 1])
    
    def encode_loan_intent(self, loan_intent: str) -> list:
        """One-hot encode loan intent"""
        mapping = {
            "DebtConsolidation": [1, 0, 0, 0, 0, 0],
            "Education": [0, 1, 0, 0, 0, 0],
            "HomeImprovement": [0, 0, 1, 0, 0, 0],
            "Medical": [0, 0, 0, 1, 0, 0],
            "Personal": [0, 0, 0, 0, 1, 0],
            "Venture": [0, 0, 0, 0, 0, 1]
        }
        return mapping.get(loan_intent, [0, 0, 0, 0, 0, 0])
    
    def prepare_features(self, client, loan_data) -> np.ndarray:
        """
        Prepare features for prediction (apenas para clientes sem default)
        """
        # Dados do cliente
        age = self.calculate_age(client.client_birthdate)
        gender = self.encode_gender(client.client_gender)
        education_encoded = self.encode_education(client.client_education)
        home_ownership_encoded = self.encode_home_ownership(client.client_home_ownership)
        income = client.client_income
        emp_exp = client.client_emp_exp
        credit_score = client.client_credit_score
        
        # NOTA: previous_default NÃO é usado aqui porque o modelo foi treinado
        # apenas com clientes que têm previous_default = 0 (No)
        
        # Dados do empréstimo
        loan_amount = loan_data.loan_amnt
        loan_intent_encoded = self.encode_loan_intent(loan_data.loan_intent)
        loan_int_rate = loan_data.loan_int_rate or 0
        loan_percent_income = loan_data.loan_percent_income or 0
        credit_history = loan_data.cb_person_cred_hist_length or 0
        
        # Construir vetor de features (24 features - sem previous_default)
        # O modelo foi treinado SEM a coluna previous_default
        features = [
            age, gender, income, emp_exp,
            loan_amount, loan_int_rate, loan_percent_income, credit_history,
            credit_score,
            *education_encoded,
            *home_ownership_encoded,
            *loan_intent_encoded
        ]

        print(f'features:{features}')
        
        # Converter para numpy array e escalar
        features_array = np.array(features).reshape(1, -1)
        features_scaled = self.scaler.transform(features_array)
        
        return features_scaled
    
    def predict(self, client, loan_data) -> int:
        """
        Make prediction for a loan
        
        REGRA DE NEGÓCIO:
        1. Clientes com default anterior (Yes) → NEGADO automaticamente
        2. Clientes sem default → Avaliados pelo modelo ML
        
        Returns:
            int: 0 = APPROVED, 1 = REJECTED
        """
        # ============================================
        # REGRA DE NEGÓCIO EXPLÍCITA
        # ============================================

        # Clientes com default anterior são NEGADOS automaticamente
        if client.client_previous_default == 1:
            print(f"   🚫 Cliente {client.client_cpf} com default anterior - NEGADO por regra de negócio")
            return 1  # NEGADO
        
        # ============================================
        # MODELO ML (treinado apenas com clientes sem default)
        # ============================================

        features = self.prepare_features(client, loan_data)
        prediction = self.model.predict(features)[0]
        
        return int(prediction)
    
    def predict_and_save(self, session, client, loan_data) -> Dict:
        """
        Predict loan status and update loan_data record
        
        Returns:
            dict: Prediction results
        """
        # Make prediction (já inclui a regra de negócio)
        prediction = self.predict(client, loan_data)
        
        # Update loan_data with result
        loan_data.loan_status = int(prediction)
        
        # Commit to database
        session.commit()
        
        return {
            'loan_status': int(prediction),
            'approved': int(prediction) == 0,   # 0 = APROVADO
            'rejected': int(prediction) == 1,   # 1 = NEGADO
            'message': 'Empréstimo aprovado!' if int(prediction) == 0 else 'Empréstimo negado.'
        }

# Instância global para usar na API
_predictor = None

def get_predictor() -> LoanPredictor:
    """Retorna a instância global do preditor"""
    global _predictor
    if _predictor is None:
        _predictor = LoanPredictor()
    return _predictor