# OpenMLE-fast task

Task ID: `employee-performance-and-productivity-data@1`

Native metric: `EmployeeResignationMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3625 bytes)
- `data/sample_submission.csv` (502735 bytes); columns: ["Employee_ID", "Resigned"]
- `data/test.csv` (2130764 bytes); columns: ["Employee_ID", "Department", "Gender", "Age", "Job_Title", "Hire_Date", "Years_At_Company", "Education_Level", "Performance_Score", "Monthly_Salary", "Work_Hours_Per_Week", "Projects_Handled", "Overtime_Hours", "Sick_Days", "Remote_Work_Frequency", "Team_Size", "Training_Hours", "Promotions", "Employee_Satisfaction_Score"]
- `data/train.csv` (8995008 bytes); columns: ["Employee_ID", "Department", "Gender", "Age", "Job_Title", "Hire_Date", "Years_At_Company", "Education_Level", "Performance_Score", "Monthly_Salary", "Work_Hours_Per_Week", "Projects_Handled", "Overtime_Hours", "Sick_Days", "Remote_Work_Frequency", "Team_Size", "Training_Hours", "Promotions", "Employee_Satisfaction_Score", "Resigned"]

## Public description

Competition: Employee Resignation Probability Prediction

Problem statement
HR teams need to anticipate employee resignation to guide retention efforts. Your task is to build a model that predicts the probability that an employee will resign based on their current profile and work history.

Data
You are provided a tabular dataset of 100,000 employees with rich features capturing job, workload, compensation, performance, training, and satisfaction signals. The data is heterogeneous (categorical, ordinal, continuous) and moderately imbalanced (~10% positives), requiring careful preprocessing and modeling.

Files provided
- train.csv: Training set with the target column Resigned.
- test.csv: Test set with the same schema but without Resigned.
- sample_submission.csv: Example of the required submission format.

Target
- Resigned: Boolean target indicating whether the employee has resigned.

Features
- Employee_ID: Unique identifier used only for joining predictions (do not use as a predictive feature).
- Department (categorical)
- Gender (categorical)
- Age (numeric; 22–60)
- Job_Title (categorical)
- Hire_Date (timestamp text; if used, derive coarse features only, e.g., hire year/month)
- Years_At_Company (numeric)
- Education_Level (categorical; High School, Bachelor, Master, PhD)
- Performance_Score (numeric; 1–5)
- Monthly_Salary (numeric)
- Work_Hours_Per_Week (numeric)
- Projects_Handled (numeric)
- Overtime_Hours (numeric)
- Sick_Days (numeric)
- Remote_Work_Frequency (categorical/ordinal; one of {0, 25, 50, 75, 100})
- Team_Size (numeric)
- Training_Hours (numeric)
- Promotions (numeric)
- Employee_Satisfaction_Score (numeric; 1.0–5.0)

Evaluation
- Metric: Average Precision (Precision–Recall AUC) on the positive class (Resigned=True).
- Details: Submissions are ranked by predicted probabilities in descending order; AP is computed as the average of precision values at ranks of true positives. AP is threshold-independent and robust for imbalanced classification.
- Rationale: AP directly reflects the precision–recall trade-off under class imbalance, rewarding models that rank likely resignations above non-resignations.

Submission format
- Submit a CSV with exactly two columns:
  - Employee_ID: Identifier from test.csv
  - Resigned: Predicted probability of resignation for each employee, a finite float in [0, 1]
- The order of rows does not matter; scoring aligns by Employee_ID.

Guidance for participants
- Data processing: Enforce correct types, validate plausible ranges, and remove duplicates if present. Encode categorical variables (e.g., one-hot or target encoding), scale/normalize continuous features where helpful, and consider interaction features (e.g., workload × overtime, salary per project, promotions per year). If using Hire_Date, derive only coarse components (year/month) to avoid leakage via synthetic timestamp precision.
- Modeling: Address imbalance with techniques such as calibrated gradient boosting (e.g., XGBoost/LightGBM), regularized tabular neural networks, or ensembles. Use robust cross-validation (e.g., stratified k-fold) to tune and compare models, and consider probability calibration.
- Ethics: Sensitive attributes such as Gender may correlate with outcomes; consider fairness-aware approaches. The evaluation focuses on predictive performance, so please be mindful of ethical implications.

Notes
- The entire dataset is utilized to maximize signal.
- train.csv and test.csv share the same feature schema; Resigned appears only in train.csv.
- Do not include file paths inside CSVs and do not rely on filenames to infer labels.
