from flask import Flask, abort, jsonify

from os import getenv
from dotenv import load_dotenv
import pyodbc
from table_gateway import *

load_dotenv()

# Read ODBC and DB settings from environment
server_host = getenv('SERVER', '127.0.0.1')
server_port = getenv('DB_SERVER_PORT', getenv('DB_PORT', '1433'))
driver = getenv('ODBC_DRIVER', 'ODBC Driver 18 for SQL Server')
encrypt = getenv('ENCRYPT', 'no')
trust = getenv('TRUST', 'no')

# For SQL Server, specify host and port as 'host,port'
server_and_port = f"{server_host},{server_port}"

conn_str = (
    f"DRIVER={{{driver}}};"
    f"SERVER={server_and_port};"
    f"DATABASE={{{getenv('DATABASE')}}};"
    f"UID={getenv('USER', "admin")};"
    f"PWD={getenv('PASSWORD')};"
    f"Encrypt={encrypt};"
    f"TrustServerCertificate={trust};"
)

conn = None

app = Flask(__name__)

gateways = {}

@app.route('/orders', methods=['POST'])
def create_order():
    abort(501, "not implemented")

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    abort(501, "not implemented")

@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    abort(501, "not implemented")

@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    abort(501, "not implemented")

@app.route('/products', methods=['POST'])
def create_product():
    abort(501, "not implemented")

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    abort(501, "not implemented")

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    abort(501, "not implemented")

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    abort(501, "not implemented")

@app.route('/products', methods=['GET'])
def list_products():
    abort(501, "not implemented")

@app.route('/warehouse', methods=['POST'])
def create_warehouse():
    abort(501, "not implemented")

@app.route('/warehouse/<int:warehouse_id>', methods=['GET'])
def get_warehouse(warehouse_id):
    abort(501, "not implemented")

@app.route('/warehouse/<int:warehouse_id>', methods=['PUT'])
def update_warehouse(warehouse_id):
    abort(501, "not implemented")

@app.route('/warehouse/<int:warehouse_id>', methods=['DELETE'])
def delete_warehouse(warehouse_id):
    abort(501, "not implemented")

@app.route('/warehouse', methods=['GET'])
def list_warehouses():
    abort(501, "not implemented")

@app.route('/inventory', methods=['POST'])
def create_inventory():
    abort(501, "not implemented")

@app.route('/inventory/<int:inventory_id>', methods=['GET'])
def get_inventory(inventory_id):
    abort(501, "not implemented")

@app.route('/inventory/<int:inventory_id>', methods=['PUT'])
def update_inventory(inventory_id):
    abort(501, "not implemented")

@app.route('/inventory/<int:inventory_id>', methods=['DELETE'])
def delete_inventory(inventory_id):
    abort(501, "not implemented")

@app.route('/payments', methods=['POST'])
def create_payment():
    abort(501, "not implemented")

@app.route('/payments/<int:payment_id>', methods=['GET'])
def get_payment(payment_id):
    abort(501, "not implemented")

@app.route('/payments/<int:payment_id>', methods=['PUT'])
def update_payment(payment_id):
    abort(501, "not implemented")

@app.route('/payments/<int:payment_id>', methods=['DELETE'])
def delete_payment(payment_id):
    abort(501, "not implemented")

@app.route('/report/sales', methods=['GET'])
def report_sales():
    abort(501, "not implemented")

@app.route('/report/stock', methods=['GET'])
def report_stock():
    abort(501, "not implemented")

@app.route('/')
def index():
    return jsonify(message="E-shop API. All endpoints currently return 501 Not Implemented.")

if __name__ == '__main__':
    try:
        conn = pyodbc.connect(conn_str)
        
        gateways = {"Orders": OrdersGateway(conn.cursor())}
    except Exception as e:
        # Provide actionable diagnostics for common ODBC issues (driver not installed, wrong name)
        try:
            available = pyodbc.drivers()
        except Exception:
            available = []
        masked = conn_str.replace(getenv('PASSWORD', ''), '****') if getenv('PASSWORD') else conn_str
        print("Failed to connect using pyodbc:", repr(e))
        print("Connection string used (password masked):", masked)
        print("Installed ODBC drivers:", available)
        print("Common fixes: install the matching Microsoft ODBC Driver for SQL Server, or set ODBC_DRIVER to a driver from the list above.")
        raise

    # Ensure port is integer
    app.run('0.0.0.0', int(getenv("API_SERVER_PORT", 5000)))