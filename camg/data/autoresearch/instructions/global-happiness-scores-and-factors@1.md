# OpenMLE-fast task

Task ID: `global-happiness-scores-and-factors@1`

Native metric: `HappinessRegressionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3035 bytes)
- `data/sample_submission.csv` (3881 bytes); columns: ["id", "happiness_score"]
- `data/test.csv` (6325 bytes); columns: ["id", "gdp_per_capita", "social_support", "healthy_life_expectancy", "freedom_to_make_life_choices", "generosity", "perceptions_of_corruption"]
- `data/train.csv` (80812 bytes); columns: ["id", "gdp_per_capita", "social_support", "healthy_life_expectancy", "freedom_to_make_life_choices", "generosity", "perceptions_of_corruption", "happiness_score"]

## Public description

World Happiness Generalization Challenge: Predict 2023 Wellbeing

Background
The World Happiness Report provides country-level wellbeing scores alongside socioeconomic and social factors (GDP per capita, social support, healthy life expectancy, freedom of choice, generosity, perceptions of corruption). This challenge focuses on learning from past years to predict the latest year’s happiness scores using only contemporaneous explanatory variables.

Problem Statement
Train a regression model on historical years (2015–2022) and predict national happiness_score for 2023. Robust preprocessing and time-aware generalization are essential: learn the relationship between the six numeric factors and the target without relying on country/region identifiers.

Data Description
You are provided with preprocessed tabular files:
- train.csv: rows from 2015–2022 with columns:
  - id: synthetic row identifier
  - gdp_per_capita
  - social_support
  - healthy_life_expectancy
  - freedom_to_make_life_choices
  - generosity
  - perceptions_of_corruption
  - happiness_score (target)
- test.csv: rows from 2023 with columns:
  - id
  - gdp_per_capita
  - social_support
  - healthy_life_expectancy
  - freedom_to_make_life_choices
  - generosity
  - perceptions_of_corruption
- sample_submission.csv: formatting example with columns:
  - id
  - happiness_score

Preparation notes reflected in the files:
- Time-aware split: train = 2015–2022; test = 2023.
- Per-year deduplication: duplicate country-year entries were aggregated by averaging numeric columns.
- Training missing values: converted placeholders to NaN and imputed per year using feature medians.
- Test missing values: minor missingness remains (e.g., a single cell) to encourage robust pipelines.
- Identifiers: country and region are excluded to prevent label leakage and ID-based memorization.

Evaluation
- Metric: Root Mean Squared Error (RMSE) on the 2023 targets.
  - RMSE = sqrt(mean((prediction − ground_truth)^2)).
  - RMSE is appropriate for continuous targets and penalizes large errors more strongly, ensuring a fair and precise comparison.
- Submission format must exactly match sample_submission.csv:
  - Columns: id, happiness_score
  - ids must match test.csv and be in the same order
  - predictions must be finite numeric values

Why It’s Challenging (and Meaningful)
- Temporal drift: factor-to-score relationships evolve over time.
- Robust preprocessing: handle minor missing values and ensure correct numeric types.
- Generalization without IDs: excluding country/region forces models to learn from explanatory variables.

Suggestions
- Use train-only statistics for preprocessing (e.g., imputation and scaling) to avoid leakage.
- Consider time-aware validation (e.g., rolling or expanding windows across years).
- Try diverse models: regularized linear models, kernel methods, tree ensembles (RF/GBDT), stacking/blending.
- Feature engineering: interactions (e.g., GDP × social_support), nonlinear transforms (e.g., logs), robust scalers.
