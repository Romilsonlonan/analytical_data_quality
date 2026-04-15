{{ config(
    materialized='table',
    schema='refined',
    tags=['refined', 'analytics']
) }}

SELECT
    DATE_TRUNC('day', order_date) AS order_date,
    status,
    customer_segment,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(total_amount) AS total_revenue,
    AVG(total_amount) AS avg_order_value,
    COUNT(DISTINCT customer_id) AS unique_customers,
    MIN(total_amount) AS min_order_value,
    MAX(total_amount) AS max_order_value,
    current_timestamp() AS computed_at
FROM
    {{ ref('trusted_orders') }}
GROUP BY
    DATE_TRUNC('day', order_date),
    status,
    customer_segment