# Usa la imagen base de Python más reciente en modo slim para un tamaño reducido.
FROM python:3.11-slim

# Establece el directorio de trabajo dentro del contenedor.
WORKDIR /app

# --- Comandos para instalar Google Chrome y ChromeDriver ---
#
# Se utilizan múltiples comandos en un solo RUN para optimizar las capas del Docker.
#
# 1. Instala las dependencias necesarias de APT para Chrome y ChromeDriver.
#    - `wget`, `ca-certificates`: Para descargas seguras.
#    - `gnupg`: Para gestionar las claves de firma del repositorio de Google.
#    - `unzip`: Para descomprimir el archivo de ChromeDriver.
#    - `jq`: Para parsear el JSON y encontrar la URL de ChromeDriver.
#    - `curl`: Para hacer la solicitud HTTP que obtiene las URLs de ChromeDriver.
#
# 2. Configura el repositorio de Google Chrome y descarga la clave de firma.
#    - Descarga la clave pública de Google y la convierte a un formato binario (`--dearmor`)
#      para almacenarla de forma segura en `/usr/share/keyrings/`.
#    - Configura el archivo de fuentes de APT (`sources.list.d`) para incluir el
#      repositorio de Google Chrome, especificando la clave de firma recién guardada
#      para verificar la autenticidad de los paquetes.
#
# 3. Instala Google Chrome estable.
#
# 4. Descarga y configura ChromeDriver.
#    - `jq` se usa para encontrar la URL de la última versión de ChromeDriver para Linux 64 bits.
#    - `wget` descarga el archivo ZIP del ChromeDriver.
#    - `unzip` extrae el ejecutable.
#    - `mv` mueve el ejecutable a una ubicación accesible en el `PATH` del sistema.
#    - `chmod +x` le da permisos de ejecución.
#
# 5. Limpia los archivos y la caché para reducir el tamaño final de la imagen.
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    ca-certificates \
    gnupg \
    unzip \
    jq \
    curl \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome-keyring.gpg \
    && sh -c 'echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && CHROME_DRIVER_URL=$(curl -s https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json | jq -r '.channels.Stable.downloads.chromedriver[] | select(.platform=="linux64") | .url') \
    && wget -O /tmp/chromedriver.zip ${CHROME_DRIVER_URL} \
    && unzip /tmp/chromedriver.zip -d /tmp \
    && mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver \
    && rm -rf /tmp/chromedriver.zip /tmp/chromedriver-linux64 \
    && rm -rf /var/lib/apt/lists/*

# --- Fin de la instalación de Chrome ---

# Instala las dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código de tu aplicación al contenedor
COPY . .

# Expone el puerto 8000 para la aplicación Uvicorn
EXPOSE 8000

# Comando para ejecutar la aplicación con Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]