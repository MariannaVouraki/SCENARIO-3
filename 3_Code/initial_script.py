# 3_Code/initial_script.py
"""
MDAT Scenario 3 - Energy Consumption & CO2 Emissions
Thessaloniki Regional Unit, 1993-2012

Uses time-varying historical emission factors from Ember / Our World in Data.
All emission factors share the SAME methodology (lifecycle emissions),
ensuring that cross-year comparisons reflect real changes in the grid mix
rather than methodological differences.
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ===============================
# Paths
# ===============================
SCRIPT_DIR = Path(__file__).resolve().parent           # 3_Code/
BASE_DIR = SCRIPT_DIR.parent                            # SCENARIO-3/
DATA_DIR = SCRIPT_DIR / "Data"                          # 3_Code/Data/
OUT_DIR = BASE_DIR / "4_Output"                         # SCENARIO-3/4_Output/
OUT_DIR.mkdir(parents=True, exist_ok=True)

excel_path = DATA_DIR / "energy_consumption_thessaloniki_1993-2012.xlsx"
output_excel = OUT_DIR / "thess_energy_analysis.xlsx"
output_emissions_chart = OUT_DIR / "co2_emissions_per_category.png"
output_energy_chart = OUT_DIR / "energy_consumption_per_category.png"
output_factor_chart = OUT_DIR / "emission_factor_evolution.png"
output_factor_extended_chart = OUT_DIR / "emission_factor_extended_1993_2025.png"
output_comparison_chart = OUT_DIR / "co2_total_current_vs_historical.png"

# ===============================
# Configuration: Emission factors
# ===============================
# Reference (latest) emission factor for the Greek grid
# Source: Ember Yearly Electricity Data (2025) - lifecycle emissions
EMISSION_FACTOR_CURRENT = 315.09       # g CO2 / kWh, lifecycle
EMISSION_FACTOR_CURRENT_YEAR = 2025    # reference year

# Historical time-varying emission factors for the Greek grid (g CO2/kWh)
# Source: Ember Yearly Electricity Data (2025), via Our World in Data
# Methodology: Lifecycle emissions (upstream methane + supply chain +
# manufacturing), CO2-equivalent over 100-year timescale.
EMISSION_FACTORS_HISTORICAL = {
    1993: 877.02,
    1994: 875.81,
    1995: 848.80,
    1996: 835.19,
    1997: 850.50,
    1998: 850.77,
    1999: 819.80,
    2000: 822.82,
    2001: 845.64,
    2002: 827.59,
    2003: 790.33,
    2004: 786.16,
    2005: 782.56,
    2006: 743.14,
    2007: 776.92,
    2008: 758.93,
    2009: 747.10,
    2010: 707.30,
    2011: 725.06,
    2012: 704.06,
}

# Extended series 2013-2025 — used ONLY for the bonus chart (context)
# Same source/methodology as the historical series above
EMISSION_FACTORS_POST_2012 = {
    2013: 636.69,
    2014: 667.88,
    2015: 603.53,
    2016: 571.51,
    2017: 579.75,
    2018: 545.14,
    2019: 496.98,
    2020: 423.07,
    2021: 383.11,
    2022: 376.81,
    2023: 336.40,
    2024: 321.65,
    2025: 315.09,
}

CATEGORIES = ["Domestic", "Commercial", "Industrial",
              "Agricultural", "Public", "Lighting"]

CATEGORY_LABELS = {
    "Domestic": "Οικιακή",
    "Commercial": "Εμπορική",
    "Industrial": "Βιομηχανική",
    "Agricultural": "Γεωργική",
    "Public": "Δημόσιες Αρχές",
    "Lighting": "Φωτισμός Οδών",
}


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

    # Force-convert numeric columns to float (handles comma decimals etc.)
    numeric_cols = ["Total", "Domestic", "Commercial", "Industrial",
                    "Agricultural", "Public", "Lighting"]
    for col in numeric_cols:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", ".", regex=False)
            .str.replace(" ", "", regex=False)
        )
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=numeric_cols)
    df = df.sort_values("Year").reset_index(drop=True)
    return df


# ===============================
# 2) COMPUTE EMISSIONS
# ===============================
def compute_emissions(df: pd.DataFrame, out_xlsx: Path) -> pd.DataFrame:
    df["EmissionFactor_Historical_gCO2_kWh"] = df["Year"].map(EMISSION_FACTORS_HISTORICAL)
    df["EmissionFactor_Current_gCO2_kWh"] = EMISSION_FACTOR_CURRENT

    for col in CATEGORIES:
        df[f"{col}_CO2_kg_current"] = df[col] * EMISSION_FACTOR_CURRENT / 1000

    for col in CATEGORIES:
        df[f"{col}_CO2_kg_historical"] = (
            df[col] * df["EmissionFactor_Historical_gCO2_kWh"] / 1000
        )

    df["Total_CO2_kg_current"] = df[[f"{c}_CO2_kg_current" for c in CATEGORIES]].sum(axis=1)
    df["Total_CO2_kg_historical"] = df[[f"{c}_CO2_kg_historical" for c in CATEGORIES]].sum(axis=1)
    df["Ratio_Historical_to_Current"] = (
        df["Total_CO2_kg_historical"] / df["Total_CO2_kg_current"]
    ).round(2)

    _export_to_excel(df, out_xlsx)
    return df


def _export_to_excel(df: pd.DataFrame, out_xlsx: Path) -> None:
    f_min = min(EMISSION_FACTORS_HISTORICAL.values())
    f_max = max(EMISSION_FACTORS_HISTORICAL.values())
    f_mean = sum(EMISSION_FACTORS_HISTORICAL.values()) / len(EMISSION_FACTORS_HISTORICAL)

    metadata = pd.DataFrame({
        "Property": [
            "Dataset Title",
            "Temporal Coverage",
            "Geographic Scope",
            "Reference Emission Factor (gCO2/kWh)",
            "Reference Emission Factor Year",
            "Reference Emission Factor Source",
            "Historical Emission Factor Range (gCO2/kWh)",
            "Historical Emission Factor Mean (gCO2/kWh)",
            "Historical Emission Factor Source",
            "Methodology",
            "DPV Process Mapping",
            "ODRL Action Mapping",
            "MDAT Concept",
        ],
        "Value": [
            "Electricity consumption and CO2 emissions, Thessaloniki",
            "1993-2012",
            "Regional Unit of Thessaloniki",
            EMISSION_FACTOR_CURRENT,
            EMISSION_FACTOR_CURRENT_YEAR,
            "Ember Yearly Electricity Data (2025) - lifecycle emissions",
            f"{f_min:.2f}-{f_max:.2f}",
            f"{f_mean:.2f}",
            "Ember Yearly Electricity Data (2025) via Our World in Data",
            "Lifecycle emissions (upstream methane + supply chain + manufacturing), "
            "CO2-equivalent over 100-year timescale",
            "dpv:Transform -> dpv:Derive -> dpv:Visualise",
            "odrl:modify -> odrl:derive -> odrl:display",
            "mdat:EnergyDataset -> mdat:CO2EmissionDataset -> mdat:EnergyEmissionVisualisation",
        ]
    })

    factors_table = pd.DataFrame(
        sorted(EMISSION_FACTORS_HISTORICAL.items()),
        columns=["Year", "EmissionFactor_gCO2_kWh"]
    )
    factors_table["Source"] = "Ember / Our World in Data (Greek grid, lifecycle emissions)"

    with pd.ExcelWriter(out_xlsx, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Analysis", index=False)
        factors_table.to_excel(writer, sheet_name="EmissionFactors", index=False)
        metadata.to_excel(writer, sheet_name="Metadata", index=False)


# ===============================
# 3) VISUALIZE
# ===============================
def visualize_energy_consumption(df: pd.DataFrame, out_png: Path) -> Path:
    plt.figure(figsize=(12, 6))
    for col in CATEGORIES:
        plt.plot(df["Year"], df[col], label=CATEGORY_LABELS[col],
                 linewidth=2, marker="o", markersize=3)
    plt.title("Κατανάλωση Ηλεκτρικής Ενέργειας (kWh) ανά Κατηγορία Χρήσης\n"
              "Περιφερειακή Ενότητα Θεσσαλονίκης (1993-2012)")
    plt.xlabel("Έτος")
    plt.ylabel("Κατανάλωση (kWh)")
    plt.legend(loc="best")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_png, dpi=120)
    plt.close()
    return out_png


def visualize_emissions_historical(df: pd.DataFrame, out_png: Path) -> Path:
    f_min = min(EMISSION_FACTORS_HISTORICAL.values())
    f_max = max(EMISSION_FACTORS_HISTORICAL.values())

    plt.figure(figsize=(12, 6))
    for col in CATEGORIES:
        plt.plot(df["Year"], df[f"{col}_CO2_kg_historical"],
                 label=CATEGORY_LABELS[col], linewidth=2, marker="o", markersize=3)
    plt.title("Εκπομπές CO2 (kg) ανά Κατηγορία Χρήσης - Ιστορικά Δεδομένα\n"
              f"Με χρονομεταβλητό συντελεστή {f_min:.0f}-{f_max:.0f} g CO2/kWh "
              "(Ember / Our World in Data)")
    plt.xlabel("Έτος")
    plt.ylabel("Εκπομπές CO2 (kg)")
    plt.legend(loc="best")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_png, dpi=120)
    plt.close()
    return out_png


def visualize_emission_factor_evolution(out_png: Path) -> Path:
    """Standard plot — only the study period 1993-2012."""
    years = sorted(EMISSION_FACTORS_HISTORICAL.keys())
    values = [EMISSION_FACTORS_HISTORICAL[y] for y in years]

    plt.figure(figsize=(12, 6))
    plt.plot(years, values, color="#C44536", linewidth=2.5, marker="o",
             markersize=5, label="Ιστορικός συντελεστής (Ember/OWID)")
    plt.axhline(y=EMISSION_FACTOR_CURRENT, color="#2E8B57", linestyle="--",
                linewidth=2,
                label=f"Συντελεστής αναφοράς ({EMISSION_FACTOR_CURRENT_YEAR}): "
                      f"{EMISSION_FACTOR_CURRENT:.1f} g CO2/kWh")
    plt.title("Διαχρονική Εξέλιξη του Συντελεστή Εκπομπών CO2\n"
              "Ελληνικό Δίκτυο Ηλεκτρικής Ενέργειας (1993-2012)")
    plt.xlabel("Έτος")
    plt.ylabel("Συντελεστής εκπομπών (g CO2/kWh)")
    plt.legend(loc="upper right")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_png, dpi=120)
    plt.close()
    return out_png


def visualize_emission_factor_extended(out_png: Path) -> Path:
    """
    BONUS — Extended evolution 1993-2025.

    Shows the full Ember series for Greece:
    - 1993-2012: study period (solid red)
    - 2013-2025: context for post-study decarbonisation (dashed orange)

    Annotates key milestones to support the narrative on accelerating
    decarbonisation of the Greek electricity mix.
    """
    # Combine both series
    all_factors = {**EMISSION_FACTORS_HISTORICAL, **EMISSION_FACTORS_POST_2012}
    study_years = sorted(EMISSION_FACTORS_HISTORICAL.keys())
    study_values = [EMISSION_FACTORS_HISTORICAL[y] for y in study_years]
    post_years = sorted(EMISSION_FACTORS_POST_2012.keys())
    post_values = [EMISSION_FACTORS_POST_2012[y] for y in post_years]

    # Bridge point so the two segments visually connect
    bridge_x = [study_years[-1], post_years[0]]
    bridge_y = [study_values[-1], post_values[0]]

    plt.figure(figsize=(13, 6.5))

    # Study period (focus)
    plt.plot(study_years, study_values,
             color="#C44536", linewidth=3, marker="o", markersize=5,
             label="Περίοδος μελέτης (1993-2012)")

    # Bridge connector (no marker, no label)
    plt.plot(bridge_x, bridge_y, color="#C44536", linewidth=1.5,
             linestyle=":", alpha=0.5)

    # Post-study context
    plt.plot(post_years, post_values,
             color="#E67E22", linewidth=2, marker="s", markersize=4,
             linestyle="--", alpha=0.85,
             label="Μετά τη μελέτη (2013-2025) - Ember")

    # Highlight study area background
    plt.axvspan(1993, 2012, alpha=0.08, color="#C44536",
                label="_nolegend_")

    # Annotations for narrative
    plt.annotate("Μέγιστο: 877 g/kWh\n(1993)",
                 xy=(1993, 877.02), xytext=(1995, 950),
                 fontsize=9, ha="center",
                 arrowprops=dict(arrowstyle="->", color="gray", lw=0.8))

    plt.annotate("Τέλος περιόδου\nμελέτης: 704 g/kWh\n(2012)",
                 xy=(2012, 704.06), xytext=(2009, 530),
                 fontsize=9, ha="center",
                 arrowprops=dict(arrowstyle="->", color="gray", lw=0.8))

    plt.annotate(f"Πιο πρόσφατη τιμή:\n{EMISSION_FACTOR_CURRENT:.1f} g/kWh\n({EMISSION_FACTOR_CURRENT_YEAR})",
                 xy=(2025, 315.09), xytext=(2021, 180),
                 fontsize=9, ha="center",
                 arrowprops=dict(arrowstyle="->", color="gray", lw=0.8))

    plt.title("Διαχρονική Εξέλιξη του Συντελεστή Εκπομπών CO2 - Επεκταμένη Σειρά\n"
              "Ελληνικό Δίκτυο Ηλεκτρικής Ενέργειας (1993-2025) - Ember / Our World in Data")
    plt.xlabel("Έτος")
    plt.ylabel("Συντελεστής εκπομπών (g CO2/kWh)")
    plt.legend(loc="upper right")
    plt.grid(True, alpha=0.3)
    plt.ylim(0, 1050)
    plt.xlim(1992, 2026)
    plt.tight_layout()
    plt.savefig(out_png, dpi=120)
    plt.close()
    return out_png


def visualize_total_comparison(df: pd.DataFrame, out_png: Path) -> Path:
    years = df["Year"].to_numpy(dtype=float)
    hist = df["Total_CO2_kg_historical"].to_numpy(dtype=float)
    curr = df["Total_CO2_kg_current"].to_numpy(dtype=float)

    plt.figure(figsize=(12, 6))
    plt.plot(years, hist,
             color="#C44536", linewidth=2.5, marker="o",
             label="Ιστορική εκτίμηση (χρονομεταβλητός συντελεστής)")
    plt.plot(years, curr,
             color="#2E8B57", linewidth=2.5, marker="s", linestyle="--",
             label=f"Εκτίμηση με συντελεστή {EMISSION_FACTOR_CURRENT_YEAR} "
                   f"({EMISSION_FACTOR_CURRENT:.1f} g CO2/kWh)")
    plt.fill_between(years, curr, hist,
                     color="#C44536", alpha=0.15,
                     label="Διαφορά εκτιμήσεων")
    plt.title("Συνολικές Εκπομπές CO2 ανά Έτος - Σύγκριση Σεναρίων\n"
              "Περιφερειακή Ενότητα Θεσσαλονίκης (1993-2012)")
    plt.xlabel("Έτος")
    plt.ylabel("Συνολικές Εκπομπές CO2 (kg)")
    plt.legend(loc="best")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_png, dpi=120)
    plt.close()
    return out_png


# ===============================
# Summary printer
# ===============================
def print_summary(df: pd.DataFrame) -> None:
    total_kwh = df[CATEGORIES].sum().sum()
    total_co2_curr = df["Total_CO2_kg_current"].sum()
    total_co2_hist = df["Total_CO2_kg_historical"].sum()
    ratio = total_co2_hist / total_co2_curr
    mean_factor = sum(EMISSION_FACTORS_HISTORICAL.values()) / len(EMISSION_FACTORS_HISTORICAL)

    print("=" * 70)
    print("SCENARIO 3 - SUMMARY (1993-2012, Thessaloniki Regional Unit)")
    print("=" * 70)
    print(f"Total electricity consumed:        {total_kwh:>14,.0f} kWh")
    print(f"Total CO2 (reference {EMISSION_FACTOR_CURRENT_YEAR} factor): {total_co2_curr:>11,.0f} kg")
    print(f"Total CO2 (historical factors):    {total_co2_hist:>14,.0f} kg")
    print(f"Historical / Reference ratio:      {ratio:>14.2f}x")
    print(f"Mean historical factor (1993-2012):{mean_factor:>14.2f} g CO2/kWh")
    print(f"Reference factor ({EMISSION_FACTOR_CURRENT_YEAR}):           {EMISSION_FACTOR_CURRENT:>14.2f} g CO2/kWh")
    print(f"Total decarbonisation 1993->{EMISSION_FACTOR_CURRENT_YEAR}: "
          f"{(1 - EMISSION_FACTOR_CURRENT/877.02)*100:>10.1f}%")
    print("-" * 70)
    print("Top 3 categories by historical CO2 (cumulative 1993-2012):")
    cat_totals = {
        CATEGORY_LABELS[c]: df[f"{c}_CO2_kg_historical"].sum() for c in CATEGORIES
    }
    for cat, val in sorted(cat_totals.items(), key=lambda x: -x[1])[:3]:
        print(f"   {cat:<20} {val:>14,.0f} kg CO2")
    print("=" * 70)


# ===============================
# Run
# ===============================
if __name__ == "__main__":
    print(f"Reading from: {excel_path}")
    print(f"Writing to:   {OUT_DIR}\n")

    if not excel_path.exists():
        raise FileNotFoundError(
            f"Δεν βρέθηκε το αρχείο: {excel_path}\n"
            f"Έλεγξε ότι το excel είναι στο: {DATA_DIR}"
        )

    df = clean_and_normalize(excel_path)
    df = compute_emissions(df, output_excel)

    visualize_energy_consumption(df, output_energy_chart)
    visualize_emissions_historical(df, output_emissions_chart)
    visualize_emission_factor_evolution(output_factor_chart)
    visualize_emission_factor_extended(output_factor_extended_chart)
    visualize_total_comparison(df, output_comparison_chart)

    print_summary(df)

    print("\nΠαραδοτέα:")
    for r in (output_excel, output_energy_chart, output_emissions_chart,
              output_factor_chart, output_factor_extended_chart,
              output_comparison_chart):
        print(f"  - {r}")