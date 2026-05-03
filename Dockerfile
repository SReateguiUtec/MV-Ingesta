FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar scripts
COPY ingesta-mysql ./ingesta-mysql
COPY ingesta-pg ./ingesta-pg
COPY ingesta-mongo ./ingesta-mongo

# El comando especifico se sobrescribe en el docker-compose.yml
CMD ["python", "--version"]
