# 2_Services/emissions.py
import pandas as pd
from pathlib import Path

def compute_emissions(df: pd.DataFrame, out_xlsx: Path) -> pd.DataFrame:
    emission_factor = 256

    for col in ["Domestic", "Commercial", "Industrial", "Agricultural", "Public", "Lighting"]:
        df[f"{col}_CO2_kg"] = df[col] * emission_factor / 1000

    df.to_excel(out_xlsx, index=False)
    return df
