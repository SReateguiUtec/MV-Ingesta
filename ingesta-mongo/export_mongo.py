import os
import csv
from pymongo import MongoClient
import boto3
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST_MONGO", "localhost")
DB_PORT = int(os.getenv("DB_PORT_MONGO", 27017))
DB_USER = os.getenv("MONGO_USER", "admin")
DB_PASSWORD = os.getenv("MONGO_PASSWORD", "")
DB_NAME = os.getenv("MONGO_DATABASE", "noticias_db")

S3_BUCKET = os.getenv("S3_RAW_BUCKET", "fintrend-raw-data")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

def export_collection(db, collection_name):
    print(f"Exportando {collection_name} desde MongoDB...")
    collection = db[collection_name]
    cursor = collection.find({})
    rows = list(cursor)
    
    if not rows:
        print(f"La colección {collection_name} está vacía.")
        return None

    keys = set()
    for row in rows:
        keys.update(row.keys())
    
    col_names = list(keys)
    
    filename = f"{collection_name}.csv"
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=col_names)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
        
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
        if DB_USER and DB_PASSWORD:
            uri = f"mongodb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?authSource=admin"
        else:
            uri = f"mongodb://{DB_HOST}:{DB_PORT}/{DB_NAME}"
            
        client = MongoClient(uri)
        db = client[DB_NAME]
        
        filename = export_collection(db, "noticias")
        if filename:
            upload_to_s3(filename, "noticias")
            
        client.close()
        print("Ingesta MongoDB completada.")
    except Exception as e:
        print(f"Error en ingesta MongoDB: {e}")

if __name__ == "__main__":
    main()
