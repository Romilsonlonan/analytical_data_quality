{{ config(
    materialized='table',
    schema='trusted',
    tags=['trusted', 'setor_vendas']
) }}

SELECT
    data AS data_venda,
    vendedor_id,
    etapa_funil,
    tipo_atividade,
    duracao_min,
    cliente_id,
    resultado,
    valor_venda,
    DATE(data_inicio) AS data_atividade,
    inicio_hora,
    fim_hora,
    CASE 
        WHEN resultado IN ('ganho', 'perdido') THEN 'finalizado'
        WHEN resultado IN ('em_andamento', 'proposta_enviada', 'ajustes') THEN 'em_negociacao'
        ELSE 'outros'
    END AS status_negociacao,
    CASE
        WHEN valor_venda > 0 THEN true
        ELSE false
    END AS tem_venda
FROM
    {{ ref('stg_setor_vendas') }}