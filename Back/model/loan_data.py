# model/loan_data.py
from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from model.base import Base
from model.loan_predictor import get_predictor

class LoanData(Base):
    
    __tablename__ = 'loan_data'
    
    loan_id = Column(Integer, primary_key=True, autoincrement=True)
    client_cpf = Column(String(11), ForeignKey('client.client_cpf'), nullable=False)
    loan_amnt = Column(Float, nullable=False)
    loan_intent = Column(String(30), nullable=False)
    loan_int_rate = Column(Float)
    loan_percent_income = Column(Float)
    cb_person_cred_hist_length = Column(Integer)
       
    # RESULTADO DA PREDIÇÃO
    loan_status = Column(Integer)  # 0 = Aprovado, 1 = Negado
    
    # METADADOS
    insertion_date = Column(DateTime, default=datetime.now)

    # RELACIONAMENTOS
    client = relationship("Client", backref="loan_data")
    
    def __init__(self, client_cpf: str, loan_amnt: float,
                 loan_intent: str, loan_int_rate: float = None,
                 loan_percent_income: float = None,
                 cb_person_cred_hist_length: int = None):
        """
        Registra um novo pedido de empréstimo
        """
        self.client_cpf = client_cpf
        self.loan_amnt = loan_amnt
        self.loan_intent = loan_intent
        self.loan_int_rate = loan_int_rate
        self.loan_percent_income = loan_percent_income
        self.cb_person_cred_hist_length = cb_person_cred_hist_length
        
        self.loan_status = None
    
    def predict_and_save(self, session, client):
        """
        Faz a predição usando o modelo e atualiza os campos de resultado
        
        O modelo retorna:
        0 = APROVADO
        1 = NEGADO
        """
        predictor = get_predictor()
        
        # Fazer predição (0 = APROVADO, 1 = NEGADO)
        prediction = predictor.predict(client, self)
        
        # Atualizar campos
        self.loan_status = prediction
        
        # Salvar no banco
        session.commit()
        
        # Retornar com a lógica do modelo (0 = APROVADO)
        return {
            'loan_status': prediction,
            'approved': prediction == 0,   # 0 = aprovado
            'message': 'Empréstimo aprovado!' if prediction == 0 else 'Empréstimo negado devido ao risco de default.'
        }