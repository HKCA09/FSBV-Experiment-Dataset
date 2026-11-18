# RQ1 Replication Instructions: Operational Feasibility

This guide describes how to use the **Functional Scenario-Based Verification Supporting Tool** to repeat the **RQ1 operational-feasibility procedure** reported in *An Automated Functional Scenario-Based Verification Approach to Support Program Maintenance*. 

For the complete feature overview and installation-package information, consult the tool's main README in the supplementary repository.

## 1. Objective and evaluation scope

RQ1 asks whether the tool can complete the functional scenario-based verification workflow for the selected FSF-specified processes. Each process is examined **independently**, using its original Java implementation and corresponding SOFL and process-level FSF specifications.

The published evaluation covers the following processes:

| Subject system | Process identifiers | Number of processes |
| --- | --- | ---: |
| Automated Teller Machine | ATM-01 to ATM-04 | 4 |
| Course Registration | CR-01 to CR-03 | 3 |
| Hospital Registration | HR-01 to HR-03 | 3 |
| Public Transport Ticketing | PTT-01 to PTT-05 | 5 |
| Stock Trading | ST-01 to ST-02 | 2 |
| Vending Machine | VM-01 to VM-03 | 3 |
| **Total** | | **20** |

A first-time user may start with one complete process to become familiar with the GUI, then apply the same procedure to all 20 processes to examine the full RQ1 evaluation scope.

## 2. Requirements and input artifacts

1. Obtain and extract the packaged verification tool. Launch the executable or launcher supplied with the package. The packaged version includes its required Java runtime, so a separate Java installation is not required for launching that version.
2. For the selected process, locate the corresponding **SOFL specification**, **process-level FSF specification**, and **original Java implementation** in the supplied experimental materials. Use the matching artifacts for the same process identifier.
3. Keep the process identifiers and relevant specification-to-program correspondences available when examining the bindings.
4. Use the experimental configuration documented with the corresponding materials. The evaluation set the generation limit to **at most 10 valid test inputs per test condition**. Distance-related settings should be taken from the provided configuration, if available, rather than guessed.

**Important:** RQ1 uses the original implementations, not the seeded faulty variants used in RQ2. A new tool execution should not be confused with inspecting an archived verification record.

## 3. Run the verification procedure

Perform the following steps for **one process at a time**, starting with a fresh execution context so that data, bindings, settings, or runtime state from another process do not affect the run. If the application does not offer an explicit way to clear the current context, close and reopen it before loading the next process.

### Step 1. Import the original Java implementation

1. Click **Add Java File** and select the Java source file for the process.
2. Confirm that the expected class and methods appear in the **Java File** tree.

### Step 2. Import the SOFL and FSF specifications

1. Click **Add Specification** and select the corresponding SOFL specification.
2. Confirm that the expected module and process appear in the **SOFL Spec** tree.
3. Select the process and add or select its corresponding process-level FSF specification.
4. Inspect the extracted functional scenarios and their **Test Conditions** and **Defining Conditions**. Select a test condition to examine the associated **Atomic Predicates**, where applicable.

### Step 3. Configure and generate test inputs

1. Open **Setting** and check the generation configuration. For an evaluation-style run, set the upper limit to **10 valid inputs per test condition**; preserve the other documented experimental settings.
2. Select a complete **Test Condition** and click **Generate** in the corresponding pane.
3. Check that the generated valid inputs appear in the **Test Case** table.
4. Repeat for all relevant test conditions of the selected process. Record any branch reported as **unsupported** or **generation_failure**; do not treat these statuses as proof that the branch is logically unsatisfiable.

Generating values for an individual **Atomic Predicate** is an available exploratory feature, but it does not replace the complete test-condition generation used for the RQ1 process-level workflow.

### Step 4. Check the expected results and bindings

1. Confirm that scenario-specific oracle expectations have been derived from the corresponding **Defining Conditions** and that the expected results are available for generated test cases.
2. Where the GUI provides **Add Test Oracle**, use it to inspect or manage the applicable oracle information as supported by the interface. The evaluated workflow does **not** require a separately imported theorem file for deriving the defining-condition-based expectations.
3. Inspect the **process-to-method binding** and verify that the SOFL process is associated with the intended Java method.
4. Inspect the **variable-to-parameter binding** and verify that the required input variables match the intended Java parameters.
5. If an automatically suggested process-to-method binding is missing or incorrect, select and confirm the correct target method manually before execution. Record this as a non-routine intervention.

Manual binding adjustments are permitted. **Do not modify** the SOFL or FSF specifications, Java implementation, generated test inputs, or oracle definitions to obtain a successful outcome.

### Step 5. Execute and inspect the results

1. Confirm that the required test cases, expected results, and bindings are ready.
2. Click **Execute Program** to execute the test cases currently listed for the active verification target.
3. Inspect the collected Java outputs, expected–actual comparisons, and Boolean verification outcomes.
4. Check that each verification result remains linked to its originating process, functional scenario, and relevant program elements.

A result of **TRUE** indicates that the observed outputs met the supported oracle expectations for that executed test case; **FALSE** indicates an observed mismatch. Neither outcome alone constitutes a diagnosis of a particular faulty statement.

### Step 6. Record the result and proceed to the next process

Record the process identifier; successfully parsed executable scenarios and test conditions; number of valid test inputs; oracle availability; binding, execution, checking, and reporting completion; and any non-routine binding intervention. Save or export generated test data and available verification records if needed for inspection.

Before starting another process, establish a fresh execution context and load the next process's matching artifacts.

## 4. Completion criteria

The RQ1 evaluation assessed seven stages. Use the following criteria when reviewing each process:

| Stage | Completion criterion |
| --- | --- |
| FSF parsing | Functional scenarios and their test and defining conditions are correctly extracted. |
| Test case generation | Valid inputs are produced for all branches required by the evaluated scenarios. Unsupported branches or generation failures are not counted as completed. |
| Oracle derivation | An expected result is obtained for every generated input. |
| Specification–program binding | The target method and required input-variable mappings are established, confirmed, and pass pre-execution checks. |
| Program execution | Every planned input reaches method invocation. |
| Conformance checking | Every planned input produces an expected–actual comparison. |
| Traceable result construction | Execution outcomes are retained with their corresponding specification and program context. |

Classify the overall process status as **Completed**, **Failed**, or **Not executed**. Record separately whether non-routine user intervention was required. A manually corrected binding does not by itself make the process unsuccessful if the required stages subsequently complete.

## 5. Published RQ1 results for comparison

The paper reports the following aggregate results in **Section 5.4.1, Table 2**:

| Reported measure | Result |
| --- | ---: |
| Evaluated processes | 20 |
| Executable functional scenarios | 47 |
| Successfully parsed scenarios | 47/47 |
| Executable test conditions producing valid inputs | 47/47 |
| Generated test inputs | 153 |
| Scenarios with completed oracle construction | 47/47 |
| Processes completing binding, execution, checking, and reporting | 20/20 |
| Processes without non-routine binding adjustments | 16/20 |
| Processes requiring manual target-method selection | 4/20 |

The four manually adjusted processes occurred across the Automated Teller Machine, Course Registration, Public Transport Ticketing, and Stock Trading systems (one process in each system). Their process-to-method bindings were corrected before the remaining automated verification activities.

**Interpretation:** These are the reported observations, not an assertion that a new run necessarily reproduces the identical concrete inputs or total input count. Exact test inputs may depend on the full generation configuration and execution behavior. For comparison with the original experiment, preserve the documented settings and consult the supplied experimental records.

## 6. Scope and troubleshooting

- **Missing or incorrect bindings:** Inspect and correct the proposed method or parameter correspondence before execution; document any manual change.
- **Unsupported test conditions or generation failures:** Record the reported status and the affected condition. Such a status does not establish logical unsatisfiability.
- **Results differ from the paper:** First confirm the process identifier, original implementation, FSF version, generation settings, and fresh execution context. Compare available recorded inputs and expectations rather than assuming independently generated values will be identical.
- **Archived records:** The tool supports viewing previously archived verification results, but importing an archived record does **not** re-execute that historical run.

The main purpose of this guide is to repeat and inspect the RQ1 process-level verification workflow. For mutation analysis and user-study statistical reproduction, use the separate RQ2 and RQ3 materials.
