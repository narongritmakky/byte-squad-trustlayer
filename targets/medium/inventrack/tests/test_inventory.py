import pytest
from inventrack.db.models import Product
from inventrack.services import inventory_service

def test_reserve_stock_success(db_session):
    product = Product(sku="SKU-1", name="Widget", unit_price=9.99, stock_quantity=10)
    db_session.add(product)
    db_session.commit()

    inventory_service.reserve_stock(db_session, product.id, 4)
    db_session.refresh(product)
    assert product.stock_quantity == 6

def test_reserve_stock_insufficient(db_session):
    product = Product(sku="SKU-2", name="Gadget", unit_price=5.0, stock_quantity=2)
    db_session.add(product)
    db_session.commit()

    with pytest.raises(inventory_service.InsufficientStockError):
        inventory_service.reserve_stock(db_session, product.id, 5)
