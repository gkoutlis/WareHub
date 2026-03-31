from database import get_connection

def create_products_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            description TEXT NOT NULL,
            price NUMERIC(10, 2) NOT NULL,
            stock_quantity INTEGER NOT NULL,
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
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
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
    conn.commit()
    cur.close()
    conn.close()
    
def seed_suppliers():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM suppliers;")
    count = cur.fetchone()[0]

    if count == 0:

        cur.execute("""
                INSERT INTO suppliers (name, email, phone, tax_id)
                VALUES
                ('Acme Electronics', 'sales@acme.com', '2101234567', '123456789'),
                ('Global Gadgets', 'info@globalgadgets.com', '2102345678', '234567891'),
                ('TechNova', 'contact@technova.com', '2103456789', '345678912'),
                ('Smart Solutions', 'support@smartsolutions.com', '2104567890', '456789123'),
                ('Green Supplies', 'hello@greensupplies.com', '2105678901', '567891234'),
                ('DigitalWorld', 'sales@digitalworld.com', '2106789012', '678912345'),
                ('FutureTech', 'contact@futuretech.com', '2107890123', '789123456'),
                ('Alpha Industries', 'info@alphaindustries.com', '2108901234', '891234567'),
                ('Omega Electronics', 'sales@omega.com', '2109012345', '912345678'),
                ('NextGen Components', 'contact@nextgen.com', '2100123456', '102345679');
                    """)
    conn.commit()
    cur.close()
    conn.close()

def seed_products():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM products;")
    count = cur.fetchone()[0]

    if count == 0:
        cur.execute("""
            INSERT INTO products (name, description, price, stock_quantity, supplier_id)
            VALUES
            ('Wireless Mouse', 'Ergonomic wireless mouse', 25.99, 100, 1),
            ('Mechanical Keyboard', 'RGB mechanical keyboard', 89.50, 50, 2),
            ('HD Webcam', '1080p webcam with mic', 45.00, 70, 3),
            ('USB-C Hub', 'Multiport USB-C hub', 29.99, 120, 4),
            ('External SSD 1TB', 'Fast external SSD', 150.00, 30, 5),
            ('Gaming Headset', 'Surround sound gaming headset', 75.00, 40, 6),
            ('Portable Charger', '10000mAh power bank', 35.00, 80, 7),
            ('Smartwatch', 'Fitness tracker smartwatch', 120.00, 25, 8),
            ('Wireless Earbuds', 'Bluetooth earbuds with case', 60.00, 60, 9),
            ('Laptop Stand', 'Adjustable aluminum stand', 40.00, 90, 10);
        """)

    conn.commit()
    cur.close()
    conn.close()


def seed_orders():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM orders;")
    count = cur.fetchone()[0]

    if count == 0:
        cur.execute("""
            INSERT INTO orders (customer_name, product_id, quantity, status)
            VALUES
            ('John Doe', 1, 2, 'pending'),
            ('Jane Smith', 3, 1, 'completed'),
            ('Michael Brown', 5, 1, 'completed'),
            ('Emily Davis', 2, 1, 'cancelled'),
            ('David Wilson', 4, 3, 'pending'),
            ('Sarah Johnson', 6, 2, 'completed'),
            ('Chris Lee', 7, 1, 'pending'),
            ('Anna White', 8, 1, 'pending'),
            ('James Martin', 9, 2, 'completed'),
            ('Laura Scott', 10, 1, 'pending');
        """)

    conn.commit()
    cur.close()
    conn.close()


def init_db():
    create_suppliers_table()
    create_products_table()
    create_orders_table()

    seed_suppliers()
    seed_products()
    seed_orders()