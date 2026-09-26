# InvenTrack

A lightweight inventory and order management system built with FastAPI and SQLAlchemy.

## Features
- Product catalog management (CRUD)
- Customer management
- Order creation with automatic stock reservation
- Basic pricing engine with tax and discount support
- CLI for restocking operations

## Setup

    pip install -r requirements.txt
    uvicorn inventrack.main:app --reload

## Running Tests

    pytest

## CLI Usage

    python -m inventrack.cli restock <product_id> <quantity>

## License
MIT — see LICENSE file.
