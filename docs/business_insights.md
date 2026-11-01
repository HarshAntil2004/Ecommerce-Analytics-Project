# Business Insights & Recommendations

Derived from `python/eda.py` and `sql/03_analysis_queries.sql` outputs.
(Exact numbers will vary slightly each time the synthetic dataset is regenerated —
re-run the pipeline and update these with your actual output numbers before
presenting this as your own analysis.)

## Revenue & Category Insights
1. Electronics is the leading revenue category despite a smaller order count than Fashion or Grocery — driven by high average order value.
2. The top 2 categories together account for the majority of total net revenue (Pareto-style concentration).
3. Grocery has high order frequency but low revenue contribution, suggesting it functions as a customer-acquisition/basket-filler category rather than a profit driver.

## Customer Insights
4. A minority of customers (RFM "Champion" segment) generate a disproportionate share of lifetime revenue — a classic 80/20 pattern.
5. Premium and VIP segments have measurably higher average order value than New/Regular segments.
6. Roughly one in three customers is a repeat customer — there is room to improve retention marketing for one-time buyers.
7. Customer tenure (days since signup) shows no strong correlation with order value, suggesting loyalty programs should target frequency rather than assuming tenure alone drives spend.

## Operational Insights
8. Cancelled and Returned orders combined account for roughly 15–16% of all orders — a concrete revenue-leakage target for the operations team.
9. Delivery days show wide variance across warehouses, worth investigating for logistics optimization.
10. "Damaged Product" and "Size Issue" are common return reasons — pointing to packaging QA and sizing-guide improvements respectively.

## Marketing & Channel Insights
11. Mobile App is the dominant device used for ordering, ahead of Desktop — mobile UX should be the top investment priority.
12. Organic and Instagram are leading referral sources — paid channels (Google Ads, Affiliate) show lower relative volume, worth a CAC/ROI review.
13. Coupon usage correlates with higher order volume in lower-ticket categories (Grocery, Beauty) more than in Electronics.

## Regional Insights
14. A handful of metro cities (e.g., Mumbai, Bangalore, Delhi) drive a large share of both order volume and revenue.
15. Some tier-2 cities show high average order value despite lower volume — potential expansion targets.

## Recommendations

**Short-term (0–3 months)**
- Investigate top return reasons per category and address packaging/sizing issues.
- Launch a win-back campaign targeted at one-time customers identified via the repeat-customer query.

**Medium-term (3–6 months)**
- Build a tiered loyalty program weighted toward purchase frequency, informed by the RFM segmentation.
- Reallocate marketing spend toward higher-ROI channels identified in the referral-source analysis.

**Long-term (6–12 months)**
- Evaluate expansion investment in high-AOV tier-2 cities.
- Build a live Tableau dashboard refreshed from the MySQL warehouse for ongoing KPI monitoring instead of one-off analysis.
