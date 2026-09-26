def test_create_and_get_product(client):
    response = client.post(
        "/products/",
        json={"sku": "SKU-100", "name": "Test Product", "unit_price": 19.99, "stock_quantity": 50},
    )
    assert response.status_code == 200
    product_id = response.json()["id"]

    get_response = client.get(f"/products/{product_id}")
    assert get_response.status_code == 200
    assert get_response.json()["sku"] == "SKU-100"

def test_list_products_page_one(client):
    for i in range(3):
        client.post(
            "/products/",
            json={"sku": f"SKU-20{i}", "name": f"Product {i}", "unit_price": 5.0, "stock_quantity": 10},
        )
    response = client.get("/products/?page=1&limit=10")
    assert response.status_code == 200
    # ไม่มี assertion เช็คจำนวน item ที่คืนมา — เผลอ ๆ test นี้ผ่านได้เสมอ
    # ทั้งที่ pagination พังอยู่ (BUG #1) นี่คือ "false sense of safety"
    # ที่ตั้งใจปล่อยไว้ให้ reviewer ต้องจับได้เอง
