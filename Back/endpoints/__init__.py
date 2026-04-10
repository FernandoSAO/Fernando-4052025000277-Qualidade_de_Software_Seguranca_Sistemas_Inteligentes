"""
Exporta todos os endpoints do sistema para facilitar o import no app.py
"""

from .info_endpoints import configure_info_endpoints
from .client_endpoints import configure_client_endpoints
from .loan_endpoints import configure_loan_test_endpoints

# Lista de todos os configuradores disponíveis
__all__ = [
    'configure_info_endpoints',
    'configure_client_endpoints',
    'configure_loan_test_endpoints'
]

# Função que configura TODOS os endpoints de uma vez
def configure_all_endpoints(app):
    """
    Configura todos os endpoints na aplicação Flask
    """
    app = configure_info_endpoints(app)  
    app = configure_client_endpoints(app)
    app = configure_loan_test_endpoints(app)
    
    return app