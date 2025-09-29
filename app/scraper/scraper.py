from selenium_driverless.types.by import By
from app.constantes.constantes import HEADERS, API_URL, APIKEY
import requests

async def obtener_categorias(driver):
    categorias = await driver.find_element(By.CLASS_NAME, "listings__facets", timeout=60)
    if not categorias:
        print("No se pudo obtener ninguna categoria")
    await driver.save_screenshot('img.png')
    groups = await categorias.find_elements(By.CLASS_NAME, "listings__facets__group") # div
    items = []
    for group in groups:
        ul = await group.find_element(By.CSS_SELECTOR, '.listings__facets__group__items') # ul
        lis = await ul.find_elements(By.CSS_SELECTOR, 'li a')
        item = {}
        valores = {}
        for li in lis:
            title_cat = await li.find_element(By.CSS_SELECTOR, '.listings__facets__group__items__item__text')
            atributo = await title_cat.text
            link = await li.get_attribute('href')
            if '?' in link:
                llave, valor = link.split('?')[1].split('=')
                valores[atributo] = valor            
                item[llave] = valores
        if item:
            items.append(item)
    
    return items

def extraer_datos(lista_bus):
    datos = []
    for bus in lista_bus:
        datos.append({
            "adress": bus['dealer']['address'],
            "city": bus['dealer']['city'],
            "state": bus['dealer']['state'],
            "phone": bus['dealer']['phone'],
            "suspension": bus["attributes"]["Suspension Type"],
            "make": bus['make'],
            "model": bus["model"],
            "year": bus['year']
            #"primaryPhoto": bus['primaryPhoto'],
        })
    return datos

def obtener_bus_cat(key, item):
    params = {
            'apiKey': APIKEY,
            'page': 1,
            key: item
            } 
    response = requests.get(API_URL, params=params, headers=HEADERS)
    data = response.json()
    productos = extraer_datos(data['units'])
    totalPag = data['statistics']['pageCount']
    if totalPag > 1:
        for i in range(1,totalPag):
            params = {
            'apiKey': APIKEY,
            'page': i + 1,
            key: item
            } 
            response = requests.get(API_URL, params=params, headers=HEADERS)
            data = response.json()
            productos.extend(extraer_datos(data['units']))
    return productos

def chequea_params(parametro, categorias):
    for cat in categorias:
        key_cat = list(cat.keys())
        for valor in cat.values():
            if valor.get(parametro):
                return key_cat[0], valor[parametro]
    return []
