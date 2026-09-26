from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ProductBase(BaseModel):
    sku: str = Field(..., min_length=1, max_length=64)
    name: str = Field(..., min_length=1, max_length=200)
    unit_price: float = Field(..., gt=0)
    stock_quantity: int = Field(default=0, ge=0)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    unit_price: Optional[float] = None

class ProductOut(ProductBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
