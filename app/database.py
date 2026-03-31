import os
import psycopg2 as pg
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

if DB_PORT is None:
    raise ValueError("DB_PORT is missing from environment variables")

import time
import psycopg2 as pg
from fastapi import HTTPException

def get_connection():
    retries = 5
    while retries > 0:
        try:
            conn = pg.connect(
                dbname="warehub_db",
                user="postgres",
                password="1234",
                host="db",
                port=5432
            )
            return conn
        except Exception as e:
            retries -= 1
            print(f"Database not ready, retrying... ({5 - retries}/5)")
            time.sleep(3)
    raise HTTPException(status_code=500, detail="Database connection failed after retries")