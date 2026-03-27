from fastapi import APIRouter, HTTPException
from typing import Optional
from app.database import get_connection
from app.schemas import SupplierCreate, SupplierUpdate

router = APIRouter(prefix="/suppliers", tags=["Suppliers"])

#CREATE ORDER
