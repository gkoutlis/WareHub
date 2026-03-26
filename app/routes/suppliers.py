from fastapi import APIRouter, HTTPException
from app.database import get_connection
from app.schemas import SupplierCreate, SupplierUpdate

router = APIRouter(prefix="/suppliers", tags=["Suppliers"])

#CREATE SUPPLIER

@router.post("/suppliers")
def create_supplier(supplier: SupplierCreate):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            INSERT INTO suppliers (name, email, phone, company_name)
            VALUES (%s, %s, %s, %s)
            RETURNING id, name, email, phone, company_name
            """,
            (
                supplier.name,
                supplier.email,
                supplier.phone,
                supplier.company_name,
            ),
        )

        new_supplier = cur.fetchone()
        conn.commit()

        return {
            "message": "Supplier created successfully",
            "supplier": {
                "id": new_supplier[0],
                "name": new_supplier[1],
                "email": new_supplier[2],
                "phone": new_supplier[3],
                "company_name": new_supplier[4],
            },
        }
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
    
