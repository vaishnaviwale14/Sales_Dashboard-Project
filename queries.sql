-- Useful queries to check the dashboard numbers (run in DB Browser for SQLite or: sqlite3 sales.db)

-- 1. The joined dataset (also saved as the view vw_sales in schema.sql)
SELECT o.*, c.customer_name, c.city, c.state, c.customer_segment
FROM orders o JOIN customers c ON c.customer_id = o.customer_id;

-- 2. KPIs  (expected: 1159206 | 240 | 59 | 5682.38)
SELECT SUM(net_amount_inr)         AS total_net_revenue,
       COUNT(DISTINCT order_id)    AS total_orders,
       COUNT(DISTINCT customer_id) AS unique_customers,
       ROUND(SUM(net_amount_inr) * 1.0 /
             COUNT(DISTINCT CASE WHEN order_status <> 'Cancelled' THEN order_id END), 2) AS avg_order_value
FROM vw_sales;

-- 3. Monthly revenue
SELECT order_month, SUM(net_amount_inr) AS revenue FROM vw_sales GROUP BY order_month ORDER BY order_month;

-- 4. Revenue by category (same pattern for customer_segment and city)
SELECT category, SUM(net_amount_inr) AS revenue FROM vw_sales GROUP BY category ORDER BY revenue DESC;

-- 5. Orders by status
SELECT order_status, COUNT(DISTINCT order_id) AS orders FROM vw_sales GROUP BY order_status;

-- 6. Top 5 products
SELECT product_name, SUM(net_amount_inr) AS revenue FROM vw_sales GROUP BY product_name ORDER BY revenue DESC LIMIT 5;
