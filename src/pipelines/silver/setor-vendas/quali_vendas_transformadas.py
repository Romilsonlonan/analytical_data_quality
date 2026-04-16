"""
Silver Pipeline - Setor Vendas: Qualitative Sales Data
Transformações simples: tipagem e separar hora de inicio/fim
"""

import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

BRONZE_PATH = Path("data/bronze/setor-vendas")
SILVER_PATH = Path("data/silver/setor-vendas")


def extract_bronze(filename: str | None = None) -> pd.DataFrame:
    if filename:
        df = pd.read_parquet(BRONZE_PATH / filename)
    else:
        parquet_files = list(BRONZE_PATH.glob("quali_vendas_*.parquet"))
        if not parquet_files:
            raise FileNotFoundError("Nenhum arquivo bronze encontrado")
        df = pd.read_parquet(sorted(parquet_files)[-1])
    print(f"Bronze: {len(df)} registros")
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    initial_rows = len(df)

    df = df.drop_duplicates()
    df = df.dropna(how="all")

    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].str.strip()
            df[col] = df[col].replace("", None)
            df[col] = df[col].replace("null", None)
            df[col] = df[col].replace("None", None)
            df[col] = df[col].replace("nan", None)
            df[col] = df[col].replace("NaN", None)

    df = df.dropna(subset=["data", "vendedor_id"])

    final_rows = len(df)
    removed = initial_rows - final_rows
    if removed > 0:
        print(f"Limpeza: {removed} registros removidos")

    return df


def transform_types(df: pd.DataFrame) -> pd.DataFrame:
    df["data"] = pd.to_datetime(df["data"], format="%Y-%m-%d", errors="coerce").dt.date
    df["data_inicio"] = pd.to_datetime(df["inicio"], format="%Y-%m-%d %H:%M", errors="coerce")
    df["data_fim"] = pd.to_datetime(df["fim"], format="%Y-%m-%d %H:%M", errors="coerce")

    df["inicio_hora"] = df["data_inicio"].dt.strftime("%H:%M")
    df["fim_hora"] = df["data_fim"].dt.strftime("%H:%M")

    df = df.drop(columns=["inicio", "fim"])

    df["duracao_min"] = pd.to_numeric(df["duracao_min"], errors="coerce").fillna(0).astype(int)
    df["valor_venda"] = pd.to_numeric(df["valor_venda"], errors="coerce").fillna(0).astype(int)

    return df


def check_data_quality(df: pd.DataFrame) -> dict:
    issues = {}

    null_by_col = df.isnull().sum()
    null_cols = null_by_col[null_by_col > 0]
    if len(null_cols) > 0:
        issues["valores_nulos"] = null_cols.to_dict()

    return issues


def save_silver(df: pd.DataFrame, filename: str) -> Path:
    SILVER_PATH.mkdir(parents=True, exist_ok=True)
    output_path = SILVER_PATH / f"{filename}.parquet"
    df.to_parquet(output_path, index=False)
    return output_path


def run(bronze_filename: str | None = None) -> dict:
    print("\n" + "=" * 80)
    print("SILVER PIPELINE - SETOR VENDAS")
    print("=" * 80 + "\n")

    try:
        df = extract_bronze(bronze_filename)

        print("1. Limpeza de dados...")
        df = clean_data(df)

        print("2. Transformação de tipos...")
        df = transform_types(df)

        print("3. Verificação de qualidade...")
        issues = check_data_quality(df)
        if issues:
            for key, val in issues.items():
                print(f"  - {key}: {val}")
        else:
            print("  ✓ Sem issues")

        output_path = save_silver(df, f"quali_vendas_silver_{datetime.now().strftime('%Y%m%d')}")

        print("\n" + "=" * 80)
        print(f"Concluído: {output_path.name}")
        print(f"Registros: {len(df)}")
        print(f"Colunas: {len(df.columns)}")
        print("=" * 80 + "\n")

        print(df.head().to_string())

        return {"status": "success", "rows": len(df), "output_path": str(output_path)}

    except Exception as e:
        print(f"\nErro: {str(e)}\n")
        return {"status": "error", "error": str(e)}


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "success" else 1)
