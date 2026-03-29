from fastapi import APIRouter, HTTPException
from typing import Optional
from app.database import get_connection
from app.schemas import OrderCreate, OrderUpdate

router = APIRouter(prefix="/orders", tags=["Orders"])

#CREATE ORDER

#READ ALL ORDERS

#SEARCH ORDER

#READ ONE ORDER

#UPDATE ORDER

#DELETE ORDER
