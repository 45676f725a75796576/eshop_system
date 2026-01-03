from flask import Flask, abort, jsonify, request, g
from os import getenv
from dotenv import load_dotenv
import pyodbc

from table_gateway import (
    OrdersGateway,
    ProductsGateway,
    WarehouseGateway,
    InventoryGateway,
    PaymentsGateway,
    SalesReportGateway, 
    StockReportGateway
)

load_dotenv()

server_host = getenv("SERVER", "127.0.0.1")
server_port = getenv("DB_SERVER_PORT", getenv("DB_PORT", "1433"))
driver = getenv("ODBC_DRIVER", "ODBC Driver 18 for SQL Server")
encrypt = getenv("ENCRYPT", "no")
trust = getenv("TRUST", "no")

server_and_port = f"{server_host},{server_port}"

CONN_STR = (
    f"DRIVER={{{driver}}};"
    f"SERVER={server_and_port};"
    f"DATABASE={getenv('DATABASE')};"
    f"UID={getenv('USER', 'admin')};"
    f"PWD={getenv('PASSWORD')};"
    f"Encrypt={encrypt};"
    f"TrustServerCertificate={trust};"
)

app = Flask(__name__)

def get_db():
    if "db" not in g:
        g.db = pyodbc.connect(CONN_STR, autocommit=False)
    return g.db

def get_cursor():
    return get_db().cursor()

@app.teardown_request
def teardown_request(exception):
    db = g.pop("db", None)
    if not db:
        return
    if exception:
        db.rollback()
    else:
        db.commit()
    db.close()
    
# ===================================================

@app.route("/orders", methods=["POST"])
def create_order():
    data = request.json
    gw = OrdersGateway(get_cursor())
    gw.insert(
        data["user_id"],
        data["shipping_address"],
        data["billing_address"],
        data["currency"],
    )
    return jsonify({"status": "created"}), 201

@app.route("/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    gw = OrdersGateway(get_cursor())
    order = gw.selectById(order_id)
    if not order:
        abort(404)
    return jsonify(order)

@app.route("/orders/<int:order_id>", methods=["PUT"])
def update_order(order_id):
    gw = OrdersGateway(get_cursor())
    gw.updateById(order_id, request.json)
    return jsonify({"status": "updated"})

@app.route("/orders/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
    gw = OrdersGateway(get_cursor())
    gw.deleteById(order_id)
    return jsonify({"status": "deleted"})

# ==============================================================================

@app.route("/products", methods=["POST"])
def create_product():
    data = request.json
    gw = ProductsGateway(get_cursor())
    gw.insert(data["product_name"], data["unit_price"], data["tax_rate"])
    return jsonify({"status": "created"}), 201

@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    gw = ProductsGateway(get_cursor())
    product = gw.selectById(product_id)
    if not product:
        abort(404)
    return jsonify(product)

@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    gw = ProductsGateway(get_cursor())
    gw.updateById(product_id, request.json)
    return jsonify({"status": "updated"})

@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    gw = ProductsGateway(get_cursor())
    gw.deleteById(product_id)
    return jsonify({"status": "deleted"})

@app.route("/products", methods=["GET"])
def list_products():
    gw = ProductsGateway(get_cursor())
    return jsonify(gw.selectAll())

# ==============================================================================

@app.route("/warehouse", methods=["POST"])
def create_warehouse():
    data = request.json
    gw = WarehouseGateway(get_cursor())
    gw.insert(data["warehouse_name"], data["location_code"], data["is_active"])
    return jsonify({"status": "created"}), 201

@app.route("/warehouse/<int:warehouse_id>", methods=["GET"])
def get_warehouse(warehouse_id):
    gw = WarehouseGateway(get_cursor())
    wh = gw.selectById(warehouse_id)
    if not wh:
        abort(404)
    return jsonify(wh)

@app.route("/warehouse/<int:warehouse_id>", methods=["PUT"])
def update_warehouse(warehouse_id):
    gw = WarehouseGateway(get_cursor())
    gw.updateById(warehouse_id, request.json)
    return jsonify({"status": "updated"})

@app.route("/warehouse/<int:warehouse_id>", methods=["DELETE"])
def delete_warehouse(warehouse_id):
    gw = WarehouseGateway(get_cursor())
    gw.deleteById(warehouse_id)
    return jsonify({"status": "deleted"})

@app.route("/warehouse", methods=["GET"])
def list_warehouses():
    gw = WarehouseGateway(get_cursor())
    return jsonify(gw.selectAll())

# ======================================================================

@app.route("/inventory", methods=["GET"])
def list_inventory():
    gw = InventoryGateway(get_cursor())
    return jsonify(gw.selectAll())

# =======================================================================

@app.route("/payments", methods=["POST"])
def create_payment():
    data = request.json
    gw = PaymentsGateway(get_cursor())
    gw.insert(data["order_id"], data["payment_provider"], data["provider_transaction_id"])
    return jsonify({"status": "created"}), 201

# =======================================================================

@app.route("/report/sales", methods=["GET"])
def report_sales():
    gw = SalesReportGateway(get_cursor())
    return jsonify(gw.selectAll())

@app.route("/report/stock", methods=["GET"])
def report_stock():
    gw = StockReportGateway(get_cursor())
    return jsonify(gw.selectAll())
    
# =========================================================================

if __name__ == '__main__':
    app.run('0.0.0.0', int(getenv("API_SERVER_PORT", 5000)))