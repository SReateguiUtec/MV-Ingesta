import os
import csv
import psycopg2
import boto3
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST_POSTGRES", "localhost")
DB_PORT = int(os.getenv("DB_PORT_POSTGRES", 5432))
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "precios_db")

S3_BUCKET = os.getenv("S3_RAW_BUCKET", "fintrend-raw-data")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

def export_table(conn, table_name):
    print(f"Exportando {table_name} desde PostgreSQL...")
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table_name}")
    rows = cur.fetchall()
    
    if not rows:
        print(f"La tabla {table_name} está vacía.")
        return None

    col_names = [desc[0] for desc in cur.description]
    
    filename = f"{table_name}.csv"
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(col_names)
        writer.writerows(rows)
        
    print(f"Exportado {len(rows)} registros a {filename}")
    return filename

def upload_to_s3(filename, folder):
    # Intentar subir usando IAM Role o credenciales de entorno
    try:
        print(f"Subiendo {filename} a s3://{S3_BUCKET}/{folder}/{filename}...")
        s3_client = boto3.client('s3', region_name=AWS_REGION)
        s3_client.upload_file(filename, S3_BUCKET, f"{folder}/{filename}")
        print("Subida completada.")
    except Exception as e:
        print(f"Error al subir a S3: {e}")

def main():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            dbname=DB_NAME
        )
        
        for table in ["simbolos", "precios_acciones"]:
            filename = export_table(conn, table)
            if filename:
                upload_to_s3(filename, table)
                
        conn.close()
        print("Ingesta PostgreSQL completada.")
    except Exception as e:
        print(f"Error en ingesta PostgreSQL: {e}")

if __name__ == "__main__":
    main()
