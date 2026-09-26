from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..db.models import Order
from ..schemas.order import OrderCreate, OrderOut
from ..services import order_service

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=OrderOut)
def create_order(payload: OrderCreate, db: Session = Depends(get_db)):
    try:
        order = order_service.create_order(
            db,
            customer_id=payload.customer_id,
            items=[item.model_dump() for item in payload.items],
            discount_pct=payload.discount_pct,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return order

@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.get("/", response_model=list[OrderOut])
def list_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()
