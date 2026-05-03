# FinTrend - Módulo de Ingesta (MV-Ingesta) 🚀

Este repositorio contiene el motor de extracción y carga (ETL) del sistema FinTrend. Su función es extraer datos de múltiples fuentes de base de datos y cargarlos en un Data Lake en Amazon S3 para su posterior análisis con AWS Athena.

## 📋 Arquitectura de Ingesta

El módulo está diseñado para ejecutarse en una instancia EC2 dentro de AWS, utilizando Docker para orquestar los procesos de extracción:

1.  **MySQL (Portafolios):** Extrae tablas de usuarios y favoritos.
2.  **PostgreSQL (Mercado):** Extrae símbolos y precios históricos de acciones.
3.  **MongoDB (Noticias):** Extrae colecciones de noticias y sentimiento de mercado.
4.  **Carga (S3):** Los datos se convierten a formato CSV y se suben a S3 utilizando **IAM Roles / LabRole** para seguridad sin llaves manuales.

## 🛠️ Tecnologías

- **Python 3.9+**: Lógica principal de los scripts de ingesta.
- **Docker & Docker Compose**: Contenedores para aislamiento de tareas.
- **Boto3**: SDK de AWS para la integración con S3.
- **PyMySQL, Psycopg2, PyMongo**: Drivers para conexión a bases de datos.

## ⚙️ Configuración (.env)

El sistema requiere las siguientes variables de entorno para funcionar (configuradas automáticamente por CloudFormation):

```env
# Bases de Datos
DB_HOST_MYSQL=xxx.xxx.xxx.xxx
MYSQL_DATABASE=portafolio_db
MYSQL_ROOT_PASSWORD=xxx

DB_HOST_POSTGRES=xxx.xxx.xxx.xxx
DB_NAME=precios_db
POSTGRES_PASSWORD=xxx

DB_HOST_MONGO=xxx.xxx.xxx.xxx
MONGO_DATABASE=noticias_db

# AWS Infra
S3_RAW_BUCKET=fintrend-raw-data-xxxx
AWS_REGION=us-east-1
```

## 🚀 Ejecución

Para iniciar el proceso de ingesta manualmente:

```bash
docker compose up -d --build
```

Los contenedores se ejecutarán, procesarán los datos y se detendrán automáticamente (`Exited 0`) al completar la subida a S3.

## 📊 Integración con Data Lake

Una vez que los datos están en S3, el **AWS Glue Crawler** escanea los archivos para poblar el Catálogo de Datos, permitiendo que el servicio de Analítica ejecute consultas SQL complejas sobre archivos CSV.

---
**Desarrollado para el curso de Cloud Computing**
