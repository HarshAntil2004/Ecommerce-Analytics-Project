# Project Architecture

## Workflow / Data Flow

```
[generate_dataset.py]
        │  raw messy CSV
        ▼
   data/raw/retailpulse_orders_raw.csv
        │
        ▼
[clean_data.py]  -- cleaning, validation, feature engineering
        │  cleaned CSV
        ▼
   data/cleaned/retailpulse_orders_cleaned.csv
        │
        ├──────────────► [eda.py] ──► reports/*.png (charts + console insights)
        │
        ▼
[load_to_mysql.py] ──► MySQL `retailpulse` DB (customers, orders tables)
        │
        ▼
[sql/03_analysis_queries.sql] ──► business query results
        │
        ▼
   Tableau (connects to MySQL or cleaned CSV) ──► dashboards
```

All of the above is orchestrated by `automation/main.py`, which logs each
step's start/success/failure to `logs/pipeline.log`.

## ER Diagram (textual description)

```
customers (1) ───< orders (many)
  customer_id PK          order_id PK
  customer_age             customer_id FK -> customers.customer_id
  customer_gender          order_date
  customer_segment         category, product_name
  signup_date               quantity, unit_price, discount_pct
  city, state               gross_revenue, net_revenue
                            payment_method, order_status
                            delivery_days, shipping_cost
                            customer_rating, is_prime_member
                            coupon_used, warehouse_id
                            device_used, referral_source
```

One customer can place many orders (1:N relationship), enforced via the
`fk_orders_customer` foreign key constraint in `sql/01_create_schema.sql`.
