import pyodbc
from json import dumps
from typing import List, Dict, Any

def row_to_dict(cursor, row) -> Dict[str, Any]:
    columns = [c[0] for c in cursor.description]
    return dict(zip(columns, row))

def rows_to_dicts(cursor, rows) -> List[Dict[str, Any]]:
    columns = [c[0] for c in cursor.description]
    return [dict(zip(columns, row)) for row in rows]

class TableGateway:
    def __init__(self, cursor: pyodbc.Cursor):
        self.cursor = cursor

    def insert(self, *args, **kwargs):
        raise NotImplementedError

    def selectById(self, id: int) -> Dict[str, Any]:
        raise NotImplementedError

    def updateById(self, id: int, new_data: dict):
        raise NotImplementedError

    def deleteById(self, id: int):
        raise NotImplementedError

    def selectAll(self) -> List[Dict[str, Any]]:
        raise NotImplementedError


class OrdersGateway(TableGateway):
    def __init__(self, cursor: pyodbc.Cursor):
        super().__init__(cursor)

    def insert(self, user_id: int, shipping_address: dict, billing_address: dict, currency: str):
        sql = """
        EXEC [dbo].[tg_order_create] 
            @user_id = ?, 
            @shipping_address = ?, 
            @billing_address = ?, 
            @currency = ?;
        """
        self.cursor.execute(sql, user_id, dumps(shipping_address), dumps(billing_address), currency)
        return self.cursor.messages

    def selectById(self, id: int) -> Dict[str, Any]:
        self.cursor.execute("SELECT * FROM orders WHERE id = ?", id)
        row = self.cursor.fetchone()
        if not row:
            return {}
        columns = [c[0] for c in self.cursor.description]
        return dict(zip(columns, row))

    def updateById(self, id: int, new_data: dict):
        if not new_data:
            return
        columns = ", ".join(f"{k} = ?" for k in new_data.keys())
        values = list(new_data.values())
        values.append(id)
        sql = f"UPDATE orders SET {columns} WHERE id = ?"
        self.cursor.execute(sql, values)
        return self.cursor.messages

    def deleteById(self, id: int):
        self.cursor.execute("DELETE FROM orders WHERE id = ?", id)
        return self.cursor.messages

    def selectAll(self) -> List[Dict[str, Any]]:
        self.cursor.execute("SELECT * FROM orders")
        columns = [c[0] for c in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]

class WarehouseGateway(TableGateway):

    def insert(self, name: str, location_code: str, is_active: bool):
        self.cursor.execute(
            "INSERT INTO warehouse (warehouse_name, location_code, is_active) VALUES (?, ?, ?)",
            name, location_code, is_active
        )

    def selectById(self, id: int):
        self.cursor.execute("SELECT * FROM warehouse WHERE id = ?", id)
        row = self.cursor.fetchone()
        return row_to_dict(self.cursor, row) if row else {}

    def updateById(self, id: int, data: dict):
        if not data:
            return
        cols = ", ".join(f"{k} = ?" for k in data)
        values = list(data.values()) + [id]
        self.cursor.execute(f"UPDATE warehouse SET {cols} WHERE id = ?", values)

    def deleteById(self, id: int):
        self.cursor.execute("DELETE FROM warehouse WHERE id = ?", id)

    def selectAll(self):
        self.cursor.execute("SELECT * FROM warehouse")
        return rows_to_dicts(self.cursor, self.cursor.fetchall())

class ProductsGateway(TableGateway):

    def insert(self, name: str, unit_price: float, tax_rate: float):
        self.cursor.execute(
            "INSERT INTO products (product_name, unit_price, tax_rate) VALUES (?, ?, ?)",
            name, unit_price, tax_rate
        )

    def selectById(self, id: int):
        self.cursor.execute("SELECT * FROM products WHERE id = ?", id)
        row = self.cursor.fetchone()
        return row_to_dict(self.cursor, row) if row else {}

    def updateById(self, id: int, data: dict):
        if not data:
            return
        cols = ", ".join(f"{k} = ?" for k in data)
        self.cursor.execute(
            f"UPDATE products SET {cols} WHERE id = ?",
            list(data.values()) + [id]
        )

    def deleteById(self, id: int):
        self.cursor.execute("DELETE FROM products WHERE id = ?", id)

    def selectAll(self):
        self.cursor.execute("SELECT * FROM products")
        return rows_to_dicts(self.cursor, self.cursor.fetchall())

class OrderItemsGateway(TableGateway):

    def addItem(self, order_id: int, product_id: int, quantity: int):
        self.cursor.execute(
            "EXEC dbo.tg_order_item_add ?, ?, ?",
            order_id, product_id, quantity
        )

    def selectByOrder(self, order_id: int):
        self.cursor.execute(
            "SELECT * FROM order_items WHERE order_id = ?",
            order_id
        )
        return rows_to_dicts(self.cursor, self.cursor.fetchall())
    
    def removeItemByNameAndOrder(self, name: str, order_id: int):
        self.cursor.execute(
            "DELETE FROM order_items WHERE order_id = ? AND product_id = (SELECT 1 id FROM products WHERE product_name = ?)",
            order_id, name
        )

class InventoryGateway(TableGateway):

    def selectByWarehouse(self, warehouse_id: int):
        self.cursor.execute(
            "SELECT * FROM inventory WHERE warehouse_id = ?",
            warehouse_id
        )
        return rows_to_dicts(self.cursor, self.cursor.fetchall())

    def selectByProduct(self, product_id: int):
        self.cursor.execute(
            "SELECT * FROM inventory WHERE product_id = ?",
            product_id
        )
        return rows_to_dicts(self.cursor, self.cursor.fetchall())

class PaymentsGateway(TableGateway):

    def insert(self, order_id: int, provider: str, transaction_id: str):
        self.cursor.execute(
            """
            INSERT INTO payments (order_id, payment_provider, provider_transaction_id)
            VALUES (?, ?, ?)
            """,
            order_id, provider, transaction_id
        )

    def selectByOrder(self, order_id: int):
        self.cursor.execute(
            "SELECT * FROM payments WHERE order_id = ?",
            order_id
        )
        return rows_to_dicts(self.cursor, self.cursor.fetchall())

class OrderSummaryViewGateway:

    def __init__(self, cursor):
        self.cursor = cursor

    def selectByUser(self, user_id: int):
        self.cursor.execute(
            "SELECT * FROM v_order_summary WHERE id_user = ?",
            user_id
        )
        return rows_to_dicts(self.cursor, self.cursor.fetchall())

class OrderItemsViewGateway:

    def __init__(self, cursor):
        self.cursor = cursor

    def selectByOrder(self, order_id: int):
        self.cursor.execute(
            "SELECT * FROM v_order_items WHERE order_id = ?",
            order_id
        )
        return rows_to_dicts(self.cursor, self.cursor.fetchall())
    
class SalesReportGateway:
    def __init__(self, cursor):
        self.cursor = cursor

    def selectAll(self):
        self.cursor.execute("SELECT * FROM v_sales_report")
        return rows_to_dicts(self.cursor, self.cursor.fetchall())

class StockReportGateway:
    def __init__(self, cursor):
        self.cursor = cursor

    def selectAll(self):
        self.cursor.execute("SELECT * FROM v_stock_report")
        return rows_to_dicts(self.cursor, self.cursor.fetchall())
