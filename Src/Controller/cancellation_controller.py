import os
import concurrent.futures
import pandas as pd
from dotenv import load_dotenv
from pyrogram.types import Message
from pyrogram import Client
from datetime import datetime
from Src.Service.cancellation_service import cancelamento
from Src.Util.formatador import formatar_incidencia, formatar_valor_multa

load_dotenv()

running = False
def executar(arg: dict, message: Message):
    if running:
        try:
            mk = int(arg.get("MK"))
            cod_pessoa = int(arg.get("Cod Pessoa"))
            contrato = int(arg.get("Contrato"))
            detalhes_cancelamento = arg.get("Detalhes Cancelamento")
            tipo_da_os = arg.get("Tipo OS")
            grupo_atendimento_os = arg.get("Grupo Atendimento OS")
            relato_do_problema = arg.get("Relato do problema")
            incidencia_multa = formatar_incidencia(arg.get("Incidencia de Multa"))
            valor_multa = formatar_valor_multa(arg.get("Valor Multa"))
            vencimento_multa = arg.get("Data Vcto Multa Contratual").strftime("%d%m%Y")
            planos_contas = arg.get("Planos de Contas")

            return cancelamento(
                mk = mk,
                cod_pessoa = cod_pessoa,
                contrato = contrato,
                detalhes_cancelamento = detalhes_cancelamento,
                tipo_da_os = tipo_da_os,
                grupo_atendimento_os = grupo_atendimento_os,
                relato_do_problema = relato_do_problema,
                incidencia_multa = incidencia_multa,
                valor_multa = valor_multa,
                vencimento_multa = vencimento_multa,
                planos_contas = planos_contas
                )
            return mk, cod_pessoa, contrato
            print(
                mk,
                cod_pessoa,
                contrato,
                detalhes_cancelamento,
                tipo_da_os,
                grupo_atendimento_os,
                relato_do_problema,
                incidencia_multa,
                valor_multa,
                vencimento_multa,
                planos_contas
                )
        except Exception as e:
            print(f'Error executar na função cancelamento:mk:{int(arg.get("MK"))} cod:{int(arg.get("Cod Pessoa"))} contrato:{int(arg.get("Contrato"))} {e}')
    else:
        message.reply_text(f'Cancelamento mk:{int(arg.get("MK"))} cod:{int(arg.get("Cod Pessoa"))} contrato:{int(arg.get("Contrato"))} parado.')

def handle_start_cancellation(client: Client, message: Message):
    global running
    if not running:
        # Verifique se a mensagem contém um documento e se o tipo MIME do documento é "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        if message.document and message.document.mime_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            running = True
            # Quantidade de itens na Pool
            limite_threads = 5

            # Baixe o arquivo XLSX
            file_path = message.download(in_memory=True)
            hora = datetime.now()
            file_name = hora.strftime("%S_%M_%H %Y-%m-%d.log")
            message.reply_text("Preparando arquivo XLSX")

            # caminho pasta de logs
            diretorio_logs = os.path.join(os.path.dirname(__file__), 'logs')

            # caminho pasta de docs
            diretorio_docs = os.path.join(os.path.dirname(__file__), 'docs')

            # cria pasta de logs em caso de nao existir
            if not os.path.exists(diretorio_logs):
                os.makedirs(diretorio_logs)

            # cria pasta de docs em caso de nao existir
            if not os.path.exists(diretorio_docs):
                os.makedirs(diretorio_docs)
            
            # Processar o arquivo XLSX conforme necessário
            try:
                try:
                    # Ler o arquivo XLSX usando pandas e especificar a codificação UTF-8
                    df = pd.read_excel(file_path, engine='openpyxl')

                    # Converter o dataframe para uma lista de dicionários
                    lista = df.to_dict(orient='records')

                    # Verificar se a chave 'MK' contém valor NaN
                    lista = [dados for dados in lista if not pd.isna(dados.get('MK'))]
                    # print(lista)

                    # Criar aquivo de log com todos os contratos enviados para cancelamento
                    with open(os.path.join(diretorio_docs, file_name), "a") as pedido:
                        for c,arg in enumerate(lista):
                            pedido.write(f"{(c + 1):03};Cancelamento;MK:{int(arg.get('MK'))};Cod:{int(arg.get('Cod Pessoa'))};Contrato:{int(arg.get('Contrato'))};Grupo:{arg.get('Grupo Atendimento OS')};Multa:R${arg.get('Valor Multa')};Agente:{message.from_user.first_name}.{message.from_user.last_name}\n")
                    
                    # Envia arquivo de docs com todos as solicitações de cancelamento
                    with open(os.path.join(diretorio_docs, file_name), "rb") as enviar_docs:
                        client.send_document(os.getenv("CHAT_ID_ADM"),enviar_docs, caption=f"solicitações {file_name}", file_name=f"solicitações {file_name}")

                    
                    message.reply_text(f"Processando arquivo XLSX de cancelamento com {len(lista)} contratos...")

                except pd.errors.ParserError:
                    message.reply_text("O arquivo fornecido não é um arquivo XLSX válido.")
                    running = False
                    return
                
                def executar(arg: dict, message: Message):
                    if running:
                        try:
                            mk = int(arg.get("MK"))
                            cod_pessoa = int(arg.get("Cod Pessoa"))
                            contrato = int(arg.get("Contrato"))
                            detalhes_cancelamento = arg.get("Detalhes Cancelamento")
                            tipo_da_os = arg.get("Tipo OS")
                            grupo_atendimento_os = arg.get("Grupo Atendimento OS")
                            relato_do_problema = arg.get("Relato do problema")
                            incidencia_multa = formatar_incidencia(arg.get("Incidencia de Multa"))
                            valor_multa = formatar_valor_multa(arg.get("Valor Multa"))
                            vencimento_multa = arg.get("Data Vcto Multa Contratual").strftime("%d%m%Y")
                            planos_contas = arg.get("Planos de Contas")

                            return cancelamento(
                                mk = mk,
                                cod_pessoa = cod_pessoa,
                                contrato = contrato,
                                detalhes_cancelamento = detalhes_cancelamento,
                                tipo_da_os = tipo_da_os,
                                grupo_atendimento_os = grupo_atendimento_os,
                                relato_do_problema = relato_do_problema,
                                incidencia_multa = incidencia_multa,
                                valor_multa = valor_multa,
                                vencimento_multa = vencimento_multa,
                                planos_contas = planos_contas
                                )
                        except Exception as e:
                            print(f'Error executar na função cancelamento:mk:{int(arg.get("MK"))} cod:{int(arg.get("Cod Pessoa"))} contrato:{int(arg.get("Contrato"))} {e}')
                    else:
                        message.reply_text(f'Cancelamento mk:{int(arg.get("MK"))} cod:{int(arg.get("Cod Pessoa"))} contrato:{int(arg.get("Contrato"))} parado.')
                
                # Criando Pool
                with concurrent.futures.ThreadPoolExecutor(max_workers=limite_threads) as executor:
                    resultados = executor.map(executar, lista)

            except Exception as e:
                print(f"Ocorreu um erro ao processar o arquivo XLSX: {e}")
                running = False
                return
            
            finally:
                # Criar aquivo de log com todos os resultados de cancelamento
                with open(os.path.join(diretorio_logs, file_name), "a") as file:
                    if resultados:
                        for resultado in resultados:
                            file.write(f"{resultado}\n")

                # Envia arquivo de log com todos os resultados de cancelamento
                with open(os.path.join(diretorio_logs, file_name), "rb") as enviar_logs:
                    message.reply_document(enviar_logs, caption=file_name, file_name=file_name)
                    client.send_document(os.getenv("CHAT_ID_ADM"), enviar_logs, caption=f"resultado {file_name}", file_name=f"resultado {file_name}")

                print("Processo Cancelamento concluído.")
                message.reply_text("O arquivo XLSX de cancelamento foi processado com sucesso!")
                running = False
                return
                
        else:
            # Responder à mensagem do usuário com uma mensagem de erro
            message.reply_text("Por favor, envie um arquivo XLSX para processar.")
            return
    else:
        message.reply_text("Cancelamento em execução.")
        return

def handle_stop_cancellation(client: Client, message: Message):
    global running
    if running:
        running = False
        message.reply_text("Pedido de parada iniciado...")
        return
    else:
        message.reply_text("Cancelamento parado")
        return
        
def handle_status_cancellation(client: Client, message: Message):
    global running
    try:
        if running:
            message.reply_text("Cancelamento em execução")
            return
        else:
            message.reply_text("Cancelamento parado")
            return
    except:
        message.reply_text("Cancelamento parado")
        return