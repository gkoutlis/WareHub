import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import psycopg2 as pg


#FastApi app
app = FastAPI()

#Database settings
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))

#Pydantic class (request body schema)
class SupplierCreate(BaseModel):
    name: str
    email: str
    phone: int
    company_name: str

class SupplierUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[int] = None
    company_name: Optional[str] = None





#Database connection function
def get_connection():
    try:
        conn = pg.connect(
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except pg.Error as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {e}")

#Creates supplier table (if not exist)

def create_suppliers_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS suppliers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email TEXT NOT NULL,
            phone NUMERIC (10) NOT NULL,
            company_name VARCHAR(100) NOT NULL
        )
        """
    )

    conn.commit()
    cur.close()
    conn.close()

#Δημιουργία Πίνακα όταν ξεκινάει το app
create_suppliers_table()

#CREATE SUPPLIER

@app.post("/suppliers")
def create_supplier(supplier: SupplierCreate):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
                INSERT INTO suppliers (name,email,phone,company_name)
                VALUES(%s, %s, %s, %s)
                RETURNING id
                """, (supplier.name,
                      supplier.email,
                      supplier.phone,
                      supplier.company_name
                ))
        
        new_id = cur.fetchone()[0]
        conn.commit()

        cur.close()
        conn.close()

        return{
            "message": "Supplier created successfully",
            "supplier": {
                "id": new_id,
                "name": supplier.name,
                "email": supplier.email,
                "phone": supplier.phone,
                "company_name": supplier.company_name
            }
        }
    except pg.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
    
