"""
Gold Pipeline - Setor Vendas: Qualitative Sales Data
Carga final com visualização Rich
"""

import sys
import json
from datetime import datetime
from pathlib import Path

import pandas as pd
from rich.console import Console
from rich.table import Table


console = Console()
SILVER_PATH = Path("data/silver/setor-vendas")
GOLD_PATH = Path("data/gold/setor-vendas")


def extract_silver(filename: str | None = None) -> pd.DataFrame:
    if filename:
        df = pd.read_parquet(SILVER_PATH / filename)
    else:
        parquet_files = list(SILVER_PATH.glob("quali_vendas_silver_*.parquet"))
        if not parquet_files:
            raise FileNotFoundError("Nenhum arquivo silver encontrado")
        df = pd.read_parquet(sorted(parquet_files)[-1])
    print(f"Silver: {len(df)} registros")
    return df


def create_metrics(df: pd.DataFrame) -> dict:
    metrics = {}

    metrics["total_registros"] = int(len(df))
    metrics["total_vendas"] = float(df["valor_venda"].sum())
    metrics["total_duracao"] = int(df["duracao_min"].sum())
    metrics["media_duracao"] = float(df["duracao_min"].mean())
    metrics["media_venda"] = float(df["valor_venda"].mean())

    metrics["vendas_por_vendedor"] = {
        k: float(v) for k, v in df.groupby("vendedor_id")["valor_venda"].sum().to_dict().items()
    }
    metrics["atividades_por_vendedor"] = df["vendedor_id"].value_counts().to_dict()
    metrics["vendas_por_etapa"] = {
        k: float(v) for k, v in df.groupby("etapa_funil")["valor_venda"].sum().to_dict().items()
    }
    metrics["atividades_por_tipo"] = df["tipo_atividade"].value_counts().to_dict()
    metrics["vendas_por_resultado"] = {
        k: float(v) for k, v in df.groupby("resultado")["valor_venda"].sum().to_dict().items()
    }

    return metrics


def show_summary(metrics: dict) -> None:
    print("\n" + "=" * 60)
    print("RESUMO GERAL")
    print("=" * 60)
    print(f"Total Registros:    {metrics['total_registros']}")
    print(f"Total Vendas (R$):  R$ {metrics['total_vendas']:,.0f}")
    print(f"Duração Total (min): {metrics['total_duracao']:,}")
    print(f"Média Duração (min): {metrics['media_duracao']:.1f}")
    print(f"Média Venda (R$):    R$ {metrics['media_venda']:,.0f}")
    print("=" * 60)


def show_top_vendedores(df: pd.DataFrame) -> None:
    print("\n" + "=" * 60)
    print("TOP 10 VENDEDORES POR VENDAS")
    print("=" * 60)

    top = (
        df.groupby("vendedor_id")
        .agg({"valor_venda": "sum", "duracao_min": "sum", "cliente_id": "count"})
        .rename(columns={"cliente_id": "atividades"})
        .sort_values("valor_venda", ascending=False)
        .head(10)
    )

    print(f"{'Vendedor':<12} {'Vendas (R$)':<18} {'Duração (min)':<15} {'Atividades':<10}")
    print("-" * 60)
    for idx, row in top.iterrows():
        print(
            f"{idx:<12} R$ {row['valor_venda']:>12,.0f} {row['duracao_min']:>12,} {row['atividades']:>8}"
        )


def show_etapa_funil(df: pd.DataFrame) -> None:
    print("\n" + "=" * 60)
    print("VENDAS POR ETAPA DO FUNIL")
    print("=" * 60)

    etapa = (
        df.groupby("etapa_funil")
        .agg({"valor_venda": "sum", "cliente_id": "count"})
        .rename(columns={"cliente_id": "atividades"})
        .sort_values("valor_venda", ascending=False)
    )

    print(f"{'Etapa':<20} {'Vendas (R$)':<18} {'Atividades':<10}")
    print("-" * 60)
    for idx, row in etapa.iterrows():
        print(f"{idx:<20} R$ {row['valor_venda']:>12,.0f} {row['atividades']:>8}")


def show_resultados(df: pd.DataFrame) -> None:
    print("\n" + "=" * 60)
    print("VENDAS POR RESULTADO")
    print("=" * 60)

    resultado = (
        df.groupby("resultado")
        .agg({"valor_venda": "sum", "cliente_id": "count"})
        .rename(columns={"cliente_id": "atividades"})
        .sort_values("valor_venda", ascending=False)
    )

    print(f"{'Resultado':<20} {'Vendas (R$)':<18} {'Atividades':<10}")
    print("-" * 60)
    for idx, row in resultado.iterrows():
        print(f"{idx:<20} R$ {row['valor_venda']:>12,.0f} {row['atividades']:>8}")


def show_tipo_atividade(df: pd.DataFrame) -> None:
    print("\n" + "=" * 60)
    print("TOP 10 TIPOS DE ATIVIDADE")
    print("=" * 60)

    tipo = (
        df.groupby("tipo_atividade")
        .agg({"duracao_min": "mean", "cliente_id": "count"})
        .rename(columns={"cliente_id": "quantidade"})
        .sort_values("quantidade", ascending=False)
        .head(10)
    )

    print(f"{'Tipo Atividade':<25} {'Média Duração (min)':<20} {'Quantidade':<10}")
    print("-" * 60)
    for idx, row in tipo.iterrows():
        print(f"{idx:<25} {row['duracao_min']:>15,.1f} {int(row['quantidade']):>8}")


def show_data_preview(df: pd.DataFrame) -> None:
    print("\n" + "=" * 60)
    print("PRÉVIA DOS DADOS")
    print("=" * 60)

    cols = [
        "data",
        "vendedor_id",
        "etapa_funil",
        "tipo_atividade",
        "duracao_min",
        "resultado",
        "valor_venda",
    ]
    print(df[cols].head(10).to_string(index=False))


def save_gold(df: pd.DataFrame, metrics: dict, filename: str) -> Path:
    GOLD_PATH.mkdir(parents=True, exist_ok=True)
    output_path = GOLD_PATH / f"{filename}.parquet"
    df.to_parquet(output_path, index=False)

    metrics_path = GOLD_PATH / f"{filename}_metrics.json"
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=2, default=str)

    print(f"\nDados salvos em: {output_path}")
    print(f"Métricas salvas em: {metrics_path}")

    return output_path


def run(silver_filename: str | None = None) -> dict:
    print("\n" + "=" * 60)
    print("GOLD PIPELINE - SETOR VENDAS")
    print("=" * 60 + "\n")

    try:
        df = extract_silver(silver_filename)

        print("Criando métricas...")
        metrics = create_metrics(df)

        show_summary(metrics)
        show_top_vendedores(df)
        show_etapa_funil(df)
        show_resultados(df)
        show_tipo_atividade(df)
        show_data_preview(df)

        output_path = save_gold(
            df, metrics, f"quali_vendas_gold_{datetime.now().strftime('%Y%m%d')}"
        )

        print("\n" + "=" * 60)
        print(f"Carga Concluída: {output_path.name}")
        print(f"Registros: {len(df)}")
        print("=" * 60 + "\n")

        return {"status": "success", "rows": len(df), "output_path": str(output_path)}

    except Exception as e:
        print(f"\nErro: {str(e)}\n")
        import traceback

        traceback.print_exc()
        return {"status": "error", "error": str(e)}


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "success" else 1)
