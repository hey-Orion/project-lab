# dbt Tutorial — For Your Postgres/Airflow Stack

**When to start this:** Only after your coding marathon is genuinely done (cold, zero-hint SQL/SQLAlchemy/pytest). This is the "add exactly one new tool" step from your plan — not something to fold in early.

**Why dbt, and why now:** dbt (data build tool) handles the "transform" step in a pipeline — turning raw loaded data into clean, modeled, analysis-ready tables using just SQL. It pairs directly with Postgres and Airflow (which you already know), and it's the single highest-leverage addition for the Analytics Engineer / BI Engineer / Data Engineer roles you're targeting at smaller EU/UK companies.

---

## 1. What dbt Actually Does (the mental model)

Your current pipeline shape:
```
Fetch (requests) → Validate (Pydantic) → Load (SQLAlchemy) → raw tables in Postgres
```

dbt adds one step after loading:
```
... → Load → raw tables in Postgres → dbt transforms → clean, modeled tables
```

**Key idea:** dbt doesn't fetch or load data — it only *transforms* data that's already in your database, using SQL `SELECT` statements. You write a `SELECT`, dbt handles turning it into a table or view for you, tracking dependencies between your models automatically.

This maps directly onto your Medallion architecture — dbt is essentially built for the Bronze → Silver → Gold transformation layer you already understand conceptually.

---

## 2. Core Concepts

- **Model** — a `.sql` file containing a single `SELECT` statement. Each model becomes a table or view in your database. This is the core unit of dbt.
- **Source** — a reference to a raw table that already exists in your database (e.g., the `orders` table your pipeline loads into). Defined in a `.yml` file, not written by hand each time.
- **Ref (`{{ ref('model_name') }}`)** — how models reference *other* dbt models instead of hardcoding table names. This is how dbt automatically figures out the order to build things in.
- **Test** — a lightweight assertion in YAML (e.g., "this column should never be null," "this should be unique") — conceptually similar to your pytest tests, but declarative, not code.
- **Docs** — dbt auto-generates documentation and a visual dependency graph from your models and YAML.

---

## 3. Project Structure

```
my_dbt_project/
├── dbt_project.yml
├── models/
│   ├── staging/
│   │   └── stg_orders.sql
│   ├── marts/
│   │   └── customer_revenue.sql
│   └── sources.yml
```

- **staging/** — thin models that clean/rename raw source columns (your "Silver" layer equivalent).
- **marts/** — business-logic models built on top of staging (your "Gold" layer equivalent).

---

## 4. A Worked Example (using your own schema)

**`models/sources.yml`** — declare the raw table dbt should read from:
```yaml
version: 2

sources:
  - name: raw
    schema: public
    tables:
      - name: orders
      - name: customers
```

**`models/staging/stg_orders.sql`** — a staging model, cleaning the raw orders table:
```sql
SELECT
    order_id,
    customer_id,
    order_date,
    amount,
    LOWER(TRIM(status)) AS status  -- normalize messy status strings, same idea as your Pandas cleaning
FROM {{ source('raw', 'orders') }}
WHERE amount IS NOT NULL
```

**`models/marts/customer_revenue.sql`** — a mart model, built on top of staging using `ref()`:
```sql
SELECT
    customer_id,
    SUM(amount) AS total_revenue,
    COUNT(order_id) AS total_orders
FROM {{ ref('stg_orders') }}
WHERE status = 'completed'
GROUP BY customer_id
```

Notice: this is the *exact same SQL patterns* you've already drilled — filtering, aggregation, GROUP BY. dbt doesn't require new SQL skill, just a new place to put SQL you already know how to write.

**`models/staging/schema.yml`** — tests, dbt's equivalent of your pytest assertions:
```yaml
version: 2

models:
  - name: stg_orders
    columns:
      - name: order_id
        tests:
          - unique
          - not_null
      - name: status
        tests:
          - accepted_values:
              values: ['completed', 'cancelled', 'pending']
```

---

## 5. Commands You'll Actually Use

```bash
dbt run          # builds all models (runs the SQL, creates tables/views)
dbt test         # runs your YAML-defined tests
dbt docs generate  # builds documentation + dependency graph
dbt docs serve     # view it locally in a browser
```

---

## 6. How This Fits Your Existing Airflow Setup

dbt runs as a step *inside* your existing orchestration — you'd add a task to your Airflow DAG that runs `dbt run` after your load step completes. This is a small addition to a DAG structure you already know how to build, not a new orchestration paradigm.

---

## 7. Setup (when you're ready to start)

```bash
pip install dbt-postgres
dbt init my_dbt_project   # interactive setup, asks for your Postgres connection details
cd my_dbt_project
dbt debug   # confirms your connection works
```

---

## 8. Suggested Learning Path (once marathon is done)

1. Get `dbt-postgres` installed and connected to a local Postgres instance (can reuse your marathon project's DB).
2. Write 2-3 staging models on top of your existing `orders`/`customers` tables.
3. Write 1-2 mart models that aggregate the staging models (reuse your SQL marathon queries — top-N per group, revenue rollups — as dbt models).
4. Add tests (unique, not_null, accepted_values) to your models.
5. Run `dbt docs generate` and look at the dependency graph — this is genuinely satisfying and useful for interviews (you can show/discuss it).
6. Add a small write-up to your Dataflow-Sentinel README describing the dbt layer, once integrated — this becomes new interview material without needing a second project.

This is a realistic 3-5 day addition once you start it, not a multi-week detour — which is exactly why it's the right "one new tool," not the modern-data-stack sprawl (Spark/Kafka/Snowflake) that was correctly ruled out earlier.