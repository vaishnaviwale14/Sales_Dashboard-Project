"""FastAPI backend. Every dashboard number comes from a SQL query on the view vw_sales."""
import sqlite3
from typing import Optional
from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI(title="Sales Dashboard API")


def run_query(sql, params=()):
    """Run one SQL query and return the rows as a list of dictionaries."""
    con = sqlite3.connect("sales.db")
    con.row_factory = sqlite3.Row
    rows = [dict(row) for row in con.execute(sql, params).fetchall()]
    con.close()
    return rows


def build_conditions(start, end, category, segment, city, status):
    """Turn the chosen filters into SQL conditions. The ? marks keep the query safe."""
    conditions, params = [], []
    if start:
        conditions.append("order_date >= ?");       params.append(start)
    if end:
        conditions.append("order_date <= ?");       params.append(end)
    if category:
        conditions.append("category = ?");          params.append(category)
    if segment:
        conditions.append("customer_segment = ?"); params.append(segment)
    if city:
        conditions.append("city = ?");              params.append(city)
    if status:
        conditions.append("order_status = ?");      params.append(status)
    return conditions, params


def where(conditions):
    return (" WHERE " + " AND ".join(conditions)) if conditions else ""


@app.get("/")
def home():
    return FileResponse("static/index.html")


@app.get("/api/filters")
def filter_options():
    """Values for the dropdowns."""
    def distinct(column):
        return [r["v"] for r in run_query(f"SELECT DISTINCT {column} AS v FROM vw_sales ORDER BY v")]
    return {
        "category": distinct("category"),
        "segment": distinct("customer_segment"),
        "city": distinct("city"),
        "status": distinct("order_status"),
        "min_date": run_query("SELECT MIN(order_date) AS d FROM vw_sales")[0]["d"],
        "max_date": run_query("SELECT MAX(order_date) AS d FROM vw_sales")[0]["d"],
    }


@app.get("/api/dashboard")
def dashboard(start: Optional[str] = None, end: Optional[str] = None,
              category: Optional[str] = None, segment: Optional[str] = None,
              city: Optional[str] = None, status: Optional[str] = None):
    conditions, params = build_conditions(start, end, category, segment, city, status)
    w = where(conditions)

    # --- KPIs ---
    kpi = run_query(f"""
        SELECT COALESCE(SUM(net_amount_inr), 0)  AS revenue,
               COUNT(DISTINCT order_id)          AS orders,
               COUNT(DISTINCT customer_id)       AS customers,
               COUNT(DISTINCT CASE WHEN order_status <> 'Cancelled' THEN order_id END) AS valid_orders
        FROM vw_sales {w}""", params)[0]
    # Average order value = revenue / NON-cancelled orders (business rule)
    kpi["aov"] = round(kpi["revenue"] / kpi["valid_orders"], 2) if kpi["valid_orders"] else 0

    # --- Bonus: repeat customers = customers with 2 or more non-cancelled orders ---
    repeat_conditions = conditions + ["order_status <> 'Cancelled'"]
    kpi["repeat_customers"] = run_query(f"""
        SELECT COUNT(*) AS n FROM (
            SELECT customer_id FROM vw_sales {where(repeat_conditions)}
            GROUP BY customer_id HAVING COUNT(DISTINCT order_id) >= 2)""", params)[0]["n"]

    # --- Charts: same pattern each time (group, then sum revenue) ---
    def group_by(column, order_by="label"):
        return run_query(f"""
            SELECT {column} AS label, SUM(net_amount_inr) AS revenue, COUNT(DISTINCT order_id) AS orders
            FROM vw_sales {w} GROUP BY {column} ORDER BY {order_by}""", params)

    return {
        "kpi": kpi,
        "monthly": group_by("order_month"),
        "category": group_by("category", "revenue DESC"),
        "segment": group_by("customer_segment", "revenue DESC"),
        "city": group_by("city", "revenue DESC"),
        "status": group_by("order_status", "orders DESC"),
        "top_products": run_query(f"""
            SELECT product_name AS label, SUM(net_amount_inr) AS revenue
            FROM vw_sales {w} GROUP BY product_name ORDER BY revenue DESC LIMIT 5""", params),
    }
