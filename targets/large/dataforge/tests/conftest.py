import pytest
from fastapi.testclient import TestClient
from dataforge.api.app import app

@pytest.fixture()
def client():
    return TestClient(app)

@pytest.fixture()
def sample_records():
    return [
        {"id": 1, "region": "US", "amount": 100.0},
        {"id": 2, "region": "EU", "amount": 200.0},
        {"id": 3, "region": "US", "amount": None},
    ]
