
import os
import telegram
from telegram.ext import Updater, CommandHandler, CallbackContext
from flask import Flask, request

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable is missing.")

bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Command handler
def activar(update: telegram.Update, context: CallbackContext):
    update.message.reply_text("Bot activado correctamente. ¡Listo para calificar URLs!")

dispatcher.add_handler(CommandHandler("activar", activar))

# Webhook endpoint
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

# Home route
@app.route('/')
def index():
    return 'Bot Galicia N4 corriendo (webhook activo).'

# Start the webhook
def main():
    port = int(os.environ.get("PORT", 10000))
    webhook_url = f"https://{os.environ['RENDER_EXTERNAL_HOSTNAME']}/{TOKEN}"

    updater.start_webhook(
        listen="0.0.0.0",
        port=port,
        url_path=TOKEN,
    )
    updater.bot.set_webhook(webhook_url)
    updater.idle()

if __name__ == '__main__':
    main()
