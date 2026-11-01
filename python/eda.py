"""
eda.py
------
Exploratory Data Analysis on the cleaned RetailPulse dataset.
Saves charts to ../reports/ and prints business insights to console.
"""

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")

df = pd.read_csv("../data/cleaned/retailpulse_orders_cleaned.csv", parse_dates=["order_date", "signup_date"])
OUT = "../reports"

# 1. Revenue by category
plt.figure(figsize=(9, 5))
rev_cat = df.groupby("category")["net_revenue"].sum().sort_values(ascending=False)
sns.barplot(x=rev_cat.values, y=rev_cat.index, palette="viridis")
plt.title("Net Revenue by Category")
plt.xlabel("Net Revenue (INR)")
plt.tight_layout()
plt.savefig(f"{OUT}/01_revenue_by_category.png", dpi=120)
plt.close()

# 2. Monthly revenue trend
plt.figure(figsize=(10, 5))
monthly = df.groupby("order_month")["net_revenue"].sum().sort_index()
monthly.plot(kind="line", marker="o")
plt.title("Monthly Net Revenue Trend")
plt.ylabel("Net Revenue (INR)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{OUT}/02_monthly_revenue_trend.png", dpi=120)
plt.close()

# 3. Order status distribution
plt.figure(figsize=(7, 5))
df["order_status"].value_counts().plot(kind="bar", color="steelblue")
plt.title("Order Status Distribution")
plt.tight_layout()
plt.savefig(f"{OUT}/03_order_status.png", dpi=120)
plt.close()

# 4. Weekend vs weekday revenue
plt.figure(figsize=(6, 5))
weekend_rev = df.groupby("is_weekend")["net_revenue"].mean()
weekend_rev.index = ["Weekday", "Weekend"]
sns.barplot(x=weekend_rev.index, y=weekend_rev.values, palette="magma")
plt.title("Average Order Revenue: Weekday vs Weekend")
plt.tight_layout()
plt.savefig(f"{OUT}/04_weekend_vs_weekday.png", dpi=120)
plt.close()

# 5. Correlation heatmap
plt.figure(figsize=(8, 6))
num_cols = ["unit_price", "quantity", "discount_pct", "net_revenue",
            "delivery_days", "shipping_cost", "customer_rating", "customer_age"]
sns.heatmap(df[num_cols].corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.savefig(f"{OUT}/05_correlation_heatmap.png", dpi=120)
plt.close()

# 6. Revenue by customer segment
plt.figure(figsize=(7, 5))
seg_rev = df.groupby("customer_segment")["net_revenue"].sum().sort_values(ascending=False)
sns.barplot(x=seg_rev.index, y=seg_rev.values, palette="crest")
plt.title("Net Revenue by Customer Segment")
plt.tight_layout()
plt.savefig(f"{OUT}/06_revenue_by_segment.png", dpi=120)
plt.close()

print("EDA charts saved to reports/. Sample business insights:\n")

total_rev = df["net_revenue"].sum()
top_cat = rev_cat.index[0]
top_cat_share = rev_cat.iloc[0] / total_rev * 100
weekend_uplift = (weekend_rev["Weekend"] / weekend_rev["Weekday"] - 1) * 100

insights = [
    f"{top_cat} is the top revenue category, contributing {top_cat_share:.1f}% of total net revenue.",
    f"Weekend orders generate {weekend_uplift:.1f}% higher average revenue than weekday orders.",
    f"Cancelled + Returned orders make up {(df['order_status'].isin(['Cancelled','Returned']).mean()*100):.1f}% of all orders.",
    f"Total net revenue across the dataset is INR {total_rev:,.0f}.",
]
for i in insights:
    print("-", i)
