# RQ2 Instructions: Mutation-Based Mismatch Detection and Localization

This guide explains how the RQ2 mutation experiment was conducted, how to repeat the verification **workflow** using the supplied tool and program artifacts, and how to inspect the **historical results** reported in *An Automated Functional Scenario-Based Verification Approach to Support Program Maintenance*.

For a summary of the experiment and a description of the data files, see the [RQ2 README](README.md). For installation and general GUI usage, consult the tool documentation provided elsewhere in the supplementary repository.

## 1. Scope and required materials

RQ2 evaluates whether FSF-derived tests detect behavioral changes introduced by approved Java mutants and whether detected mismatches are associated with the expected functional scenarios and observable fields. The reported experiment covers **20 processes**, **59 approved mutants**, and **six subject systems**.

The following materials serve different purposes:

| Material | Use |
| --- | --- |
| Runnable verification tool and its tool README | Launch the GUI and execute new verification runs. |
| SOFL and process-level FSF specifications | Define each process, its functional scenarios, test conditions, and expected behavior. |
| Original Java implementations and approved mutant implementations | Provide the original and modified implementations for the verification workflow. |
| `rq2_experiment_data.xlsx` → `MutantSummary` | Identify mutants and their predefined affected scenarios, input regions, and observable fields. |
| `rq2_experiment_data.xlsx` → `FixedTestSuite` | Inspect the fixed concrete test inputs recorded for the original experiment. |
| `rq2_experiment_data.xlsx` → `MutantRunData` | Inspect recorded detection, mismatch counts, test-case identifiers, and localization outcomes. |
| `Archived_Verification_Records/` | Inspect saved outcomes through the GUI without rerunning Java code. |

The specifications, Java implementations, tool package, and relevant configuration are supplied in the accompanying repository materials; their locations may differ from the RQ2 data folder. Match artifacts using their **process and mutant identifiers** rather than assuming a particular directory layout.

## 2. Original experimental procedure

The steps below describe the **procedure used to produce the reported RQ2 results**. They are also the procedural model for a new GUI-based run, subject to the replay limitation in Section 5.

1. **Prepare one process.** Load its SOFL specification, corresponding process-level FSF specification, and original Java implementation. Establish and confirm the required process-to-method and variable-to-parameter bindings.
2. **Apply the test-generation configuration.** For the evaluation, generation was configured to produce **at most 10 valid test inputs per test condition**. The other generation parameters must follow the supplied experimental configuration; do not infer unspecified values.
3. **Generate and freeze the process-level suite.** Generate the complete suite from the **original FSF specification**, including concrete test inputs and their expected results. The suite was generated **once per process**, before running any mutant of that process.
4. **Load a mutant.** Replace the original Java implementation with one approved mutant of the same process using the GUI. Re-establish and confirm the required bindings to the loaded implementation, using the same predefined specification–program correspondences.
5. **Execute the complete fixed suite.** Run the process-level suite against the mutant and inspect the expected–actual comparisons, Boolean verification outcomes, and associated functional scenarios and observable fields.
6. **Record the run.** Record the mutant identifier, mismatches, mismatching test-case identifiers, and the associated scenario/field information.
7. **Continue with the next mutant.** Replace the loaded implementation with the next approved mutant of the same process, reconfirm bindings, and repeat execution **without regenerating or modifying the process-level test suite**.
8. **Continue with the next process.** Establish a fresh process context and repeat the procedure using that process's original FSF-derived suite.

**Fixed-suite rule:** The SOFL and FSF specifications, test-generation configuration, concrete test inputs, expected results, and oracle definitions remained unchanged among mutant runs belonging to the **same process**. Inputs could differ **between processes** and among test conditions, but not between mutants of the same process. The GUI replacement of Java implementations and binding confirmation were supervised operations.

**Important:** The `FixedTestSuite` worksheet records the historical fixed inputs. It is **not** an executable replay package for the current tool. Section 5 explains what a newly performed run can and cannot reproduce.

## 3. Examine the recorded RQ2 results

Use `rq2_experiment_data.xlsx` to trace recorded outcomes back to the predefined mutation targets:

1. Open **`MutantSummary`** and locate a mutant using its identifier. Review its mutation category, affected functional scenario(s), expected input region, and expected mismatching field(s).
2. Open **`FixedTestSuite`** and find the process's recorded test cases. Check the scenario and test-case identifiers used to organize its historical inputs.
3. Open **`MutantRunData`** and find the same mutant identifier. Inspect the reported detected/not-detected status, number of mismatch observations, relevant test-case identifiers, and scenario/field associations.
4. For a detected mutant, compare the reported scenario and observable-field associations against the predefined information in `MutantSummary`.
5. Where an archived record is available, use Section 4 to inspect the corresponding saved verification outcomes in the GUI.

A **mismatch observation** is an individual test case that produces a mismatch. A mutant is counted as **detected** when at least one reported mismatch is consistent with the predefined ground truth. Consequently, mismatch observations and detected mutants are **different counting units**.

The historical results reported in Section 5.4.2 of the paper are:

| Result | Reported value |
| --- | ---: |
| Approved mutants | 59 |
| Detected mutants | 57 |
| Mutant-level detection rate | 96.6% |
| Mismatch observations | 180 |
| Correctly localized functional scenarios among detected mutants | 57/57 |
| Correctly localized observable fields among detected mutants | 57/57 |

The two undetected mutants were **ATM-02-M01** and **PTT-04-M02**. Their distinguishing input regions were not exercised by the historical fixed suites. The published analysis identifies the boundary value `a_amount = 30000` for ATM-02-M01 and a positive-amount subregion of `PTT04-FS-01` for PTT-04-M02.

**Counting clarification:** If the dataset includes `Affected_Scenario_Test_Case_Count`, this is the number of tests associated with the functional scenarios affected by a given mutant. It is **not** the complete process-level test-suite size, and variation in this field does not mean mutant-specific suites were generated.

## 4. Inspect archived verification records in the GUI

The `Archived_Verification_Records/` folder contains saved verification records for **view-only inspection** through the existing theorem import interface.

1. Launch the provided GUI tool using the installation instructions in the tool README.
2. Use **Add theorem** to import **`theorem_RQ2_History.txt`**.
3. Once that file appears in the tool, **right-click the imported item** and choose **Add CSV Data**.
4. Select a compatible saved CSV verification record from `Archived_Verification_Records/`.
5. Inspect the restored test information and Boolean outcomes. In the result display, **green** represents a stored `true` result and **red** represents a stored `false` result.
6. Compare the archived outcome with the corresponding entry in `MutantRunData`, using the process, mutant, and test-case identifiers where available.

**This is an inspection operation only.** Importing a saved record does **not** recompile Java source code, re-execute a mutant, generate new inputs, or repeat oracle comparisons. The historical colors and outcomes describe **stored** results.

## 5. Repeating the workflow versus reproducing historical executions

Two forms of independent examination are supported:

- **Repeat the verification workflow:** Use the supplied tool, specifications, Java implementations, and configuration to generate a process-level suite and execute it against approved mutants. Keep that newly generated suite fixed across mutant runs of the same process.
- **Audit the reported historical experiment:** Use `MutantSummary`, `FixedTestSuite`, `MutantRunData`, and archived records to examine the original fixed inputs, mutant results, and reported scenario/field associations.

The current tool **cannot import the historical fixed inputs and automatically replay the original mutant executions**. A new generation run may therefore produce different concrete inputs and different detection results, even when the same process and generation limit are used. Do **not** treat newly generated inputs or subsequent GUI executions as identical reproductions of the historical fixed-suite runs.

This limitation also means that the reported **57/59** detection result and **180** mismatch observations should be checked against the supplied historical records, rather than promised as automatic outputs of a newly generated run.
