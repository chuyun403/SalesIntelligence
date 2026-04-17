
## 🎯 Executive Summary
The most expensive mistake a sales organization can make is scaling a strategy that only looks successful on paper. 

This repository documents the quantitative evaluation of Medshift's "High-End Upsell" marketing campaign. Our objective was to determine if a new, ROI-focused case study could successfully migrate low-margin consumable buyers (Group A) to high-margin surgical devices (Group B).

While top-line average revenue suggested the new campaign was a success, **this data pipeline proved the lift was statistically insignificant.** By identifying the "noise" in our sales variance, we prevented a costly, premature company-wide rollout and preserved the marketing budget for a redesigned iteration.

## 💼 The Business Challenge
Medshift is actively pivoting its sales motion from high-volume/low-margin plastics to lower-volume/high-margin implants. A regional A/B test was launched to test a new enablement tool designed to accelerate this pivot.

However, the field execution resulted in highly fragmented data:
* Data was returned in messy, localized Excel files across three distinct regions.
* Schema was inconsistent (conflicting date formats, varying column headers, mismatched boolean values).
* "Whale" accounts (massive Tier 1 hospitals) created extreme variance, obscuring the true performance of the middle-market clinics.

## 🏗️ The Commercial Operations Pipeline
To evaluate the campaign, an automated, end-to-end data pipeline to ingest, clean, and statistically validate the field results was bult.

### Phase 1: Ingestion & Normalization (The ETL Engine)
* **Script:** `02_A_clean_ab_data.py`
* **Action:** Built a dynamic Python/Pandas parser that sweeps regional folders, maps conflicting headers (`Rev(TWD)` vs. `Total_Rev`) into a standardized schema, handles missing values, and enforces ISO date formatting.
* **Impact:** Reduced a multi-day manual Excel reconciliation process down to a 3-second automated script, ensuring zero data loss.

### Phase 2: The Reality Check (Statistical Validation)
* **Script:** `05_run_realistic_test.py`
* **Action:** Applied Welch’s T-Test (via `scipy.stats`) to account for the extreme variance inherent in medical sales data. 
* **Impact:** Discovered a **P-Value of ~0.15**. Despite Group B showing higher average revenue, there was a 15% probability the lift was due to random chance (capturing a few massive orders) rather than the campaign itself.

## 📊 The "Stakeholder Reality Check" Dashboard
* **Notebook:** `06_dashboard_noise.ipynb`

To defend the recommendation against rolling out the campaign, I built a visual dashboard specifically designed to communicate variance to non-technical stakeholders. 

> *The side-by-side visualization below (generated via Seaborn) clearly demonstrates that while the "averages" differed, the core buying behavior of the clinics remained nearly identical.*

*(Insert screenshot of your two-chart dashboard here)*

## 🛑 Strategic Outcomes & Next Steps
1. **Budget Preservation:** Halted the planned company-wide rollout of the Group B enablement materials, saving the organization significant printing and training costs.
2. **Campaign Redesign:** The marketing team is currently restructuring the case study to specifically target the "middle 80%" of clinics, rather than relying on outliers to drive the average.
3. **Pipeline Scalability:** The ETL pipeline built for this test is now standard protocol for all future regional data ingestion, drastically reducing reporting latency.

---

## 🛠️ Technical Execution (For Ops & Engineering)
If you wish to run the simulation and view the data architecture locally:

**1. Clone the repository:**
```bash
git clone [https://github.com/yourusername/Medshift-Growth-AB-Test.git](https://github.com/yourusername/Medshift-Growth-AB-Test.git)
cd Medshift-Growth-AB-Test

# 🏥 Medshift Commercial Strategy: The Margin Pivot (A/B Test Analysis)

![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat&logo=python)
![ETL Pipeline](https://img.shields.io/badge/ETL-Data_Cleaning-00a3e0?style=flat)
![SciPy](https://img.shields.io/badge/SciPy-Statistical_Testing-8CAAE6?style=flat&logo=scipy)
![Seaborn](https://img.shields.io/badge/Seaborn-Data_Viz-4B8BBE?style=flat)
