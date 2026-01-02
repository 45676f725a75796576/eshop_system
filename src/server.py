from flask import Flask, abort, jsonify

from os import getenv
from dotenv import load_dotenv
import pymssql

load_dotenv()

conn = pymssql.MSSQL(
    server=getenv("SERVER"),
    user=getenv("USER"),
    password=getenv("PASSWORD"),
    database=getenv("DATABASE")
)

app = Flask(__name__)

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
    app.run('0.0.0.0', getenv("API_SERVER_PORT"))