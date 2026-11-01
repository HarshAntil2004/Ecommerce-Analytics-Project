-- =========================================================
-- RetailPulse Analytics - Business SQL Queries
-- =========================================================
USE retailpulse;

-- 1. TOP 10 CUSTOMERS BY LIFETIME REVENUE
-- Business question: Who are our most valuable customers (for VIP treatment / retention)?
SELECT c.customer_id, c.customer_segment, c.city,
       ROUND(SUM(o.net_revenue), 2) AS lifetime_revenue,
       COUNT(o.order_id) AS total_orders
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_segment, c.city
ORDER BY lifetime_revenue DESC
LIMIT 10;


-- 2. MONTHLY REVENUE TREND WITH MoM GROWTH %
-- Business question: Is revenue growing month over month?
WITH monthly AS (
    SELECT DATE_FORMAT(order_date, '%Y-%m') AS ym,
           SUM(net_revenue) AS revenue
    FROM orders
    GROUP BY ym
)
SELECT ym, revenue,
       ROUND(100.0 * (revenue - LAG(revenue) OVER (ORDER BY ym))
             / LAG(revenue) OVER (ORDER BY ym), 2) AS mom_growth_pct
FROM monthly
ORDER BY ym;


-- 3. RUNNING TOTAL (CUMULATIVE) REVENUE BY MONTH
-- Business question: What does our cumulative revenue trajectory look like this year?
SELECT DATE_FORMAT(order_date, '%Y-%m') AS ym,
       SUM(net_revenue) AS monthly_revenue,
       SUM(SUM(net_revenue)) OVER (ORDER BY DATE_FORMAT(order_date, '%Y-%m')) AS running_total
FROM orders
GROUP BY ym
ORDER BY ym;


-- 4. CATEGORY REVENUE CONTRIBUTION % (PARETO-STYLE)
-- Business question: Which categories drive most of our revenue (80/20 rule)?
WITH cat_rev AS (
    SELECT category, SUM(net_revenue) AS revenue
    FROM orders
    GROUP BY category
)
SELECT category, revenue,
       ROUND(100.0 * revenue / SUM(revenue) OVER (), 2) AS pct_of_total,
       ROUND(100.0 * SUM(revenue) OVER (ORDER BY revenue DESC) / SUM(revenue) OVER (), 2) AS cumulative_pct
FROM cat_rev
ORDER BY revenue DESC;


-- 5. CUSTOMER RANKING WITHIN EACH SEGMENT (WINDOW + RANK)
-- Business question: Who is the top customer within each segment (New/Regular/Premium/VIP)?
SELECT customer_id, customer_segment, total_spent, rnk
FROM (
    SELECT c.customer_id, c.customer_segment,
           SUM(o.net_revenue) AS total_spent,
           RANK() OVER (PARTITION BY c.customer_segment ORDER BY SUM(o.net_revenue) DESC) AS rnk
    FROM orders o
    JOIN customers c ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.customer_segment
) ranked
WHERE rnk <= 3
ORDER BY customer_segment, rnk;


-- 6. 3-MONTH MOVING AVERAGE OF REVENUE
-- Business question: What is the smoothed revenue trend, ignoring monthly noise?
WITH monthly AS (
    SELECT DATE_FORMAT(order_date, '%Y-%m') AS ym, SUM(net_revenue) AS revenue
    FROM orders GROUP BY ym
)
SELECT ym, revenue,
       ROUND(AVG(revenue) OVER (ORDER BY ym ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) AS moving_avg_3m
FROM monthly
ORDER BY ym;


-- 7. REPEAT CUSTOMER ANALYSIS
-- Business question: What % of customers order more than once (loyalty indicator)?
SELECT
    CASE WHEN order_count = 1 THEN 'One-time' ELSE 'Repeat' END AS customer_type,
    COUNT(*) AS num_customers,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS pct_of_customers
FROM (
    SELECT customer_id, COUNT(*) AS order_count
    FROM orders
    GROUP BY customer_id
) t
GROUP BY customer_type;


-- 8. SIMPLIFIED RFM SEGMENTATION (Recency, Frequency, Monetary)
-- Business question: Which customers are high value vs at-risk, for targeted marketing?
WITH rfm AS (
    SELECT customer_id,
           DATEDIFF(CURDATE(), MAX(order_date)) AS recency_days,
           COUNT(*) AS frequency,
           SUM(net_revenue) AS monetary
    FROM orders
    GROUP BY customer_id
),
scored AS (
    SELECT *,
           NTILE(4) OVER (ORDER BY recency_days DESC) AS r_score,
           NTILE(4) OVER (ORDER BY frequency ASC) AS f_score,
           NTILE(4) OVER (ORDER BY monetary ASC) AS m_score
    FROM rfm
)
SELECT customer_id, recency_days, frequency, monetary,
       (r_score + f_score + m_score) AS rfm_total,
       CASE
           WHEN (r_score + f_score + m_score) >= 10 THEN 'Champion'
           WHEN (r_score + f_score + m_score) >= 7 THEN 'Loyal'
           WHEN (r_score + f_score + m_score) >= 4 THEN 'At Risk'
           ELSE 'Lost'
       END AS rfm_segment
FROM scored
ORDER BY rfm_total DESC;


-- 9. BEST PERFORMING CITIES (REGIONAL PERFORMANCE)
-- Business question: Where should we expand warehouse/marketing investment?
SELECT c.city, c.state,
       COUNT(o.order_id) AS total_orders,
       ROUND(SUM(o.net_revenue), 2) AS revenue,
       ROUND(AVG(o.net_revenue), 2) AS avg_order_value
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
GROUP BY c.city, c.state
HAVING COUNT(o.order_id) > 50
ORDER BY revenue DESC
LIMIT 10;


-- 10. MOST PROFITABLE PRODUCTS (BY AVG ORDER VALUE, FILTERED)
-- Business question: Which products should we push in marketing campaigns?
SELECT product_name, category,
       COUNT(*) AS orders_count,
       ROUND(AVG(net_revenue), 2) AS avg_revenue_per_order,
       ROUND(SUM(net_revenue), 2) AS total_revenue
FROM orders
WHERE order_status NOT IN ('Cancelled', 'Returned')
GROUP BY product_name, category
HAVING COUNT(*) >= 30
ORDER BY total_revenue DESC
LIMIT 15;


-- 11. YEAR-OVER-YEAR (YoY) GROWTH BY CATEGORY
-- Business question: Which categories are growing/declining year over year?
WITH yearly AS (
    SELECT category, YEAR(order_date) AS yr, SUM(net_revenue) AS revenue
    FROM orders
    GROUP BY category, yr
)
SELECT category, yr, revenue,
       LAG(revenue) OVER (PARTITION BY category ORDER BY yr) AS prev_year_revenue,
       ROUND(100.0 * (revenue - LAG(revenue) OVER (PARTITION BY category ORDER BY yr))
             / LAG(revenue) OVER (PARTITION BY category ORDER BY yr), 2) AS yoy_growth_pct
FROM yearly
ORDER BY category, yr;


-- 12. VIEW: CUSTOMER 360 SUMMARY (reusable object for dashboards/BI tools)
CREATE OR REPLACE VIEW vw_customer_summary AS
SELECT c.customer_id, c.customer_segment, c.city, c.state,
       COUNT(o.order_id) AS total_orders,
       ROUND(SUM(o.net_revenue), 2) AS lifetime_value,
       ROUND(AVG(o.customer_rating), 2) AS avg_rating,
       MAX(o.order_date) AS last_order_date
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.customer_segment, c.city, c.state;
