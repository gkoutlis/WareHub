from pydantic import BaseModel
from typing import Optional

# PRODUCTS
class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    stock_quantity: int
    supplier_id: int

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None
    supplier_id: Optional[int] =None
class StockUpdate(BaseModel):
    change: int

# SUPPLIERS
class SupplierCreate(BaseModel):
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    tax_id: Optional[int] = None

class SupplierUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    tax_id: Optional[int] = None


#ORDERS
class OrderCreate(BaseModel):
    customer_name: str
    product_id: Optional[int] = None
    quantity: Optional[int] = None
    status: Optional[str] = None
    created_at: Optional[str] = None

class OrderUpdate(BaseModel):
    customer_name: str
    product_id: Optional[int] = None
    quantity: Optional[int] = None
    status: Optional[str] = None
    created_at: Optional[str] = None