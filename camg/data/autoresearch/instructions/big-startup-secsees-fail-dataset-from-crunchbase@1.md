# OpenMLE-fast task

Task ID: `big-startup-secsees-fail-dataset-from-crunchbase@1`

Native metric: `StartupExitAUCMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3610 bytes)
- `data/sample_submission.csv` (36640 bytes); columns: ["id", "prediction"]
- `data/test.csv` (429934 bytes); columns: ["id", "name", "category_list", "funding_total_usd", "funding_rounds", "country_code", "state_code", "region", "city", "founded_at", "first_funding_at", "last_funding_at"]
- `data/train.csv` (1021725 bytes); columns: ["id", "name", "category_list", "funding_total_usd", "funding_rounds", "country_code", "state_code", "region", "city", "founded_at", "first_funding_at", "last_funding_at", "is_success"]

## Public description

Title: Startup Exit Outcome — Success vs Failure (Binary Classification)

Overview:
Build a model that predicts whether a startup ultimately succeeds (exits via acquisition or IPO) or fails (shuts down) using historical tabular attributes such as categories, funding, geography, and dates. The task is designed to be challenging and realistic: features are mixed-type, sparse, skewed, and often missing, requiring careful data processing and feature engineering.

Data files:
- train.csv: Labeled startups with features and a binary target column is_success (1 = success via acquisition/IPO, 0 = failure via shutdown).
- test.csv: Unlabeled startups with the same feature columns as train.csv except the target; includes id for joining.
- sample_submission.csv: Example submission file with id and prediction columns.

Target definition:
- Success = status in {acquired, ipo}
- Failure = status in {closed}
The target column is_success encodes success as 1 and failure as 0 in train.csv. The raw status label is not included in train/test features.

Columns present in train.csv and test.csv:
- id: Integer identifier.
- name: Company name (string).
- category_list: Pipe-separated list of categories (string; e.g., "Software|Analytics").
- funding_total_usd: Total funding in USD (string/numeric; may be missing or "-").
- funding_rounds: Number of funding rounds (integer-like; may be missing or 0).
- country_code: Country code (string; may be missing).
- state_code: State/region code (string; may be missing or non-standard).
- region: Macro region label (string; may be missing).
- city: City name (string; may be missing).
- founded_at: Company founding date (YYYY-MM-DD or empty).
- first_funding_at: First funding date (YYYY-MM-DD or empty).
- last_funding_at: Last funding date (YYYY-MM-DD or empty).
- train.csv only: is_success (0/1 target label).

Not included as features:
- status (raw outcome), permalink, homepage_url.

Recommended approach:
- Data processing: parse numerics robustly (handle "-" and blanks), standardize strings, impute missing values, and create explicit missing indicators.
- Feature engineering: derive time-based features (e.g., age at first funding, funding span, year parts via YYYY), log-transform skewed durations/funding, multi-hot encode frequent category tokens, encode geographies, and extract simple name features (length, token flags).
- Modeling: train ML classifiers suitable for mixed tabular data (e.g., LightGBM/XGBoost/CatBoost, linear or neural models with appropriate encodings). Use thorough cross-validation locally; the official leaderboard uses a single held-out test split.

Evaluation metric:
- Submissions are scored by ROC AUC on the predicted probability of success.
- ROC AUC is fair and precise for this setting: it evaluates ranking quality without requiring a threshold, handles mild class imbalance, and is robust to probability calibration differences.

Submission format:
- A CSV file with exactly two columns and a header: id,prediction
- id: integer identifiers matching rows in test.csv.
- prediction: your predicted probability that the startup is a success (float in [0,1]).

Additional notes:
- The train/test split is stratified to preserve class balance; both classes appear in train and test.
- Use all available data—do not subsample. Heavy feature engineering is expected and rewarded.
- Do not attempt to recover hidden labels from names or identifiers; focus on predictive signals in the provided features.
- The sample_submission.csv demonstrates a valid format and typical baseline behavior (near-random AUC ≈ 0.5).
