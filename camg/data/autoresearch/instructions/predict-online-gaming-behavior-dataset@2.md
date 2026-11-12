# OpenMLE-fast task

Task ID: `predict-online-gaming-behavior-dataset@2`

Native metric: `OnlineGamingPurchaseMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2310 bytes)
- `data/sample_submission.csv` (119861 bytes); columns: ["PlayerID", "purchase_probability"]
- `data/test.csv` (761248 bytes); columns: ["PlayerID", "Age", "Gender", "Location", "GameGenre", "PlayTimeHours", "GameDifficulty", "SessionsPerWeek", "AvgSessionDurationMinutes", "PlayerLevel", "AchievementsUnlocked"]
- `data/train.csv` (1831473 bytes); columns: ["PlayerID", "Age", "Gender", "Location", "GameGenre", "PlayTimeHours", "GameDifficulty", "SessionsPerWeek", "AvgSessionDurationMinutes", "PlayerLevel", "AchievementsUnlocked", "InGamePurchases"]

## Public description

Predicting Purchase Propensity in Online Gaming

Problem statement
- Given player demographics, genre, difficulty, and play/engagement cadence features, predict the probability that a player will make an in-game purchase (InGamePurchases: 0/1). Your model should output well-calibrated probabilities for ranking players by purchase likelihood under class imbalance.

Files provided
- train.csv: Training data with features and target.
- test.csv: Test data with features only.
- sample_submission.csv: Template with required columns and example probabilities.

Target and features
- Target: InGamePurchases (binary; 1 = buyer, 0 = non-buyer)
- ID: PlayerID (unique row identifier)
- Features:
  - Age (numeric)
  - Gender (categorical)
  - Location (categorical)
  - GameGenre (categorical)
  - PlayTimeHours (numeric)
  - GameDifficulty (categorical)
  - SessionsPerWeek (numeric)
  - AvgSessionDurationMinutes (numeric)
  - PlayerLevel (numeric)
  - AchievementsUnlocked (numeric)

Evaluation
- Primary metric: Average Precision (AP) for the positive class (buyers), computed from predicted probabilities. AP focuses on precision-recall tradeoff and is robust under class imbalance. Higher is better.
- Submission format: A CSV with two columns: PlayerID, purchase_probability. PlayerID must match test.csv order exactly; purchase_probability must be in [0, 1].

Rules and important notes
- Use the provided train/test split; do not attempt to infer test labels.
- No external data is required. Feature engineering, class imbalance strategies, probability calibration, and robust validation are encouraged.
- Avoid label leakage. Columns related to other targets (e.g., EngagementLevel) are not present in the competition files.

Suggestions for approach (non-binding)
- Encoding: One-hot/target encoding for categorical variables; consider ordinal mapping for GameDifficulty.
- Scaling: Standardize numeric features; consider winsorization for heavy-tailed variables.
- Modeling: Regularized logistic regression, gradient boosting (e.g., XGBoost/LightGBM/CatBoost), and calibrated ensembles are effective.
- Imbalance: Class weights, focal/balanced loss, and decision threshold tuning based on PR curves.

Deliverables
- Submit a single CSV named submission.csv with columns: PlayerID,purchase_probability.
