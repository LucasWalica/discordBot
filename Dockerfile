FROM python:3.12

WORKDIR /code

# Copiar el archivo requirements.txt y ejecutar la instalación de dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto (esto incluye entrypoint.sh)
COPY . .

# Hacer que el script entrypoint.sh sea ejecutable
RUN chmod +x ./entrypoint.sh

# Establecer entrypoint para que se ejecute cuando el contenedor arranque
ENTRYPOINT ["./entrypoint.sh"]

# Por último, el comando por defecto (podría ser sobrescrito en docker-compose)
CMD ["python", "bot_discord/bot.py"]
