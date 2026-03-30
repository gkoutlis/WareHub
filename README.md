# WareHub CRUD API

## Description

This project is a **Warehouse Management System (WMS)** 🏭 designed as a portfolio-ready backend application. It provides full CRUD (Create, Read, Update, Delete) functionality for managing **products, suppliers, and orders**, including stock management and search capabilities.

### Tech Stack 🛠️
- **Python** 🐍 – core programming language
- **FastAPI** ⚡ – web framework for building REST APIs
- **PostgreSQL** 🐘 – relational database
- **Docker & Docker Compose** 🐳 – containerized development and deployment
- **psycopg2** – PostgreSQL adapter for Python
- **Swagger UI / Postman** 📬 – for API testing

### Features ✨
- **Products** 📦
  - Create, read, update, and delete products
  - Manage stock levels with increment/decrement
  - Search products by name or availability
  - View product statistics (total products, average price)
- **Suppliers** 🏢
  - Create, read, update, and delete suppliers
  - Search suppliers by name or tax ID
- **Orders** 📝
  - Create, read, update, and delete orders
  - Assign orders to products and track order status
  - Order status limited to `pending`, `completed`, or `cancelled`
- **Database Relationships** 🔗
  - Relational design connecting products → suppliers → orders
  - Foreign keys ensure data integrity
- **Seed Data** 🌱
  - Pre-populated database with sample suppliers, products, and orders for testing and demo


---

## Requirements

- Docker 20+
- Docker Compose 1.29+
- Python 3.12+ (for development without Docker)

---


> ⚠️ **Work in Progress:** This project is currently under development.
> Some features may not be fully implemented yet and the API is still being tested.
> Contributions and feedback are welcome.
