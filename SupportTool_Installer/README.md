# Functional Scenario-Based Verification Supporting Tool

## Overview

This tool supports the automated functional scenario-based verification approach proposed in the paper An Automated Functional Scenario-Based Verification Approach to Support Program Maintenance. 

The tool integrates SOFL formal specification parsing, Functional Scenario Form (FSF) processing, test case generation, test oracle derivation, specification–program binding, automated Java method execution, and conformance checking within a unified JavaFX graphical interface. It generates scenario-linked test cases from FSF test conditions using V-Method-based techniques and derives expected results from the corresponding defining conditions. By establishing mappings between specification elements and Java program interfaces, the tool executes the target methods and evaluates their actual results against the specified expectations.

This implementation builds on earlier V-Method prototype tools and extends their capabilities toward an integrated workflow for specification-guided program verification and maintenance-oriented result analysis.

\---

## Download and Installation

The executable version of the FSF Verification Tool is distributed as a Windows installer through GitHub Releases.

1. Open the **Releases** section of this repository.
2. Download the latest available Windows installer (`.exe`) from the release assets.
3. Run the installer and follow the installation instructions.
4. Launch the FSF Verification Tool after installation.

The installer includes the required Java runtime environment, so a separate Java installation is not required for normal use of the packaged application.

For instructions on loading SOFL specifications, generating test cases, executing Java programs, and inspecting verification results, see the **Quick Start** section below.

\---

## Main Features

### 1\. SOFL Specification Processing

* Imports SOFL specification files.
* Reads Functional Scenario Form (FSF) associated with a specification process.
* Extracts Test Conditions (TCs) and their Atomic Predicates (APs).
* Displays the structure of the loaded specification through the GUI.

### 2\. Automatic Test-Data Generation

* Generates test data from a selected Test Condition.
* Generates test data from an individual Atomic Predicate.
* Applies the Vibration Method to generate values at specified distances from constraint boundaries.
* Allows users to configure:

  * the number of generated test cases;
  * vibration distance;
  * distance increment;
  * other generation-related settings.

### 3\. Supported Expression Categories

The improved tool supports test-data generation for a variety of SOFL expression categories, including:

* Numeric expressions
* Sequence expressions
* Set expressions
* Composite-type expressions
* Conjunctions containing multiple Atomic Predicates
* Selected combinations of SOFL operators and arithmetic expressions

### 4\. Distance-Based Test Generation

The Vibration Method generates test data according to the distance between a generated value and a constraint boundary.

For example, given:

```text
x > 10
```

the tool can generate test values at user-defined distances from the boundary value `10`.

The distance settings can be configured through the **Setting** interface. Depending on the selected data type and expression structure, the tool applies the corresponding generation strategy.

### 5\. Java File Support

* Imports Java source files.
* Displays Java classes and methods in the GUI.
* Allows Java source code to be viewed together with the corresponding specification materials.

### 6\. Specification–Program Binding

* Establishes mappings between SOFL specification processes and their corresponding Java methods.
* Supports variable-to-parameter binding to connect specification inputs with Java method parameters.
* Provides automatically suggested bindings and allows users to manually select or correct mappings when necessary.
* Preserves the relationships between specification elements and implementation interfaces throughout verification.

### 7\. Test Oracle Derivation and Management

* Derives expected results from the Defining Conditions (DCs) of functional scenarios.
* Supports test oracles for method return values and observable object fields.
* Allows users to add test oracles associated with the corresponding functional scenarios and generated test cases.
* Uses the expected results as checking criteria for subsequent program verification.

### 8\. Automated Java Execution and Conformance Checking

* Imports Java source files and displays their classes and methods through the GUI.
* Executes the target Java methods using test cases generated from FSF Test Conditions.
* Allows users to initiate verification through the **Execute Program** function.
* Evaluates actual execution results against the expected results specified by the corresponding test oracles.
* Reports passing and failing verification outcomes based on the observed conformance of the Java implementation to the specification.

### 9\. Theorem-Based Testing Functions

The tool retains theorem-related functions from the original V-Method prototype.

* Theorem files can be imported.
* Test data can be generated from theorem assumptions.
* Generated data can be used to check whether the theorem conclusion holds.
* The result is displayed as `TRUE` or `FALSE`.

### 10\. Verification Result Management

* Supports saving verification-related information for subsequent inspection and analysis.
* Allows users to import previously archived verification records for result inspection.
* Displays historical verification outcomes and their associated information without requiring new test generation.
* Facilitates the review and reuse of verification evidence in maintenance-oriented activities.

\---

## Installation

1. Extract the installation package to a local directory.
2. Run the executable or launcher included in the package.
3. Keep the example files included in the package available for initial testing.

The required Java runtime environment is bundled with the installation package. Users do not need to install Java separately before running the tool.

\---

## User Interface

The main interface contains the following areas:

* **SOFL Spec**  
Displays imported SOFL specifications, modules, processes, and associated FSF files.
* **Java File**  
Displays imported Java classes and methods.
* **Test Condition**  
Lists the test conditions derived from the selected Functional Scenario Form.
* **Atomic Predicate**  
Displays the atomic predicates contained in the selected Test Condition.
* **Add Test Oracle / Theorem**  
Displays Test Oracle / theorem-related information when theorem-based testing is used.
* **Test Case**  
Displays generated test data, including variables, values, distances, and available result information.
* **Preview / Source Code**  
Displays the selected specification or Java source file.
* **Setting**  
Opens the configuration interface for test-data generation.

\---

## Quick Start

### Step 1: Import a Java File

1. Click **Add Java File**.
2. Select a Java source file.
3. The imported class and its methods will appear in the **Java File** tree.

### Step 2: Add a Specification

1. Click **Add Specification**, or use the corresponding operation for the selected project/class.
2. Select the SOFL specification file.
3. Confirm that the module and process are displayed in the **SOFL Spec** tree.

### Step 3: Add the Functional Scenario Form

1. Select the target SOFL process.
2. Add or select the corresponding FSF file.
3. The tool extracts the functional scenarios and lists them as **Test Condition 1**, **Test Condition 2**, and so on.

### Step 4: Inspect Test Conditions and Atomic Predicates

1. Select a Test Condition.
2. The Atomic Predicates belonging to that condition are displayed in the **Atomic Predicate** pane.
3. You may generate test data either from the complete Test Condition or from an individual Atomic Predicate.

### Step 5: Configure Test-Data Generation

1. Click **Setting**.
2. Configure the required generation parameters, such as:

   * number of test cases;
   * distance;
   * distance increment.
3. Return to the main interface after saving the settings.

### Step 6: Generate Test Data from a Test Condition

1. Select the target Test Condition.
2. Click **Generate** above the Test Condition pane.
3. The generated test data are displayed in the **Test Case** table.

### Step 7: Generate Test Data from an Atomic Predicate

1. Select an Atomic Predicate.
2. Click **Generate** above the Atomic Predicate pane.
3. The generated data for the selected AP are displayed in the table.

### Step 8: Review the Generated Test Cases

The **Test Case** table normally includes:

* variable names;
* generated values;
* distance values;
* other available test information.

Review the generated data before saving or using them in subsequent testing activities.

### Step 9: Save Generated Test Cases

1. Click **Save**.
2. Select the output location.
3. Keep the saved test data together with the corresponding specification and generation settings if the experiment needs to be reproduced.

\---

## Program Verification Using Test Oracles

### Step 1: Add a Test Oracle

1. Select the relevant functional scenario and its generated test cases.
2. Click **Add Test Oracle**.
3. Add the test oracle corresponding to the selected functional scenario (defining condition).

The test oracle provides the expected result derived from the defining condition of the functional scenario and is used to evaluate the actual program execution result.

### Step 2: Confirm Specification–Program Binding

1. Identify the Java method corresponding to the selected SOFL process.
2. Confirm that the process-to-method and variable-to-parameter bindings are correct.

If the automatically proposed binding is incorrect or unavailable, select the appropriate target method or mapping manually.
Correct specification–program bindings are required to execute the generated test cases against the intended Java implementation.

### Step 3: Execute the Java Program

1. Confirm that the required test cases and test oracle are available.
2. Click **Execute Program**.
3. Inspect the expected and actual values and their corresponding verification outcomes.
4. A result of `TRUE` indicates that the observed behavior satisfies the test oracle for the executed test case, while `FALSE` indicates an observed mismatch.

\---

## Recommended Workflow for First-Time Users

1. Start with the example projects included in the installation package.
2. Import the Java file.
3. Import the SOFL specification.
4. Add the corresponding FSF file.
5. Select a Test Condition and inspect its Atomic Predicates.
6. Open **Setting** and configure the test-generation parameters.
7. Generate test cases from the complete Test Condition.
8. Review the generated test cases and save them if required.
9. Click **Add Test Oracle** to add the corresponding test oracle.
10. Confirm that the SOFL process and its variables are correctly bound to the target Java method and parameters.
11. Click **Execute Program** to perform program verification.
12. After confirming that the example works correctly, repeat the same process using your own specification.

\---

## Notes and Current Scope

The current implementation supports a broad range of SOFL expressions, but some highly complex combinations may still require further extension. Examples include very deeply nested expressions or unusual combinations of multiple data abstractions.

When evaluating the tool, users are encouraged to keep the exact specification, FSF file, generation settings, and generated test cases so that results can be reproduced.

\---

## Example Files

The installation package includes example materials that can be used to test the tool, such as:

* Java source file;
* SOFL specification file;
* Functional Scenario Form file;
* theorem file.

It is recommended that first-time users run an included example before importing their own project.

\---

## Contact

For questions, bug reports, or further information, please contact the development team.

Email: **syliu@sei.ecnu.edu.cn**

