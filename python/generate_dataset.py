"""
generate_dataset.py
--------------------
Generates a realistic, messy synthetic E-COMMERCE ORDERS dataset for the
'RetailPulse Analytics' portfolio project.

Business context: RetailPulse is a mid-size online retailer selling
Electronics, Fashion, Home & Kitchen, Beauty, Sports and Grocery products
across India. Management wants a Data Analyst to build an end-to-end
pipeline to understand sales performance, customer behaviour, and
product/category profitability.

The dataset intentionally contains:
  - missing values
  - duplicate rows
  - inconsistent text casing / whitespace
  - bad date formats
  - outliers in price/quantity
  - mixed currency-like strings in a few numeric columns
  - impossible values (negative age, negative price)

Run:
    python generate_dataset.py
Output:
    ../data/raw/retailpulse_orders_raw.csv
"""

import numpy as np
import pandas as pd
from faker import Faker
import random

fake = Faker("en_IN")
Faker.seed(42)
np.random.seed(42)
random.seed(42)

N_ROWS = 12000

categories = {
    "Electronics": ["Smartphone", "Laptop", "Headphones", "Smartwatch", "Tablet", "Bluetooth Speaker"],
    "Fashion": ["T-Shirt", "Jeans", "Sneakers", "Jacket", "Kurti", "Saree"],
    "Home & Kitchen": ["Mixer Grinder", "Cookware Set", "Bedsheet", "Water Bottle", "Lamp"],
    "Beauty": ["Face Wash", "Shampoo", "Lipstick", "Perfume", "Sunscreen"],
    "Sports": ["Yoga Mat", "Dumbbells", "Cricket Bat", "Running Shoes", "Cycling Helmet"],
    "Grocery": ["Rice 5kg", "Cooking Oil 1L", "Atta 10kg", "Tea Pack", "Snacks Combo"],
}

payment_methods = ["Credit Card", "Debit Card", "UPI", "Net Banking", "Cash on Delivery", "EMI"]
order_status = ["Delivered", "Shipped", "Cancelled", "Returned", "Processing"]
cities = ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Pune", "Kolkata",
          "Ahmedabad", "Jaipur", "Lucknow", "Chandigarh", "Ambala", "Surat", "Indore"]
states = {
    "Mumbai": "Maharashtra", "Pune": "Maharashtra", "Delhi": "Delhi", "Bangalore": "Karnataka",
    "Hyderabad": "Telangana", "Chennai": "Tamil Nadu", "Kolkata": "West Bengal",
    "Ahmedabad": "Gujarat", "Surat": "Gujarat", "Jaipur": "Rajasthan", "Lucknow": "Uttar Pradesh",
    "Chandigarh": "Chandigarh", "Ambala": "Haryana", "Indore": "Madhya Pradesh"
}
customer_segments = ["New", "Regular", "Premium", "VIP"]
genders = ["Male", "Female", "Other"]

n_customers = 3000
customer_ids = [f"CUST{str(i).zfill(5)}" for i in range(1, n_customers + 1)]
customer_signup = {cid: fake.date_between(start_date="-3y", end_date="-30d") for cid in customer_ids}
customer_gender = {cid: random.choice(genders) for cid in customer_ids}
customer_age = {cid: random.randint(18, 65) for cid in customer_ids}
customer_city = {cid: random.choice(cities) for cid in customer_ids}
customer_segment = {cid: random.choices(customer_segments, weights=[30, 40, 20, 10])[0] for cid in customer_ids}

rows = []
for i in range(1, N_ROWS + 1):
    order_id = f"ORD{str(i).zfill(6)}"
    cust_id = random.choice(customer_ids)
    category = random.choices(list(categories.keys()), weights=[25, 25, 15, 15, 10, 10])[0]
    product = random.choice(categories[category])
    base_price = {
        "Electronics": np.random.uniform(1500, 60000),
        "Fashion": np.random.uniform(300, 4000),
        "Home & Kitchen": np.random.uniform(400, 8000),
        "Beauty": np.random.uniform(150, 2500),
        "Sports": np.random.uniform(300, 10000),
        "Grocery": np.random.uniform(80, 1200),
    }[category]

    quantity = np.random.choice([1, 1, 1, 2, 2, 3, 5, 10], p=[0.35, 0.2, 0.15, 0.12, 0.08, 0.05, 0.03, 0.02])
    unit_price = round(base_price, 2)
    discount_pct = round(random.choice([0, 0, 5, 10, 15, 20, 25, 30, 50]), 2)

    order_date = fake.date_between(start_date="-2y", end_date="today")
    status = random.choices(order_status, weights=[65, 12, 8, 8, 7])[0]

    city = customer_city[cust_id]
    state = states[city]

    row = {
        "order_id": order_id,
        "customer_id": cust_id,
        "customer_age": customer_age[cust_id],
        "customer_gender": customer_gender[cust_id],
        "customer_segment": customer_segment[cust_id],
        "signup_date": customer_signup[cust_id],
        "order_date": order_date,
        "category": category,
        "product_name": product,
        "quantity": quantity,
        "unit_price": unit_price,
        "discount_pct": discount_pct,
        "payment_method": random.choice(payment_methods),
        "order_status": status,
        "city": city,
        "state": state,
        "delivery_days": np.random.randint(1, 12),
        "shipping_cost": round(np.random.uniform(0, 150), 2),
        "customer_rating": random.choices([np.nan, 1, 2, 3, 4, 5], weights=[20, 3, 5, 12, 30, 30])[0],
        "is_prime_member": random.choice([True, False]),
        "coupon_used": random.choice(["Yes", "No"]),
        "return_reason": np.nan,
        "warehouse_id": f"WH{random.randint(1,8)}",
        "device_used": random.choice(["Mobile App", "Website", "Mobile Web", "Desktop App"]),
        "referral_source": random.choice(["Instagram", "Google Ads", "Organic", "Email", "Affiliate", "Direct"]),
    }

    if status == "Returned":
        row["return_reason"] = random.choice(
            ["Damaged Product", "Size Issue", "Not as Described", "Changed Mind", "Late Delivery"]
        )

    rows.append(row)

df = pd.DataFrame(rows)

# ---------------------------------------------------------------
# Inject realistic MESSINESS (this is what the cleaning script fixes)
# ---------------------------------------------------------------

# 1. Duplicates (~1.5%)
dupe_rows = df.sample(frac=0.015, random_state=1)
df = pd.concat([df, dupe_rows], ignore_index=True)

# 2. Missing values scattered across several columns
for col, frac in [("customer_rating", 0.15), ("shipping_cost", 0.02),
                   ("delivery_days", 0.03), ("discount_pct", 0.01),
                   ("city", 0.01), ("payment_method", 0.02)]:
    idx = df.sample(frac=frac, random_state=hash(col) % 1000).index
    df.loc[idx, col] = np.nan

# 3. Inconsistent text casing / whitespace
def messify_text(x):
    if pd.isna(x):
        return x
    choice = random.random()
    if choice < 0.2:
        return f"  {x.upper()}  "
    elif choice < 0.4:
        return x.lower()
    return x

for col in ["category", "payment_method", "city", "customer_gender", "device_used"]:
    df[col] = df[col].apply(messify_text)

# 4. Bad / inconsistent date formats stored as strings
def messify_date(d):
    d = pd.to_datetime(d)
    fmt = random.choice(["%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%m/%d/%Y", "%d %b %Y"])
    return d.strftime(fmt)

df["order_date"] = df["order_date"].apply(messify_date)
df["signup_date"] = df["signup_date"].apply(messify_date)

# 5. Currency-like strings mixed into unit_price (simulate messy export)
def messify_price(p):
    if random.random() < 0.05:
        return f"Rs. {p:,.2f}"
    return p

df["unit_price"] = df["unit_price"].apply(messify_price)

# 6. Outliers / impossible values
outlier_idx = df.sample(frac=0.005, random_state=2).index
df.loc[outlier_idx, "quantity"] = df.loc[outlier_idx, "quantity"] * 50

neg_idx = df.sample(frac=0.003, random_state=3).index
df.loc[neg_idx, "customer_age"] = -df.loc[neg_idx, "customer_age"]

neg_price_idx = df.sample(frac=0.002, random_state=4).index
df.loc[neg_price_idx, "shipping_cost"] = -abs(df.loc[neg_price_idx, "shipping_cost"])

# 7. Shuffle rows so it doesn't look artificially ordered
df = df.sample(frac=1, random_state=7).reset_index(drop=True)

df.to_csv("../data/raw/retailpulse_orders_raw.csv", index=False)
print(f"Generated {len(df)} rows, {df.shape[1]} columns -> data/raw/retailpulse_orders_raw.csv")
