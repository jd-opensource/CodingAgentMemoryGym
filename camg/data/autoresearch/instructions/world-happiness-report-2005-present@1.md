# OpenMLE-fast task

Task ID: `world-happiness-report-2005-present@1`

Native metric: `WorldHappinessRMSEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3248 bytes)
- `data/sample_submission.csv` (7715 bytes); columns: ["row_id", "Life Ladder"]
- `data/test.csv` (49463 bytes); columns: ["Country Name", "Regional Indicator", "Year", "Log GDP Per Capita", "Social Support", "Healthy Life Expectancy At Birth", "Freedom To Make Life Choices", "Generosity", "Perceptions Of Corruption", "Positive Affect", "Negative Affect", "Confidence In National Government", "row_id"]
- `data/train.csv` (279162 bytes); columns: ["Country Name", "Regional Indicator", "Year", "Life Ladder", "Log GDP Per Capita", "Social Support", "Healthy Life Expectancy At Birth", "Freedom To Make Life Choices", "Generosity", "Perceptions Of Corruption", "Positive Affect", "Negative Affect", "Confidence In National Government"]

## Public description

Competition: Forecasting National Happiness (World Happiness Report 2005–2022)

Problem statement:
Build machine learning models to forecast the Life Ladder (0–10) for each country in recent years using historical socio-economic and affect indicators. The task emphasizes time-aware generalization across countries and years.

Data provided to participants:
- train.csv: Feature columns plus the Life Ladder target for training years.
- test.csv: Feature columns for forecasting years; Life Ladder is withheld. Includes a unique row_id for each row.
- sample_submission.csv: A template with the required submission format.

Target and features:
- Target: Life Ladder (continuous, range [0,10]).
- Features:
  - Country Name (categorical)
  - Regional Indicator (categorical)
  - Year (numeric)
  - Log GDP Per Capita (numeric)
  - Social Support (numeric)
  - Healthy Life Expectancy At Birth (numeric)
  - Freedom To Make Life Choices (numeric)
  - Generosity (numeric)
  - Perceptions Of Corruption (numeric)
  - Positive Affect (numeric)
  - Negative Affect (numeric)
  - Confidence In National Government (numeric)

Split and forecasting setup:
- Train: Rows with Year ≤ 2019.
- Test: Rows with Year ≥ 2020.
This deterministic split prevents temporal leakage and evaluates true forecasting. Countries may have varying coverage across years.

Submission format:
- A CSV file with exactly two columns and no header changes:
  - row_id: The identifier provided in test.csv (match exactly; one prediction per row_id).
  - Life Ladder: The predicted value for the Life Ladder (numeric, finite). Values outside [0,10] are permitted but will be clipped to [0,10] during scoring.

Evaluation:
- Metric: Root Mean Squared Error (RMSE) on Life Ladder across all test rows.
- RMSE is fair, precise, and sensitive to larger errors, appropriate for continuous outcomes in [0,10] and cross-country forecasting.

Guidelines and notes:
- Avoid leakage: Engineer features only from information available up to and including the prediction year (e.g., use country-level lags built from prior years). Do not use test labels.
- Categorical handling: Encode Country Name and Regional Indicator suitably (e.g., one-hot, embeddings, target-encoding with proper CV). Treat Year as a numeric feature and/or a relative index within country.
- Time-aware features: Consider per-country lag features (e.g., Life Ladder t−1, predictor lags), rolling statistics, and year-over-year changes. Ensure lags for test rows are derived strictly from the dataset’s historical rows.
- Missing values: The dataset contains missingness in several features. Apply principled imputation strategies (e.g., country-wise forward/backward fill, regional medians, model-based imputation) and consider adding missingness indicators. Do not impute the target.
- Scaling: Fit any scalers on training data only and apply to test.
- External data: Not required; focus on the provided dataset for comparability.
- Recommended validation: Within train years, use time-aware CV (e.g., expanding window or blocked time splits) to estimate generalization.

Deliverables:
- Submit a file following sample_submission.csv format. The leaderboard is scored by RMSE on the test set Life Ladder.
