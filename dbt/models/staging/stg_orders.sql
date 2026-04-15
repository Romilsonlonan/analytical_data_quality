{{ config(
    materialized='view',
    schema='staging',
    tags=['staging', 'source']
) }}

SELECT
    order_id,
    customer_id,
    order_date,
    status,
    total_amount,
    delivery_address,
    created_at,
    updated_at,
    '{{ env_var("SOURCE_SYSTEM", "logistics_platform") }}' AS source_system,
    current_timestamp() AS loaded_at
FROM
    {{ source('raw', 'orders') }}
WHERE
    created_at IS NOT NULL