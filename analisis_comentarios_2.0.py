from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import pandas as pd
import matplotlib.pyplot as plt

datos_reseñas = []
pagina = 1
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

URL = 'https://mydramalist.com/681019-i-told-sunset-about-you-part-2/reviews'
driver.get(URL)
while True:
    time.sleep(7)
    Reseñas_pantalla = driver.find_elements(By.CLASS_NAME, 'review-body')
    for reseñas in Reseñas_pantalla:
        dict_reseña = {'texto': reseñas.text.strip(), 'longitud': len(reseñas.text.strip())}
        datos_reseñas.append(dict_reseña)
    try:
        botton_next = driver.find_element(By.XPATH, '//li[contains(@class, "next")]/a')
        driver.execute_script('arguments[0].scrollIntoView({block: "center"});', botton_next) 
        time.sleep(2)
        driver.execute_script('arguments[0].click();', botton_next)
        pagina += 1
    except Exception:
        print('No hay mas que leer')
        break
driver.quit()
df = pd.DataFrame(datos_reseñas)
if not df.empty:
    df.to_csv('reseñas_ipytm.csv', index= False)
else:
    print('No hay data')

    

df = pd.read_csv('reseñas_ipytm.csv')

keywords_incongruencia = [
        'different', 'toxic', 'out of character', 'inconsistent', 
        'ruined', 'disappointed', 'mess', 'cheating', 'personality'
    ]

def detectar_incongruencia(texto):
    if pd.isna(texto): return "Sin texto"
        
    texto_minuscula = texto.lower()
    for palabra in keywords_incongruencia:
        if palabra in texto_minuscula:
            return "Perdieron su esencia"
                
    return "Mantuvieron su esencia"

print(" Clasificando las reseñas...")
df['veredicto'] = df['texto'].apply(detectar_incongruencia)

df.to_csv('reseñas_finales.csv', index=False)

conteo = df['veredicto'].value_counts()
print("\n--- RESULTADOS DEL ANÁLISIS ---")
print(conteo)
etiquetas = conteo.index
colores = ['#ff6666', '#66b3ff']
explode = (0.1, 0)
plt.figure(figsize=(8, 6))
plt.pie(conteo, explode=explode, labels=etiquetas, colors=colores, autopct='%1.1f%%', shadow=True, startangle=140)
plt.title('¿perdieron Teh y Oh-aew su esencia en Bangkok? \n(Análisis basado en reseñas de MyDramaList)')
plt.axis('equal')
plt.savefig('Grafico_IPYTM.png')
plt.show()