# ⚙️ Scenario 3 — Energy Consumption & CO₂ Emissions in Thessaloniki (1993–2012)

## 🧩 Scenario Description

**Title:** Energy Consumption & CO₂ Emissions — Thessaloniki (1993–2012)  
**Objective:** Analyze the evolution of electricity consumption by category and estimate indirect CO₂ emissions using Greece’s average grid emission factor (256 g CO₂/kWh).  
**Data Source:** `energy_consumption_thessaloniki_1993-2012.xlsx`  
**Coverage:** Thessaloniki Regional Unit (Years 1993 – 2012)  
**Emission Factor Source:** Nowtricity (2023)  
**Outputs:**  
- `output/thess_energy_analysis.xlsx`  
- `output/co2_emissions_per_category.png`  
- `output/energy_consumption_per_category.png`

---

## 👥 Roles (Ontology Alignment)

| Role | Description | DPV Term | ODRL Term | Proposed Custom Term (`mdat:`) | Notes |
|------|--------------|----------|------------|--------------------------------|-------|
| **Data Provider** | Entity supplying the regional energy dataset. | `dpv:DataController` / `dpv:DataSource` | — | `mdat:EnergyProvider` | e.g. ΔΕΔΔΗΕ, ΕΛΣΤΑΤ |
| **Data Analyst** | Person or process that cleans, computes, and visualizes the data. | `dpv:DataProcessor` | — | `mdat:EnergyAnalyst` | Implements analysis workflow |
| **Researcher / Policy User** | Uses derived results for environmental and energy policy decisions. | `dpv:DataUser` / `dpv:Recipient` | — | `mdat:PolicyResearcher` | Accesses aggregated results only |
| **MDAT Platform** | Manages access, metadata, and sharing policies. | `dpv:DataController` / `dpv:AccessControlMethod` | `odrl:policy` | `mdat:PlatformService` | Ensures DPV/ODRL compliance |

---

## 🔁 Workflow (Mapped to DPV & ODRL)

| Element (Process–Action) / Description | DPV Term | ODRL Term | Proposed Custom Term (`mdat:`) | Notes / Usage |
|----------------------------------------|-----------|------------|--------------------------------|----------------|
| **1. Load energy dataset (1993–2012)** – import Excel file for Thessaloniki | `dpv:Collect` | `odrl:use` | `mdat:LoadEnergyData` | Base data ingestion |
| **2. Normalize and clean columns** – harmonize names and units | `dpv:Transform`, `dpv:Clean`, `dpv:Standardise` | `odrl:modify` | `mdat:NormalizeEnergyData` | Ensures consistency across years |
| **3. Filter by Thessaloniki region** – select relevant rows | `dpv:Transform` | `odrl:use` | `mdat:ExtractRegionSubset` | Regional focus step |
| **4. Calculate CO₂ emissions per category** – apply emission factor (256 g CO₂/kWh) | `dpv:Derive`, `dpv:Calculate` | `odrl:derive` | `mdat:CalculateCO2Emissions` | Produces derived environmental indicator |
| **5. Store enriched dataset (energy + CO₂)** – export Excel with computed values | `dpv:Store`, `dpv:Record` | `odrl:reproduce` | `mdat:StoreDerivedDataset` | Persist for reuse |
| **6. Generate charts (energy & emissions)** – visualize trends per category | `dpv:Visualise`, `dpv:Analyse` | `odrl:present`, `odrl:analyze` | `mdat:GenerateEnergyCharts` | Output PNG files |
| **7. Share or publish results** – provide aggregated outputs via MDAT | `dpv:Disclose`, `dpv:Share` | `odrl:distribute` | `mdat:PublishEnergyIndicators` | For research and policy use |

---

## 📘 Ontological Consistency Notes

- All **DPV terms** are verified against **DPV 2.2** (W3C Data Privacy Vocabulary
