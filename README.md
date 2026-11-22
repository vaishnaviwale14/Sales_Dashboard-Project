# Sales Dashboard (Excel -> SQL database -> FastAPI -> HTML dashboard)

## Tools used
Python, pandas (loading Excel), SQLite (database), FastAPI (backend API), HTML + JavaScript + Chart.js (dashboard).

## Setup (Mac / Linux)
```bash
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
python load_data.py               # creates sales.db and loads both Excel files
uvicorn main:app --reload
```
Open http://127.0.0.1:8000 for the dashboard (API docs at /docs).

## Project files
| File | Purpose |
|---|---|
| `schema.sql` | Table creation SQL: primary key, foreign key, and the joined view `vw_sales` |
| `load_data.py` | Data-loading script: Excel -> database, with checks |
| `queries.sql` | SQL used to verify metrics |
| `main.py` | FastAPI backend, runs SQL with the selected filters |
| `static/index.html` | The dashboard page |

## Database design
- `customers.customer_id` = PRIMARY KEY.
- `orders.order_id` = PRIMARY KEY, `orders.customer_id` = FOREIGN KEY to customers (one customer, many orders).
- View `vw_sales` joins the two tables on `customer_id`. All dashboard queries read from this view.

## Metric definitions
| Metric | Definition |
|---|---|
| Total net revenue | SUM(`net_amount_inr`); cancelled orders are 0 in the data |
| Total orders | COUNT(DISTINCT `order_id`) |
| Unique customers | COUNT(DISTINCT `customer_id`) |
| Average order value | Net revenue / count of non-cancelled orders |
| Repeat customers (bonus) | Customers with 2 or more non-cancelled orders |

Expected values with no filters: Rs 11,59,206 revenue, 240 orders, 59 customers, Rs 5,682.38 AOV.

## Dashboard contents
KPI cards (revenue, orders, customers, AOV, repeat customers); monthly revenue trend; revenue by category,
segment and city; order count by status; top 5 products.
Filters (6): date from, date to, category, segment, city, order status. All filters work together.

## Assumptions
- Returned orders stay in revenue (as required). Select Order status = Returned to see them.
- "Unique customers" counts customers who have at least one order in the current filter (59 of 60 overall; one customer has never ordered).
- Data checks before loading: no duplicate IDs, every order has a valid customer.
- SQLite stores dates as text `YYYY-MM-DD`; PostgreSQL would use a DATE type.
