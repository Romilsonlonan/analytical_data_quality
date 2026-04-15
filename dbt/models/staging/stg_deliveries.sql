{{ config(
    materialized='view',
    schema='staging',
    tags=['staging', 'source']
) }}

SELECT
    delivery_id,
    order_id,
    carrier_id,
    driver_id,
    delivery_date,
    status,
    created_at,
    updated_at,
    '{{ env_var("SOURCE_SYSTEM", "logistics_platform") }}' AS source_system,
    current_timestamp() AS loaded_at
FROM
    {{ source('raw', 'deliveries') }}
WHERE
    created_at IS NOT NULL