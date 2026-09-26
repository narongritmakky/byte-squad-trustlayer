from fastapi import FastAPI
from .db.database import engine, Base
from .routers import products, orders, customers

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="InvenTrack",
    description="Lightweight inventory and order management API",
    version="0.1.0",
)

app.include_router(products.router)
app.include_router(orders.router)
app.include_router(customers.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
