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

def get_connection():
    try:
        conn = pg.connect(
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=int(DB_PORT)
        )
        return conn
    except pg.Error as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {e}")