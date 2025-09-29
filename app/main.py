from selenium_driverless import webdriver
from app.scraper.scraper import obtener_categorias, obtener_bus_cat, chequea_params
from app.constantes.constantes import URL
from contextlib import asynccontextmanager
import asyncio
from fastapi import FastAPI

categorias_disponibles = []

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando la carga de datos...")

    global categorias_disponibles
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = await webdriver.Chrome(options=chrome_options)
    try:
        await driver.get(URL)
        await asyncio.sleep(15)
        items = await obtener_categorias(driver)
        categorias_disponibles = items
        print("Datos de categorías cargados con éxito. Puedes ingresar a ver las categorias")
    except Exception as e :
        print("Hubo un error en la carga de datos ", e)
    finally:
        await driver.quit()
        print("Navegador cerrado.")
    
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def index():
    return {"Message": "estas son las categorias que puede scrappear", "categorias": categorias_disponibles}

@app.get("/{categoria}")
def get_cats(categoria :str):
    if chequea_params(categoria, categorias_disponibles):
        key, valor = chequea_params(categoria, categorias_disponibles)
        return obtener_bus_cat(key, valor)
    return []