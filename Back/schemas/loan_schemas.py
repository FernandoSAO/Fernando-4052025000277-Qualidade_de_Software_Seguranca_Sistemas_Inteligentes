from pydantic import BaseModel
from typing import Optional, List

# /registerLoanData

class LoanDataRequestSchema(BaseModel):
    """Schema para requisição de registro de empréstimo"""
    
    client_cpf: str # CPF para identificar o cliente
    loan_amnt: float # Valor solicitado
    loan_intent: str # Objetivo do empréstimo 
    loan_int_rate: float # Taxa de juros
    loan_percent_income: float # Percentual da renda comprometido
    cb_person_cred_hist_length: int # Histórico de crédito (anos)

class LoanDataResponseSchema(BaseModel):
    """Schema para resposta de registro de empréstimo"""
    success: bool
    loan_id: int
    client_cpf: str
    approved: Optional[bool] = None
    probability_approval: Optional[float] = None
    probability_default: Optional[float] = None
    message: str

# /getLoanHistory

class LoanHistoryItemSchema(BaseModel):
    """Schema para um item do histórico de empréstimos"""
    loan_id: int
    date: str  # Data formatada como DD/MM/AAAA
    client_cpf: str
    loan_amnt: float
    loan_status: Optional[int] = None
    loan_status_text: str  # "Aprovado", "Negado", "Pendente"

class LoanHistoryResponseSchema(BaseModel):
    """Schema para resposta do histórico de empréstimos"""
    success: bool
    loans: List[LoanHistoryItemSchema]
    message: str

# /deleteLoan

class DeleteLoanRequestSchema(BaseModel):
    """Schema para requisição de delete de empréstimo"""
    loan_id: int

class DeleteLoanResponseSchema(BaseModel):
    """Schema para resposta de delete de empréstimo"""
    success: bool
    message: str
    loan_id: int   