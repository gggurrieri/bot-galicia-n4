
from flask import Flask, request
import telegram
import os
from calificar import ejecutar_calificacion

# Config
TELEGRAM_TOKEN = "7863131299:AAHAc4TdPQpQL0riIDbGaqS8sts6wKzCv_0"
CHAT_ID_AUTORIZADO = 5171106537

bot = telegram.Bot(token=TELEGRAM_TOKEN)
app = Flask(__name__)

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"]
        if chat_id != CHAT_ID_AUTORIZADO:
            bot.send_message(chat_id=chat_id, text="🚫 Acceso no autorizado.")
            return "ok"

        bot.send_message(chat_id=chat_id, text=f"📨 Recibido: {text}")

        if text.startswith("/status"):
            bot.send_message(chat_id=chat_id, text="✅ El bot está activo.")
        elif text.startswith("/calificar"):
            partes = text.split()
            cantidad = int(partes[1]) if len(partes) > 1 and partes[1].isdigit() else 1
            ejecutar_calificacion(bot, chat_id, cantidad)
    return "ok"

@app.route("/")
def index():
    return "Bot Galicia N4 activo"

if __name__ == "__main__":
    app.run(debug=True)
