# How to explain this project (about 5 minutes)

## Flow in one line
Excel -> `load_data.py` -> SQLite (2 tables + join view) -> `main.py` (FastAPI runs SQL) -> `index.html` (charts)

## Show the files in this order
1. **schema.sql** - "Two tables. customer_id is the primary key. orders.customer_id is a foreign key, so one customer can have many orders. The view joins them once, so every chart uses the same data."
2. **load_data.py** - "Reads both Excel files, cleans column names and dates, checks for duplicates and orphan orders, then loads customers first and orders second because of the foreign key."
3. **main.py** - "`build_conditions` turns the selected filters into a WHERE clause using `?` placeholders (safe from SQL injection). The KPI query calculates everything in SQL. Average order value divides by non-cancelled orders only."
4. **index.html** - "When a filter changes, JavaScript calls `/api/dashboard` with the filters, then redraws the cards and charts."
5. **Demo** - Pick Status = Cancelled (revenue 0), then Returned, then combine Category + Segment.

## Questions and short answers
- **Why a view?** The join is written once; changes happen in one place.
- **Why COUNT(DISTINCT)?** Each order or customer is counted once, as the rules require.
- **Why is AOV 5,682 and not 4,830?** Cancelled orders have zero revenue, so they are removed from the divisor: 204 orders, not 240.
- **Why 59 customers and not 60?** One customer has no orders. The count comes from orders.
- **Why FastAPI?** Simple Python API with automatic docs at /docs.
- **Why SQLite?** No installation; the reviewer can run it in two commands. The SQL works on PostgreSQL/MySQL with small type changes.
- **What would you improve?** Login, tests, Docker, a database like PostgreSQL or Oracle, React for a larger app.

## Marks map
| Criteria | Where |
|---|---|
| Data loading and relationships (25%) | schema.sql, load_data.py |
| SQL join and metric accuracy (25%) | vw_sales view, main.py, queries.sql |
| Dashboard visuals (25%) | index.html |
| Filters and usability (15%) | 6 filters, Reset button, updates instantly |
| Code organisation and README (10%) | Clear files, comments, README.md |
