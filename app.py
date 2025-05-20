import os
from dotenv import load_dotenv
load_dotenv()

from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import Update
from flask import Flask
import threading
import time

# Variables de entorno
TOKEN = os.getenv("TOKEN")
print(f"[DEBUG] TOKEN obtenido: {TOKEN}")
if not TOKEN:
    raise ValueError("La variable TOKEN no está definida. Verificá tus variables de entorno en Render o el .env local.")
CHAT_ID_AUTORIZADO = os.getenv("CHAT_ID_AUTORIZADO")
URL_INICIAL = os.getenv("URL_INICIAL")

if not TOKEN:
    raise ValueError("La variable TOKEN no está definida. Verificá tus variables de entorno en Render o el .env local.")

print(f"[DEBUG] TOKEN cargado correctamente.")

# Resto de tu código...
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Bot Galicia N4 activado correctamente.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()