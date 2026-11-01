"""
load_to_mysql.py
-----------------
Loads the cleaned CSV into the MySQL `retailpulse` database created by
sql/01_create_schema.sql. Splits the flat cleaned CSV into `customers`
and `orders` tables to match the schema.

Requires: pip install mysql-connector-python sqlalchemy pandas
Set your local MySQL credentials via environment variables:
    RP_DB_HOST, RP_DB_USER, RP_DB_PASSWORD
"""

import os
import pandas as pd
from sqlalchemy import create_engine

DB_HOST = os.environ.get("RP_DB_HOST", "localhost")
DB_USER = os.environ.get("RP_DB_USER", "root")
DB_PASSWORD = os.environ.get("RP_DB_PASSWORD", "")
DB_NAME = "retailpulse"


def get_engine():
    url = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    return create_engine(url)


def main():
    df = pd.read_csv("../data/cleaned/retailpulse_orders_cleaned.csv",
                      parse_dates=["order_date", "signup_date"])

    customers = (
        df[["customer_id", "customer_age", "customer_gender",
            "customer_segment", "signup_date", "city", "state"]]
        .drop_duplicates(subset="customer_id")
    )

    orders = df[["order_id", "customer_id", "order_date", "category", "product_name",
                 "quantity", "unit_price", "discount_pct", "gross_revenue", "net_revenue",
                 "payment_method", "order_status", "delivery_days", "shipping_cost",
                 "customer_rating", "is_prime_member", "coupon_used", "warehouse_id",
                 "device_used", "referral_source"]]

    engine = get_engine()
    customers.to_sql("customers", engine, if_exists="append", index=False, chunksize=1000)
    orders.to_sql("orders", engine, if_exists="append", index=False, chunksize=1000)
    print(f"Loaded {len(customers)} customers and {len(orders)} orders into MySQL.")


if __name__ == "__main__":
    main()
