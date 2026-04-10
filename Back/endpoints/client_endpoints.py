from flask_openapi3 import Tag
from logger import logger
from schemas import *
from model import Client
from sqlalchemy.exc import IntegrityError
from model import Session
from datetime import datetime

# definindo tag
client_tag = Tag(name="Client", description="Inserção de clientes na base de dados")

def configure_client_endpoints(app):
    """
    Configura todas as rotas relacionadas a clientes
    """

    @app.post('/registerClient', tags=[client_tag],
            responses={"200": ClientResponseSchema, "400": ErrorSchema, "409": ErrorSchema, "500": ErrorSchema})
    def register_client(form: ClientRequestSchema):
        """
        Registra um novo cliente na base de dados
        """
        try:

            # EXTRAIR DADOS DO FORMULÁRIO
            
            # Informações Pessoais
            client_cpf = form.client_cpf
            client_full_name = form.client_full_name
            client_birthdate_str = form.client_birthdate
            client_gender = form.client_gender
            client_cell_phone = form.client_cell_phone
            
            # Informações Financeiras e Profissionais
            client_education = form.client_education
            client_income = form.client_income
            client_profession = form.client_profession
            client_emp_exp = form.client_emp_exp
            client_credit_score = form.client_credit_score
            client_previous_default = form.client_previous_default
            client_home_ownership = form.client_home_ownership

            # VALIDAÇÕES

            # Informações Pessoais
            if not client_cpf:
                return ErrorSchema(message="CPF é obrigatório").dict(), 400
            if not client_full_name:
                return ErrorSchema(message="Nome completo é obrigatório").dict(), 400
            if not client_birthdate_str:
                return ErrorSchema(message="Data de nascimento é obrigatória").dict(), 400
            if not client_gender:
                return ErrorSchema(message="Gênero é obrigatório").dict(), 400
            if not client_cell_phone:
                return ErrorSchema(message="Telefone celular é obrigatório").dict(), 400
            
            # Informações Financeiras e Profissionais
            if not client_education:
                return ErrorSchema(message="Nível de educação é obrigatório").dict(), 400
            if client_income is None:
                return ErrorSchema(message="Renda anual é obrigatória").dict(), 400
            if client_profession is None:
                return ErrorSchema(message="Profissão é obrigatória").dict(), 400
            if client_emp_exp is None:
                return ErrorSchema(message="Experiência profissional é obrigatória").dict(), 400
            if client_credit_score is None:
                return ErrorSchema(message="Nota de crédito é obrigatória").dict(), 400
            if client_previous_default is None:
                return ErrorSchema(message="Histórico de inadimplência é obrigatório").dict(), 400
            if not client_home_ownership:
                return ErrorSchema(message="Situação de moradia é obrigatória").dict(), 400

            # VALIDAÇÕES - FORMATOS E VALORES

            # CPF (11 dígitos)
            if len(client_cpf) != 11 or not client_cpf.isdigit():
                return ErrorSchema(message="CPF inválido. Deve conter 11 dígitos numéricos.").dict(), 400

            # Gênero
            valid_genders = ["masculino", "feminino", "male", "female"]
            if client_gender.lower() not in [g.lower() for g in valid_genders]:
                return ErrorSchema(message="Gênero inválido. Opções: masculino ou feminino.").dict(), 400
            gender_standard = "male" if client_gender.lower() in ["masculino", "male"] else "female"

            # Data de Nascimento
            try:
                birth_date = datetime.strptime(client_birthdate_str, "%Y-%m-%d").date()
            except ValueError:
                return ErrorSchema(
                    message=f"Data inválida: '{client_birthdate_str}'."
                ).dict(), 400
            
            if birth_date > datetime.now().date():
                return ErrorSchema(
                    message=f"Data de nascimento não pode ser no futuro. Data fornecida: {client_birthdate_str}"
                ).dict(), 400

            # Renda Anual
            if client_income <= 0:
                return ErrorSchema(message="Renda anual deve ser maior ou igual a zero.").dict(), 400

            # Experiência Profissional
            if client_emp_exp < 0:
                return ErrorSchema(message="Experiência profissional não pode ser negativa.").dict(), 400

            # Nota de Crédito
            if client_credit_score < 300 or client_credit_score > 850:
                return ErrorSchema(message="Nota de crédito deve estar entre 300 e 850.").dict(), 400

            # Histórico de Inadimplência
            if client_previous_default not in [0, 1]:
                return ErrorSchema(message="Valor de inadimplência inválido. Use 0 (Não) ou 1 (Sim).").dict(), 400

            # Nível de Educação
            valid_education = ["Associate", "Bachelor", "Doctorate", "High School", "Master", "No Education"]
            if client_education not in valid_education:
                return ErrorSchema(message=f"Educação inválida. Opções: {', '.join(valid_education)}").dict(), 400

            # Situação de Moradia
            valid_home_ownership = ["Own", "Rent", "Other", "Mortage"]
            if client_home_ownership not in valid_home_ownership:
                return ErrorSchema(message=f"Situação de moradia inválida. Opções: {', '.join(valid_home_ownership)}").dict(), 400

            # VERIFICAR SE CPF JÁ EXISTE
            
            session = Session()
            existing_client = session.query(Client).filter_by(client_cpf=client_cpf).first()
            
            if existing_client:
                session.close()
                logger.warning(f"Tentativa de cadastro com CPF já existente: {client_cpf}")
                return ErrorSchema(message=f"Cliente com CPF {client_cpf} já está cadastrado.").dict(), 409

            # INSERIR NOVO CLIENTE

            new_client = Client(
                client_cpf=client_cpf,
                client_full_name=client_full_name,
                client_birthdate=birth_date,
                client_gender=gender_standard,
                client_cell_phone=client_cell_phone,
                client_education=client_education,
                client_income=client_income,
                client_emp_exp=client_emp_exp,
                client_credit_score=client_credit_score,
                client_previous_default=client_previous_default,
                client_home_ownership=client_home_ownership,
                client_profession=client_profession
            )

            session.add(new_client)
            session.commit()           
            session.close()

            logger.info(f"Cliente {client_cpf} cadastrado com sucesso")
            
            # Resposta de sucesso
            resposta = ClientResponseSchema(
                success=True,
                message="Cliente cadastrado com sucesso",
                client_cpf=client_cpf,
            )
            
            return resposta.dict(), 200

        except IntegrityError as e:
            logger.error(f"Erro de integridade ao cadastrar cliente: {e}")
            return ErrorSchema(message="Erro de integridade no banco de dados. CPF pode já estar cadastrado.").dict(), 409
        except Exception as e:
            logger.error(f"Erro ao cadastrar cliente: {e}")
            return ErrorSchema(message=f"Erro interno ao cadastrar cliente: {str(e)}").dict(), 500
        finally:
            if 'session' in locals():
                session.close()

    @app.post('/checkCPF', tags=[client_tag],
            responses={"200": CheckCPFResponseSchema, "400": ErrorSchema, "500": ErrorSchema})
    def check_cpf(form: CheckCPFRequestSchema):
        """
        Verifica se um CPF já está cadastrado na base de dados
        """
        try:
            # Extrair dados do formulário
            client_cpf = form.client_cpf

            # Verificar se o campo foi preenchido
            if not client_cpf:
                return ErrorSchema(message="CPF é obrigatório").dict(), 400

            # Validar formato do CPF (11 dígitos)
            if len(client_cpf) != 11 or not client_cpf.isdigit():
                return ErrorSchema(message="CPF inválido. Deve conter 11 dígitos numéricos.").dict(), 400

            # Verificar se CPF existe na base de dados
            session = Session()
            existing_client = session.query(Client).filter_by(client_cpf=client_cpf).first()
            session.close()
            
            if existing_client:
                logger.info(f"CPF {client_cpf} encontrado na base")
                return CheckCPFResponseSchema(
                    exists=True,
                    message="CPF já cadastrado",
                    client_cpf=client_cpf
                ).dict(), 200
            else:
                logger.info(f"CPF {client_cpf} não encontrado na base")
                return CheckCPFResponseSchema(
                    exists=False,
                    message="CPF disponível para cadastro",
                    client_cpf=client_cpf
                ).dict(), 200

        except Exception as e:
            logger.error(f"Erro ao verificar CPF: {e}")
            return ErrorSchema(message="Erro interno ao verificar CPF").dict(), 500

    return app

# Exportação padrão para o __init__.py
__all__ = ['configure_client_endpoints']