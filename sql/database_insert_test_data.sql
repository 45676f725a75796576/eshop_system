/*
    This code down there is made entirely by ChatGPT to check if anything works
*/

USE [eshop];
GO

/* ============================================================
   TEST DATA INSERT SCRIPT
   Respects FK order and constraints
============================================================ */

/* ---------- WAREHOUSES ---------- */
INSERT INTO warehouse (warehouse_name, location_code, is_active)
VALUES
('Main Warehouse', 'WH-PRG-01', 1),
('Secondary Warehouse', 'WH-BRN-01', 0);
GO

/* ---------- PRODUCTS ---------- */
INSERT INTO products (product_name, unit_price, tax_rate)
VALUES
('Laptop', 25000.00, 0.21),
('Mouse', 499.00, 0.21),
('Keyboard', 1299.00, 0.21),
('Monitor', 5999.00, 0.21),
('USB Cable', 199.00, 0.21);
GO

/* ---------- INVENTORY ---------- */
INSERT INTO inventory (warehouse_id, product_id, quantity_available, quantity_reserved)
VALUES
(1, 1, 50, 0),
(1, 2, 200, 0),
(1, 3, 150, 0),
(1, 4, 40, 0),
(1, 5, 500, 0);
GO

/* ---------- ORDERS ---------- */
INSERT INTO orders (
    id_user,
    status_id,
    payment_status,
    warehouse_id,
    total_amount,
    currency,
    shipping_address,
    billing_address
)
VALUES
(
    1,
    (SELECT id FROM order_status WHERE status_name = 'CREATED'),
    (SELECT id FROM payment_status WHERE status_name = 'INITIATED'),
    1,
    0,
    'CZK',
    N'{"street":"Main 1","city":"Prague","zip":"11000","country":"CZ"}',
    N'{"street":"Main 1","city":"Prague","zip":"11000","country":"CZ"}'
);
GO

/* ---------- ORDER ITEMS ---------- */
INSERT INTO order_items (order_id, product_id, quantity, unit_price, tax_rate)
VALUES
(1, 1, 1, 25000.00, 0.21),
(1, 2, 2, 499.00, 0.21),
(1, 5, 3, 199.00, 0.21);
GO

/* ---------- RECALCULATE ORDER TOTAL ---------- */
UPDATE orders
SET total_amount =
(
    SELECT SUM(quantity * unit_price * (1 + tax_rate))
    FROM order_items
    WHERE order_id = orders.id
),
updated_at = SYSDATETIME()
WHERE id = 1;
GO

/* ---------- PAYMENTS ---------- */
INSERT INTO payments (order_id, payment_provider, provider_transaction_id)
VALUES
(1, 'TEST_GATEWAY', 'TXN-0001');
GO

/* ---------- CONFIRM PAYMENT ---------- */
EXEC tg_payment_confirm @order_id = 1;
GO

/* ---------- RESERVE STOCK ---------- */
EXEC tg_stock_reserve @order_id = 1;
GO

/* ---------- SECOND ORDER (PAID) ---------- */
DECLARE @order2 INT;

EXEC tg_order_create
    @user_id = 2,
    @shipping_address = N'{"street":"Side 5","city":"Brno","zip":"60200","country":"CZ"}',
    @billing_address = N'{"street":"Side 5","city":"Brno","zip":"60200","country":"CZ"}',
    @currency = 'CZK',
    @order_id = @order2 OUTPUT;

EXEC tg_order_item_add @order2, 3, 1;
EXEC tg_order_item_add @order2, 4, 2;

EXEC tg_payment_confirm @order2;
EXEC tg_stock_reserve @order2;
GO

/* ---------- QUICK CHECK ---------- */
SELECT * FROM v_order_summary;
SELECT * FROM v_order_items;
SELECT * FROM inventory;
GO
