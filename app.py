import os
import random
import requests
from flask import Flask
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from bs4 import BeautifulSoup
from threading import Thread

TOKEN = os.getenv("BOT_TOKEN")
GALICIA_URL = "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/"

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot Galicia N4 activo"

def obtener_urls_n4():
    try:
        response = requests.get(GALICIA_URL)
        soup = BeautifulSoup(response.text, "html.parser")
        urls = [a['href'] for a in soup.find_all('a', href=True) if "/n4/" in a['href']]
        urls = list(set(urls))
        return urls
    except Exception as e:
        return []

def calificar_url(session, full_url):
    try:
        session.post(f"{full_url}/Utilidad", data={"valor": "1"})
        session.post(f"{full_url}/Satisfaccion", data={"valor": "5"})
        return True
    except:
        return False

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Bot Galicia N4 activo. Usá /activar 3 para calificar 3 URLs.")

def activar(update: Update, context: CallbackContext):
    cantidad = 1
    if context.args and context.args[0].isdigit():
        cantidad = min(int(context.args[0]), 10)

    urls = obtener_urls_n4()
    if not urls:
        update.message.reply_text("No se pudieron obtener URLs N4.")
        return

    seleccionadas = random.sample(urls, min(cantidad, len(urls)))
    session = requests.Session()
    resumen = []

    for url in seleccionadas:
        full_url = f"https://ayudaempresas.galicia.ar{url}"
        exito = calificar_url(session, full_url)
        resumen.append(f"✅ {full_url}" if exito else f"❌ {full_url}")

    mensaje = "\n".join(resumen)
    update.message.reply_text(f"Calificación completa:\n{mensaje}")

def correr_bot():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("activar", activar))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    Thread(target=correr_bot).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
