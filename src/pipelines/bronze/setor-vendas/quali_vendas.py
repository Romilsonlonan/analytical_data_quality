"""
Bronze Pipeline - Setor Vendas: Qualitative Sales Data
Extração simples de dados brutos para a camada Bronze
"""

import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

BRONZE_PATH = Path("data/bronze/setor-vendas")
SPREADSHEET_URL = (
    "https://docs.google.com/spreadsheets/d/1vV7b1eXG6OPrLgBqbTvhR9OSMz8HnfBgI-jC5VfJP78/edit?gid=0"
)


def extract_google_sheets(url: str) -> pd.DataFrame:
    csv_url = url.replace("/edit?gid=0", "/export?format=csv")
    return pd.read_csv(csv_url)


def extract_excel(file_path: str) -> pd.DataFrame:
    return pd.read_excel(file_path)


def save_bronze(df: pd.DataFrame, filename: str) -> Path:
    BRONZE_PATH.mkdir(parents=True, exist_ok=True)
    output_path = BRONZE_PATH / f"{filename}.parquet"
    df.to_parquet(output_path, index=False)
    return output_path


def run(
    source: str = "google_sheets", url: str | None = None, file_path: str | None = None
) -> dict:
    print("\n" + "=" * 80)
    print("BRONZE PIPELINE - SETOR VENDAS")
    print("=" * 80 + "\n")

    try:
        if source == "google_sheets":
            df = extract_google_sheets(url or SPREADSHEET_URL)
        elif source == "excel":
            if file_path is None:
                raise ValueError("file_path é obrigatório")
            df = extract_excel(file_path)
        else:
            raise ValueError(f"Source inválido: {source}")

        print(df.to_string())

        output_path = save_bronze(df, f"quali_vendas_{datetime.now().strftime('%Y%m%d')}")

        print("\n" + "=" * 80)
        print(f"Concluído: {output_path.name}")
        print(f"Registros: {len(df)}")
        print("=" * 80 + "\n")

        return {"status": "success", "rows": len(df), "output_path": str(output_path)}

    except Exception as e:
        print(f"\nErro: {str(e)}\n")
        return {"status": "error", "error": str(e)}


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "success" else 1)
