# OpenMLE-fast task

Task ID: `credit-card-customers@1`

Native metric: `CreditCardChurnMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (4175 bytes)
- `data/sample_submission.csv` (38305 bytes); columns: ["Row_ID", "Attrited_Probability"]
- `data/test.csv` (212853 bytes); columns: ["Row_ID", "Customer_Age", "Gender", "Dependent_count", "Education_Level", "Marital_Status", "Income_Category", "Card_Category", "Months_on_book", "Total_Relationship_Count", "Months_Inactive_12_mon", "Contacts_Count_12_mon", "Credit_Limit", "Total_Revolving_Bal", "Avg_Open_To_Buy", "Total_Amt_Chng_Q4_Q1", "Total_Trans_Amt", "Total_Trans_Ct", "Total_Ct_Chng_Q4_Q1", "Avg_Utilization_Ratio"]
- `data/train.csv` (995568 bytes); columns: ["Row_ID", "Attrition_Flag", "Customer_Age", "Gender", "Dependent_count", "Education_Level", "Marital_Status", "Income_Category", "Card_Category", "Months_on_book", "Total_Relationship_Count", "Months_Inactive_12_mon", "Contacts_Count_12_mon", "Credit_Limit", "Total_Revolving_Bal", "Avg_Open_To_Buy", "Total_Amt_Chng_Q4_Q1", "Total_Trans_Amt", "Total_Trans_Ct", "Total_Ct_Chng_Q4_Q1", "Avg_Utilization_Ratio"]

## Public description

Credit Card Customer Churn Prediction

Background
A bank is observing rising attrition in its credit card portfolio and wants to proactively identify customers at risk of churning so retention teams can intervene. You are tasked with building a model to rank customers by the likelihood of attrition.

Problem Statement
Given historical demographic and account summary attributes of credit card customers, predict the probability that a customer will churn. The positive class is “Attrited Customer”. Your goal is to produce well-calibrated, high-quality risk scores to prioritize interventions.

Data Description
You are provided with a tabular dataset of 10,127 customers, including a churn indicator and customer characteristics. The final competition files are:
- train.csv: Training set with features and the target label.
- test.csv: Test set with features only.
- sample_submission.csv: Example of the required submission format.

Target label
- Attrition_Flag (string): "Attrited Customer" (positive class) or "Existing Customer" (negative class).

Features
The following columns are provided as model inputs. Identifier and leakage-prone columns have been removed.
- Row_ID: A deterministic, anonymized identifier for each row (string). Use this to align your predictions with the test set.
- Customer_Age (int)
- Gender (category: M/F)
- Dependent_count (int)
- Education_Level (category)
- Marital_Status (category)
- Income_Category (category)
- Card_Category (category)
- Months_on_book (int)
- Total_Relationship_Count (int)
- Months_Inactive_12_mon (int)
- Contacts_Count_12_mon (int)
- Credit_Limit (float)
- Total_Revolving_Bal (int)
- Avg_Open_To_Buy (float)
- Total_Amt_Chng_Q4_Q1 (float)
- Total_Trans_Amt (int)
- Total_Trans_Ct (int)
- Total_Ct_Chng_Q4_Q1 (float)
- Avg_Utilization_Ratio (float)

Notes on data processing
- The following raw columns were excluded from the released feature set to prevent leakage or memorization: CLIENTNUM (identifier), and two columns whose names start with "Naive_Bayes_Classifier_" (model-generated probabilities). These columns are not present in train.csv or test.csv.
- Categorical values such as "Unknown" are preserved as-is. There are no empty missing values in the raw data.

Train/Test Split
- The data have been split into train/test using a deterministic 80/20 stratified split on the target to preserve class balance in both sets.
- The split is performed at the customer level, and Row_ID preserves the row mapping across files.

Submission Format
- Your submission must be a CSV file with exactly two columns and a header row:
  - Row_ID: Must match the Row_ID values in test.csv.
  - Attrited_Probability: Your predicted probability (float in [0, 1]) that the corresponding customer is an "Attrited Customer".
- The order of rows does not matter, but Row_ID values must be present exactly once. The sample_submission.csv demonstrates the expected format.

Evaluation
- Metric: Area Under the ROC Curve (ROC AUC) computed on the test set, using the positive class "Attrited Customer".
- Rationale: AUROC is threshold-independent, robust to the dataset’s moderate class imbalance (~16% attrited), and emphasizes ranking quality, which aligns with practical retention prioritization.
- Requirements for scoring:
  - Predictions should be finite real numbers. Values outside [0,1] will be clipped for scoring.
  - If your submission is missing or duplicates any Row_ID, it will be rejected.

Guidance
- Consider appropriate handling of categorical features (e.g., one-hot encoding or tree-based models that natively handle categories), class imbalance (e.g., sampling, class weights), and feature interactions.
- Strong baselines include gradient boosting decision trees, calibrated logistic regression with well-engineered encodings, and stacking. Calibration can improve probability quality and thus AUROC stability.

Files
- train.csv: Includes Row_ID, features, and Attrition_Flag.
- test.csv: Includes Row_ID and the same feature columns as train.csv (excluding Attrition_Flag).
- sample_submission.csv: Includes Row_ID and Attrited_Probability with example values.

Good luck and happy modeling!
