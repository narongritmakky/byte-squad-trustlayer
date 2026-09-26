from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)

class OrderCreate(BaseModel):
    customer_id: int
    items: List[OrderItemCreate]
    discount_pct: float = Field(default=0.0, ge=0.0, le=1.0)

class OrderItemOut(BaseModel):
    product_id: int
    quantity: int
    unit_price_at_purchase: float

    class Config:
        from_attributes = True

class OrderOut(BaseModel):
    id: int
    customer_id: int
    status: str
    created_at: datetime
    items: List[OrderItemOut]

    class Config:
        from_attributes = True
