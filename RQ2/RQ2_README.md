# RQ2: Mutation-Based Mismatch Detection and Localization

This directory contains the experimental records and supporting materials for **RQ2** of *An Automated Functional Scenario-Based Verification Approach to Support Program Maintenance*. RQ2 examines whether the proposed approach detects behavioral mismatches introduced by Java program mutations and associates detected mismatches with the relevant functional scenarios and observable program elements.

The reported experiment covers **20 processes from six subject systems** and **59 approved mutants**. Of these, **57 mutants were detected**, corresponding to a **96.6% mutant-level detection rate**, with **180 mismatch observations**. The original experiment was conducted interactively using the tool's graphical user interface (GUI).

## 1. Files and Their Roles

| Material | Purpose |
| --- | --- |
| `rq2_experiment_data.xlsx` — `MutantSummary` | Identifies each mutant, its mutation category, the affected functional scenario(s), the expected input region, and the expected mismatching field(s). |
| `rq2_experiment_data.xlsx` — `MutantRunData` | Records mutant-level outcomes, including detected/not-detected status, mismatch counts, test-case identifiers associated with mismatches, and reported scenario/field associations. |
| `rq2_experiment_data.xlsx` — `FixedTestSuite` | Records the fixed test inputs used for each process, organized by process, functional scenario, and test-case identifier. |
| `Archived_Verification_Records/` | Contains saved verification records that can be imported into the tool to inspect previously stored outcomes. |

The SOFL/FSF specifications, original Java implementations, approved mutant implementations, relevant bindings, and runnable tool package are provided separately in the accompanying repository materials. Consult the repository's tool instructions for installation and launch requirements.

## 2. RQ2 Experimental Procedure

1. For each process, the SOFL specification and corresponding FSF specification were loaded, and the required specification–program bindings and test-generation settings were established.
2. The process-level test suite and associated oracle information were generated **once** for that process.
3. The original Java implementation was replaced manually with one approved mutant through the GUI. The SOFL/FSF specifications, functional scenarios, bindings, test-generation settings, generated test inputs, and oracle definitions were not changed between mutant runs of that process.
4. The complete fixed process-level test suite was executed against the loaded mutant. The verification outcomes and the associated scenario/field information were inspected and recorded.
5. The Java implementation was replaced with the next mutant of the same process, without regenerating the test suite, and Steps 3–4 were repeated.

## 3. Inspecting Archived Verification Records

The `Archived_Verification_Records/` directory contains saved verification data for inspection through the tool's existing **Add theorem** import function.

1. Launch the provided GUI tool.
2. Use **Add theorem** to select the `theorem_RQ2_History.txt` file. Once the theorem file has been added, right-click on it, use **Add CSV Data** to select a compatible archival records.
3. Inspect the verification information restored by the tool. In the result display, **green** indicates a stored `true` outcome and **red** indicates a stored `false` outcome.

**Importing an archived verification record only restores previously saved information for inspection. It does not recompile or re-execute the corresponding Java mutant.** These archives are provided as **historical verification records**.

## 4. Reproducing the Workflow

The runnable tool and accompanying specification, Java, mutant, and configuration artifacts allow researchers to **repeat the functional scenario-based verification workflow** through the GUI. The fixed-input worksheet, mutant-level summary, and archived verification records allow the **reported historical experiment** to be examined separately.

The current tool does **not** support importing the archived fixed test inputs and automatically replaying the original mutant executions. Accordingly, rerunning test generation may produce a different set of inputs and may not reproduce the exact reported mutant-detection totals. We do not present newly generated test inputs or subsequent runs as records of the original experiment.
