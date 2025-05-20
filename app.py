from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
import os

TOKEN = os.getenv("BOT_TOKEN")  # Seteado desde Render como variable de entorno

def start(update: Update, context: CallbackContext):
    update.message.reply_text("¡Hola! El bot Galicia N4 está activo desde Render.")

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
