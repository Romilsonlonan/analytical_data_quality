{{ config(
    materialized='table',
    schema='trusted',
    tags=['trusted', 'business']
) }}

SELECT
    o.order_id,
    o.customer_id,
    c.segment AS customer_segment,
    o.order_date,
    o.status,
    o.total_amount,
    o.delivery_address,
    CASE 
        WHEN o.status IN ('delivered', 'completed') THEN TRUE 
        ELSE FALSE 
    END AS is_completed,
    CASE 
        WHEN o.order_date >= CURRENT_DATE - INTERVAL '7 days' THEN TRUE 
        ELSE FALSE 
    END AS is_recent,
    o.created_at,
    o.updated_at,
    o.loaded_at
FROM
    {{ ref('stg_orders') }} o
LEFT JOIN 
    {{ ref('stg_customers') }} c ON o.customer_id = c.customer_id
WHERE
    o.order_id IS NOT NULL
    AND o.customer_id IS NOT NULL
    AND o.order_date IS NOT NULL