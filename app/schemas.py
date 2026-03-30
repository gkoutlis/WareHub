from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

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
    tax_id: str

class SupplierUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    tax_id: Optional[str] = None


#ORDERS

class OrderStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    cancelled = "cancelled"
class OrderCreate(BaseModel):
    customer_name: str
    product_id: int
    quantity: int = Field(gt=0)
    status: OrderStatus = OrderStatus.pending
    

class OrderUpdate(BaseModel):
    customer_name: Optional[str] = None
    product_id: Optional[int] = None
    quantity: Optional[int] = Field(default=None, gt=0) 
    status: Optional[OrderStatus] = None
    

