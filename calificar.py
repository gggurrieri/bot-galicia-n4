import time
import random

def ejecutar_calificacion(n=1):
    print(f"🔁 Iniciando calificación de {n} URL(s)...")
    for i in range(n):
        url = f"https://ayudaempresas.galicia.ar/AyudajuridicaSPA/n4/fake-url-{random.randint(1000,9999)}"
        print(f"🔗 Entrando a: {url}")
        time.sleep(1)  # Simula tiempo de carga
        print("✅ Clic en 'Sí'")
        time.sleep(1)
        print("⭐ Clic en estrella 5")
        print(f"✔️ URL {i+1}/{n} calificada.")
        time.sleep(1)
    print("🎉 Calificación completada.")
