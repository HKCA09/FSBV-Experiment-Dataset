# FSBV-Experiment-Dataset

This repository contains the experimental datasets, supporting materials, and analysis artifacts associated with our manuscript:

> **An Automated Functional Scenario-Based Verification Approach to Support Program Maintenance**

The materials are organized into three directories corresponding to the research questions (RQ1–RQ3) presented in the paper.

---

## 📁 Repository Contents

### RQ1 — Operational Feasibility

The `RQ1/` directory contains:

- **`Materials/`** — Supporting experimental materials for RQ1.
- **`RQ1_experiment_data.xlsx`** — Recorded experimental data for the operational feasibility evaluation.

### RQ2 — Mismatch Detection and Localization

The `RQ2/` directory contains:

- **`Archived Verification Records/`** — Archived verification records for inspecting previously obtained verification results.
- **`Mutant Programs/`** — Java mutant programs used in the mutation-testing evaluation.
- **`RQ2_README.md`** — Additional documentation describing the RQ2 materials and their usage.
- **`rq2_experiment_data.xlsx`** — Experimental data and recorded mismatch detection and localization results.
- **`theorem_RQ2_History.txt`** — An auxiliary file used solely for viewing archived RQ2 verification records.

### RQ3 — Maintenance-Oriented Reporting

The `RQ3/` directory contains:

- **`Questionnaires/`** — Collected questionnaire materials.
- **`RQ3_Completion_Time_Package/`** — Analysis materials for review-task completion time.
- **`RQ3_Total_Accuracy_FullPosterior_Package/`** — Bayesian statistical analysis materials for total task accuracy, including posterior estimation.
- **`RQ3_Wilcoxon_Analysis_Package/`** — Materials for paired Wilcoxon signed-rank analyses.
- **`RQ3_experiment_analysis.xlsx`** — Experimental data and analysis records for RQ3.
- **`RQ3_questionnaire_template.docx`** — Questionnaire template used in the participant evaluation.

---

## 🛠 Supporting Tool

The FSF-based verification tool supports SOFL specification processing, automatic test case generation, test oracle derivation, specification–program binding, Java program execution, conformance checking, and scenario-level traceable reporting.

**The executable Windows installer is available through [GitHub Releases](https://github.com/HKCA09/FSBV-Experiment-Dataset/releases).**

The installer includes the required Java runtime environment. Installation instructions and a quick-start guide are provided in the accompanying tool documentation.

**Note:** Archived verification records can be imported for result inspection, but the current tool does not support re-executing Java programs directly from imported historical records.

---

## 📖 Citation

If you use the experimental materials or supporting tool in academic research, please cite the associated manuscript:

*An Automated Functional Scenario-Based Verification Approach to Support Program Maintenance.*

Full methodological details and experimental results are described in the manuscript.

---

## 📜 License

This dataset is licensed under the [Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License (CC BY-NC-ND 4.0)](https://creativecommons.org/licenses/by-nc-nd/4.0/).

You are free to:
- **Share** — Copy and redistribute the material in any medium or format.

Under the following terms:
- **Attribution** — You must give appropriate credit.
- **NonCommercial** — You may not use the material for commercial purposes.
- **NoDerivatives** — If you remix, transform, or build upon the material, you may not distribute the modified material.

Full license text is available in the `LICENSE` file.
