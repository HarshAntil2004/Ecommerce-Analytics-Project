"""
clean_data.py
-------------
Cleans data/raw/retailpulse_orders_raw.csv and writes
data/cleaned/retailpulse_orders_cleaned.csv

Every function below documents WHAT problem it fixes and WHY it matters
to the business, so this file doubles as living documentation.
"""

import pandas as pd
import numpy as np
import re

RAW_PATH = "../data/raw/retailpulse_orders_raw.csv"
CLEAN_PATH = "../data/cleaned/retailpulse_orders_cleaned.csv"


def load_raw(path=RAW_PATH) -> pd.DataFrame:
    df = pd.read_csv(path)
    print(f"Loaded raw data: {df.shape[0]} rows, {df.shape[1]} columns")
    return df


def drop_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    WHY: Duplicate order rows inflate revenue and order-count metrics,
    which would mislead management about actual sales volume.
    """
    before = len(df)
    df = df.drop_duplicates(subset=[c for c in df.columns if c != "order_id"] + ["order_id"])
    df = df.drop_duplicates(subset="order_id", keep="first")
    print(f"Removed {before - len(df)} duplicate rows")
    return df


def clean_text_columns(df: pd.DataFrame, cols) -> pd.DataFrame:
    """
    WHY: Inconsistent casing/whitespace ('electronics', ' ELECTRONICS ')
    causes GROUP BY / dashboard filters to treat the same category as
    multiple distinct categories, corrupting every aggregation.
    """
    for col in cols:
        df[col] = df[col].astype(str).str.strip().str.title()
        df[col] = df[col].replace("Nan", np.nan)
    return df


def parse_mixed_dates(df: pd.DataFrame, cols) -> pd.DataFrame:
    """
    WHY: Source systems (web app, mobile app, CSV export) often write dates
    in different formats. Without standardizing, time-series analysis
    (monthly revenue, YoY growth) silently breaks or misparses dates.
    """
    for col in cols:
        df[col] = pd.to_datetime(df[col], dayfirst=True, errors="coerce", format="mixed")
    return df


def clean_price_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    WHY: 'Rs. 1,234.50' style strings mixed into a numeric column force
    the whole column to be read as text (object dtype), breaking all
    numeric aggregation (SUM, AVG) until fixed.
    """
    def _to_float(v):
        if isinstance(v, str):
            v = re.sub(r"[^0-9.]", "", v)
        try:
            return float(v)
        except (ValueError, TypeError):
            return np.nan
    df["unit_price"] = df["unit_price"].apply(_to_float)
    df["unit_price"] = df["unit_price"].fillna(df["unit_price"].median())
    return df


def fix_impossible_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    WHY: Negative ages, negative shipping costs, and absurd quantities
    (e.g. 500 units of a single smartphone order) are data-entry/ETL
    errors, not real business events. Left uncorrected they distort
    averages and can trigger false 'best customer' or 'best product'
    conclusions.
    """
    df["customer_age"] = df["customer_age"].abs()
    df.loc[(df["customer_age"] < 15) | (df["customer_age"] > 90), "customer_age"] = np.nan

    df["shipping_cost"] = df["shipping_cost"].abs()

    # Cap extreme quantity outliers at the 99.5th percentile instead of deleting
    # the row (we don't want to lose an otherwise valid order).
    cap = df["quantity"].quantile(0.995)
    df["quantity"] = np.where(df["quantity"] > cap, cap, df["quantity"])
    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    WHY: Different columns need different missing-value strategies.
    A rating of NaN usually means 'customer didn't rate' (not a random
    accident), so we keep it as NaN rather than imputing a fake rating
    that would bias average-rating KPIs.
    """
    df["payment_method"] = df["payment_method"].fillna("Unknown")
    df["city"] = df["city"].fillna("Unknown")
    df["discount_pct"] = df["discount_pct"].fillna(0)
    df["delivery_days"] = df["delivery_days"].fillna(df["delivery_days"].median())
    df["shipping_cost"] = df["shipping_cost"].fillna(df["shipping_cost"].median())
    # customer_rating intentionally left as NaN -> represents "not rated"
    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates business-relevant derived columns used throughout SQL/EDA.
    """
    df["gross_revenue"] = df["unit_price"] * df["quantity"]
    df["net_revenue"] = df["gross_revenue"] * (1 - df["discount_pct"] / 100)
    df["order_year"] = df["order_date"].dt.year
    df["order_month"] = df["order_date"].dt.to_period("M").astype(str)
    df["order_weekday"] = df["order_date"].dt.day_name()
    df["is_weekend"] = df["order_weekday"].isin(["Saturday", "Sunday"])
    df["customer_tenure_days"] = (df["order_date"] - df["signup_date"]).dt.days
    df["age_group"] = pd.cut(
        df["customer_age"],
        bins=[0, 24, 34, 44, 54, 100],
        labels=["<25", "25-34", "35-44", "45-54", "55+"],
    )
    return df


def validate(df: pd.DataFrame) -> None:
    """Basic sanity checks before saving cleaned data."""
    assert df["order_id"].is_unique, "order_id is not unique after cleaning!"
    assert (df["unit_price"] >= 0).all(), "Negative prices remain!"
    assert (df["quantity"] >= 0).all(), "Negative quantities remain!"
    print("Validation checks passed.")


def run_pipeline():
    df = load_raw()
    df = drop_duplicates(df)
    df = clean_text_columns(df, ["category", "payment_method", "city",
                                  "customer_gender", "device_used"])
    df = parse_mixed_dates(df, ["order_date", "signup_date"])
    df = clean_price_column(df)
    df = fix_impossible_values(df)
    df = handle_missing_values(df)
    df = engineer_features(df)
    validate(df)
    df.to_csv(CLEAN_PATH, index=False)
    print(f"Saved cleaned data: {df.shape[0]} rows, {df.shape[1]} columns -> {CLEAN_PATH}")
    return df


if __name__ == "__main__":
    run_pipeline()
