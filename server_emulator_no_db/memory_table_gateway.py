from memory_db import db, next_id, now
from decimal import Decimal
import json

# ========================= base

class TableGateway:
    pass

# ========================= orders

class OrdersGateway(TableGateway):

    def insert(self, user_id, shipping_address, billing_address, currency):
        status_id = 1  # CREATED
        payment_status = 1  # INITIATED
        warehouse = next((w for w in db["warehouse"] if w["is_active"]), None)
        warehouse_id = warehouse["id"] if warehouse else 0

        order = {
            "id": next_id("orders"),
            "id_user": user_id,
            "status_id": status_id,
            "payment_status": payment_status,
            "warehouse_id": warehouse_id,
            "total_amount": Decimal("0.00"),
            "currency": currency,
            "shipping_address": json.dumps(shipping_address),
            "billing_address": json.dumps(billing_address),
            "created_at": now(),
            "updated_at": now(),
        }
        db["orders"].append(order)

    def selectById(self, id):
        return next((o for o in db["orders"] if o["id"] == id), {})

    def updateById(self, id, new_data):
        order = self.selectById(id)
        if not order:
            return
        order.update(new_data)
        order["updated_at"] = now()

    def deleteById(self, id):
        db["orders"][:] = [o for o in db["orders"] if o["id"] != id]

    def selectAll(self):
        return list(db["orders"])


# ========================= products

class ProductsGateway(TableGateway):

    def insert(self, name, unit_price, tax_rate):
        db["products"].append({
            "id": next_id("products"),
            "product_name": name,
            "unit_price": Decimal(unit_price),
            "tax_rate": Decimal(tax_rate),
        })

    def selectById(self, id):
        return next((p for p in db["products"] if p["id"] == id), {})

    def updateById(self, id, data):
        p = self.selectById(id)
        if p:
            p.update(data)

    def deleteById(self, id):
        db["products"][:] = [p for p in db["products"] if p["id"] != id]

    def selectAll(self):
        return list(db["products"])


# ========================= warehouse

class WarehouseGateway(TableGateway):

    def insert(self, name, location_code, is_active):
        db["warehouse"].append({
            "id": next_id("warehouse"),
            "warehouse_name": name,
            "location_code": location_code,
            "is_active": bool(is_active),
        })

    def selectById(self, id):
        return next((w for w in db["warehouse"] if w["id"] == id), {})

    def updateById(self, id, data):
        w = self.selectById(id)
        if w:
            w.update(data)

    def deleteById(self, id):
        db["warehouse"][:] = [w for w in db["warehouse"] if w["id"] != id]

    def selectAll(self):
        return list(db["warehouse"])


# ========================= order items (stored proc emulation)

class OrderItemsGateway(TableGateway):

    def addItem(self, order_id, product_id, quantity):
        product = next((p for p in db["products"] if p["id"] == product_id), None)
        order = next((o for o in db["orders"] if o["id"] == order_id), None)

        if not product or not order:
            raise ValueError("Invalid order or product")

        price = product["unit_price"]
        tax = product["tax_rate"]

        db["order_items"].append({
            "id": next_id("order_items"),
            "order_id": order_id,
            "product_id": product_id,
            "quantity": quantity,
            "unit_price": price,
            "tax_rate": tax,
        })

        order["total_amount"] += price * quantity * (Decimal("1.0") + tax)
        order["updated_at"] = now()

    def selectByOrder(self, order_id):
        return [i for i in db["order_items"] if i["order_id"] == order_id]
    
    def removeItemByNameAndOrder(self, name, order_id):
        for oi in list(db["order_items"]):
            if oi["order_id"] == order_id and db["order_items"][ oi["product_id"]]["name"] == name:
                list(db["order_items"]).remove(oi)
        return 


# ========================= inventory

class InventoryGateway(TableGateway):

    def selectAll(self):
        return list(db["inventory"])

    def selectByWarehouse(self, warehouse_id):
        return [i for i in db["inventory"] if i["warehouse_id"] == warehouse_id]

    def selectByProduct(self, product_id):
        return [i for i in db["inventory"] if i["product_id"] == product_id]


# ========================= payments

class PaymentsGateway(TableGateway):

    def insert(self, order_id, provider, transaction_id):
        db["payments"].append({
            "id": next_id("payments"),
            "order_id": order_id,
            "payment_provider": provider,
            "provider_transaction_id": transaction_id,
            "created_at": now(),
        })


# ========================= reports (views)

class SalesReportGateway:

    def selectAll(self):
        result = []
        for o in db["orders"]:
            result.append({
                "order_id": o["id"],
                "id_user": o["id_user"],
                "total_amount": float(o["total_amount"]),
                "currency": o["currency"],
                "created_at": o["created_at"],
            })
        return result


class StockReportGateway:

    def selectAll(self):
        return list(db["inventory"])
