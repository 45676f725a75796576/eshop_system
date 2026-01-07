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
    "warehouse": [{"id": 1, "warehouse_name":'Main Warehouse', "location_code":'WH-PRG-01', "is_active":1},{"id": 2, "warehouse_name":'Secondary Warehouse', "location_code":'WH-BRN-01', "is_active":0}],
    "products": [{"id": 1, "product_name":'Laptop', "unit_price":25000.00, "tax_rate":0.21}],
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
