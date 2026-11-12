RQ3 Completion Time analysis files
================================================
1. RQ3_Completion_Time_Analysis.py
   Reproducible Python script. It reads the Experiment_Data sheet in the original
   RQ3 workbook, validates the timing arithmetic, fits the primary cross-classified
   mixed-effects model, runs model sensitivity checks, leave-one-out checks, and
   a parametric bootstrap, then writes an output workbook.

2. RQ3_Completion_Time_Results.xlsx
   Summary of the current re-analysis, including data checks, model estimates,
   sensitivity analyses, bootstrap interval, and interruption records.

Recommended environment
-------------------
   Python 3.10+
   pandas
   numpy
   scipy
   statsmodels 0.14.6
   openpyxl

Run
---
   pip install pandas numpy scipy statsmodels openpyxl
   python RQ3_Completion_Time_Analysis.py "RQ3_experiment_analysis(2).xlsx" --bootstrap 1000 --seed 20261108

Timing definition
-------------------
   From display of the complete validation result until submission of Q1-Q4.
   Only external interruptions or technical failures are deducted. 
   The three Likert ratings are not included in Completion Time.

Important
-------------------
   The parametric-bootstrap refits converged, but some bootstrap variance-component
   estimates were at/near the boundary. The script reports this count explicitly.
   Use the bootstrap interval as a sensitivity check alongside the REML Wald interval.
