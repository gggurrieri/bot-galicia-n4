
import os
import random
import time
import logging
from telegram.ext import Updater, CommandHandler
from telegram import ParseMode
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Configuración
TOKEN = os.getenv("TELEGRAM_TOKEN")
AUTHORIZED_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
BASE_URL = "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/"
URL_N4 = "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/n3/n4/356"

# Estado del bot
estado_bot = {"activo": False, "cantidad": 1}

def obtener_urls_n4(driver):
    driver.get(URL_N4)
    time.sleep(2)
    enlaces = driver.find_elements(By.XPATH, '//a[contains(@href, "/n4/")]')
    urls = list({e.get_attribute("href") for e in enlaces if e.get_attribute("href")})
    random.shuffle(urls)
    return urls

def click_si_y_estrellas(driver):
    try:
        boton_si = driver.find_element(By.ID, "btnUtil")
        boton_si.click()
        print("✅ Botón 'Sí' clickeado")

        time.sleep(1)

        estrella = driver.find_element(By.CSS_SELECTOR, ".fa.fa-star.fa-2x")
        estrella.click()
        print("⭐ Estrella 5 clickeada")
    except Exception as e:
        print(f"⚠️ Error al calificar: {e}")

def calificar_urls_n4():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    urls_visitadas = []
    try:
        urls = obtener_urls_n4(driver)
        for url in urls[:estado_bot["cantidad"]]:
            driver.get(url)
            time.sleep(2)
            click_si_y_estrellas(driver)
            urls_visitadas.append(url)
    finally:
        driver.quit()
    return urls_visitadas

# Telegram handlers
def start(update, context):
    update.message.reply_text("Bot Galicia N4 activo. Usá /activar [n] para comenzar.")

def activar(update, context):
    if str(update.effective_chat.id) != AUTHORIZED_CHAT_ID:
        return

    try:
        cantidad = int(context.args[0]) if context.args else 1
    except:
        cantidad = 1
    estado_bot["activo"] = True
    estado_bot["cantidad"] = cantidad

    urls = calificar_urls_n4()
    mensaje = f"✅ Se calificaron {len(urls)} URL(s):\n" + "\n".join(urls)
    context.bot.send_message(chat_id=update.effective_chat.id, text=mensaje)

def pausar(update, context):
    if str(update.effective_chat.id) != AUTHORIZED_CHAT_ID:
        return

    estado_bot["activo"] = False
    context.bot.send_message(chat_id=update.effective_chat.id, text="⏸️ Bot pausado")

# Main
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("activar", activar))
    dp.add_handler(CommandHandler("pausar", pausar))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
