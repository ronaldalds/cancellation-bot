import os
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import Message
from Src.Middleware.authentication import authorization
from Src.Controller.cancellation_controller import handle_start_cancellation, handle_stop_cancellation, handle_status_cancellation

load_dotenv()

version = "0.0.15"

app = Client(
    name=os.getenv("BOT_NAME_TELEGRAM"), 
    api_hash=os.getenv("API_HASH_TELEGRAM"),
    api_id=os.getenv("API_ID_TELEGRAM"),
    bot_token=os.getenv("BOT_TOKEN_TELEGRAM")
    )


@app.on_message(filters.command("start"))
def start(client: Client, message: Message):
    message.reply_text(f"""
/cancelamento - Setor Cancelamento
/chat - Informa seu chat_id
/chatgroup - Informa chat_id grupo
""")

@app.on_message(filters.command("cancelamento"))
@authorization()
def financeiro(client: Client, message: Message):
    message.reply_text(f"""
/iniciar_cancelamento - Iniciar Cancelamento
/parar_cancelamento - Parar Cancelamento
/status_cancelamento - Status Cancelamento
""")

@app.on_message(filters.command("chatgroup"))
@authorization()
def handle_chatgroup_id(client: Client, message: Message):
    client.send_message(message.from_user.id, message)

@app.on_message(filters.command("chat"))
def handle_chat_id(client: Client, message: Message):
    text = f"{message.from_user.first_name}.{message.from_user.last_name} - ID:{message.from_user.id}"
    client.send_message(message.from_user.id, text)
    if int(os.getenv("CHAT_ID_ADM")) != message.from_user.id:
        client.send_message(int(os.getenv("CHAT_ID_ADM")), text)

# iniciar cancelamento
@app.on_message(filters.command("iniciar_cancelamento"))
@authorization()
def iniciar_cancellation(client: Client, message: Message):
    handle_start_cancellation(client, message)

# parar cancelamento
@app.on_message(filters.command("parar_cancelamento"))
@authorization()
def parar_cancellation(client: Client, message: Message):
    handle_stop_cancellation(client, message)

# status cancelamento
@app.on_message(filters.command("status_cancelamento"))
@authorization()
def status_cancellation(client: Client, message: Message):
    handle_status_cancellation(client, message)

# stop service
@app.on_message(filters.command("stop_service"))
@authorization()
def stop(client: Client, message: Message):
    print("Service Stopping")
    app.stop()

print("Service Telegram Up!")
print(f"Version {version}")
app.run()

