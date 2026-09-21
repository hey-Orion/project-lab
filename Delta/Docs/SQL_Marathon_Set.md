# Marathon Project: SQL-Only — E-commerce Reporting Set

**Covers:** joins, aggregation (GROUP BY/HAVING), CTEs, and window functions — the 4 core SQL "tools" you've drilled across the 10-day program, now as one cohesive scenario instead of separate daily sets.

---

## Schema (fixed — use this every time)

```sql
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT,
    country TEXT,
    signup_date DATE
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date DATE,
    amount FLOAT,
    status TEXT
);

CREATE TABLE order_items (
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER
);

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    name TEXT,
    category TEXT,
    price FLOAT
);
```

---

## The Queries (build all 8, in order, same schema every time)

**Q1 — Join + filter**
Get customer name, order date, and amount for all completed orders over €200.

```sql
SELECT c.name, o.order_date, o.amount
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.status = 'completed' AND o.amount > 200;
```

**Q2 — Aggregation + HAVING**
Total revenue per country, only countries with more than 10 completed orders.

```sql
SELECT c.country, SUM(o.amount) AS total_revenue
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.status = 'completed'
GROUP BY c.country
HAVING COUNT(o.order_id) > 10;
```

**Q3 — Multi-table join + aggregation**
Total units sold per product category.

```sql
SELECT p.category, SUM(oi.quantity) AS total_units
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.category
ORDER BY total_units DESC;
```

**Q4 — Window function (LAG)**
For each customer, show each order's amount next to their previous order's amount.

```sql
SELECT
    customer_id, order_date, amount,
    LAG(amount) OVER (PARTITION BY customer_id ORDER BY order_date) AS prev_amount
FROM orders;
```

**Q5 — Window function (running total)**
Running total of each customer's spend over time.

```sql
SELECT
    customer_id, order_date, amount,
    SUM(amount) OVER (PARTITION BY customer_id ORDER BY order_date) AS running_total
FROM orders;
```

**Q6 — CTE + top-N per group**
Each customer's single highest-value order.

```sql
WITH ranked AS (
    SELECT
        customer_id, order_id, amount,
        RANK() OVER (PARTITION BY customer_id ORDER BY amount DESC) AS rnk
    FROM orders
)
SELECT customer_id, order_id, amount
FROM ranked
WHERE rnk = 1;
```

**Q7 — CTE + comparison to overall average**
Customers whose total spend is above the overall average customer spend.

```sql
WITH customer_totals AS (
    SELECT customer_id, SUM(amount) AS total_amount
    FROM orders
    GROUP BY customer_id
)
SELECT customer_id, total_amount
FROM customer_totals
WHERE total_amount > (SELECT AVG(total_amount) FROM customer_totals);
```

**Q8 — CTE + percentile (top 10%)**
Customers in the top 10% by total spend.

```sql
WITH customer_totals AS (
    SELECT customer_id, SUM(amount) AS total_amount
    FROM orders
    GROUP BY customer_id
),
ranked AS (
    SELECT
        customer_id, total_amount,
        PERCENT_RANK() OVER (ORDER BY total_amount DESC) AS pct_rank
    FROM customer_totals
)
SELECT customer_id, total_amount
FROM ranked
WHERE pct_rank <= 0.10;
```

---

## Drilling Method

1. **Study once** — read all 8, understand why each clause is where it is (especially clause order: WHERE → GROUP BY → HAVING → ORDER BY).
2. **Close the file. Rewrite all 8 from memory**, same schema, same order (Q1 easiest → Q8 hardest — they build in difficulty on purpose).
3. **Talk out loud** as you write each — say which pattern it is ("this is top-N per group, so I need RANK in a CTE") before you type it.
4. **Track where you peek.** The CTE + window combo (Q6-Q8) is historically your weakest zone (it tripped you up on Day 3 twice) — expect to peek there longest, and treat that as the real signal of progress once it stops happening.
5. **Repeat daily until zero peeks**, then vary: swap in a different aggregate (MIN/MAX instead of SUM), change the percentile to top 25%, or rank by a different column.
