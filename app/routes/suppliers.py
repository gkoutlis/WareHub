from fastapi import APIRouter, HTTPException
from typing import Optional
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
            INSERT INTO suppliers (name, email, phone, tax_id)
            VALUES (%s, %s, %s, %s)
            RETURNING id, name, email, phone, tax_id
            """,
            (
                supplier.name,
                supplier.email,
                supplier.phone,
                supplier.tax_id,
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
                "tax_id": new_supplier[4],
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
    
#READ ALL SUPPLIERS
@router.get("/suppliers")
def get_suppliers():
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT id, name, email, phone, tax_id
            FROM suppliers
            ORDER BY id DESC
    """)
        
        rows = cur.fetchall()

        suppliers = []

        for row in rows :
            suppliers.append({
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "phone": row[3],
                "tax_id": row[4]
            })
        return {"suppliers":suppliers}
    except Exception as e:
        
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

#SEARCH SUPPLIER
@router.get("/suppliers/search")
def search_supplier(name: Optional[str]=None, tax_id: Optional[str]=None):
    conn = None
    cur = None
    try:
        if not name and not tax_id:
            raise HTTPException(status_code=400, detail="Provide at least one search parameter")
        
        conn = get_connection()
        cur = conn.cursor()
        
        query = """
            SELECT id, name, email, phone, tax_id
            FROM suppliers
            WHERE 1=1
            """
        params = []

        if name:
            query += " AND name ILIKE %s"
            params.append(f"%{name}%")

        if tax_id:
            query += " AND tax_id = %s"
            params.append(tax_id)

        cur.execute(query, tuple(params))
        rows = cur.fetchall()

        suppliers = []

        for row in rows:
            suppliers.append({
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "phone": row[3],
                "tax_id": row[4]
            })
        return {"suppliers": suppliers}

    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
        




#READ ONE SUPPLIER
@router.get("/suppliers/{supplier_id}")
def get_supplier(supplier_id: int):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
        SELECT id , name, email, phone, tax_id
        FROM suppliers 
        where id = %s
                    """, (supplier_id,))

        row = cur.fetchone()
        

        if row is None:
            raise HTTPException(status_code=404, detail="Product not found")
        else:
            return {
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "phone": float(row[3]),
                "tax_id": row[4]
            }
    except Exception as e:
        if cur:
            cur.close()
        if conn:
            conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

#UPDATE SUPPLIER
@router.put("/supplier/{supplier_id}")
def update_supplier(supplier_id: int, supplier: SupplierUpdate):
    try:
        conn = get_connection()
        cur = conn.cursor()

        fields = []
        values = []

        if supplier.name is not None:
            fields.routerend("name = %s")
            values.routerend(supplier.name)
        if supplier.description is not None:
            fields.routerend("description = %s")
            values.routerend(supplier.description)
        if supplier.price is not None:
            fields.routerend("price = %s")
            values.routerend(supplier.price)
        if supplier.stock_quantity is not None:
            fields.routerend("stock_quantity = %s")
            values.routerend(supplier.stock_quantity)

        if not fields:
            raise HTTPException(status_code=400, detail="No fields provided to update")


        sql = f"UPDATE suppliers SET {', '.join(fields)} WHERE id = %s RETURNING *"
        values.routerend(supplier_id)

        cur.execute(sql, tuple(values))
        row = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        if row is None:
            raise HTTPException(status_code=404, detail="supplier not found")

        return {
            "message": "supplier updated successfully",
            "supplier": {
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "phone": float(row[3]),
                "tax_id": row[4]
            }
        }
    except Exception as e:
        if cur:
            cur.close()
        if conn:
            conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    
#DELETE supplier
@router.delete("/suppliers/{supplier_id}")
def delete_supplier(supplier_id: int):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            DELETE FROM suppliers
            WHERE id = %s
            RETURNING *
        """, (supplier_id,))

        row = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        if row is None:
            raise HTTPException(status_code=404, detail="supplier not found")

        return {
            "message": "Supplier deleted successfully",
            "supplier": {
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "phone": float(row[3]),
                "tax_id": row[4]
            }
        }
    except Exception as e:
        if cur:
            cur.close()
        if conn:
            conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
        

    

    

