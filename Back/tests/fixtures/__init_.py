# tests/fixtures/__init__.py
"""
Fixtures e dados de teste para os testes

Este módulo fornece dados de exemplo para os testes unitários.
"""

from tests.fixtures.test_data import (
    MockClient,
    MockLoanData,
    get_training_data,
    get_test_cases
)

# Define o que será exportado quando alguém fizer:
# from tests.fixtures import *
__all__ = [
    'MockClient',
    'MockLoanData',
    'get_training_data',
    'get_test_cases'
]