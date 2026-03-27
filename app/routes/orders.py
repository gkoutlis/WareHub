from fastapi import APIRouter, HTTPException
from typing import Optional
from app.database import get_connection
from app.schemas import SupplierCreate, SupplierUpdate

router = APIRouter(prefix="/orders", tags=["Orders"])

#CREATE ORDER

#READ ALL ORDERS

#SEARCH ORDER

#READ ONE ORDER

#UPDATE ORDER

#DELETE ORDER
