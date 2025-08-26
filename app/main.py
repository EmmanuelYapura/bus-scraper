from selenium_driverless import webdriver
from app.scraper.scraper import obtener_categorias, obtener_bus_cat, chequea_params
from app.constantes.constantes import URL
import asyncio, uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def index():
    return {"Message": "estas son las categorias que puede scrappear", "categorias": asyncio.run(main())}

@app.get("/{categoria}")
def get_cats(categoria :str):
    categorias = asyncio.run(main())
    if chequea_params(categoria, categorias):
        key, valor = chequea_params(categoria, categorias)
        return obtener_bus_cat(key, valor)
    return []

async def main():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")  # Ejecuta Chrome sin interfaz gráfica
    chrome_options.add_argument("--no-sandbox") # Deshabilita el sandbox, necesario en entornos de contenedores
    chrome_options.add_argument("--disable-dev-shm-usage") # Evita problemas de memoria compartida
    chrome_options.add_argument("--disable-gpu") # Deshabilita la aceleración por hardware de la GPU

    driver = await webdriver.Chrome(options=chrome_options) 
    try:
        await driver.get(URL)
        await asyncio.sleep(15)
        items = await obtener_categorias(driver)
        if not items:
            print('No se pudo obtener las cats')
    except Exception as e:
        print("El error es: ", e)

    finally:
        await driver.quit()
        return items

if __name__ == "main":
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True
    )