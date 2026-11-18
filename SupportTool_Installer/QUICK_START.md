# Quick Start: Functional Scenario-Based Verification Tool

This guide explains how to launch the tool and complete a basic **functional scenario-based verification run** using the example materials supplied with the installation package. For tool features, supported expressions, and additional settings, see the [main README](README.md).

## Launch the tool

1. Extract the installation package into a local directory.
2. Start the executable or launcher provided in the extracted package.
3. Keep the included example files available for the steps below.

**Java setup:** The installation package includes the required Java runtime; a separate Java installation is not required for this packaged version.

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