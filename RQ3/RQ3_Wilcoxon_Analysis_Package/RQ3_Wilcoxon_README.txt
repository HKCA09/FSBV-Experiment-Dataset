RQ3 Wilcoxon and Case-Level Descriptive Analysis
=================================================

Purpose
-------
This standalone package reproduces the five participant-level Wilcoxon
signed-rank analyses reported for RQ3 and generates a 20-row case-level
DESCRIPTIVE comparison file. 

Included files
--------------
- RQ3_experiment_analysis(2).xlsx
  Frozen input workbook used by this package. It is a self-contained copy of
  the RQ3 source workbook.
- RQ3_Wilcoxon_Validation.py
  Reproducible analysis script. It reads the bundled workbook by default.
- RQ3_Wilcoxon_Summary.csv
  Five participant-level Wilcoxon results, including zero counts, tied-rank
  information, exact two-sided p-values, rank-biserial effects, Holm-adjusted
  Likert p-values, and participant-paired bootstrap intervals.
- RQ3_Wilcoxon_Paired_Differences.csv
  Participant-level paired values and signed differences for all five metrics.
- RQ3_Case_Level_Descriptives.csv
  One row per case, showing the two condition-specific observations, the
  participants who reviewed them, accuracy differences, and time reductions.
- requirements.txt
  Python dependencies.


Data and design checks
----------------------
The script validates that the workbook contains 40 valid review records,
20 participants, and 20 cases. Each participant must have one record under
Baseline and one under Traceability-assisted, with different cases. Each case
must have one record under each condition, reviewed by different participants.
It also checks that each total-accuracy score equals the sum of the four task
correctness fields and that adjusted completion time equals end time minus
start time minus recorded interruption time.

Statistical methods
-------------------
1. Participant-level comparisons
   - Five paired comparisons: total accuracy, completion time, analysability,
     modifiability, and testability.
   - Zero differences are excluded from signed-rank ranking (Wilcox convention)
     and their counts are reported.
   - Tied nonzero absolute differences receive average ranks.
   - Two-sided exact p-values are computed from the sign-permutation
     distribution conditional on the observed nonzero average ranks, using
     dynamic programming to enumerate all 2^n sign assignments.
   - W is the smaller of the positive and negative signed-rank sums.
   - Rank-biserial correlation is (W+ - W-)/(W+ + W-); positive values favor
     traceability-assisted reporting. For completion time, the signed
     difference is Baseline minus Traceability-assisted; for all other
     measures, it is Traceability-assisted minus Baseline.
   - The three Likert p-values are adjusted using Holm's step-down procedure.
   - Percentile 95% bootstrap intervals for mean participant-paired
     differences are generated using 50,000 participant resamples by default
     (seed 20261108). These intervals are supplementary uncertainty estimates.

2. Case-level descriptive comparisons
   - Each case has one Baseline and one Traceability-assisted review, performed
     by different participants.
   - Each participant contributes to two different case-level comparisons:
     once through their Baseline review and once through their
     Traceability-assisted review. Thus, the 20 case-level differences are not
     independent of one another.
   - The case-level CSV is therefore descriptive only. The script does not
     calculate case-level Wilcoxon p-values or case-level bootstrap CIs.
   - Adjusted models that include participant and case effects are reported
     separately in the Completion Time and Total Accuracy analysis packages.

How to run
----------
Install dependencies:
    pip install -r requirements.txt

Run from this directory:
    python RQ3_Wilcoxon_Validation.py

Optional arguments:
    python RQ3_Wilcoxon_Validation.py --input-xlsx "path/to/workbook.xlsx"
    python RQ3_Wilcoxon_Validation.py --output-dir "path/to/output"
    python RQ3_Wilcoxon_Validation.py --bootstrap-repetitions 50000 --seed 20261108

The script does not modify the input workbook. By default, the three CSV
outputs are written to this directory and overwrite previous generated CSVs.

Verified descriptive results from the bundled workbook
-------------------------------------------------------
- 40 valid records, 20 participants, 20 cases.
- Participant-level Wilcoxon W values: 8, 35, 7, 7, and 0.
- Participant-level exact two-sided p-values: 0.0283203125, 0.0069599152,
  0.0017089844, 0.0004272461, and 0.0004882813.
- Zero-difference counts: 9, 0, 6, 4, and 8.
- Holm-adjusted Likert p-values: 0.0017089844, 0.0012817383, and 0.0012817383.
- Case-level accuracy: 7 improved, 13 unchanged, 0 lower.
- Case-level completion time: lower in all 20 cases; median reduction 42.5 s,
  Q1 20 s, Q3 55 s, and mean reduction 41.5 s.

These case-level counts and summaries are descriptive and are not accompanied
by inferential p-values or confidence intervals.
