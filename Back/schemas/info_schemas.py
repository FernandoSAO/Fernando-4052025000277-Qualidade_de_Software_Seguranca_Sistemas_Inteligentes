from pydantic import BaseModel
from typing import Optional, List

# /getInformation

class InformationResponseSchema(BaseModel):
    """Envia informações para o frontend (dropdown options)"""
    person_education: List[str]
    home_ownership: List[str]
    loan_intent: List[str]
    message: Optional[str] = None
