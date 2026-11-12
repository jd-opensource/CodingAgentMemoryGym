# OpenMLE-fast task

Task ID: `project-management-risk-raw@1`

Native metric: `ProjectRiskQWKMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2721 bytes)
- `data/sample_submission.csv` (13065 bytes); columns: ["Project_ID", "Risk_Level"]
- `data/test.csv` (227610 bytes); columns: ["Project_ID", "Project_Type", "Team_Size", "Project_Budget_USD", "Estimated_Timeline_Months", "Complexity_Score", "Stakeholder_Count", "Methodology_Used", "Team_Experience_Level", "Past_Similar_Projects", "External_Dependencies_Count", "Change_Request_Frequency", "Project_Phase", "Requirement_Stability", "Team_Turnover_Rate", "Vendor_Reliability_Score", "Historical_Risk_Incidents", "Communication_Frequency", "Regulatory_Compliance_Level", "Technology_Familiarity", "Geographical_Distribution", "Stakeholder_Engagement_Level", "Executive_Sponsorship", "Funding_Source", "Market_Volatility", "Integration_Complexity", "Resource_Availability", "Priority_Level", "Organizational_Change_Frequency", "Cross_Functional_Dependencies", "Previous_Delivery_Success_Rate", "Technical_Debt_Level", "Project_Manager_Experience", "Org_Process_Maturity", "Data_Security_Requirements", "Key_Stakeholder_Availability", "Tech_Environment_Stability", "Contract_Type", "Resource_Contention_Level", "Industry_Volatility", "Client_Experience_Level", "Change_Control_Maturity", "Risk_Management_Maturity", "Team_Colocation", "Documentation_Quality", "Project_Start_Month", "Seasonal_Risk_Factor"]
- `data/train.csv` (929783 bytes); columns: ["Project_ID", "Project_Type", "Team_Size", "Project_Budget_USD", "Estimated_Timeline_Months", "Complexity_Score", "Stakeholder_Count", "Methodology_Used", "Team_Experience_Level", "Past_Similar_Projects", "External_Dependencies_Count", "Change_Request_Frequency", "Project_Phase", "Requirement_Stability", "Team_Turnover_Rate", "Vendor_Reliability_Score", "Historical_Risk_Incidents", "Communication_Frequency", "Regulatory_Compliance_Level", "Technology_Familiarity", "Geographical_Distribution", "Stakeholder_Engagement_Level", "Executive_Sponsorship", "Funding_Source", "Market_Volatility", "Integration_Complexity", "Resource_Availability", "Priority_Level", "Organizational_Change_Frequency", "Cross_Functional_Dependencies", "Previous_Delivery_Success_Rate", "Technical_Debt_Level", "Project_Manager_Experience", "Org_Process_Maturity", "Data_Security_Requirements", "Key_Stakeholder_Availability", "Tech_Environment_Stability", "Contract_Type", "Resource_Contention_Level", "Industry_Volatility", "Client_Experience_Level", "Change_Control_Maturity", "Risk_Management_Maturity", "Team_Colocation", "Documentation_Quality", "Project_Start_Month", "Seasonal_Risk_Factor", "Risk_Level"]

## Public description

Project Risk Level Prediction (Ordinal Classification)

Problem statement
Participants must predict the overall project Risk_Level for each project in the test set. Risk_Level is an ordered categorical variable with four classes: Low < Medium < High < Critical. The task emphasizes realistic early risk assessment from diverse project attributes.

Provided files
- train.csv: Tabular training data with project features and the target column Risk_Level.
- test.csv: Tabular test data with the same feature columns as train.csv (excluding Risk_Level).
- sample_submission.csv: Example submission file with two columns: Project_ID, Risk_Level.

Target and features
- Target: Risk_Level with possible values {Low, Medium, High, Critical}.
- Identifier: Project_ID uniquely identifies each row and must be used to align predictions to rows in test.csv. It is not intended as a predictive feature.
- Features: The competition includes a broad set of categorical and numerical attributes spanning project demographics, operations, human factors, organization, technical context, and external influences.
- Excluded near-outcome KPIs to avoid leakage: Schedule_Pressure, Budget_Utilization_Rate, and Current_Phase_Duration_Months are not present in the provided train/test files. This enforces a realistic early-risk modeling setup and preserves the challenge.

Evaluation
- Metric: Quadratic Weighted Kappa (QWK) on the ordered labels [Low, Medium, High, Critical]. QWK penalizes larger mistakes more severely (e.g., predicting Low instead of Critical is worse than predicting High instead of Critical), and is robust to class imbalance compared to plain accuracy.
- Submission format: A CSV with header and exactly two columns in this order:
  - Project_ID
  - Risk_Level (one of: Low, Medium, High, Critical)
Predictions must provide one label per Project_ID found in test.csv with no duplicates and no missing values.

Rules and recommendations
- Use any machine learning techniques for tabular data (e.g., tree ensembles, linear/GLMs, neural networks). Ordinal-specific approaches and calibration can further improve performance.
- Handle missing values carefully. Many categorical fields may contain NaNs; numeric fields can be median-imputed. Consider adding missing-indicator features and preserving ordinal relationships in ordered categorical variables.
- Feature engineering, robust cross-validation, and attention to class imbalance are encouraged. Avoid using Project_ID as a feature.

Reproducibility and integrity
- The split is stratified by Risk_Level and deterministic.
- All classes present in the test set also appear in the training set.

Good luck, and enjoy building a high-quality ordinal risk predictor!
