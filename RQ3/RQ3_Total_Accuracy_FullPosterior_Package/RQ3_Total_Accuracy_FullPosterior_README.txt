RQ3 TOTAL ACCURACY — FULL POSTERIOR ANALYSIS
================================================

Scientific purpose
------------------
To estimate Total Accuracy differences between baseline and traceability-assisted
reporting while jointly accounting for participant and case variability, and for
dependence among the four task responses in each case review.

Original experiment
-------------------
20 participants, 20 cases, 40 review records and 160 binary task outcomes.
Baseline 67/80 correct tasks, average 3.35/4.
Traceability-assisted 78/80 correct tasks, average 3.90/4.
Task 2 was correct in all 40 reviews.

Statistical model
-----------------
Bayesian task-level logistic GLMM with fixed effects for Condition, Period,
Sequence and Task. Participant, Case and Review Record have crossed random
intercepts. Intercept: Normal(0, 2). Remaining fixed effects: Normal(0, 1.5)
main model. Each random-intercept standard deviation: HalfNormal(scale=1).

Inference
---------
Full posterior MCMC via block elliptical slice sampling for Gaussian-prior latent
vectors and a Metropolis-Hastings update of log standard deviations. Four chains,
3500 warmup and 7000 retained iterations per chain (28,000 posterior draws).
Fixed effects and variance component estimates are genuine posterior samples,
not a variational Bayes approximation.

Main analysis
-------------
Adjusted Total Accuracy improvement (posterior median): 0.463
95% Bayesian credible interval: [0.145, 0.849]
Posterior probability of improvement: 99.69%
Max rank-normalized split R-hat: 1.0068
Min bulk ESS: 509
Min tail ESS: 669

Interpretation
--------------
Adjusted score difference is the posterior distribution of the difference in
predicted numbers of correct tasks (out of four), integrated over random-effect
distributions and balanced across the observed condition/order cells.
A Bayesian 95% credible interval is NOT a frequentist 95% confidence interval.
The conditional odds ratio is prior sensitive due to near-ceiling performance.
Do not describe the model as fitting 160 independent participants; the data are
160 task outcomes nested in 40 reviews from 20 participants and 20 cases.

Sensitivity
-----------
Fixed-effect prior SD = 1.0, 1.5, 2.0, 3.0; random SD prior scales = 0.5,
1.0, 1.5. Omission of always-correct Task 2 was also checked. See the workbook.
MCMC convergence indicates the sampler reached a stable posterior under the
chosen model; it does not prove the model, prior or data are free of limitations.

Files included
--------------
- RQ3_Total_Accuracy_FullPosterior_Results.xlsx: summary/diagnostic tables.
- RQ3_Total_Accuracy_FullPosterior.py: runnable MCMC analysis script.
- RQ3_Total_Accuracy_Main_Posterior.json: primary analysis summary.
- RQ3_Total_Accuracy_Main_Posterior_Draws.npz: compressed full main-chain draws.
- RQ3_experiment_analysis(2).xlsx: original input for reproducibility.

Run
---
python -m pip install numpy scipy numba artifact-tool
python -u RQ3_Total_Accuracy_FullPosterior.py "RQ3_experiment_analysis(2).xlsx" \
    --chains 4 --warmup 3500 --draws 7000 --fixed-sd 1.5 --sd-prior 1.0

