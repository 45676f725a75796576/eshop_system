from flask import Flask, request, jsonify, abort
from memory_table_gateway import *

import secrets

app = Flask(__name__)

loggedUsers = []

# ===== orders

@app.route("/orders", methods=["POST"])
def create_order():
    gw = OrdersGateway()
    data = request.json
    gw.insert(
        data["user_id"],
        data["shipping_address"],
        data["billing_address"],
        data["currency"],
    )
    return {"status": "created"}, 201


@app.route("/orders/<int:id>")
def get_order(id):
    o = OrdersGateway().selectById(id)
    if not o:
        abort(404)
    return jsonify(o)


@app.route("/orders/all")
def orders_all():
    return jsonify(OrdersGateway().selectAll())

@app.route("/orders/<int:order_id>/items", methods=["POST"])
def add_item_to_order(order_id: int):
    data = request.json
    gw = OrderItemsGateway()
    return jsonify(gw.addItem(order_id, data["product_id"], data["quantity"]))
@app.route("/orders/<int:order_id>/items", methods=["DELETE"])
def remove_item_from_order(order_id: int):
    data = request.json
    gw = OrderItemsGateway()
    return jsonify(gw.removeItemByNameAndOrder(data["name"], order_id))
@app.route("/orders/<int:order_id>/items", methods=["GET"])
def get_all_items_from_order(order_id: int):
    gw = OrderItemsGateway()
    return jsonify(gw.selectByOrder(order_id))


# ===== products

@app.route("/products", methods=["POST"])
def create_product():
    d = request.json
    ProductsGateway().insert(d["product_name"], d["unit_price"], d["tax_rate"])
    return {"status": "created"}, 201


@app.route("/products/all")
def products_all():
    return jsonify(ProductsGateway().selectAll())


# ===== warehouse

@app.route("/warehouses", methods=["POST"])
def create_warehouse():
    d = request.json
    WarehouseGateway().insert(d["warehouse_name"], d["location_code"], d["is_active"])
    return {"status": "created"}, 201


@app.route("/warehouses/all")
def warehouse_all():
    return jsonify(WarehouseGateway().selectAll())


# ===== inventory

@app.route("/inventory")
def inventory():
    return jsonify(InventoryGateway().selectAll())


# ===== payments

@app.route("/payments", methods=["POST"])
def payment():
    d = request.json
    PaymentsGateway().insert(d["order_id"], d["payment_provider"], d["provider_transaction_id"])
    return {"status": "created"}, 201

# ===== reports

@app.route("/report/sales")
def report_sales():
    return jsonify(SalesReportGateway().selectAll())


@app.route("/report/stock")
def report_stock():
    return jsonify(StockReportGateway().selectAll())


@app.route('/authorize', methods=['GET'])
def authorize():
    global loggedUsers
    try:        
        loggedUsers.append(secrets.token_hex(16))

        return { "token": loggedUsers[-1] }
        
    except Exception as e:
        abort(500, (repr(e)))
        
@app.route('/logout', methods=['DELETE'])
def logout():
    global loggedUsers
    token = request.args.get("token")
    if not token:
        abort(401, "Missing user token")
    for lu in loggedUsers:
        if lu == token:
            loggedUsers.remove(lu)
            return jsonify({"deleted token": "succesfully"})
    return jsonify({"deleted token": "token not found"})



if __name__ == "__main__":
    app.run('0.0.0.0', 5000, debug=True)
