{{ config(
    materialized='view',
    schema='staging',
    tags=['staging', 'setor_vendas']
) }}

SELECT
    data AS data_venda,
    vendedor_id,
    etapa_funil,
    tipo_atividade,
    data_inicio,
    data_fim,
    inicio_hora,
    fim_hora,
    duracao_min,
    cliente_id,
    resultado,
    valor_venda,
    current_timestamp() AS loaded_at
FROM
    {{ source('bronze', 'quali_vendas') }}