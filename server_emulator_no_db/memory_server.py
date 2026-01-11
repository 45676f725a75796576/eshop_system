from flask import Flask, abort, jsonify, request, g
from flask_cors import CORS
import secrets
from copy import deepcopy

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# -------------------- in-memory storage --------------------
loggedUsers = []

db = {
    "orders": {1: {
        "id": 1,
        "id_user": 1,
        "status": "CREATED",
        "total_amount": 0,
        "unit_price": 0,
        "tax_rate": 0,
        "currency": "CZK",
        "payment_status": "INITIATED",
        "warehouse_id": 1,
        "shipping_address": "Armenska 2673, Kladno 27201",
        "billing_address": "Armenska 2673, Kladno 27201",
        "created_at": "2025-12-23T00:00:00",
        "updated_at": "2025-12-23T00:00:00"
    }},        # dict: order_id -> order
    "order_items": {1: {
        "id": 1,
        "order_id": 1,
        "product_id": 1,
        "quantity": 1
    }},   # dict: item_id -> item
    "products": {1: {"id": 1, "product_name": "ThinkPad X270", "unit_price": 1700, "tax_rate": 0.21}},      # dict: product_id -> product
    "warehouses": {1: {"id": 1, "warehouse_name": "Main", "location_code": "PRG1", "is_active": True}}, 
    "inventory": {1: {"id": 1,"warehouse_id": 1, "product_id": 1, "quantity_available": 30, "quantity_reserved": 5}},
    "payments": {},
}


counters = {
    "orders": 2,
    "order_items": 2,
    "products": 2,
    "warehouses": 2,
    "inventory": 2,
    "payments": 1
}

order_status_lookup = ["CREATED", "AWAITING_PAYMENT", "PAID", "PACKING", "SHIPPED", "CANCELLED"]
payment_status_lookup = ["INITIATED", "CONFIRMED", "FAILED", "REFUNDED"]

# -------------------- helper functions --------------------
def next_id(table):
    i = counters[table]
    counters[table] += 1
    return i

def get_order(order_id):
    return db["orders"].get(order_id)

def get_inventory_item(item_id):
    return db["inventory"].get(item_id)

def get_product(product_id):
    return db["products"].get(product_id)

def get_warehouse(warehouse_id):
    return db["warehouses"].get(warehouse_id)

# -------------------- orders --------------------
@app.route("/orders", methods=["POST"])
def create_order():
    data = request.json
    order_id = next_id("orders")
    order = {
        "id": order_id,
        "id_user": data["user_id"],
        "status": "CREATED",
        "total_amount": 0,
        "unit_price": 0,
        "tax_rate": 0,
        "currency": data["currency"],
        "payment_status": "INITIATED",
        "warehouse_id": 1,
        "shipping_address": data["shipping_address"],
        "billing_address": data["billing_address"],
        "created_at": "2025-12-23T00:00:00",
        "updated_at": "2025-12-23T00:00:00"
    }
    db["orders"][order_id] = order
    return jsonify({"status": "created", "order_id": order_id}), 201

@app.route("/orders/<int:order_id>", methods=["GET"])
def get_order_route(order_id):
    order = get_order(order_id)
    if not order:
        abort(404)
    return jsonify(order)

@app.route("/orders/<int:order_id>", methods=["PUT"])
def update_order(order_id):
    order = get_order(order_id)
    if not order:
        abort(404)
    order.update(request.json)
    return jsonify({"status": "updated"})

@app.route("/orders/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
    if order_id in db["orders"]:
        del db["orders"][order_id]
    return jsonify({"status": "deleted"})

@app.route("/orders/all", methods=["GET"])
def get_all_orders():
    return jsonify(list(db["orders"].values()))

# -------------------- order items --------------------
@app.route("/orders/<int:order_id>/items", methods=["POST"])
def add_item_to_order(order_id):
    order = get_order(order_id)
    if not order:
        abort(404)
    data = request.json
    item_id = next_id("order_items")
    item = {
        "id": item_id,
        "order_id": order_id,
        "product_id": data["product_id"],
        "quantity": data["quantity"]
    }
    db["order_items"][item_id] = item
    return jsonify(item)

@app.route("/orders/<int:order_id>/items", methods=["DELETE"])
def remove_item_from_order(order_id):
    data = request.json
    items_to_delete = [k for k, v in db["order_items"].items()
                       if v["order_id"] == order_id and v.get("product_name") == data.get("name")]
    for k in items_to_delete:
        del db["order_items"][k]
    return jsonify({"deleted": len(items_to_delete)})

@app.route("/orders/<int:order_id>/items", methods=["GET"])
def get_all_items_from_order(order_id):
    items = [v for v in db["order_items"].values() if v["order_id"] == order_id]
    return jsonify(items)

# -------------------- products --------------------
@app.route("/products", methods=["POST"])
def create_product():
    data = request.json
    product_id = next_id("products")
    product = {
        "id": product_id,
        "product_name": data["product_name"],
        "unit_price": data["unit_price"],
        "tax_rate": data["tax_rate"]
    }
    db["products"][product_id] = product
    return jsonify({"status": "created"}), 201

@app.route("/products/<int:product_id>", methods=["GET"])
def get_product_route(product_id):
    product = get_product(product_id)
    if not product:
        abort(404)
    return jsonify(product)

@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    product = get_product(product_id)
    if not product:
        abort(404)
    product.update(request.json)
    return jsonify({"status": "updated"})

@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    if product_id in db["products"]:
        del db["products"][product_id]
    return jsonify({"status": "deleted"})

@app.route("/products", methods=["GET"])
def list_products():
    return jsonify(list(db["products"].values()))

@app.route("/products/all", methods=["GET"])
def get_all_products():
    return jsonify(list(db["products"].values()))

# -------------------- warehouses --------------------
@app.route("/warehouses", methods=["POST"])
def create_warehouse():
    data = request.json
    warehouse_id = next_id("warehouses")
    warehouse = {
        "id": warehouse_id,
        "warehouse_name": data["warehouse_name"],
        "location_code": data["location_code"],
        "is_active": data["is_active"]
    }
    db["warehouses"][warehouse_id] = warehouse
    return jsonify({"status": "created"}), 201

@app.route("/warehouses/<int:warehouse_id>", methods=["GET"])
def get_warehouse_route(warehouse_id):
    wh = get_warehouse(warehouse_id)
    if not wh:
        abort(404)
    return jsonify(wh)

@app.route("/warehouses/<int:warehouse_id>", methods=["PUT"])
def update_warehouse(warehouse_id):
    wh = get_warehouse(warehouse_id)
    if not wh:
        abort(404)
    wh.update(request.json)
    return jsonify({"status": "updated"})

@app.route("/warehouses/<int:warehouse_id>", methods=["DELETE"])
def delete_warehouse(warehouse_id):
    if warehouse_id in db["warehouses"]:
        del db["warehouses"][warehouse_id]
    return jsonify({"status": "deleted"})

@app.route("/warehouses", methods=["GET"])
def list_warehouses():
    return jsonify(list(db["warehouses"].values()))

@app.route("/warehouses/all", methods=["GET"])
def get_all_warehouses():
    return jsonify(list(db["warehouses"].values()))

# -------------------- inventory --------------------
@app.route("/inventory", methods=["POST"])
def create_inventory():
    data = request.json
    item_id = next_id("inventory")
    item = {
        "id": item_id,
        "warehouse_id": data["warehouse_id"],
        "product_id": data["product_id"],
        "quantity_available": data["quantity_available"],
        "quantity_reserved": data.get("quantity_reserved", 0)
    }
    db["inventory"][item_id] = item
    return jsonify({"status": "created"}), 201

@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_inventory_route(item_id):
    item = get_inventory_item(item_id)
    if not item:
        abort(404)
    return jsonify(item)

@app.route("/inventory/<int:item_id>", methods=["PUT"])
def update_inventory_route(item_id):
    item = get_inventory_item(item_id)
    if not item:
        abort(404)
    item.update(request.json)
    return jsonify({"status": "updated"})

@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_inventory_route(item_id):
    if item_id in db["inventory"]:
        del db["inventory"][item_id]
    return jsonify({"status": "deleted"})

@app.route("/inventory/all", methods=["GET"])
def list_inventory():
    return jsonify(list(db["inventory"].values()))

@app.route("/inventory/warehouse/<int:warehouse_id>", methods=["GET"])
def list_inventory_by_warehouse(warehouse_id):
    items = [v for v in db["inventory"].values() if v["warehouse_id"] == warehouse_id]
    return jsonify(items)

@app.route("/inventory/product/<int:product_id>", methods=["GET"])
def list_inventory_by_product(product_id):
    items = [v for v in db["inventory"].values() if v["product_id"] == product_id]
    return jsonify(items)

# -------------------- payments --------------------
@app.route("/payments", methods=["POST"])
def create_payment():
    data = request.json
    payment_id = next_id("payments")
    payment = {
        "id": payment_id,
        "order_id": data["order_id"],
        "payment_provider": data["payment_provider"],
        "provider_transaction_id": data["provider_transaction_id"]
    }
    db["payments"][payment_id] = payment
    return jsonify({"status": "created"}), 201

# -------------------- reports --------------------
from collections import defaultdict
from datetime import datetime

# ==========================
# Sales report
# ==========================
@app.route("/report/sales", methods=["GET"])
def report_sales():
    sales_report = []

    # Group order items by order_id
    items_by_order = defaultdict(list)
    for item in db["order_items"].values():
        items_by_order[item["order_id"]].append(item)

    for k, order in db["orders"].items():
        order_id = order["id"]
        items = items_by_order[order_id]

        total_items = sum(item["quantity"] for item in items)
        total_amount_calculated = sum(item["unit_price"] * item["quantity"] * (1 + item.get("tax_rate", 0.21)) for item in items)

        # Get warehouse name safely
        warehouse = next((w for k, w in db.get("warehouses", []).items() if w.get("id") == order.get("warehouse_id")), {})
        warehouse_name = warehouse.get("warehouse_name", "UNKNOWN")

        sales_report.append({
            "order_id": order_id,
            "user_id": order["user_id"],
            "order_status": order["status"],
            "payment_status": order["payment_status"],
            "total_amount": order["total_amount"],
            "currency": order["currency"],
            "warehouse_name": warehouse_name,
            "created_at": order["created_at"],
            "total_items": total_items,
            "total_amount_calculated": total_amount_calculated
        })

    return jsonify(sales_report)


# ==========================
# Stock report
# ==========================
@app.route("/report/stock", methods=["GET"])
def report_stock():
    stock_report = []

    for k, inv in db["inventory"].items():
        warehouse = next((w for k, w in db["warehouses"].items() if w["id"] == inv["warehouse_id"]), {})
        product = next((p for p in db["products"].values() if p["id"] == inv["product_id"]), {})

        stock_report.append({
            "inventory_id": inv.get("id"),
            "warehouse_name": warehouse.get("warehouse_name", "UNKNOWN"),
            "product_name": product.get("product_name", "UNKNOWN"),
            "quantity_available": inv["quantity_available"],
            "quantity_reserved": inv["quantity_reserved"],
            "quantity_total": inv["quantity_available"] + inv["quantity_reserved"]
        })

    return jsonify(stock_report)
# -------------------- authorization --------------------
@app.route('/authorize', methods=['GET'])
def authorize():
    try:
        password = request.args.get('password')
        if password == "password":
            token = secrets.token_hex(16)
            loggedUsers.append(token)
            return jsonify({"token": token})
    except Exception as e:
        abort(500, str(e))

@app.route('/logout', methods=['DELETE'])
def logout():
    token = request.args.get("token")
    if not token:
        abort(401, "Missing user token")
    if token in loggedUsers:
        loggedUsers.remove(token)
        return jsonify({"deleted token": "successfully"})
    return jsonify({"deleted token": "token not found"}), 404

# -------------------- run --------------------
if __name__ == "__main__":
    app.run("0.0.0.0", 5000)
