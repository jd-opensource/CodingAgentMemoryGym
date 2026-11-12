# OpenMLE-fast task

Task ID: `travel-insurance-prediction-data@1`

Native metric: `TravelInsurancePurchaseMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2328 bytes)
- `data/sample_submission.csv` (14199 bytes); columns: ["row_id", "TravelInsurance"]
- `data/test.csv` (33006 bytes); columns: ["row_id", "Age", "Employment Type", "GraduateOrNot", "AnnualIncome", "FamilyMembers", "ChronicDiseases", "FrequentFlyer", "EverTravelledAbroad"]
- `data/train.csv` (79345 bytes); columns: ["row_id", "Age", "Employment Type", "GraduateOrNot", "AnnualIncome", "FamilyMembers", "ChronicDiseases", "FrequentFlyer", "EverTravelledAbroad", "TravelInsurance"]

## Public description

Title: Travel Insurance Purchase Propensity

Problem statement
Estimate, for each customer, the probability of purchasing a travel insurance package. You are provided customer demographics and simple behavioral flags. Your task is to build a model that outputs calibrated probabilities and ranks customers by likelihood to buy.

Data description
Each row is a customer described by the following columns:
- row_id: integer identifier (do not use as a predictive feature)
- Age: integer years
- Employment Type: categorical (e.g., Government Sector, Private Sector/Self Employed)
- GraduateOrNot: Yes/No
- AnnualIncome: integer (INR)
- FamilyMembers: integer count
- ChronicDiseases: 0/1
- FrequentFlyer: Yes/No
- EverTravelledAbroad: Yes/No
- TravelInsurance: 0/1 target (present only in train.csv)

Provided files
- train.csv: row_id + all features + TravelInsurance target (0/1)
- test.csv: row_id + all features (no target)
- sample_submission.csv: row_id + TravelInsurance (predicted probability of the positive class)

Submission format
Upload a CSV with exactly two columns:
- row_id: integer identifier matching test.csv
- TravelInsurance: predicted probability (float in [0,1]) that the customer buys insurance
The submission may be in any row order; row_ids must match the official test set exactly once. Values will be safely clipped to [0,1] if needed.

Evaluation
- Metric: ROC-AUC on the full test set, computed using your submitted probabilities versus the hidden true labels.
- Rationale: The class distribution is moderately imbalanced; ROC-AUC assesses ranking quality across thresholds and is robust to calibration differences. This ensures a fair and precise leaderboard.

Official split
- All rows are used; no subsampling. The split is deterministic and fixed (stratified 70/30).

Modeling guidance
- Encode categorical variables appropriately (e.g., one-hot encode Employment Type; map Yes/No to 1/0 for binary flags). Consider tree-based models or regularized linear models.
- Account for class imbalance and consider probability calibration (e.g., Platt scaling or isotonic regression) to improve probability quality.
- Use cross-validation on train.csv for model selection; do not attempt to infer test labels.
- Avoid using row_id as a feature; it is a surrogate identifier with no predictive meaning.
