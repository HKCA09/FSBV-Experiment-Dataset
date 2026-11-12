#!/usr/bin/env python3
"""
RQ3 Completion Time analysis for the FSF-based program-maintenance study.

Primary model:
    log(CompletionTime) ~ Condition + Period + Sequence
                          + (1 | Participant) + (1 | Case)

The participant and case random intercepts are crossed variance components.
The model is fitted by REML. Parametric-bootstrap intervals and leave-one-out
sensitivity analyses are included.

Usage:
    python RQ3_Completion_Time_Analysis.py "RQ3_experiment_analysis(2).xlsx"
    python RQ3_Completion_Time_Analysis.py input.xlsx --bootstrap 1000 --seed 20261108

Requirements:
    pandas, numpy, scipy, statsmodels, openpyxl
Tested with statsmodels 0.14.6.
"""

import argparse
import warnings
from pathlib import Path
from collections import Counter

import numpy as np
import pandas as pd
import scipy
from scipy.stats import norm
import statsmodels
import statsmodels.api as sm
import statsmodels.formula.api as smf
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter


MAIN_FORMULA = (
    "log_time ~ "
    "C(Condition, Treatment(reference='Baseline')) + "
    "C(Period, Treatment(reference='First')) + "
    "C(Sequence, Treatment(reference='Baseline-first'))"
)
CONDITION_TERM = (
    "C(Condition, Treatment(reference='Baseline'))"
    "[T.Traceability-assisted]"
)
PERIOD_TERM = "C(Period, Treatment(reference='First'))[T.Second]"
SEQUENCE_TERM = (
    "C(Sequence, Treatment(reference='Baseline-first'))"
    "[T.Traceability-first]"
)


def prepare_data(input_path):
    df = pd.read_excel(input_path, sheet_name="Experiment_Data")

    required = [
        "participant_id", "order_group", "review_case_order", "condition",
        "case_id", "start_time", "end_time", "interruption_seconds",
        "completion_time_seconds", "valid_record"
    ]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = df[df["valid_record"] == 1].copy()
    if df.empty:
        raise ValueError("No valid records were found.")

    numeric = [
        "start_time", "end_time", "interruption_seconds",
        "completion_time_seconds", "review_case_order"
    ]
    for col in numeric:
        df[col] = pd.to_numeric(df[col], errors="raise")

    expected_time = (
        df["end_time"] - df["start_time"] - df["interruption_seconds"]
    )
    if not np.allclose(
        df["completion_time_seconds"].to_numpy(),
        expected_time.to_numpy(),
        rtol=0,
        atol=1e-9
    ):
        bad = df.loc[
            ~np.isclose(
                df["completion_time_seconds"],
                expected_time,
                rtol=0,
                atol=1e-9
            ),
            ["participant_id", "case_id", "completion_time_seconds"]
        ]
        raise ValueError(
            "Completion-time arithmetic is inconsistent. "
            f"Check these rows:\n{bad.to_string(index=False)}"
        )

    if (df["completion_time_seconds"] <= 0).any():
        raise ValueError("Completion time must be strictly positive.")

    df["participant_id"] = df["participant_id"].astype(str)
    df["case_id"] = df["case_id"].astype(str)
    df["Condition"] = pd.Categorical(
        df["condition"],
        categories=["Baseline", "Traceability-assisted"]
    )
    period_map = {1: "First", 2: "Second"}
    df["Period"] = pd.Categorical(
        df["review_case_order"].map(period_map),
        categories=["First", "Second"]
    )
    df["Sequence"] = pd.Categorical(
        df["order_group"],
        categories=["Baseline-first", "Traceability-first"]
    )
    df["condition_binary"] = (
        df["condition"] == "Traceability-assisted"
    ).astype(int)
    df["log_time"] = np.log(df["completion_time_seconds"])
    df["all_group"] = 1

    if df[["Condition", "Period", "Sequence"]].isna().any().any():
        raise ValueError(
            "Unexpected condition, period, or sequence labels were found."
        )
    return df


def fit_crossed_model(data, method="powell"):
    d = data.copy()
    d["all_group"] = 1
    model = smf.mixedlm(
        MAIN_FORMULA,
        data=d,
        groups=d["all_group"],
        vc_formula={
            "participant": "0 + C(participant_id)",
            "case": "0 + C(case_id)"
        }
    )
    result = model.fit(
        reml=True,
        method=method,
        maxiter=10000,
        disp=False
    )
    return result


def condition_summary(result):
    coef = float(result.fe_params[CONDITION_TERM])
    se = float(result.bse_fe[CONDITION_TERM])
    ci = np.asarray(result.conf_int().loc[CONDITION_TERM], dtype=float)
    z_value = coef / se
    p_value = float(2 * norm.sf(abs(z_value)))
    ratio = float(np.exp(coef))
    ratio_ci = np.exp(ci)
    reduction = float(100 * (1 - ratio))
    reduction_ci = (
        float(100 * (1 - ratio_ci[1])),
        float(100 * (1 - ratio_ci[0]))
    )
    return {
        "coefficient_log_scale": coef,
        "SE": se,
        "z": z_value,
        "p_value": p_value,
        "CI_log_lower": float(ci[0]),
        "CI_log_upper": float(ci[1]),
        "adjusted_time_ratio": ratio,
        "time_ratio_CI_lower": float(ratio_ci[0]),
        "time_ratio_CI_upper": float(ratio_ci[1]),
        "estimated_time_reduction_percent": reduction,
        "reduction_CI_lower_percent": reduction_ci[0],
        "reduction_CI_upper_percent": reduction_ci[1]
    }


def fixed_effect_table(result):
    ci = result.conf_int()
    rows = []
    labels = {
        "Intercept": "Intercept",
        CONDITION_TERM: "Condition: Traceability-assisted vs Baseline",
        PERIOD_TERM: "Period: Second vs First",
        SEQUENCE_TERM: "Sequence: Traceability-first vs Baseline-first"
    }
    for term in result.fe_params.index:
        coef = float(result.fe_params[term])
        se = float(result.bse_fe[term])
        z_value = coef / se
        p_value = float(2 * norm.sf(abs(z_value)))
        lo, hi = [float(x) for x in ci.loc[term].to_numpy()]
        rows.append({
            "Effect": labels.get(term, term),
            "Coefficient": coef,
            "SE": se,
            "z": z_value,
            "p_value": p_value,
            "95% CI lower": lo,
            "95% CI upper": hi
        })
    return pd.DataFrame(rows)


def make_data_checks(df):
    participant_counts = df.groupby("participant_id", observed=True).size()
    case_counts = df.groupby("case_id", observed=True).size()
    participant_condition = df.groupby(
        ["participant_id", "condition"], observed=True
    ).size()
    case_condition = df.groupby(
        ["case_id", "condition"], observed=True
    ).size()
    period_condition = df.groupby(
        ["condition", "review_case_order"], observed=True
    ).size()
    seq_counts = df.groupby("order_group", observed=True)[
        "participant_id"
    ].nunique()

    nonzero_interruptions = sorted(
        df.loc[df["interruption_seconds"] > 0, "interruption_seconds"].tolist()
    )
    checks = [
        ("Valid review records", len(df), "Expected 40"),
        ("Unique participants", df["participant_id"].nunique(), "Expected 20"),
        ("Unique cases", df["case_id"].nunique(), "Expected 20"),
        ("Participants with exactly two records",
         int((participant_counts == 2).sum()), "Expected 20"),
        ("Cases with exactly two records",
         int((case_counts == 2).sum()), "Expected 20"),
        ("Participant-condition cells with one record",
         int((participant_condition == 1).sum()), "Expected 40"),
        ("Case-condition cells with one record",
         int((case_condition == 1).sum()), "Expected 40"),
        ("Baseline-first participants",
         int(seq_counts.get("Baseline-first", 0)), "Expected 10"),
        ("Traceability-first participants",
         int(seq_counts.get("Traceability-first", 0)), "Expected 10"),
        ("Condition-period cells with 10 records",
         int((period_condition == 10).sum()), "Expected 4"),
        ("Nonzero interruption count", len(nonzero_interruptions),
         "Researcher confirmed all were external/technical interruptions"),
        ("Sorted nonzero interruption seconds",
         str(nonzero_interruptions), "Expected [30, 45, 45]"),
        ("Time arithmetic matches end-start-interruption",
         bool(np.allclose(
             df["completion_time_seconds"],
             df["end_time"] - df["start_time"] - df["interruption_seconds"]
         )), "Must be True")
    ]
    return pd.DataFrame(checks, columns=["Check", "Observed", "Expected / Note"])


def fit_sensitivity_models(df):
    rows = []

    # Sensitivity A: participant fixed effects, case random intercept.
    # Sequence is absorbed by participant fixed effects and therefore omitted.
    pfe_formula = (
        "log_time ~ "
        "C(Condition, Treatment(reference='Baseline')) + "
        "C(Period, Treatment(reference='First')) + "
        "C(participant_id)"
    )
    pfe_model = smf.mixedlm(
        pfe_formula,
        data=df,
        groups=df["all_group"],
        vc_formula={"case": "0 + C(case_id)"}
    )
    with warnings.catch_warnings(record=True) as pfe_warnings:
        warnings.simplefilter("always")
        pfe_result = pfe_model.fit(
            reml=True, method="powell", maxiter=10000, disp=False
        )
    pfe_sum = condition_summary(pfe_result)
    rows.append({
        "Model": "Participant fixed effects + Case random intercept",
        **pfe_sum,
        "Model diagnostics": (
            "Converged; participant differences controlled by fixed effects; "
            "Sequence omitted because it is constant within participant."
        )
    })

    # Sensitivity B: case fixed effects, participant random intercept.
    casefe_formula = MAIN_FORMULA + " + C(case_id)"
    casefe_model = smf.mixedlm(
        casefe_formula,
        data=df,
        groups=df["participant_id"],
        re_formula="1"
    )
    with warnings.catch_warnings(record=True) as casefe_warnings:
        warnings.simplefilter("always")
        casefe_result = casefe_model.fit(
            reml=True, method="powell", maxiter=10000, disp=False
        )
    casefe_sum = condition_summary(casefe_result)
    participant_var = float(casefe_result.cov_re.iloc[0, 0])
    rows.append({
        "Model": "Case fixed effects + Participant random intercept",
        **casefe_sum,
        "Model diagnostics": (
            f"Participant random-intercept variance={participant_var:.3g}; "
            "estimated at/near the boundary, so treated as a diagnostic "
            "sensitivity model rather than the primary model."
        )
    })

    # Sensitivity C: independent participant random intercept and slope.
    slope_vc = {
        "participant_intercept": "0 + C(participant_id)",
        "participant_slope": "0 + C(participant_id):condition_binary",
        "case": "0 + C(case_id)"
    }
    slope_rows = []
    for method in ["powell", "lbfgs"]:
        slope_model = smf.mixedlm(
            MAIN_FORMULA,
            data=df,
            groups=df["all_group"],
            vc_formula=slope_vc
        )
        with warnings.catch_warnings(record=True) as slope_warnings:
            warnings.simplefilter("always")
            slope_result = slope_model.fit(
                reml=True, method=method, maxiter=20000, disp=False
            )
        slope_sum = condition_summary(slope_result)
        slope_names = slope_result.model.exog_vc.names
        slope_variances = dict(zip(slope_names, slope_result.vcomp))
        slope_rows.append({
            "Model": f"Participant random intercept + independent slope ({method})",
            **slope_sum,
            "Model diagnostics": (
                f"Participant-slope variance="
                f"{slope_variances.get('participant_slope', np.nan):.4g}; "
                f"optimizer warnings={len(slope_warnings)}."
            )
        })

    rows.extend(slope_rows)
    return pd.DataFrame(rows), pfe_result, casefe_result


def optimizer_check(df):
    rows = []
    for method in ["lbfgs", "powell", "cg", "nm"]:
        try:
            with warnings.catch_warnings(record=True) as ws:
                warnings.simplefilter("always")
                res = fit_crossed_model(df, method=method)
            vc = dict(zip(res.model.exog_vc.names, res.vcomp))
            rows.append({
                "Optimizer": method,
                "Converged": bool(res.converged),
                "Condition coefficient": float(res.fe_params[CONDITION_TERM]),
                "Case variance": float(vc.get("case", np.nan)),
                "Participant variance": float(vc.get("participant", np.nan)),
                "Residual variance": float(res.scale),
                "Warnings": " | ".join(str(w.message) for w in ws)
            })
        except Exception as exc:
            rows.append({
                "Optimizer": method,
                "Converged": False,
                "Condition coefficient": np.nan,
                "Case variance": np.nan,
                "Participant variance": np.nan,
                "Residual variance": np.nan,
                "Warnings": f"{type(exc).__name__}: {exc}"
            })
    return pd.DataFrame(rows)


def leave_one_out(df):
    rows = []
    methods = ["lbfgs", "cg", "nm", "powell"]

    for unit in ["participant_id", "case_id"]:
        for removed in sorted(df[unit].unique()):
            sub = df[df[unit] != removed].copy()
            fitted = None
            chosen_method = None
            attempt_notes = []
            for method in methods:
                try:
                    with warnings.catch_warnings(record=True) as ws:
                        warnings.simplefilter("always")
                        candidate = fit_crossed_model(sub, method=method)
                    attempt_notes.append(
                        f"{method}: converged={candidate.converged}"
                    )
                    if candidate.converged:
                        fitted = candidate
                        chosen_method = method
                        break
                except Exception as exc:
                    attempt_notes.append(
                        f"{method}: {type(exc).__name__}"
                    )
            if fitted is None:
                rows.append({
                    "Leave-one-out unit": unit,
                    "Removed ID": removed,
                    "Converged": False,
                    "Optimizer": None,
                    "Condition coefficient": np.nan,
                    "Estimated time reduction (%)": np.nan,
                    "Attempts": "; ".join(attempt_notes)
                })
            else:
                coef = float(fitted.fe_params[CONDITION_TERM])
                rows.append({
                    "Leave-one-out unit": unit,
                    "Removed ID": removed,
                    "Converged": True,
                    "Optimizer": chosen_method,
                    "Condition coefficient": coef,
                    "Estimated time reduction (%)":
                        float(100 * (1 - np.exp(coef))),
                    "Attempts": "; ".join(attempt_notes)
                })

    loo_df = pd.DataFrame(rows)
    summaries = []
    for unit, label in [
        ("participant_id", "Leave-one-participant-out"),
        ("case_id", "Leave-one-case-out")
    ]:
        part = loo_df[
            (loo_df["Leave-one-out unit"] == unit) & loo_df["Converged"]
        ]
        summaries.append({
            "Sensitivity analysis": label,
            "Successful fits": len(part),
            "Total fits": int((loo_df["Leave-one-out unit"] == unit).sum()),
            "Minimum time reduction (%)":
                float(part["Estimated time reduction (%)"].min()),
            "Maximum time reduction (%)":
                float(part["Estimated time reduction (%)"].max()),
            "Optimizers used": ", ".join(
                f"{k}: {v}" for k, v in
                Counter(part["Optimizer"]).items()
            )
        })
    return loo_df, pd.DataFrame(summaries)


def parametric_bootstrap(result, n_boot, seed):
    rng = np.random.default_rng(seed)
    X = result.model.exog
    vc_spec = result.model.exog_vc
    Z_matrices = [
        vc_spec.mats[k][0] for k in range(len(result.vcomp))
    ]
    beta = np.asarray(result.fe_params, dtype=float)
    variances = np.asarray(result.vcomp, dtype=float)
    residual_variance = float(result.scale)
    n = X.shape[0]

    coefficients = []
    boundary_warning_count = 0
    failed = 0

    for _ in range(n_boot):
        y_sim = X @ beta
        for variance, Z in zip(variances, Z_matrices):
            y_sim = y_sim + Z @ rng.normal(
                0, np.sqrt(max(variance, 0)), size=Z.shape[1]
            )
        y_sim = y_sim + rng.normal(
            0, np.sqrt(max(residual_variance, 0)), size=n
        )

        try:
            sim_model = sm.MixedLM(
                y_sim,
                X,
                groups=np.ones(n),
                exog_vc=vc_spec
            )
            with warnings.catch_warnings(record=True) as ws:
                warnings.simplefilter("always")
                sim_result = sim_model.fit(
                    reml=True, method="powell", maxiter=5000, disp=False
                )
            if sim_result.converged and np.all(np.isfinite(sim_result.fe_params)):
                coefficients.append(float(sim_result.fe_params[1]))
            else:
                failed += 1
            if any("boundary" in str(w.message).lower() for w in ws):
                boundary_warning_count += 1
        except Exception:
            failed += 1

    coefficients = np.asarray(coefficients, dtype=float)
    if len(coefficients) < max(1, int(np.ceil(0.9 * n_boot))):
        raise RuntimeError(
            f"Only {len(coefficients)} of {n_boot} bootstrap fits converged. "
            "Do not use the bootstrap interval without further investigation."
        )

    ci = np.quantile(coefficients, [0.025, 0.975])
    ratio_ci = np.exp(ci)
    reduction_ci = [
        float(100 * (1 - ratio_ci[1])),
        float(100 * (1 - ratio_ci[0]))
    ]
    summary = pd.DataFrame([{
        "Requested replicates": n_boot,
        "Converged replicates": len(coefficients),
        "Failed replicates": failed,
        "Replicates with boundary warning": boundary_warning_count,
        "Bootstrap coefficient median": float(np.median(coefficients)),
        "Coefficient 2.5th percentile": float(ci[0]),
        "Coefficient 97.5th percentile": float(ci[1]),
        "Time-ratio CI lower": float(ratio_ci[0]),
        "Time-ratio CI upper": float(ratio_ci[1]),
        "Time-reduction CI lower (%)": reduction_ci[0],
        "Time-reduction CI upper (%)": reduction_ci[1],
        "Random seed": seed
    }])
    samples = pd.DataFrame({
        "Bootstrap replicate": np.arange(1, len(coefficients) + 1),
        "Condition coefficient": coefficients
    })
    return summary, samples


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="RQ3 Excel workbook")
    parser.add_argument(
        "--output-dir", default="RQ3_Completion_Time_Results",
        help="Directory for output workbook and CSV files"
    )
    parser.add_argument("--bootstrap", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=20261108)
    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    df = prepare_data(input_path)
    data_checks = make_data_checks(df)

    main_result = fit_crossed_model(df, method="powell")
    main_effects = fixed_effect_table(main_result)
    main_condition = condition_summary(main_result)

    vc = dict(zip(main_result.model.exog_vc.names, main_result.vcomp))
    total_var = sum(vc.values()) + float(main_result.scale)
    variance_table = pd.DataFrame([
        {
            "Component": "Case random intercept",
            "Variance": float(vc.get("case", np.nan)),
            "Share of total variance": float(vc.get("case", 0) / total_var)
        },
        {
            "Component": "Participant random intercept",
            "Variance": float(vc.get("participant", np.nan)),
            "Share of total variance": float(vc.get("participant", 0) / total_var)
        },
        {
            "Component": "Residual",
            "Variance": float(main_result.scale),
            "Share of total variance": float(main_result.scale / total_var)
        }
    ])

    descriptives = df.groupby(
        "condition", observed=True
    )["completion_time_seconds"].agg(
        n="count", mean="mean", SD="std", median="median"
    ).reset_index()
    q = df.groupby(
        "condition", observed=True
    )["completion_time_seconds"].quantile([0.25, 0.75]).unstack()
    q.columns = ["Q1", "Q3"]
    descriptives = descriptives.merge(
        q.reset_index(), on="condition", how="left"
    )
    raw_means = df.groupby(
        "condition", observed=True
    )["completion_time_seconds"].mean()
    raw_reduction = float(
        100 * (1 - raw_means["Traceability-assisted"] / raw_means["Baseline"])
    )

    interruptions = df.loc[
        df["interruption_seconds"] > 0,
        [
            "participant_id", "condition", "case_id", "start_time",
            "end_time", "interruption_seconds", "completion_time_seconds"
        ]
    ].copy()
    interruptions["Researcher confirmation"] = (
        "External interruption or technical failure; deducted from elapsed time"
    )

    sensitivity, pfe_result, casefe_result = fit_sensitivity_models(df)
    optimizer_table = optimizer_check(df)
    loo_data, loo_summary = leave_one_out(df)
    bootstrap_summary, bootstrap_samples = parametric_bootstrap(
        main_result, args.bootstrap, args.seed
    )

    environment = pd.DataFrame([
        ("Python", __import__("sys").version.split()[0]),
        ("pandas", pd.__version__),
        ("numpy", np.__version__),
        ("scipy", scipy.__version__),
        ("statsmodels", statsmodels.__version__),
        ("Primary estimator", "REML; Powell optimizer"),
        ("Primary formula", MAIN_FORMULA),
        ("Bootstrap", f"{args.bootstrap} parametric replicates; seed={args.seed}")
    ], columns=["Item", "Value"])

    notes = pd.DataFrame([
        ("Timing definition",
         "From presentation of the complete validation result until submission of Q1-Q4."),
        ("Interruption handling",
         "Only external interruptions or technical failures are deducted. The three nonzero records (45, 45, 30 seconds) were confirmed by the researcher."),
        ("Excluded time",
         "The three Likert ratings are not included in Completion Time."),
        ("Primary model",
         "Cross-classified linear mixed-effects model with participant and case random intercepts."),
        ("Model interpretation",
         "exp(beta_condition) is the adjusted geometric-mean time ratio. 1-exp(beta_condition) is the estimated percentage time reduction."),
        ("Period and sequence",
         "Condition, Period, and Sequence are included as fixed effects. Condition x Period is not included because it is linearly dependent on these terms under the two-period, two-sequence design."),
        ("Random-slope check",
         "An independent participant condition-slope variance component was tested. Its estimate was optimizer-sensitive and reached the boundary under Powell/Nelder-Mead; it was not retained in the primary model."),
        ("Bootstrap caution",
         "Bootstrap refits with a variance component at/near zero are retained when the optimizer reports convergence. The number of boundary warnings is reported explicitly."),
        ("Case/participant sensitivity",
         "A participant-fixed-effects plus case-random-intercept model is reported as a conservative sensitivity analysis. Sequence is absorbed by participant fixed effects in that model."),
        ("Scope",
         "The model estimates the condition association for the 20 study cases and 20 participants; it does not establish universal effects for all maintenance tasks.")
    ], columns=["Topic", "Description"])

    output_xlsx = output_dir / "RQ3_Completion_Time_Results.xlsx"
    with pd.ExcelWriter(output_xlsx, engine="openpyxl") as writer:
        data_checks.to_excel(writer, sheet_name="Data_Validation", index=False)
        descriptives.to_excel(writer, sheet_name="Descriptives", index=False)
        interruptions.to_excel(writer, sheet_name="Interruptions", index=False)
        main_effects.to_excel(writer, sheet_name="Main_Model", index=False)
        variance_table.to_excel(writer, sheet_name="Variance_Components", index=False)
        sensitivity.to_excel(writer, sheet_name="Model_Sensitivity", index=False)
        optimizer_table.to_excel(writer, sheet_name="Optimizer_Check", index=False)
        loo_data.to_excel(writer, sheet_name="Leave_One_Out", index=False)
        loo_summary.to_excel(writer, sheet_name="LOO_Summary", index=False)
        bootstrap_summary.to_excel(writer, sheet_name="Bootstrap_Summary", index=False)
        bootstrap_samples.to_excel(writer, sheet_name="Bootstrap_Samples", index=False)
        environment.to_excel(writer, sheet_name="Environment", index=False)
        notes.to_excel(writer, sheet_name="Notes", index=False)

        workbook = writer.book
        for ws in workbook.worksheets:
            ws.freeze_panes = "A2"
            ws.auto_filter.ref = ws.dimensions
            for cell in ws[1]:
                cell.font = Font(bold=True, color="FFFFFF")
                cell.fill = PatternFill("solid", fgColor="34495E")
                cell.alignment = Alignment(wrap_text=True, vertical="center")
            for col_cells in ws.columns:
                max_len = max(
                    len(str(cell.value)) if cell.value is not None else 0
                    for cell in col_cells
                )
                ws.column_dimensions[get_column_letter(col_cells[0].column)].width = min(
                    max(14, max_len + 2), 55
                )
            ws.row_dimensions[1].height = 30

    bootstrap_samples.to_csv(
        output_dir / "RQ3_Completion_Time_Bootstrap_Samples.csv",
        index=False
    )

    print("Analysis completed.")
    print(f"Input: {input_path.resolve()}")
    print(f"Results workbook: {output_xlsx.resolve()}")
    print(f"Bootstrap samples: {args.bootstrap}")
    print(f"Raw arithmetic-mean time reduction: {raw_reduction:.2f}%")
    print(
        "Primary adjusted time reduction: "
        f"{main_condition['estimated_time_reduction_percent']:.2f}%"
    )
    print(
        "Primary REML Wald 95% CI: "
        f"[{main_condition['reduction_CI_lower_percent']:.2f}%, "
        f"{main_condition['reduction_CI_upper_percent']:.2f}%]"
    )
    print(
        "Bootstrap 95% CI: "
        f"[{bootstrap_summary.iloc[0]['Time-reduction CI lower (%)']:.2f}%, "
        f"{bootstrap_summary.iloc[0]['Time-reduction CI upper (%)']:.2f}%]"
    )


if __name__ == "__main__":
    main()
