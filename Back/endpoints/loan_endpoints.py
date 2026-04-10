from flask_openapi3 import Tag
from logger import logger
from schemas import *
from model import Session, Client, LoanData
from sqlalchemy.exc import IntegrityError

# definindo tag
loan_tag = Tag(name="LoanTest", description="Inserção de clientes na base de dados")

def configure_loan_test_endpoints(app):
    """
    Configura todas as rotas relacionadas a clientes
    """

    @app.post('/registerLoanData', tags=[loan_tag],
            responses={"200": LoanDataResponseSchema, "400": ErrorSchema, "404": ErrorSchema, "409": ErrorSchema, "500": ErrorSchema})
    def register_loan_data(form: LoanDataRequestSchema):
        """
        Registra os detalhes do empréstimo pedido e faz a análise de crédito
        
        O cliente deve já estar cadastrado no banco (via /registerClient)
        """
        try:

            # EXTRAIR DADOS DO FORMULÁRIO
            
            client_cpf = form.client_cpf
            loan_amnt = form.loan_amnt
            loan_intent = form.loan_intent
            loan_int_rate = form.loan_int_rate
            loan_percent_income = form.loan_percent_income
            cb_person_cred_hist_length = form.cb_person_cred_hist_length

            # VALIDAÇÕES BÁSICAS
            
            # Verificar CPF
            if not client_cpf:
                return ErrorSchema(message="CPF é obrigatório").dict(), 400
            
            # Validar formato do CPF (11 dígitos)
            if len(client_cpf) != 11 or not client_cpf.isdigit():
                return ErrorSchema(message="CPF inválido. Deve conter 11 dígitos numéricos.").dict(), 400
            
            # Validar valor do empréstimo
            if loan_amnt <= 0:
                return ErrorSchema(message="Valor do empréstimo deve ser maior que zero.").dict(), 400
            
            # Validar taxa de juros
            if loan_int_rate < 0:
                return ErrorSchema(message="Taxa de juros não pode ser negativa.").dict(), 400
            
            # Validar percentual da renda
            if loan_percent_income < 0 or loan_percent_income > 100:
                return ErrorSchema(message="Percentual da renda deve estar entre 0 e 100.").dict(), 400
            
            # Validar histórico de crédito
            if cb_person_cred_hist_length < 0:
                return ErrorSchema(message="Histórico de crédito não pode ser negativo.").dict(), 400
            
            # Validar objetivo do empréstimo
            valid_intents = ["Education", "HomeImprovement", "Medical", "Personal", "Venture", "DebtConsolidation"]
            if loan_intent not in valid_intents:
                return ErrorSchema(message=f"Objetivo do empréstimo inválido. Opções: {', '.join(valid_intents)}").dict(), 400
            
            # VERIFICAR SE CLIENTE EXISTE NO BANCO
            
            session = Session()
            
            # Buscar cliente pelo CPF
            client = session.query(Client).filter_by(client_cpf=client_cpf).first()
            
            if not client:
                session.close()
                logger.warning(f"Tentativa de registro de empréstimo para CPF não cadastrado: {client_cpf}")
                return ErrorSchema(message=f"Cliente com CPF {client_cpf} não encontrado. Cadastre o cliente primeiro.").dict(), 404
            
            # INSERIR NOVO TESTE DE EMPRÉSTIMO
            
            loan_data = LoanData(
                client_cpf=client.client_cpf,
                loan_amnt=loan_amnt,
                loan_intent=loan_intent,
                loan_int_rate=loan_int_rate,
                loan_percent_income=loan_percent_income,
                cb_person_cred_hist_length=cb_person_cred_hist_length
            )
            
            session.add(loan_data)
            session.flush()
            
            # FAZER PREDIÇÃO USANDO O MÉTODO DA PRÓPRIA CLASSE
            
            try:

                result = loan_data.predict_and_save(session, client)
                
                approved = result['approved']
                message = result['message']
                probability_approval = result.get('probability_approval')
                probability_default = result.get('probability_default')
                
            except Exception as e:
                # Se o modelo não estiver disponível, ainda assim salva sem predição
                logger.warning(f"Modelo não disponível: {e}")
                session.commit()
                approved = None
                probability_approval = None
                probability_default = None
                message = "Análise de crédito não disponível no momento."
            
            # RETORNAR RESPOSTA
            
            loan_id = loan_data.loan_id
            session.close()
            
            logger.info(f"Empréstimo registrado: id_loan={loan_id}, cliente={client_cpf}, status={loan_data.loan_status}")
            
            # Resposta de sucesso
            resposta = LoanDataResponseSchema(
                success=True,
                loan_id=loan_id,
                client_cpf=client_cpf,
                approved=approved,
                probability_approval=probability_approval,
                probability_default=probability_default,
                message=message
            )
            
            return resposta.dict(), 200
            
        except IntegrityError as e:
            if 'session' in locals():
                session.rollback()
            logger.error(f"Erro de integridade ao registrar empréstimo: {e}")
            return ErrorSchema(message="Erro de integridade no banco de dados.").dict(), 409
        except Exception as e:
            if 'session' in locals():
                session.rollback()
            logger.error(f"Erro ao registrar empréstimo: {e}")
            return ErrorSchema(message=f"Erro interno ao registrar empréstimo: {str(e)}").dict(), 500
        finally:
            if 'session' in locals():
                session.close()    

    @app.get('/getLoanHistory', tags=[loan_tag],
            responses={"200": LoanHistoryResponseSchema, "400": ErrorSchema, "404": ErrorSchema, "500": ErrorSchema})
    def get_loan_history():
        """
        Retorna o histórico de todos os empréstimos registrados
        
        Retorna lista com id_loan, data, client_cpf, loan_amnt, loan_status
        """
        try:
            session = Session()
            
            # Buscar todos os empréstimos ordenados por data decrescente
            loans = session.query(LoanData).order_by(LoanData.insertion_date.desc()).all()
            
            if not loans:
                return LoanHistoryResponseSchema(
                    success=True,
                    loans=[],
                    message="Nenhum empréstimo encontrado."
                ).dict(), 200
            
            # Construir lista de empréstimos
            loans_list = []
            for loan in loans:
                # Formatar a data para DD/MM/AAAA
                date_str = loan.insertion_date.strftime('%d/%m/%Y') if loan.insertion_date else ''
                
                # Converter loan_status para texto
                status_text = ""
                if loan.loan_status == 0:
                    status_text = "Negado"
                elif loan.loan_status == 1:
                    status_text = "Aprovado"
                else:
                    status_text = "Pendente"
                
                loans_list.append({
                    'loan_id': loan.loan_id,
                    'date': date_str,
                    'client_cpf': loan.client_cpf,
                    'loan_amnt': loan.loan_amnt,
                    'loan_status': loan.loan_status,
                    'loan_status_text': status_text
                })
            
            session.close()
            
            return LoanHistoryResponseSchema(
                success=True,
                loans=loans_list,
                message=f"{len(loans_list)} empréstimos encontrados."
            ).dict(), 200
            
        except Exception as e:
            logger.error(f"Erro ao buscar histórico de empréstimos: {e}")
            return ErrorSchema(message=f"Erro interno ao buscar histórico: {str(e)}").dict(), 500
        finally:
            if 'session' in locals():
                session.close()
    
    @app.delete('/deleteLoan', tags=[loan_tag],
                responses={"200": DeleteLoanResponseSchema, "400": ErrorSchema, "404": ErrorSchema, "500": ErrorSchema})
    def delete_loan(form: DeleteLoanRequestSchema):
        """
        Deleta um empréstimo do banco de dados pelo seu ID
        
        Args:
            form: Contém o loan_id a ser deletado
        """
        try:
            loan_id = form.loan_id
            
            # Validar se o ID foi informado
            if not loan_id:
                return ErrorSchema(message="ID do empréstimo é obrigatório.").dict(), 400
            
            session = Session()
            
            # Buscar o empréstimo pelo ID
            loan = session.query(LoanData).filter_by(loan_id=loan_id).first()
            
            # Verificar se o empréstimo existe
            if not loan:
                session.close()
                logger.warning(f"Tentativa de deletar empréstimo não encontrado: loan_id={loan_id}")
                return ErrorSchema(message=f"Empréstimo com ID {loan_id} não encontrado.").dict(), 404
            
            # Salvar informações para o log antes de deletar
            loan_info = {
                'loan_id': loan.loan_id,
                'client_cpf': loan.client_cpf,
                'loan_amnt': loan.loan_amnt,
                'loan_status': loan.loan_status
            }
            
            # Deletar o empréstimo
            session.delete(loan)
            session.commit()
            session.close()
            
            logger.info(f"Empréstimo deletado com sucesso: loan_id={loan_id}, cliente={loan_info['client_cpf']}")
            
            return DeleteLoanResponseSchema(
                success=True,
                message=f"Empréstimo ID {loan_id} deletado com sucesso.",
                loan_id=loan_id
            ).dict(), 200
            
        except Exception as e:
            if 'session' in locals():
                session.rollback()
            logger.error(f"Erro ao deletar empréstimo: {e}")
            return ErrorSchema(message=f"Erro interno ao deletar empréstimo: {str(e)}").dict(), 500
        finally:
            if 'session' in locals():
                session.close()
    
       

    return app

# Exportação padrão para o __init__.py
__all__ = ['configure_client_endpoints']