
from flask import Flask, request
import telegram
import os
from calificar import ejecutar_calificacion

TELEGRAM_TOKEN = "7863131299:AAHAc4TdPQpQL0riIDbGaqS8sts6wKzCv_0"
CHAT_ID_AUTORIZADO = 5171106537

bot = telegram.Bot(token=TELEGRAM_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Galicia N4 activo"

@app.route('/', methods=['POST'])
def recibir_mensaje():
    data = request.get_json()

    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"]

        if chat_id != CHAT_ID_AUTORIZADO:
            bot.send_message(chat_id=chat_id, text="⛔ No estás autorizado para usar este bot.")
            return "No autorizado"

        print(f"📩 Recibido: {text}")

        if text.startswith("/status"):
            bot.send_message(chat_id=chat_id, text="✅ Bot activo y esperando órdenes.")
        elif text.startswith("/calificar"):
            try:
                partes = text.split(" ")
                cantidad = int(partes[1]) if len(partes) > 1 else 1
                ejecutar_calificacion(cantidad)
                bot.send_message(chat_id=chat_id, text=f"✅ Se calificaron {cantidad} URLs N4.")
            except Exception as e:
                print("Error al ejecutar calificación:", e)
                bot.send_message(chat_id=chat_id, text="❌ Error al intentar calificar.")
        else:
            bot.send_message(chat_id=chat_id, text="🤖 Comando no reconocido.")

    return "ok"
