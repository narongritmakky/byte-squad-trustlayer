def calculate_line_total(unit_price: float, quantity: int) -> float:
    return unit_price * quantity  # BUG #4: float arithmetic กับเงิน

def calculate_order_total(line_totals: list, discount_pct: float = 0.0,
                            tax_pct: float = 0.07) -> float:
    subtotal = sum(line_totals)
    # BUG #5: คิด tax ก่อน discount — ทำให้ discount มีผลมากเกินจริง
    # ที่ถูกต้องคือ apply discount ก่อน แล้วคิด tax จากยอดหลังหักส่วนลด
    with_tax = subtotal * (1 + tax_pct)
    final_total = with_tax * (1 - discount_pct)
    return round(final_total, 2)
