import os
import csv
import pymysql
import boto3
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST_MYSQL", "localhost")
DB_PORT = int(os.getenv("DB_PORT_MYSQL", 3306))
DB_USER = os.getenv("MYSQL_USER", "root")
DB_PASSWORD = os.getenv("MYSQL_ROOT_PASSWORD", "")
DB_NAME = os.getenv("MYSQL_DATABASE", "portafolio_db")

S3_BUCKET = os.getenv("S3_RAW_BUCKET", "fintrend-raw-data")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

def export_table(conn, table_name):
    print(f"Exportando {table_name} desde MySQL...")
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table_name}")
    rows = cur.fetchall()
    
    if not rows:
        print(f"La tabla {table_name} está vacía.")
        return None

    col_names = [i[0] for i in cur.description]
    
    filename = f"{table_name}.csv"
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(col_names)
        writer.writerows(rows)
        
    print(f"Exportado {len(rows)} registros a {filename}")
    return filename

def upload_to_s3(filename, folder):
    if not os.getenv("AWS_ACCESS_KEY_ID"):
        print(f"Saltando subida a S3 de {filename} (no hay credenciales AWS)")
        return

    print(f"Subiendo {filename} a s3://{S3_BUCKET}/{folder}/{filename}...")
    s3_client = boto3.client('s3', region_name=AWS_REGION)
    s3_client.upload_file(filename, S3_BUCKET, f"{folder}/{filename}")
    print("Subida completada.")

def main():
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            charset='utf8mb4'
        )
        
        for table in ["portafolios", "favoritos"]:
            filename = export_table(conn, table)
            if filename:
                upload_to_s3(filename, "mysql")
                
        conn.close()
        print("Ingesta MySQL completada.")
    except Exception as e:
        print(f"Error en ingesta MySQL: {e}")

if __name__ == "__main__":
    main()
