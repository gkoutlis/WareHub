from app.database import get_connection

def create_products_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            description TEXT NOT NULL,
            price NUMERIC(10, 2) NOT NULL,
            stock_quantity INTEGER NOT NULL
        )
    """)

    conn.commit()
    cur.close()
    conn.close()

def create_suppliers_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS suppliers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100),
            phone VARCHAR(20),
            tax_id VARCHAR(9) UNIQUE NOT NULL
        )
    """)

    conn.commit()
    cur.close()
    conn.close()

def init_db():
    create_products_table()
    create_suppliers_table()