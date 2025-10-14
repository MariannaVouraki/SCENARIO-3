# 📘 Data Specification — Scenario 3  
## Ανάλυση Ηλεκτρικής Κατανάλωσης & Υπολογισμός Έμμεσων Εκπομπών CO₂ στη Θεσσαλονίκη (1993–2012)

---

### Dataset 1: Energy Consumption by Category (Thessaloniki, 1993–2012)

**Title:**  
Κατανάλωση ηλεκτρικής ενέργειας κατά κατηγορία χρήσης στη Θεσσαλονίκη (1993–2012)

**Description:**  
Το dataset περιέχει ιστορικά δεδομένα κατανάλωσης ηλεκτρικής ενέργειας (kWh) για την Περιφερειακή Ενότητα Θεσσαλονίκης, διαχωρισμένα ανά κατηγορία χρήσης για την περίοδο 1993–2012.  
Χρησιμοποιείται για τον υπολογισμό των έμμεσων εκπομπών CO₂ ανά τομέα κατανάλωσης (οικιακός, εμπορικός, βιομηχανικός, γεωργικός, δημόσιος και φωτισμός οδών).

**Source:**  
TDS – OKF Greece (Thessaloniki Data Space)  
[https://tds.okfn.gr/dataset/energy-consumption-thessaloniki-1993-2012](https://tds.okfn.gr/dataset/energy-consumption-thessaloniki-1993-2012)

**Format:**  
Excel (.xlsx)

**Temporal Coverage:**  
1993 – 2012

**Geographic Scope:**  
Περιφερειακή Ενότητα Θεσσαλονίκης

**Categories of Use:**  
- Οικιακή χρήση  
- Εμπορική χρήση  
- Βιομηχανική χρήση  
- Γεωργική χρήση  
- Δημόσιες & Δημοτικές Αρχές  
- Φωτισμός οδών  

**Key Fields:**  
| Column Name | Description | Unit |
|--------------|-------------|------|
| Region | Περιοχή αναφοράς (Nomos Thessalonikis) | — |
| Year | Έτος μέτρησης | — |
| Domestic | Οικιακή κατανάλωση | kWh |
| Commercial | Εμπορική κατανάλωση | kWh |
| Industrial | Βιομηχανική κατανάλωση | kWh |
| Agricultural | Γεωργική κατανάλωση | kWh |
| Public | Δημόσιες υπηρεσίες | kWh |
| Lighting | Φωτισμός οδών | kWh |
| Total | Συνολική κατανάλωση | kWh |

**Emission Factor:**  
0.267 kg CO₂/kWh (2024 – Greece grid mix, Nowtricity)

**Derived Outputs:**  
- `thess_energy_analysis.xlsx` – περιλαμβάνει κατανάλωση και υπολογισμένες εκπομπές CO₂ ανά έτος.  
- `co2_emissions_per_category.png` – γραφική απεικόνιση εκπομπών CO₂.  
- `energy_consumption_per_category.png` – γραφική απεικόνιση κατανάλωσης ενέργειας.  

**Data Category (DPV):**  
`dpv:EnvironmentalData`, `dpv:StatisticalData`

**Sensitivity:**  
`dpv:NonPersonalData`

**Domain Concepts (mdat):**  
- `mdat:EnergyDataset`  
- `mdat:CO2EmissionDataset`

---

**Attribution:**  
© Thessaloniki Data Space / OKF Greece – 2025  
Data used under open data terms (CC BY 4.0)
