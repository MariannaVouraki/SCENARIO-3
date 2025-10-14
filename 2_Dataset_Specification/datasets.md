# Data Specification — Scenario 3  
## Analysis of Electricity Consumption & Estimation of Indirect CO₂ Emissions in Thessaloniki (1993–2012)  
(Ανάλυση Ηλεκτρικής Κατανάλωσης & Υπολογισμός Έμμεσων Εκπομπών CO₂ στη Θεσσαλονίκη, 1993–2012)

---

### Dataset 1: Energy Consumption by Category (Thessaloniki, 1993–2012)  

**Title :**  
Electricity consumption by category of use in Thessaloniki (1993–2012)  
(Κατανάλωση ηλεκτρικής ενέργειας κατά κατηγορία χρήσης στη Θεσσαλονίκη, 1993–2012)

**Description:**  
The dataset contains historical electricity consumption data (kWh) for the Regional Unit of Thessaloniki,  
disaggregated by category of use for the period 1993–2012.  
It is used to estimate indirect CO₂ emissions for each consumption sector  
(domestic, commercial, industrial, agricultural, public administration, and street lighting).  
(Το dataset περιέχει ιστορικά δεδομένα κατανάλωσης ηλεκτρικής ενέργειας (kWh) για την Περιφερειακή Ενότητα Θεσσαλονίκης,  
διαχωρισμένα ανά κατηγορία χρήσης για την περίοδο 1993–2012.  
Χρησιμοποιείται για τον υπολογισμό των έμμεσων εκπομπών CO₂ ανά τομέα κατανάλωσης.)

**Source:**  
TDS – OKF Greece (Thessaloniki Data Space)  
[https://tds.okfn.gr/dataset/energy-consumption-thessaloniki-1993-2012](https://tds.okfn.gr/dataset/energy-consumption-thessaloniki-1993-2012)

**Format:**  
Excel (.xlsx)

**Temporal Coverage:**  
1993 – 2012

**Geographic Scope:**  
Regional Unit of Thessaloniki (Περιφερειακή Ενότητα Θεσσαλονίκης)

**Categories of Use:**  
- Domestic use (Οικιακή χρήση)  
- Commercial use (Εμπορική χρήση)  
- Industrial use (Βιομηχανική χρήση)  
- Agricultural use (Γεωργική χρήση)  
- Public & Municipal Authorities (Δημόσιες & Δημοτικές Αρχές)  
- Street lighting (Φωτισμός οδών)

**Key Fields:**

| Column Name | Description | Unit |
|--------------|--------------------------|----------------|
| Region | Reference area (Περιοχή αναφοράς – Νομός Θεσσαλονίκης) | — |
| Year | Year of measurement (Έτος μέτρησης) | — |
| Domestic | Domestic consumption (Οικιακή κατανάλωση) | kWh |
| Commercial | Commercial consumption (Εμπορική κατανάλωση) | kWh |
| Industrial | Industrial consumption (Βιομηχανική κατανάλωση) | kWh |
| Agricultural | Agricultural consumption (Γεωργική κατανάλωση) | kWh |
| Public | Public sector consumption (Δημόσιες υπηρεσίες) | kWh |
| Lighting | Street lighting consumption (Φωτισμός οδών) | kWh |
| Total | Total consumption (Συνολική κατανάλωση) | kWh |

**Emission Factor:**  
0.267 kg CO₂/kWh (2024 – Greece grid mix, Nowtricity)  

**Derived Outputs:**  
- `thess_energy_analysis.xlsx` – includes consumption and calculated CO₂ emissions per year.
- `co2_emissions_per_category.png` – visualisation of CO₂ emissions.
- `energy_consumption_per_category.png` – visualisation of energy consumption.

**Data Category:**  
`dpv:EnvironmentalData`

**Sensitivity:**  
`dpv:NonPersonalData`

**Domain Concepts (mdat):**  
- `mdat:EnergyDataset` (Ενεργειακό Dataset)  
- `mdat:CO2EmissionDataset` (Dataset Εκπομπών CO₂)

---

**Attribution (Αναφορά Πηγής):**  
© Thessaloniki Data Space / OKF Greece – 2025  
Data used under open data terms (CC BY 4.0)  
(Δεδομένα χρησιμοποιούνται υπό τους όρους ανοιχτών δεδομένων, άδεια CC BY 4.0)
