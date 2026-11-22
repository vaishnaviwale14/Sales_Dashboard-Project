-- Run by load_data.py. Creates 2 tables, the relationship, and the joined view.
DROP VIEW  IF EXISTS vw_sales;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;

-- One row per customer. customer_id is the PRIMARY KEY.
CREATE TABLE customers (
    customer_id         TEXT PRIMARY KEY,
    customer_name       TEXT NOT NULL,
    email               TEXT,
    city                TEXT,
    state               TEXT,
    customer_segment    TEXT,
    join_date           DATE,
    acquisition_channel TEXT
);

-- One row per order. customer_id is a FOREIGN KEY -> one customer can have many orders.
CREATE TABLE orders (
    order_id       TEXT PRIMARY KEY,
    customer_id    TEXT NOT NULL,
    order_date     DATE NOT NULL,
    product_id     TEXT,
    product_name   TEXT,
    category       TEXT,
    quantity       INTEGER,
    unit_price_inr INTEGER,
    discount_rate  REAL,
    net_amount_inr INTEGER NOT NULL,
    payment_method TEXT,
    order_status   TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
);

-- The joined dataset. The whole dashboard reads from this view.
CREATE VIEW vw_sales AS
SELECT  o.order_id, o.order_date,
        substr(o.order_date, 1, 7) AS order_month,     -- e.g. '2026-03' for the monthly trend
        o.product_name, o.category, o.quantity, o.net_amount_inr,
        o.payment_method, o.order_status,
        c.customer_id, c.customer_name, c.city, c.state, c.customer_segment
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id;
