# RQ3 Instructions: Reproducing the Maintenance-Oriented Reporting Analyses

This document provides a single entry point for examining and reproducing the statistical analyses for **RQ3 (Maintenance-Oriented Reporting)** in *An Automated Functional Scenario-Based Verification Approach to Support Program Maintenance*. It consolidates the execution instructions from three analysis packages while leaving their package-specific README files as the authoritative references for implementation details.

The instructions below concern **reanalysis of the recorded RQ3 study data**, not the automatic recreation of the original participant sessions. Each analysis can be run independently.

## 1. Study Data and Experimental Design

The controlled within-subject crossover study compared two reporting conditions:

- **Baseline:** Basic expected–actual reporting, with the FSF specification and Java implementation separately accessible.
- **Traceability-assisted:** The same verification artifacts and execution results, with explicit links to functional scenarios, conditions, the target method, and observable fields.

The recorded study contains **20 participants**, **20 faulty review cases**, **40 review records** (20 per condition), and **160 binary task outcomes** (four tasks per review). Each participant reviewed two *different* cases, one under each condition. Each case was reviewed once under each condition by *different* participants. The presentation order was counterbalanced.

The four scored tasks were:

1. **Scenario identification** — identify the functional scenario associated with the mismatch.
2. **Violated behavior identification** — identify the violated expected behavior or defining condition.
3. **Implementation-context identification** — identify the relevant Java method and observable field.
4. **Follow-up verification planning** — identify the test case and oracle for checking the implementation after correction.

Each correct task contributes one point to **Total Accuracy (0–4)**. Completion time is measured from display of the complete verification result to submission of the four task answers, excluding only documented external interruptions or technical failures. The three subsequent Likert ratings are **not** included in completion time; compilation, program execution, and result generation are also outside this human-review measure.

The source workbook referenced by the analysis packages is **`RQ3_experiment_analysis(2).xlsx`**. The completion-time package reads its **`Experiment_Data`** worksheet. The original package documentation indicates that the Wilcoxon and total-accuracy packages each contain a copy of the source workbook; check that the supplied copies refer to the same frozen data before comparing outputs.

## 2. Analyses and Their Outputs

| Analysis package | Main script | Reported results supported | Main output files |
| --- | --- | --- | --- |
| Participant-level Wilcoxon and case-level descriptive analyses | `RQ3_Wilcoxon_Validation.py` | Table 5, paired bootstrap accuracy interval, and descriptive case-level comparisons | `RQ3_Wilcoxon_Summary.csv`, `RQ3_Wilcoxon_Paired_Differences.csv`, `RQ3_Case_Level_Descriptives.csv` |
| Completion-time analysis | `RQ3_Completion_Time_Analysis.py` | Table 6, adjusted time reduction, and completion-time sensitivity analyses | `RQ3_Completion_Time_Results.xlsx` |
| Bayesian total-accuracy analysis | `RQ3_Total_Accuracy_FullPosterior.py` | Adjusted total-accuracy effect, 95% Bayesian credible interval, posterior diagnostics, and associated sensitivity summaries | `RQ3_Total_Accuracy_FullPosterior_Results.xlsx`, `RQ3_Total_Accuracy_Main_Posterior.json`, `RQ3_Total_Accuracy_Main_Posterior_Draws.npz` |

**File locations:** These packages are maintained in separate analysis directories under RQ3. The directory names are not specified here: **open a terminal in the directory containing the script named in each subsection** and use the workbook and other files supplied with that package. Refer to the local package README for any additional package-specific details.

## 3. Software Environment

Use a Python environment that supports the packages below. **Python 3.10 or later** is recommended in the completion-time package's documentation. If package dependencies conflict, use a separate virtual environment for each analysis package.

The required dependencies are documented as follows:

| Package | Dependencies |
| --- | --- |
| Wilcoxon and case-level descriptive | Install the supplied `requirements.txt` |
| Completion time | `pandas`, `numpy`, `scipy`, `statsmodels` (**0.14.6** in the supplied recommendation), `openpyxl` |
| Bayesian total accuracy | `numpy`, `scipy`, `numba`, `artifact-tool` |

Preserve the original workbook and archived results when running these scripts. The Wilcoxon package explicitly writes its CSV outputs to the current directory by default and **overwrites existing generated CSVs**. Use a copied working directory or the supported `--output-dir` option if the published output files should remain unchanged.

## 4. Reproduce the Participant-Level and Case-Level Analyses

In the directory containing `RQ3_Wilcoxon_Validation.py` and its `requirements.txt`, run:

```bash
python -m pip install -r requirements.txt
python RQ3_Wilcoxon_Validation.py
```

The script reads its bundled `RQ3_experiment_analysis(2).xlsx` by default. To specify an input workbook, output directory, or bootstrap settings, use the documented options:

```bash
python RQ3_Wilcoxon_Validation.py --input-xlsx "RQ3_experiment_analysis(2).xlsx" --bootstrap-repetitions 50000 --seed 20261108
```

The script checks the crossover design, verifies that Total Accuracy equals the sum of the four task scores, and checks the arithmetic for interruption-adjusted completion time. It produces five paired participant-level comparisons: Total Accuracy, Completion Time, Analysability Support, Modifiability-Related Support, and Testability Support.

Its statistical procedures include the **Wilcoxon signed-rank test**, excluding zero differences, averaging ranks of tied nonzero absolute differences, and calculating exact two-sided sign-permutation *p*-values. The three Likert *p*-values are adjusted by the Holm procedure. A **50,000-resample paired bootstrap**, using seed `20261108` by default, supplies a supplementary confidence interval for the participant-level mean difference.

The case-level CSV compares the two conditions for each of the 20 cases, but these comparisons are **descriptive only**: the paired case observations belong to different participants, and each participant also contributes to another case's comparison. Do not interpret the 20 case-level differences as independent samples for statistical inference.

### Results to check

| Measure | Wilcoxon W | Reported p-value |
| --- | ---: | ---: |
| Total Accuracy | 8 | 0.0283 |
| Completion Time | 35 | 0.0070 |
| Analysability Support | 7 | 0.0017 |
| Modifiability-Related Support | 7 | 0.0013 |
| Testability Support | 0 | 0.0013 |

The three support-rating *p*-values above are **Holm-adjusted**; the first two *p*-values are not Holm-adjusted. The mean within-participant Total Accuracy difference is **0.55 points** in favor of traceability-assisted reporting, with a **95% paired-bootstrap confidence interval of [0.15, 0.95]**.

The case-level summaries should show **7 cases with higher accuracy** and **13 with equal accuracy** under traceability-assisted reporting, together with **lower completion time in all 20 cases** and a **median case-level reduction of 42.5 seconds**.

## 5. Reproduce the Completion-Time Mixed-Effects Analysis

In the directory containing `RQ3_Completion_Time_Analysis.py`, run:

```bash
python -m pip install pandas numpy scipy "statsmodels==0.14.6" openpyxl
python RQ3_Completion_Time_Analysis.py "RQ3_experiment_analysis(2).xlsx" --bootstrap 1000 --seed 20261108
```

This script checks the timing data, fits the primary **cross-classified linear mixed-effects model** for log-transformed completion time, and performs sensitivity and leave-one-out analyses. The primary model includes Condition, Period, and Sequence as fixed effects, with Participant and Case as crossed random intercepts. The reported fixed-effect intervals are based on the REML model's Wald estimates.

### Results to check

| Quantity | Reported result |
| --- | --- |
| Median completion time, baseline | 110.0 s |
| Median completion time, traceability-assisted | 57.5 s |
| Condition coefficient on log-time scale | −0.526 |
| Adjusted time ratio | 0.591 |
| Adjusted reduction in completion time | 40.9% |
| 95% CI for percentage reduction | [36.7%, 44.8%] |
| Condition effect significance | p < 0.001 |

The alternative model with participant fixed effects and a case random intercept gave a **40.9% reduction** (95% CI **[33.6%, 47.4%]**). Leave-one-participant-out estimates ranged from **39.3% to 42.3%**, and leave-one-case-out estimates from **39.4% to 42.1%**.

**Interpretation note:** Some parametric-bootstrap variance-component estimates were at or near the boundary, although the documented bootstrap refits converged. The package reports these counts. Treat the bootstrap interval as a **sensitivity check**, not as a replacement for the primary REML Wald confidence interval reported in the paper.

## 6. Reproduce the Bayesian Total-Accuracy Analysis

In the directory containing `RQ3_Total_Accuracy_FullPosterior.py` and the supplied source workbook, run:

```bash
python -m pip install numpy scipy numba artifact-tool
python -u RQ3_Total_Accuracy_FullPosterior.py "RQ3_experiment_analysis(2).xlsx" --chains 4 --warmup 3500 --draws 7000 --fixed-sd 1.5 --sd-prior 1.0
```

This is the documented **main-model** configuration: four chains, 3,500 warm-up iterations and 7,000 retained iterations per chain, giving **28,000 retained posterior draws**. The analysis models the **160 task-level binary responses nested within 40 review records**; these are **not** 160 independent participants.

The Bayesian logistic generalized linear mixed-effects model includes **Condition, Period, Sequence, and Task** as fixed effects, with random intercepts for Participant, Case, and Review Record. The documented main priors are Normal(0, 2) for the intercept, Normal(0, 1.5) for the other fixed effects, and HalfNormal(1) for random-intercept standard deviations.

The adjusted effect is reported on the original **0–4 Total Accuracy scale**, obtained from posterior-predicted task correctness probabilities after accounting for the modeled random-effect distributions and presentation factors.

### Results to check

| Quantity | Reported result |
| --- | --- |
| Adjusted Total Accuracy improvement (posterior median) | 0.463 points |
| 95% Bayesian credible interval | [0.145, 0.849] |
| Posterior probability of improvement | 99.69% |
| Maximum rank-normalized split R-hat | 1.0068 |
| Minimum bulk ESS | 509 |
| Minimum tail ESS | 669 |

The package documentation also records sensitivity checks with fixed-effect prior standard deviations **1.0, 1.5, 2.0, and 3.0**, random-effect standard-deviation prior scales **0.5, 1.0, and 1.5**, and a model excluding Task 2, which was correct in every review. See the supplied results workbook for these analyses; the command above specifies the **main model** and should not by itself be described as rerunning every sensitivity configuration.

A Bayesian **credible interval** is not interchangeable with a frequentist **confidence interval**. Posterior diagnostics assess computation under the chosen model; they do not independently establish the model's validity.

## 7. Check Task-Level Findings Corresponding to Figure 5

The paper reports the following correctness percentages under the two reporting conditions:

| Task | Baseline | Traceability-assisted |
| --- | ---: | ---: |
| Scenario identification | 75% | 100% |
| Violated behavior identification | 100% | 100% |
| Implementation-context identification | 90% | 100% |
| Follow-up verification planning | 70% | 90% |

These percentages can be checked against the **task-level correctness observations in the original RQ3 workbook**. The three uploaded package READMEs do **not** specify a standalone command to regenerate the Figure 5 image, so this document claims reproducibility of the underlying values, **not automated regeneration of the figure artwork**.

## 8. Scope and Limitations of Reproduction

The included analysis packages enable independent **recalculation and inspection of the statistical analyses** using the recorded study data. They do not reproduce the original human participants' decisions or review times. Conducting a new controlled user study would additionally require the task materials, case assignments, tutorial, reporting interfaces, and participant recruitment and administration procedures described in the paper and any accompanying study materials.

The analyses should be interpreted with the experimental unit and comparison structure intact:

- **Participant-level paired comparisons:** 20 participants with one review under each reporting condition.
- **Task-level Bayesian model:** 160 task responses nested within 40 reviews, from 20 participants and 20 cases.
- **Completion-time model:** 40 review records, with participant and case variability accounted for.
- **Case-level comparisons:** descriptive only, not 20 independent inferential pairs.

Randomized analyses may show small numerical variations across environments and runs. Compare with the included result files, report the software environment, and preserve the source workbook when rerunning the scripts.

For tool operation and execution of the original FSF-based verification workflow (as distinct from RQ3 statistical reanalysis), refer to the repository's tool documentation and the corresponding RQ1/RQ2 instructions.
