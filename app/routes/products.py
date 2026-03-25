



#Creates products table (if not exist)

def create_products_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            description TEXT NOT NULL,
            price NUMERIC (10, 2) NOT NULL,
            stock_quantity INTEGER NOT NULL
        )
        """
    )

    conn.commit()
    cur.close()
    conn.close()

#Δημιουργία Πίνακα όταν ξεκινάει το app
create_products_table()

#ROOT endpoint
@app.get("/")
def home():
    return {"message": "Warehouse API is running!"}

#CREATE product

@app.post("/products")
def create_product(product: ProductCreate):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO products (name, description, price, stock_quantity)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (product.name,
              product.description,
              product.price,
              product.stock_quantity

        ))

        new_id = cur.fetchone()[0]
        conn.commit()

        cur.close()
        conn.close()

        return{
            "message": "Product created Successfully",
            "product": {
                "id": new_id,
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "stock_quantity": product.stock_quantity
            }
        }
    except pg.Error as e:
        if cur:
            cur.close()
        if conn:
            conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
#READ ALL PRODUCTS
@app.get("/products")
def get_products():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
        SELECT id, name, description, price, stock_quantity
        FROM products
        ORDER BY id DESC
    """)
        rows = cur.fetchall()

        cur.close()
        conn.close()

        products = []

        for row in rows:
            products.append({
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "price": float(row[3]),
                "stock_quantity": row[4]
            })
        return {"products": products}
    except pg.Error as e:
        if cur:
            cur.close()
        if conn:
            conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

#SEARCH PRODUCT
@app.get("/products/search")
def search_products(name: Optional[str]=None, in_stock: Optional[bool]=None):

    try:
        conn = get_connection()
        cur = conn.cursor()

        conditions = []
        values = []

        if name is not None:
            conditions.append("name iLIKE %s")
            values.append(f"%{name}%")
        if in_stock is True:
            conditions.append("stock_quantity > 0")
        if in_stock is False:
            conditions.append("stock_quantity = 0")


        if not conditions:
            query = "SELECT * FROM products ORDER BY id DESC"
        else:
            query = "SELECT * FROM products WHERE  " + " AND ".join(conditions) + "ORDER BY id DESC"

        if values:
            cur.execute(query, tuple(values))
        else:
            cur.execute(query)

        rows = cur.fetchall()

        cur.close()
        conn.close()

        products = []

        for row in rows:
            products.append({
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "price": float(row[3]),
                "stock_quantity": row[4]
            })
        return {"products": products}

    except pg.Error as e:
        if cur:
            cur.close()
        if conn:
            conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


#READ ONE PRODUCT
@app.get("/products/{product_id}")
def get_product(product_id: int):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
        SELECT id , name, description, price, stock_quantity
        FROM products 
        where id = %s
                    """, (product_id,))

        row = cur.fetchone()
        cur.close()
        conn.close()

        if row is None:
            raise HTTPException(status_code=404, detail="Product not found")
        else:
            return {
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "price": float(row[3]),
                "stock_quantity": row[4]
            }
    except pg.Error as e:
        if cur:
            cur.close()
        if conn:
            conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
#UPDATE PRODUCT
@app.put("/products/{product_id}")
def update_product(product_id: int, product: ProductUpdate):
    try:
        conn = get_connection()
        cur = conn.cursor()

        fields = []
        values = []

        if product.name is not None:
            fields.append("name = %s")
            values.append(product.name)
        if product.description is not None:
            fields.append("description = %s")
            values.append(product.description)
        if product.price is not None:
            fields.append("price = %s")
            values.append(product.price)
        if product.stock_quantity is not None:
            fields.append("stock_quantity = %s")
            values.append(product.stock_quantity)

        if not fields:
            raise HTTPException(status_code=400, detail="No fields provided to update")


        sql = f"UPDATE products SET {', '.join(fields)} WHERE id = %s RETURNING *"
        values.append(product_id)

        cur.execute(sql, tuple(values))
        row = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        if row is None:
            raise HTTPException(status_code=404, detail="Product not found")

        return {
            "message": "Product updated successfully",
            "product": {
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "price": float(row[3]),
                "stock_quantity": row[4]
            }
        }
    except pg.Error as e:
        if cur:
            cur.close()
        if conn:
            conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

#DELETE PRODUCT

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            DELETE FROM products 
            WHERE id = %s
            RETURNING *
        
        """, (product_id,))

        row = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        if row is None:
            raise HTTPException(status_code=404, detail="Product not found")

        return {
            "message": "Product deleted successfully",
            "product": {
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "price": float(row[3]),
                "stock_quantity": row[4]
            }
        }
    except pg.Error as e:
        if cur:
            cur.close()
        if conn:
            conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

@app.patch("/products/{product_id}/stock")
def update_stock(product_id:int, stock: StockUpdate):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(f"""
            SELECT * FROM products WHERE id = %s
        """, (product_id,) )
        row = cur.fetchone()

        if row is None:
            cur.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Product not found")

        new_stock = row[4] + stock.change

        if new_stock < 0:
            cur.close()
            conn.close()
            raise HTTPException(status_code=400, detail="Stock cannot be negative")

        cur.execute("""
               UPDATE products
               SET stock_quantity = %s
               WHERE id = %s
               RETURNING *
           """, (new_stock, product_id))

        updated_row = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        return {
            "message": "Stock updated successfully",
            "product": {
                "id": updated_row[0],
                "name": updated_row[1],
                "description": updated_row[2],
                "price": float(updated_row[3]),
                "stock_quantity": updated_row[4]

            }
        }
    except pg.Error as e:
        if cur:
            cur.close()
        if conn:
            conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

@app.get("/products/stats")
def get_stats():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT 
                COUNT(*) AS total_products,
                COUNT(CASE WHEN stock_quantity > 0 THEN 1 END) AS in_stock_products,
                COUNT(CASE WHEN stock_quantity = 0 THEN 1 END) AS out_of_stock_products,
                AVG(price) AS average_price,
                SUM(stock_quantity) AS total_stock_units,
                MAX(price) AS max_price,
                MIN(price) AS min_price
            FROM products;
        """)

        stats = cur.fetchone()
        cur.close()
        conn.close()

        return {
            "total_products": stats[0],
            "in_stock_products": stats[1],
            "out_of_stock_products": stats[2],
            "average_price": float(stats[3]) if stats[3] is not None else 0,
            "total_stock_units": stats[4],
            "max_price": float(stats[5]) if stats[5] is not None else 0,
            "min_price": float(stats[6]) if stats[6] is not None else 0
        }
    except pg.Error as e:
        if cur:
            cur.close()
        if conn:
            conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")