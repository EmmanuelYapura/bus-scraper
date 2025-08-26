from selenium_driverless import webdriver
from app.scraper.scraper import obtener_categorias, obtener_bus_cat, chequea_params
from app.constantes.constantes import URL
import asyncio
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
    chrome_options.add_argument("--headless")
    driver = await webdriver.Chrome(options=chrome_options) 
    try:
        await driver.get(URL)
        await asyncio.sleep(15)
        items = await obtener_categorias(driver)

    finally:
        await driver.quit()
        return items
