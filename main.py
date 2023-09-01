import os
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import Message
from Src.Middleware.authentication import authorization_adm, authorization_group
from Src.Controller.cancellation_controller import handle_start_cancellation, handle_stop_cancellation, handle_status_cancellation

load_dotenv()

version = "0.0.15"

app = Client(
    name=os.getenv("BOT_NAME_TELEGRAM"), 
    api_hash=os.getenv("API_HASH_TELEGRAM"),
    api_id=os.getenv("API_ID_TELEGRAM"),
    bot_token=os.getenv("BOT_TOKEN_TELEGRAM")
    )

chat_adm = [
    int(os.getenv("CHAT_ID_ADM")),
]

chat_group = [
    int(os.getenv("CHAT_ID_ADM")),
    int(os.getenv("CHAT_ID_GROUP_CANCELLATION")),
]

@app.on_message(filters.command("start"))
def start(client, message: Message):
    message.reply_text(f"""
/cancelamento - Setor Cancelamento
/chat - Informa seu chat_id
/chatgroup - Informa chat_id grupo
""")

@app.on_message(filters.command("cancelamento"))
@authorization_group(chat_group)
def financeiro(client, message: Message):
    message.reply_text(f"""
/iniciar_cancelamento - Iniciar Cancelamento
/parar_cancelamento - Parar Cancelamento
/status_cancelamento - Status Cancelamento
""")

@app.on_message(filters.command("chatgroup"))
@authorization_adm(chat_adm)
def handle_chatgroup_id(client: Client, message: Message):
    client.send_message(message.from_user.id, message)

@app.on_message(filters.command("chat"))
def handle_chat_id(client: Client, message: Message):
    text = f"{message.from_user.first_name}.{message.from_user.last_name} - ID:{message.from_user.id}"
    client.send_message(message.from_user.id, text)
    client.send_message(chat_adm[0], text)

# iniciar cancelamento
@app.on_message(filters.command("iniciar_cancelamento"))
@authorization_group(chat_group)
def iniciar_cancellation(client: Client, message: Message):
    handle_start_cancellation(client, message)

# parar cancelamento
@app.on_message(filters.command("parar_cancelamento"))
@authorization_group(chat_group)
def parar_cancellation(client: Client, message: Message):
    handle_stop_cancellation(client, message)

# status cancelamento
@app.on_message(filters.command("status_cancelamento"))
@authorization_group(chat_group)
def status_cancellation(client: Client, message: Message):
    handle_status_cancellation(client, message)

# stop service
@app.on_message(filters.command("stop_service"))
@authorization_adm(chat_adm)
def stop(client: Client, message: Message):
    print("Service Stopping")
    app.stop()

print("Service Telegram Up!")
print(f"Version {version}")
app.run()

