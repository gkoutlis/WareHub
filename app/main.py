from fastapi import FastAPI

from routes.products import router as products_router
from routes.suppliers import router as suppliers_router
from routes.orders import router as orders_router
from db.init_db import init_db

app = FastAPI(title="WareHub API")


@app.on_event("startup")
def startup_event():
    init_db()


@app.get("/")
def root():
    return {"message": "WareHub API is running"}


app.include_router(products_router)
app.include_router(suppliers_router)
app.include_router(orders_router)