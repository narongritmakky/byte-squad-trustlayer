from sqlalchemy import text

def search_products_by_name(db, name_query: str):
    # BUG #3 (CRITICAL): string interpolation ตรงเข้า SQL —
    # input เช่น "x'; DROP TABLE products; --" จะทำลาย query ได้ทันที
    query = f"SELECT * FROM products WHERE name LIKE '%{name_query}%'"
    return db.execute(text(query)).fetchall()
