CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    price NUMERIC(10,2),
    stock_quantity INT
);

INSERT INTO products (name, description, price, stock_quantity) VALUES
('Apple MacBook Pro 16', 'Laptop με Apple M2 Pro, 16GB RAM, 512GB SSD', 2499.99, 10),
('Dell XPS 13', 'Ultrabook με Intel i7, 16GB RAM, 512GB SSD', 1499.99, 15),
('HP Spectre x360', '2-in-1 Laptop με Intel i7, 16GB RAM, 1TB SSD', 1699.99, 8),
('Samsung Galaxy S23', 'Smartphone 256GB, 8GB RAM, AMOLED display', 899.99, 25),
('iPhone 15 Pro', 'Apple iPhone 15 Pro 128GB, A17 chip, OLED display', 1199.99, 20),
('Sony WH-1000XM5', 'Ασύρματα ακουστικά με Noise Cancelling', 399.99, 30),
('Logitech MX Master 3', 'Επαγγελματικό ασύρματο ποντίκι', 99.99, 50),
('Razer BlackWidow V3', 'Gaming keyboard με RGB φωτισμό', 149.99, 20),
('Samsung 34'' Curved Monitor', 'Ultra-wide monitor για επαγγελματική χρήση', 599.99, 12),
('NVIDIA RTX 4070 Ti', 'Κάρτα γραφικών υψηλής απόδοσης για gaming και AI', 899.99, 5),
('Intel Core i9-14900K', 'CPU για high-end desktops, 24 cores', 799.99, 7),
('Corsair Vengeance 32GB', 'RAM DDR5 6000MHz για gaming και επαγγελματικά PCs', 199.99, 25),
('Samsung 2TB NVMe SSD', 'Υψηλής ταχύτητας αποθήκευση για PC/Laptop', 249.99, 18),
('Apple iPad Pro 12.9', 'Tablet με M2 chip, 256GB, Liquid Retina XDR', 1099.99, 15),
('Amazon Echo Dot (5th Gen)', 'Smart speaker με Alexa', 49.99, 40),
('Google Nest Hub 2', 'Smart display για σπίτι με Google Assistant', 99.99, 25),
('DJI Mini 4 Drone', 'Φορητό drone με 4K camera', 499.99, 10),
('GoPro HERO12 Black', 'Action camera με 5K video recording', 449.99, 15),
('Microsoft Surface Laptop 5', 'Laptop με Intel i7, 16GB RAM, 512GB SSD', 1299.99, 8),
('Anker PowerCore 20000', 'Power bank 20000mAh για γρήγορη φόρτιση', 49.99, 35);