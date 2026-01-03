import pyodbc
from json import dumps
from typing import List, Dict, Any

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
