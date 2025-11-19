# 2_Services/cleaner.py
import pandas as pd
from pathlib import Path

def clean_and_normalize(path: Path) -> pd.DataFrame:
    df = pd.read_excel(path, skiprows=1)
    df.columns = [
        "Region", "Total", "Domestic", "Commercial", "Industrial",
        "Agricultural", "Public", "Lighting", "Region_EN", "Year"
    ]
    df = df[df["Region"].str.contains("Θεσσαλονίκης", na=False)]
    df = df.dropna(subset=["Year", "Total"])
    df["Year"] = df["Year"].astype(str).str.extract(r"(\d{4})").astype(int)
    return df
