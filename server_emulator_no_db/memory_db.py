from datetime import datetime
from decimal import Decimal

db = {
    "order_status": [
        {"id": 1, "status_name": "CREATED"},
        {"id": 2, "status_name": "AWAITING_PAYMENT"},
        {"id": 3, "status_name": "PAID"},
        {"id": 4, "status_name": "PACKING"},
        {"id": 5, "status_name": "SHIPPED"},
        {"id": 6, "status_name": "CANCELLED"},
    ],
    "payment_status": [
        {"id": 1, "status_name": "INITIATED"},
        {"id": 2, "status_name": "CONFIRMED"},
        {"id": 3, "status_name": "FAILED"},
        {"id": 4, "status_name": "REFUNDED"},
    ],
    "warehouse": [],
    "products": [],
    "orders": [],
    "order_items": [],
    "inventory": [],
    "payments": [],
}

counters = {k: 1 for k in db}


def next_id(table: str) -> int:
    val = counters[table]
    counters[table] += 1
    return val


def now():
    return datetime.utcnow()
