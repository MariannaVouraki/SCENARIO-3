import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# --- Διαδρομές Αρχείων ---
excel_path = Path("energy_consumtion_thessaloniki_1993-2012.xlsx")
output_excel = Path("thess_energy_analysis.xlsx")
output_emissions_chart = Path("o2_emissions_per_category.png")
output_energy_chart = Path("energy_consumption_per_category.png")

# --- Διαβάζουμε το αρχείο (skiprows=1 για να πηδήξουμε την πρώτη γραμμή τίτλου) ---
df = pd.read_excel(excel_path, skiprows=1)

# --- Κανονικοποίηση στηλών ---
df.columns = [
    "Region", "Total", "Domestic", "Commercial", "Industrial",
    "Agricultural", "Public", "Lighting", "Region_EN", "Year"
]

# --- Καθαρισμός ---
df = df[df["Region"].str.contains("Θεσσαλονίκης", na=False)]
df = df.dropna(subset=["Year", "Total"])

# --- Μετατροπή Year ---
df["Year"] = df["Year"].astype(str).str.extract(r"(\d{4})").astype(int)

# --- Υπολογισμός CO2 Εκπομπών ανά κατηγορία ---
# Πηγή: Ενεργειακή ένταση δικτύου Ελλάδας ~256 g CO2eq/kWh (2023 Nowtricity)
emission_factor = 256  # grams CO2 per kWh

for col in ["Domestic", "Commercial", "Industrial", "Agricultural", "Public", "Lighting"]:
    df[f"{col}_CO2_kg"] = df[col] * emission_factor / 1000  # από g σε kg

# --- Αποθήκευση καθαρού και εμπλουτισμένου αρχείου ---
df.to_excel(output_excel, index=False)

# --- Γράφημα Εκπομπών CO2 ανά κατηγορία ---
plt.figure(figsize=(12, 6))
for col in ["Domestic_CO2_kg", "Commercial_CO2_kg", "Industrial_CO2_kg", "Agricultural_CO2_kg", "Public_CO2_kg", "Lighting_CO2_kg"]:
    plt.plot(df["Year"], df[col], label=col.replace("_CO2_kg", ""))

plt.title("Εκπομπές CO2 (kg) ανά Κατηγορία Χρήσης στην Περιφερειακή Ενότητα Θεσσαλονίκης")
plt.xlabel("Έτος")
plt.ylabel("Εκπομπές CO2 (χιλιάδες kg)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(output_emissions_chart)
plt.close()

# --- Γράφημα Κατανάλωσης Ενέργειας ανά κατηγορία ---
plt.figure(figsize=(12, 6))
for col in ["Domestic", "Commercial", "Industrial", "Agricultural", "Public", "Lighting"]:
    plt.plot(df["Year"], df[col], label=col)

plt.title("Κατανάλωση Ηλεκτρικής Ενέργειας (kWh) ανά Κατηγορία Χρήσης")
plt.xlabel("Έτος")
plt.ylabel("Κατανάλωση (σε χιλιάδες kWh)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(output_energy_chart)
plt.close()

# Επιστροφή διαδρομών αρχείων
output_excel, output_emissions_chart, output_energy_chart
