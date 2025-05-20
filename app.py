import os
import random
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from bs4 import BeautifulSoup

TOKEN = os.getenv("BOT_TOKEN")
GALICIA_URL = "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/"

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Bot Galicia N4 activo. Usá /activar 3 para calificar 3 URLs.")

def obtener_urls_n4():
    try:
        response = requests.get(GALICIA_URL)
        soup = BeautifulSoup(response.text, "html.parser")
        urls = [a['href'] for a in soup.find_all('a', href=True) if "/n4/" in a['href']]
        urls = list(set(urls))  # eliminar duplicados
        return urls
    except Exception as e:
        return []

def calificar_url(session, full_url):
    try:
        session.post(f"{full_url}/Utilidad", data={"valor": "1"})  # Votar "Sí"
        session.post(f"{full_url}/Satisfaccion", data={"valor": "5"})  # Votar 5 estrellas
        return True
    except:
        return False

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

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("activar", activar))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
