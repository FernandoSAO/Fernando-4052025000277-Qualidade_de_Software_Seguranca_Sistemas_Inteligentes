# model/client.py
from sqlalchemy import Column, String, Integer, DateTime, Date, Float
from datetime import datetime
from model.base import Base

class Client(Base):
    __tablename__ = 'client'
      
    # CPF as primary key
    client_cpf = Column(String(11), primary_key=True) # chave primária
    client_full_name = Column(String(100), nullable=False)
    client_birthdate = Column(Date, nullable=False) # data de nascimento em YYYY-MM-DD
    client_gender = Column(String(20), nullable=False)  # "male" ou "female"
    client_cell_phone = Column(String(20)) # telefone
    client_education = Column(String(50), nullable=False)  # Educação: Bachelor, Doctorate, High School, Master, etc.
    client_income = Column(Float, nullable=False)  # Renda anual
    client_profession = Column(String(100)) # profissão
    client_emp_exp = Column(Float, nullable=False)  # Anos de experiência
    client_credit_score = Column(Integer, nullable=False)  # Score de crédito entre 300 e 850
    client_previous_default = Column(Integer, nullable=False)  # Histórico de Inadimplência: 0 = Não, 1 = Sim
    client_home_ownership = Column(String(20), nullable=False)  # Situação de Moradia: OWN, RENT, OTHER, MORTGAGE

    # METADADOS
    insertion_date = Column(DateTime, default=datetime.now) # data automática
    
    def __init__(self, client_cpf: str, client_full_name: str, client_birthdate: Date,
                 client_gender: str, client_cell_phone: str,
                 client_education: str, client_income: float,
                 client_emp_exp: float, client_credit_score: int,
                 client_previous_default: int, client_home_ownership: str,
                 client_profession: str = None):
        """
        Registra um novo cliente
        
        Args:
            client_cpf: CPF do cliente (chave primária)
            client_full_name: Nome completo do cliente
            client_birthdate: Data de nascimento
            client_gender: Gênero (male/female)
            client_cell_phone: Telefone celular
            client_education: Nível de educação (Bachelor, Doctorate, etc.)
            client_income: Renda anual (R$)
            client_emp_exp: Experiência profissional (anos)
            client_credit_score: Nota de crédito (300-850)
            client_previous_default: Histórico de inadimplência (0=Não, 1=Sim)
            client_home_ownership: Situação de moradia (OWN, RENT, OTHER, MORTGAGE)
            client_profession: Profissão
        """
        self.client_cpf = client_cpf
        self.client_full_name = client_full_name
        self.client_birthdate = client_birthdate
        self.client_gender = client_gender
        self.client_cell_phone = client_cell_phone
        self.client_education = client_education
        self.client_income = client_income
        self.client_emp_exp = client_emp_exp
        self.client_credit_score = client_credit_score
        self.client_previous_default = client_previous_default
        self.client_home_ownership = client_home_ownership
        self.client_profession = client_profession