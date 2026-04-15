{{ config(
    materialized='table',
    schema='refined',
    tags=['refined', 'setor_vendas', 'analytics']
) }}

SELECT
    data_atividade,
    vendedor_id,
    etapa_funil,
    resultado,
    COUNT(*) AS total_atividades,
    SUM(duracao_min) AS duracao_total_min,
    AVG(duracao_min) AS duracao_media_min,
    SUM(valor_venda) AS valor_venda_total,
    AVG(valor_venda) AS valor_venda_medio,
    MAX(valor_venda) AS valor_venda_maximo,
    COUNT(CASE WHEN tem_venda = true THEN 1 END) AS qtde_vendas,
    COUNT(CASE WHEN status_negociacao = 'finalizado' THEN 1 END) AS qtde_finalizados,
    COUNT(CASE WHEN status_negociacao = 'em_negociacao' THEN 1 END) AS qtde_em_negociacao
FROM
    {{ ref('trusted_setor_vendas') }}
GROUP BY
    data_atividade,
    vendedor_id,
    etapa_funil,
    resultado