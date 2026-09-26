from ..db.models import Order, OrderItem, Product, Customer
from . import inventory_service, pricing_service

def create_order(db, customer_id: int, items: list, discount_pct: float = 0.0) -> Order:
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise ValueError(f"Customer {customer_id} not found")

    order = Order(customer_id=customer_id, status="pending")
    db.add(order)
    db.flush()  # ได้ order.id ก่อนเพิ่ม items

    line_totals = []
    for item in items:
        product = db.query(Product).filter(Product.id == item["product_id"]).first()
        if not product:
            raise ValueError(f"Product {item['product_id']} not found")

        try:
            inventory_service.reserve_stock(db, product.id, item["quantity"])
        except Exception:
            # BUG #7: bare except กลืนทั้ง InsufficientStockError, ValueError,
            # และ DB error อื่นๆ ไปหมด — caller ไม่รู้เลยว่าทำไม item ถูก skip
            # และ order ที่ถูก add ไปแล้วก็ไม่ถูก rollback เหลือค้างเป็น "pending"
            continue

        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=item["quantity"],
            unit_price_at_purchase=product.unit_price,
        )
        db.add(order_item)
        line_totals.append(
            pricing_service.calculate_line_total(product.unit_price, item["quantity"])
        )

    pricing_service.calculate_order_total(line_totals, discount_pct=discount_pct)
    order.status = "confirmed"
    db.commit()
    db.refresh(order)
    return order
