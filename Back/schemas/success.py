from pydantic import BaseModel

class SuccessSchema(BaseModel):
    """ Define como uma mensagem de confirmação será representada
    """
    mesage: str
