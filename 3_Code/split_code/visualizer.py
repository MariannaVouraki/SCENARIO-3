# 2_Services/visualizer.py
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def visualize_emissions(df: pd.DataFrame, out_png: Path) -> Path:
    plt.figure(figsize=(12, 6))

    for col in [
        "Domestic_CO2_kg", "Commercial_CO2_kg", "Industrial_CO2_kg",
        "Agricultural_CO2_kg", "Public_CO2_kg", "Lighting_CO2_kg"
    ]:
        plt.plot(df["Year"], df[col], label=col.replace("_CO2_kg", ""))

    plt.title("Εκπομπές CO2 (kg) ανά κατηγορία")
    plt.xlabel("Έτος")
    plt.ylabel("Εκπομπές CO2 (kg)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_png)
    plt.close()
    return out_png


def visualize_energy_consumption(df: pd.DataFrame, out_png: Path) -> Path:
    plt.figure(figsize=(12, 6))

    for col in ["Domestic", "Commercial", "Industrial", "Agricultural", "Public", "Lighting"]:
        plt.plot(df["Year"], df[col], label=col)

    plt.title("Κατανάλωση ενέργειας (kWh) ανά κατηγορία")
    plt.xlabel("Έτος")
    plt.ylabel("kWh")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_png)
    plt.close()
    return out_png
