
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def ejecutar_calificacion(bot, chat_id, cantidad=1):
    bot.send_message(chat_id=chat_id, text=f"⚙️ Iniciando calificación de {cantidad} URL(s)...")

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    url_base = "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/"
    driver.get(url_base)

    links = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/n4/"]')
    urls_n4 = [a.get_attribute("href") for a in links if "/n4/" in a.get_attribute("href")]
    urls_n4 = list(dict.fromkeys(urls_n4))  # sin duplicados

    for i, url in enumerate(urls_n4[:cantidad]):
        try:
            driver.get(url)
            print(f"🔗 Entrando a: {url}")
            time.sleep(2)
            driver.find_element(By.ID, "btnSi").click()
            time.sleep(1)
            driver.find_element(By.CLASS_NAME, "clasificacion").find_elements(By.TAG_NAME, "a")[4].click()
            time.sleep(1)
        except Exception as e:
            print(f"❌ Error en {url}: {e}")
            bot.send_message(chat_id=chat_id, text=f"❌ Error al calificar {url}")

    driver.quit()
    bot.send_message(chat_id=chat_id, text="✅ Calificación finalizada.")
