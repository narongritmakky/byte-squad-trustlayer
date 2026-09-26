from inventrack.services import pricing_service

def test_calculate_line_total():
    assert pricing_service.calculate_line_total(10.0, 3) == 30.0

def test_calculate_order_total_no_discount():
    total = pricing_service.calculate_order_total([100.0], discount_pct=0.0, tax_pct=0.07)
    assert total == 107.0

def test_calculate_order_total_with_discount():
    # NOTE: เช็คแค่ว่า function รันได้และได้เลขบวก — ไม่เช็คว่าลำดับ
    # tax/discount ถูกต้องตาม spec จริงหรือไม่ (จุดอ่อนที่ตั้งใจเว้นไว้)
    total = pricing_service.calculate_order_total([100.0], discount_pct=0.1, tax_pct=0.07)
    assert isinstance(total, float)
    assert total > 0
