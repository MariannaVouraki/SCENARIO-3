# 3_Code/script.py
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ===============================
# Paths relative to this script
# ===============================
BASE_DIR = Path(__file__).resolve().parent.parent  # project root (πάνω από 3_Code)
DATA_DIR = BASE_DIR / "Data"
OUT_DIR = BASE_DIR / "4_Output"
OUT_DIR.mkdir(parents=True, exist_ok=True)

excel_path = DATA_DIR / "energy_consumption_thessaloniki_1993-2012.xlsx"
output_excel = OUT_DIR / "thess_energy_analysis.xlsx"
output_emissions_chart = OUT_DIR / "co2_emissions_per_category.png"
output_energy_chart = OUT_DIR / "energy_consumption_per_category.png"

# ===============================
# 1) CLEAN & NORMALIZE
# ===============================
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

# ===============================
# 2) COMPUTE EMISSIONS (CO2)
# ===============================
def compute_emissions(df: pd.DataFrame, out_xlsx: Path) -> pd.DataFrame:
    emission_factor = 256  # g CO2 per kWh
    for col in ["Domestic", "Commercial", "Industrial", "Agricultural", "Public", "Lighting"]:
        df[f"{col}_CO2_kg"] = df[col] * emission_factor / 1000  # g → kg
    df.to_excel(out_xlsx, index=False)
    return df

# ===============================
# 3) VISUALIZE (EMISSIONS & ENERGY)
# ===============================
def visualize_emissions(df: pd.DataFrame, out_png: Path) -> Path:
    plt.figure(figsize=(12, 6))
    for col in [
        "Domestic_CO2_kg", "Commercial_CO2_kg", "Industrial_CO2_kg",
        "Agricultural_CO2_kg", "Public_CO2_kg", "Lighting_CO2_kg"
    ]:
        plt.plot(df["Year"], df[col], label=col.replace("_CO2_kg", ""))
    plt.title("Εκπομπές CO2 (kg) ανά Κατηγορία Χρήσης στην Περιφερειακή Ενότητα Θεσσαλονίκης")
    plt.xlabel("Έτος")
    plt.ylabel("Εκπομπές CO2 (χιλιάδες kg)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out_png)
    plt.close()
    return out_png

def visualize_energy_consumption(df: pd.DataFrame, out_png: Path) -> Path:
    plt.figure(figsize=(12, 6))
    for col in ["Domestic", "Commercial", "Industrial", "Agricultural", "Public", "Lighting"]:
        plt.plot(df["Year"], df[col], label=col)
    plt.title("Κατανάλωση Ηλεκτρικής Ενέργειας (kWh) ανά Κατηγορία Χρήσης")
    plt.xlabel("Έτος")
    plt.ylabel("Κατανάλωση (σε χιλιάδες kWh)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out_png)
    plt.close()
    return out_png

# ===============================
# Run
# ===============================
if __name__ == "__main__":
    df = clean_and_normalize(excel_path)
    df = compute_emissions(df, output_excel)
    visualize_emissions(df, output_emissions_chart)
    visualize_energy_consumption(df, output_energy_chart)

    # ίδια “επιστροφή” όπως στο αρχικό σκριπτ:
    result = (output_excel, output_emissions_chart, output_energy_chart)
