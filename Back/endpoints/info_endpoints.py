from flask_openapi3 import Tag
from logger import logger
from schemas import *

# definindo tag
info_tag = Tag(name="Info", description="Busca de informações para preenchimento do frontend")


def configure_info_endpoints(app):
    """
    Configura todas as rotas relacionadas a informações de frontend
    """

    @app.get('/getInformation', tags=[info_tag],
             responses={"200": InformationResponseSchema, "500": ErrorSchema})
    def get_information():
        """
        Faz a busca das informações para preenchimento do frontend
        """
        try:
            # Tipos de educação
            person_education = ["Associate", "Bachelor", "Doctorate", "High School", "Master"]

            # Tipos de residência
            home_ownership = ["Mortage", "Other", "Own", "Rent"]

            # Objetivos do empréstimo
            loan_intent = ["Debt Consolidation", "Education", "Home Improvement", "Medical", "Personal", "Venture"]

            # Guarda os dados formatados
            resposta = InformationResponseSchema(
                person_education=person_education,
                home_ownership=home_ownership,
                loan_intent=loan_intent,
                message="Informações carregadas com sucesso"
            )

            logger.info("Informações de frontend enviadas com sucesso")
            return resposta.dict(), 200

        except Exception as e:
            logger.error(f"Erro ao buscar informações: {e}")
            return ErrorSchema(message="Erro interno ao buscar informações").dict(), 500

    return app

# Exportação padrão para o __init__.py
__all__ = ['configure_info_endpoints']