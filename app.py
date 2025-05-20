import os
from flask import Flask, request
from telegram import Bot
from calificar import ejecutar_calificacion

app = Flask(__name__)

TELEGRAM_TOKEN = '7863131299:AAHAc4TdPQpQL0riIDbGaqS8sts6wKzCv_0'
CHAT_ID_AUTORIZADO = 5171106537

bot = Bot(token=TELEGRAM_TOKEN)
ultimas_urls_calificadas = []

@app.route('/', methods=['POST'])
def webhook():
    global ultimas_urls_calificadas

    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        mensaje = data["message"].get("text", "")

        if chat_id != CHAT_ID_AUTORIZADO:
            return "No autorizado", 200

        if mensaje.startswith("/activar"):
            try:
                partes = mensaje.strip().split()
                cantidad = int(partes[1]) if len(partes) > 1 else 1
                urls = ejecutar_calificacion(cantidad)
                ultimas_urls_calificadas = urls
                resumen = "\n".join(f"🔹 {url}" for url in urls)
                respuesta = f"✅ Se calificaron {len(urls)} URLs:\n{resumen}"
            except Exception as e:
                respuesta = f"⚠️ Error al ejecutar la calificación: {str(e)}"

        elif mensaje.startswith("/status"):
            if ultimas_urls_calificadas:
                resumen = "\n".join(f"🔹 {url}" for url in ultimas_urls_calificadas)
                respuesta = f"📊 Últimas URLs calificadas:\n{resumen}"
            else:
                respuesta = "ℹ️ No se calificaron URLs aún."

        elif mensaje.startswith("/start"):
            respuesta = "👋 Bot Galicia N4 activo. Usá /activar [cantidad] o /status."

        else:
            respuesta = "❓ Comando no reconocido. Usá /activar [cantidad] o /status."

        bot.send_message(chat_id=chat_id, text=respuesta)

    return "OK", 200
