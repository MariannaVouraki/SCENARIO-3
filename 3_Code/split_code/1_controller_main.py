# 1_Controller/main.py
from pathlib import Path
from cleaner import clean_and_normalize
from emissions import compute_emissions
from visualizer import visualize_emissions, visualize_energy_consumption


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "Data"
OUT_DIR = BASE_DIR / "4_Output"
OUT_DIR.mkdir(parents=True, exist_ok=True)

excel_path = DATA_DIR / "energy_consumption_thessaloniki_1993-2012.xlsx"
output_excel = OUT_DIR / "thess_energy_analysis.xlsx"
output_emissions_chart = OUT_DIR / "co2_emissions_per_category.png"
output_energy_chart = OUT_DIR / "energy_consumption_per_category.png"

def main():
    df = clean_and_normalize(excel_path)
    df = compute_emissions(df, output_excel)
    visualize_emissions(df, output_emissions_chart)
    visualize_energy_consumption(df, output_energy_chart)

    return output_excel, output_emissions_chart, output_energy_chart


if __name__ == "__main__":
    results = main()
    print("Completed:", results)
