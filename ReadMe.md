# MDAT Scenario 3 — Energy Consumption & CO₂ Emissions in Thessaloniki (1993 – 2012)

This scenario calculates energy consumption trends and resulting CO₂ emissions per usage category in the Regional Unit of Thessaloniki (1993–2012).  
It reuses ontological alignment patterns from **Scenario 1 (Urban Green)** and **Scenario 2 (Air Quality & Population Exposure)** to ensure interoperability and policy traceability.

---

## Scenario Description

| Element | Description |
|----------|--------------|
| **Dataset Source** | `energy_consumption_thessaloniki_1993-2012.xlsx` |
| **Geographic Coverage** | Thessaloniki Regional Unit |
| **Temporal Coverage** | 1993 – 2012 |
| **Purpose** | Quantify and visualize electricity consumption and corresponding CO₂ emissions by category |
| **Emission Factor** | 256 g CO₂eq / kWh (2023 Nowtricity – Greece grid mix) |
| **Outputs** | `thess_energy_analysis.xlsx`, `co2_emissions_per_category.png`, `energy_consumption_per_category.png` |

---

## Roles (Ontology Alignment)

| Role | DPV Term | ODRL Term | Notes / Usage |
|------|-----------|------------|----------------|
| **Data Provider** | `dpv:DataSource`, `dpv:DataController` | — | Provides historical energy consumption data. |
| **Data Analyst** | `dpv:DataProcessor` | — | Performs data cleaning, transformation, and CO₂ derivation. |
| **Researcher / Policy User** | `dpv:Recipient`, `dpv:DataUser` | — | Uses analytical outputs for energy and climate policy decisions. |

---

## Workflow (Mapped to DPV & ODRL)

| Element (process – action) / Description | DPV Term | ODRL Term | Proposed Custom Term (`mdat:`) |
|------------------------------------------|-----------|-------------|--------------------------------|
| Negotiate and authorize dataset use | `dpv:Access`, `dpv:AuthorisationProcedure`, `dpv:NegotiateContract` | *(policy-level)* | `mdat:NegotiatedAccessPolicy` |
| Load energy consumption dataset | `dpv:Collect`, `dpv:Access` | `odrl:use` | — |
| Normalize and clean records (Region, Year, Category) | `dpv:Transform`, `dpv:Clean`, `dpv:Standardise` | `odrl:derive` | — |
| Compute CO₂ emissions per category (apply emission factor) | `dpv:Derive`, `dpv:Aggregate`, `dpv:Calculate` | `odrl:derive` | `mdat:CalculateEmissionIndicator` |
| Store derived dataset (energy + CO₂) | `dpv:Store`, `dpv:DerivedData` | `odrl:reproduce` | — |
| Generate visualisations (emissions & energy by category) | `dpv:Visualise`, `dpv:Analyse`, `dpv:Use` | `odrl:display`, `odrl:reproduce` | `mdat:GenerateEmissionCharts` |
| Interpret and evaluate energy trends & emission patterns | `dpv:Assess`, `dpv:Analyse` | `odrl:analyze`, `odrl:present` | `mdat:EnergyEmissionAssessment` |
| Share derived graphs and summary indicators (open outputs) | `dpv:Disclose`, `dpv:Share`, `dpv:DerivedData` | `odrl:distribute` | — |

---

## Data Types and Vocabularies

| Data Type | DPV Term | Proposed Custom Term (`mdat:`) | Notes |
|------------|-----------|-------------------------------|-------|
| Energy consumption dataset | `dpv:EnvironmentalData`, `dpv:StatisticalData` | `mdat:EnergyDataset` | Electricity use (kWh) by sector and year |
| Emission indicator dataset | `dpv:DerivedData`, `dpv:EmissionData` | `mdat:CO2EmissionDataset` | CO₂ kg values computed from energy use |
| Visual outputs (plots & charts) | `dpv:VisualisationData` | `mdat:EmissionVisualisation` | PNG graphs for reports and dashboards |

---

## Ontological Consistency Notes

- All DPV terms verified against **DPV 2.2** (core and extension modules).  
- ODRL actions refer to the **ODRL Core Vocabulary (2.2)**.  
- Energy and CO₂ derivation reuses the semantic pattern of Scenario 2’s `mdat:CalculateMeanPollutant`.  
- Visualisation and assessment reuse `dpv:Visualise`, `dpv:Analyse` and `odrl:present` from Scenario 1 for alignment.  
- Ensures semantic interoperability and policy traceability within the MDAT data space framework.

---

## requirements.txt
pandas==2.2.2
matplotlib==3.9.2
openpyxl==3.1.5
