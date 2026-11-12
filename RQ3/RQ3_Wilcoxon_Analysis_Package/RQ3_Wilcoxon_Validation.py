#!/usr/bin/env python3
"""Reproduce participant-level RQ3 Wilcoxon analyses and case-level descriptives.

The package is self-contained: by default, the script reads the frozen workbook
located beside this script and writes CSV outputs to the same directory.

Usage:
    python RQ3_Wilcoxon_Validation.py
    python RQ3_Wilcoxon_Validation.py --input-xlsx path/to/workbook.xlsx
    python RQ3_Wilcoxon_Validation.py --output-dir results --bootstrap-repetitions 50000

Dependencies: openpyxl, numpy, scipy.
"""

from __future__ import annotations
import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path
import hashlib
import numpy as np
from openpyxl import load_workbook
from scipy.stats import rankdata

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_INPUT = BASE_DIR / "RQ3_experiment_analysis(2).xlsx"
VALID_CONDITIONS = {"Baseline", "Traceability-assisted"}
TASK_COLUMNS = [
    "task1_scenario_identification_correct",
    "task2_violated_behavior_identification_correct",
    "task3_implementation_context_identification_correct",
    "task4_followup_verification_planning_correct",
]
METRICS = [
    ("Total accuracy", "total_accuracy", "higher"),
    ("Completion time (s)", "completion_time_seconds", "lower"),
    ("Analysability", "likert_analysability", "higher"),
    ("Modifiability", "likert_modifiability", "higher"),
    ("Testability", "likert_testability", "higher"),
]


def read_input(path: Path):
    if not path.is_file():
        raise FileNotFoundError(f"Input workbook not found: {path}")
    wb = load_workbook(path, data_only=True, read_only=True)
    if "Experiment_Data" not in wb.sheetnames:
        raise ValueError("Workbook does not contain the 'Experiment_Data' worksheet")
    ws = wb["Experiment_Data"]
    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        raise ValueError("Experiment_Data worksheet is empty")
    headers = list(rows[0])
    required = [
        "participant_id", "order_group", "condition", "case_id",
        "start_time", "end_time", "interruption_seconds",
        "completion_time_seconds", *TASK_COLUMNS, "total_accuracy",
        "likert_analysability", "likert_modifiability", "likert_testability",
        "valid_record",
    ]
    missing = [c for c in required if c not in headers]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    records = [dict(zip(headers, row)) for row in rows[1:]
               if row[headers.index("valid_record")] == 1]
    if len(records) != 40:
        raise ValueError(f"Expected 40 valid review records; found {len(records)}")
    for r in records:
        if r["condition"] not in VALID_CONDITIONS:
            raise ValueError(f"Unexpected condition: {r['condition']}")
        task_sum = sum(int(r[k]) for k in TASK_COLUMNS)
        if int(r["total_accuracy"]) != task_sum:
            raise ValueError(
                f"Task scores do not sum to total_accuracy for {r['participant_id']} / {r['case_id']}"
            )
        adjusted = float(r["end_time"]) - float(r["start_time"]) - float(r["interruption_seconds"])
        if not np.isclose(adjusted, float(r["completion_time_seconds"])):
            raise ValueError(
                f"Completion-time adjustment mismatch for {r['participant_id']} / {r['case_id']}: "
                f"expected {adjusted}, found {r['completion_time_seconds']}"
            )
    validate_design(records)
    return records


def validate_design(records):
    participants = defaultdict(list)
    cases = defaultdict(list)
    for r in records:
        participants[str(r["participant_id"])].append(r)
        cases[str(r["case_id"])].append(r)
    if len(participants) != 20 or len(cases) != 20:
        raise ValueError(f"Expected 20 participants and 20 cases; got {len(participants)} and {len(cases)}")
    for pid, group in participants.items():
        conds = [r["condition"] for r in group]
        if len(group) != 2 or set(conds) != VALID_CONDITIONS:
            raise ValueError(f"Participant {pid} does not have exactly one record per condition")
        if group[0]["case_id"] == group[1]["case_id"]:
            raise ValueError(f"Participant {pid} reviewed the same case in both conditions")
    for cid, group in cases.items():
        conds = [r["condition"] for r in group]
        if len(group) != 2 or set(conds) != VALID_CONDITIONS:
            raise ValueError(f"Case {cid} does not have exactly one record per condition")
        if group[0]["participant_id"] == group[1]["participant_id"]:
            raise ValueError(f"Case {cid} was reviewed by the same participant in both conditions")


def paired_groups(records, pair_key):
    groups = defaultdict(dict)
    for r in records:
        key = str(r[pair_key])
        condition = r["condition"]
        if condition in groups[key]:
            raise ValueError(f"Duplicate {condition} record for {pair_key}={key}")
        groups[key][condition] = r
    if len(groups) != 20 or any(set(g) != VALID_CONDITIONS for g in groups.values()):
        raise ValueError(f"Expected 20 complete Baseline/Traceability-assisted pairs by {pair_key}")
    return dict(sorted(groups.items()))


def oriented_difference(baseline, assisted, direction):
    # Positive values always favor traceability-assisted reporting.
    return float(baseline - assisted) if direction == "lower" else float(assisted - baseline)


def exact_two_sided_sign_permutation_p(w, ranks):
    """Exact two-sided p from all 2^n sign assignments to observed average ranks.

    Ranks are half-integers at most, so doubling them gives integer weights for
    exact dynamic-programming enumeration without floating-point comparisons.
    The two-sided probability is twice the lower tail at W=min(W+, W-).
    """
    distribution = {0: 1}
    for rank in ranks:
        weight = int(round(float(rank) * 2))
        nxt = distribution.copy()
        for total, count in distribution.items():
            nxt[total + weight] = nxt.get(total + weight, 0) + count
        distribution = nxt
    threshold = int(round(2 * float(w)))
    lower_tail_count = sum(count for total, count in distribution.items() if total <= threshold)
    return min(1.0, 2.0 * lower_tail_count / (2 ** len(ranks)))


def signed_rank_statistics(differences):
    d = np.asarray(differences, dtype=float)
    nonzero = d[d != 0]
    ranks = rankdata(np.abs(nonzero), method="average") if len(nonzero) else np.array([], dtype=float)
    w_plus = float(ranks[nonzero > 0].sum())
    w_minus = float(ranks[nonzero < 0].sum())
    w = min(w_plus, w_minus)
    total_rank = w_plus + w_minus
    rank_biserial = (w_plus - w_minus) / total_rank if total_rank else float("nan")
    tied_counts = Counter(float(x) for x in np.abs(nonzero))
    tied_groups = [f"{value:g}: {count}" for value, count in sorted(tied_counts.items()) if count > 1]
    return {
        "n_pairs": int(len(d)),
        "n_nonzero": int(len(nonzero)),
        "n_zero": int(np.sum(d == 0)),
        "positive_differences": int(np.sum(d > 0)),
        "negative_differences": int(np.sum(d < 0)),
        "W_positive": w_plus,
        "W_negative": w_minus,
        "W": w,
        "two_sided_exact_p": exact_two_sided_sign_permutation_p(w, ranks) if len(nonzero) else 1.0,
        "rank_biserial": rank_biserial,
        "tied_absolute_difference_groups": "; ".join(tied_groups),
    }


def holm_adjust(p_values):
    indexed = sorted(enumerate(p_values), key=lambda item: item[1])
    adjusted = [None] * len(p_values)
    running = 0.0
    for rank, (original_index, p) in enumerate(indexed):
        running = max(running, min(1.0, (len(p_values) - rank) * float(p)))
        adjusted[original_index] = running
    return adjusted


def bootstrap_mean_ci(differences, rng, repetitions):
    d = np.asarray(differences, dtype=float)
    draws = rng.integers(0, len(d), size=(repetitions, len(d)))
    means = d[draws].mean(axis=1)
    lower, upper = np.quantile(means, [0.025, 0.975])
    return float(lower), float(upper)


def quartiles(values):
    a = np.asarray(values, dtype=float)
    q1, q3 = np.quantile(a, [0.25, 0.75], method="linear")
    return float(np.median(a)), float(q1), float(q3), float(q3 - q1)


def write_csv(path, rows):
    if not rows:
        raise ValueError(f"Refusing to write an empty CSV: {path}")
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def build_participant_outputs(records, output_dir, bootstrap_repetitions, seed):
    groups = paired_groups(records, "participant_id")
    rng = np.random.default_rng(seed)
    summary_rows = []
    paired_rows = []
    for metric_name, column, direction in METRICS:
        differences = []
        baseline_values = []
        assisted_values = []
        for pid, group in groups.items():
            baseline = group["Baseline"]
            assisted = group["Traceability-assisted"]
            b = float(baseline[column])
            a = float(assisted[column])
            diff = oriented_difference(b, a, direction)
            differences.append(diff)
            baseline_values.append(b)
            assisted_values.append(a)
            paired_rows.append({
                "participant_id": pid,
                "order_group": baseline["order_group"],
                "metric": metric_name,
                "baseline_case_id": baseline["case_id"],
                "traceability_assisted_case_id": assisted["case_id"],
                "baseline_value": b,
                "traceability_assisted_value": a,
                "signed_difference_favoring_assisted": diff,
            })
        d = np.asarray(differences, dtype=float)
        stats = signed_rank_statistics(d)
        ci_low, ci_high = bootstrap_mean_ci(d, rng, bootstrap_repetitions)
        b_med, b_q1, b_q3, b_iqr = quartiles(baseline_values)
        a_med, a_q1, a_q3, a_iqr = quartiles(assisted_values)
        summary_rows.append({
            "analysis_level": "Participant-level",
            "metric": metric_name,
            "baseline_median": b_med,
            "baseline_q1": b_q1,
            "baseline_q3": b_q3,
            "baseline_iqr": b_iqr,
            "traceability_assisted_median": a_med,
            "traceability_assisted_q1": a_q1,
            "traceability_assisted_q3": a_q3,
            "traceability_assisted_iqr": a_iqr,
            "difference_direction": "Baseline minus assisted" if direction == "lower" else "Assisted minus baseline",
            "mean_paired_difference": float(np.mean(d)),
            "median_paired_difference": float(np.median(d)),
            "paired_bootstrap_95CI_lower": ci_low,
            "paired_bootstrap_95CI_upper": ci_high,
            **stats,
            "Holm_adjusted_p": "",
        })
    likert_indices = [i for i, row in enumerate(summary_rows)
                      if row["metric"] in {"Analysability", "Modifiability", "Testability"}]
    adjusted = holm_adjust([summary_rows[i]["two_sided_exact_p"] for i in likert_indices])
    for idx, p_adj in zip(likert_indices, adjusted):
        summary_rows[idx]["Holm_adjusted_p"] = p_adj
    write_csv(output_dir / "RQ3_Wilcoxon_Summary.csv", summary_rows)
    write_csv(output_dir / "RQ3_Wilcoxon_Paired_Differences.csv", paired_rows)
    return summary_rows, paired_rows


def build_case_descriptives(records, output_dir):
    groups = paired_groups(records, "case_id")
    rows = []
    for case_id, group in groups.items():
        b = group["Baseline"]
        a = group["Traceability-assisted"]
        accuracy_diff = oriented_difference(float(b["total_accuracy"]), float(a["total_accuracy"]), "higher")
        time_reduction = oriented_difference(float(b["completion_time_seconds"]), float(a["completion_time_seconds"]), "lower")
        rows.append({
            "case_id": case_id,
            "baseline_participant_id": b["participant_id"],
            "traceability_assisted_participant_id": a["participant_id"],
            "baseline_total_accuracy": int(b["total_accuracy"]),
            "traceability_assisted_total_accuracy": int(a["total_accuracy"]),
            "accuracy_difference_favoring_assisted": accuracy_diff,
            "accuracy_comparison": "Improved" if accuracy_diff > 0 else ("Unchanged" if accuracy_diff == 0 else "Lower"),
            "baseline_completion_time_seconds": float(b["completion_time_seconds"]),
            "traceability_assisted_completion_time_seconds": float(a["completion_time_seconds"]),
            "completion_time_reduction_seconds": time_reduction,
        })
    write_csv(output_dir / "RQ3_Case_Level_Descriptives.csv", rows)
    accuracy_diffs = np.array([r["accuracy_difference_favoring_assisted"] for r in rows], dtype=float)
    time_reductions = np.array([r["completion_time_reduction_seconds"] for r in rows], dtype=float)
    accuracy_counts = Counter(r["accuracy_comparison"] for r in rows)
    return {
        "case_count": len(rows),
        "accuracy_improved": accuracy_counts.get("Improved", 0),
        "accuracy_unchanged": accuracy_counts.get("Unchanged", 0),
        "accuracy_lower": accuracy_counts.get("Lower", 0),
        "accuracy_mean_difference": float(np.mean(accuracy_diffs)),
        "accuracy_median_difference": float(np.median(accuracy_diffs)),
        "time_reduced_cases": int(np.sum(time_reductions > 0)),
        "time_unchanged_cases": int(np.sum(time_reductions == 0)),
        "time_increased_cases": int(np.sum(time_reductions < 0)),
        "time_reduction_mean_seconds": float(np.mean(time_reductions)),
        "time_reduction_median_seconds": float(np.median(time_reductions)),
        "time_reduction_q1_seconds": float(np.quantile(time_reductions, 0.25, method="linear")),
        "time_reduction_q3_seconds": float(np.quantile(time_reductions, 0.75, method="linear")),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-xlsx", default=str(DEFAULT_INPUT), help="Frozen Excel input; defaults to the workbook in this folder.")
    parser.add_argument("--output-dir", default=str(BASE_DIR), help="Directory for generated CSV files; defaults to this folder.")
    parser.add_argument("--bootstrap-repetitions", type=int, default=50000)
    parser.add_argument("--seed", type=int, default=20261108)
    args = parser.parse_args()
    if args.bootstrap_repetitions < 1000:
        raise ValueError("Use at least 1,000 bootstrap repetitions; default is 50,000")
    input_path = Path(args.input_xlsx).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    records = read_input(input_path)
    summary, _ = build_participant_outputs(records, output_dir, args.bootstrap_repetitions, args.seed)
    case_summary = build_case_descriptives(records, output_dir)
    digest = hashlib.sha256(input_path.read_bytes()).hexdigest()
    print(f"Input workbook: {input_path}")
    print(f"Input SHA-256: {digest}")
    print(f"Valid records: {len(records)}; participants: 20; cases: 20")
    print("Participant-level Wilcoxon results:")
    for row in summary:
        print(f"  {row['metric']}: W={row['W']:.1f}, exact p={row['two_sided_exact_p']:.10f}, "
              f"r_rb={row['rank_biserial']:.6f}, zero={row['n_zero']}, "
              f"Holm={row['Holm_adjusted_p']}")
    print("Case-level descriptive results (no inferential test):")
    for key, value in case_summary.items():
        print(f"  {key}: {value}")
    print(f"Outputs written to: {output_dir}")


if __name__ == "__main__":
    main()
