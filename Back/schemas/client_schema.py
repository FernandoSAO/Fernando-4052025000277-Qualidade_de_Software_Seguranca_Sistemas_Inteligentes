from pydantic import BaseModel
from typing import Optional
from datetime import date

# /registerClient

class ClientRequestSchema(BaseModel):
    """Schema para requisição de registro de cliente"""

    # Informações Pessoais
    client_cpf: str
    client_full_name: str
    client_birthdate: str  # formato YYYY-MM-DD
    client_gender: str     # male / female
    client_cell_phone: str
    
    # Informações Financeiras e Profissionais
    client_education: str           # Associate, Bachelor, Doctorate, High School, Master, No Education
    client_income: float            # Renda anual
    client_profession: str          # Profissão (opcional)
    client_emp_exp: float           # Experiência profissional (anos)
    client_credit_score: int        # Nota de crédito (300-850)
    client_previous_default: int    # 0 = Não, 1 = Sim
    client_home_ownership: str      # OWN, RENT, OTHER, MORTGAGE

class ClientResponseSchema(BaseModel):
    """Schema para resposta de registro de cliente"""
    success: bool
    message: str
    client_cpf: str

# /checkCPF

class CheckCPFRequestSchema(BaseModel):
    """Schema para requisição de verificação de CPF"""
    client_cpf: str

class CheckCPFResponseSchema(BaseModel):
    """Schema para resposta de verificação de CPF"""
    exists: bool
    message: str
    client_cpf: str