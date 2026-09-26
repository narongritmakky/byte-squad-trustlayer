from ..db.models import Product

class InsufficientStockError(Exception):
    pass

def reserve_stock(db, product_id: int, quantity: int) -> None:
    """
    NOTE: read-then-write ไม่ atomic — สอง request พร้อมกันอาจทำให้
    สต็อก oversell ได้ (ไม่มี SELECT ... FOR UPDATE)
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise ValueError(f"Product {product_id} not found")

    current_stock = product.stock_quantity
    # BUG #2: ไม่มี row-level lock ระหว่าง read กับ write
    if current_stock < quantity:
        raise InsufficientStockError(
            f"Not enough stock: requested {quantity}, available {current_stock}"
        )
    product.stock_quantity = current_stock - quantity
    db.commit()

def restock(db, product_id: int, quantity: int) -> None:
    # BUG #6: ไม่เช็คว่า quantity > 0 — ค่าติดลบจะไปลดสต็อกแทนที่จะเพิ่ม
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise ValueError(f"Product {product_id} not found")
    product.stock_quantity += quantity
    db.commit()
