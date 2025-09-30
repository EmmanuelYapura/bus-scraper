# Scraper buses

Este proyecto es un web scraper que obtiene informacion desde la pagina de autobuses [devivobus](https://www.devivobus.com/inventory/).
Se recopilan datos como direccion, ciudad, estado, telefono, suspension, marca, modelo, etc.

## Tecnologias utilizadas

- Python 3
- requests
- FastAPI
- Selenium driverless

## Que hace este scraper?

- Obtiene las categorias principales de los buses salteando el captcha con selenium driverless
- Utiliza la API interna de devivobus para la peticiones.
- Extrae datos relevantes de cada bus: city, phone, make, model, year, suspension.

## Como utilizar el scraper

1. **Clonar el repositorio**
```
git clone https://github.com/EmmanuelYapura/bus-scraper.git .
```

2. **Crear un entorno virtual**
```
python -m venv venv
```

- Windows
```
venv/Scripts/activate
```

- Linux/macOs
```
source venv/bin/activate
```

3. **Instalar las dependencias**
```
pip install -r requirements.txt
```

4. **Levantar el servidor**

Para levantar el servidor utilizamos uvicorn
```
uvicorn app.main:app --reload
```

5. **Ingresar al puerto**

Luego de ver por consola que las categorias fueron cargadas con exito ingresamos a:
```
http://127.0.0.1:8000
```

## Endpoints para uso
  Nota: Las categorias son las keys dentro de cada tipo de categoria, ejemplo en "designation" -> las categorias para scrapear son New y Used

- GET /

  - Descripcion: Devuelve un objeto con un mensaje y las categorias para poder utilizar

  - Ejemplo

  ```
  curl http://127.0.0.1:8000/
  ```

  - Respuesta

  ```
  {
  "Message": "estas son las categorias que puede scrappear",
  "categorias": [
    {
      "designation": {
        "New": "0",
        "Used": "1"
      }
    },
    {
      "vehtype": {
        "Activity Bus": "198",
        "Commercial Bus": "141",
        "School Bus": "142",
        "Van": "114"
      }
    },
    {
      "year": {
        "2013": "2013",
        "2014": "2014",
        "2015": "2015",
        "2016": "2016",
        "2023": "2023",
        "2024": "2024",
        "2025": "2025",
        "2026": "2026"
      }
    },...]
  }
  ```

- GET /{categoria}

  - Descripcion: Devuelve una lista de buses de la categoria especificada

  - Parametros

    - categoria (string)

  - Ejemplo

  ```
  curl http://127.0.0.1:8000/New
  ```

  - Respuesta

  ```
  [
  {
    "adress": "315 South Street",
    "city": "New Britain",
    "state": "CT",
    "phone": "(860) 356-0252",
    "suspension": "Spring",
    "make": "Collins",
    "model": "DH500",
    "year": 2026
  },
  {
    "adress": "315 South Street",
    "city": "New Britain",
    "state": "CT",
    "phone": "(860) 356-0252",
    "suspension": "Air",
    "make": "IC Bus",
    "model": "CE",
    "year": 2026
  },
  {
    "adress": "315 South Street",
    "city": "New Britain",
    "state": "CT",
    "phone": "(860) 356-0252",
    "suspension": "Spring",
    "make": "Collins",
    "model": "DE516WR",
    "year": 2026
  },
  ...]
  ```

## Notas importantes

- Este proyecto fue realizado con fines educativos y de práctica en web scraping.
- La estructura de la web puede cambiar y romper el scraper en el futuro.
  
## Autor

- **Emmanuel Yapura**  
  [LinkedIn](https://www.linkedin.com/in/emmanuelyapura)
