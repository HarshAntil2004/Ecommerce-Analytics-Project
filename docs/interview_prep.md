# Interview Preparation — RetailPulse Analytics Project

## SQL Questions

1. **What's the difference between a CTE and a subquery?**
   A CTE (`WITH ... AS`) is named, can be referenced multiple times in the
   same query, and improves readability; a subquery is inline and often
   less reusable. Performance is usually similar — the optimizer treats
   most CTEs like inline views in modern MySQL/Postgres.

2. **Explain the window function `RANK() OVER (PARTITION BY ... ORDER BY ...)` used in this project.**
   `PARTITION BY` resets the ranking per group (e.g., per customer segment);
   `ORDER BY` determines the ranking order within that group. Used here to
   find top 3 customers within each segment without a self-join.

3. **Why use indexes on order_date, category, customer_id, order_status?**
   These are the columns most frequently filtered/grouped/joined on in the
   analysis queries; indexing them speeds up read-heavy analytical queries
   at the cost of slightly slower writes — an acceptable trade-off for an
   analytics workload.

4. **What is RFM analysis and how did you implement it in SQL?**
   Recency, Frequency, Monetary — segments customers by how recently they
   ordered, how often, and how much they spent. Implemented using
   `NTILE(4)` to bucket customers into quartiles per dimension, then summed
   the scores to classify into Champion/Loyal/At Risk/Lost.

5. **Why use a VIEW (`vw_customer_summary`) instead of just running the query each time?**
   Views encapsulate reusable logic for BI tools/dashboards, keep queries
   DRY, and can simplify permissions (grant access to the view, not raw tables).

*(Continue expanding this list to 40 SQL questions covering GROUP BY vs HAVING,
normalization, indexing trade-offs, transaction isolation, etc., as you study.)*

## Python / Pandas Questions

1. **Why use `pd.to_datetime(..., format="mixed", dayfirst=True)` here?**
   The raw data has multiple date formats mixed together (a real-world
   ETL problem); `format="mixed"` lets pandas infer per-value while
   `dayfirst=True` resolves ambiguous DD/MM vs MM/DD cases correctly for
   an India-based dataset.

2. **Why fill `customer_rating` NaN differently than other columns?**
   A missing rating usually means the customer didn't leave one — that's
   meaningful information, not a random gap. Imputing a fake average rating
   would bias the "average rating" KPI, so it's deliberately left as NaN
   and excluded from rating aggregates via `AVG()` (which ignores NULLs).

3. **What's the risk of capping outliers instead of removing rows?**
   Capping keeps the (likely still valid) order rather than losing revenue
   data, but can slightly compress the tail of the distribution — reasonable
   here since only 0.5% of rows are affected.

## Business Analytics / Scenario Questions

1. **If Electronics has the highest revenue but also the highest return rate, what would you recommend?**
   Look at return reasons specifically for Electronics — if it's mostly
   "Damaged Product," focus on packaging/logistics QA rather than pulling
   back marketing spend, since the category is still your top revenue driver.

2. **How would you present the RFM segmentation to a non-technical marketing manager?**
   Translate segments into plain language and action: "Champions — reward
   them, don't spam them. At Risk — win-back campaign now before they churn.
   Lost — deprioritize unless CLV history justifies reactivation spend."

*(Expand this document with the full 40/40/30/30/20/20/20 question sets from
your original brief as you study — this file is meant to be a living document
you keep adding to.)*
