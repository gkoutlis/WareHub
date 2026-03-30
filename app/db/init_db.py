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
            supplier_id INTEGER NOT NULL,
            CONSTRAINT fk_products_supplier
                FOREIGN KEY (supplier_id)
                REFERENCES suppliers(id)
                ON DELETE RESTRICT
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

def create_orders_table():
    conn = get_connection
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE orders (
            id SERIAL PRIMARY KEY,
            customer_name VARCHAR(100) NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL CHECK (quantity > 0),
            status VARCHAR(30) NOT NULL DEFAULT 'pending',
            CHECK (status IN ('pending', 'completed', 'cancelled')),
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT fk_orders_product
                FOREIGN KEY (product_id)
                REFERENCES products(id)
                ON DELETE RESTRICT
        );
                """)

def init_db():
    create_products_table()
    create_suppliers_table()
    create_orders_table()