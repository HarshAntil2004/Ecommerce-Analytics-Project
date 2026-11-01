-- =========================================================
-- RetailPulse Analytics - Schema Creation
-- =========================================================
-- Star-schema-inspired design: one fact table (orders) plus
-- lookup/dimension tables for customers. Kept simple on purpose
-- (fresher-appropriate) while still demonstrating PK/FK/index usage.

CREATE DATABASE IF NOT EXISTS retailpulse;
USE retailpulse;

DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id       VARCHAR(10) PRIMARY KEY,
    customer_age      INT,
    customer_gender   VARCHAR(20),
    customer_segment  VARCHAR(20),
    signup_date       DATE,
    city              VARCHAR(50),
    state             VARCHAR(50)
);

CREATE TABLE orders (
    order_id            VARCHAR(12) PRIMARY KEY,
    customer_id         VARCHAR(10),
    order_date          DATE NOT NULL,
    category            VARCHAR(50),
    product_name        VARCHAR(100),
    quantity            INT CHECK (quantity >= 0),
    unit_price          DECIMAL(12,2) CHECK (unit_price >= 0),
    discount_pct        DECIMAL(5,2) DEFAULT 0,
    gross_revenue       DECIMAL(14,2),
    net_revenue         DECIMAL(14,2),
    payment_method      VARCHAR(30),
    order_status        VARCHAR(20),
    delivery_days       INT,
    shipping_cost       DECIMAL(10,2),
    customer_rating     DECIMAL(2,1),
    is_prime_member     BOOLEAN,
    coupon_used         VARCHAR(5),
    warehouse_id        VARCHAR(10),
    device_used         VARCHAR(30),
    referral_source     VARCHAR(30),
    CONSTRAINT fk_orders_customer FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
);

-- Indexes to speed up the analytical queries in 03_analysis_queries.sql
CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_orders_category ON orders(category);
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_status ON orders(order_status);
