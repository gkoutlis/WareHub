-- ===========================
-- WareHub Seed Data
-- ===========================

-- =====================================
-- 1. Suppliers
-- =====================================
INSERT INTO suppliers (name, contact_email, phone_number)
VALUES
('Acme Electronics', 'sales@acme.com', '2101234567'),
('Global Gadgets', 'info@globalgadgets.com', '2102345678'),
('TechNova', 'contact@technova.com', '2103456789'),
('Smart Solutions', 'support@smartsolutions.com', '2104567890'),
('Green Supplies', 'hello@greensupplies.com', '2105678901'),
('DigitalWorld', 'sales@digitalworld.com', '2106789012'),
('FutureTech', 'contact@futuretech.com', '2107890123'),
('Alpha Industries', 'info@alphaindustries.com', '2108901234'),
('Omega Electronics', 'sales@omega.com', '2109012345'),
('NextGen Components', 'contact@nextgen.com', '2100123456');

-- =====================================
-- 2. Products
-- =====================================
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

-- =====================================
-- 3. Orders
-- =====================================
-- Status can be 'pending', 'completed', 'cancelled'
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

-- =====================================
-- End of Seed
-- =====================================