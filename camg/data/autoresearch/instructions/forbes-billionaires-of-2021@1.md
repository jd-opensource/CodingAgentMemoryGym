# OpenMLE-fast task

Task ID: `forbes-billionaires-of-2021@1`

Native metric: `ForbesNetWorthMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3401 bytes)
- `data/sample_submission.csv` (14063 bytes); columns: ["Id", "NetWorth"]
- `data/test.csv` (35641 bytes); columns: ["Id", "Name", "Country", "Source", "Age", "Industry"]
- `data/train.csv` (152782 bytes); columns: ["Id", "Name", "Country", "Source", "Age", "Industry", "NetWorth"]

## Public description

Title: Forbes Billionaires 2021 — Net Worth Prediction

Problem statement
Participants are given profiles of individuals from Forbes’ 2021 Billionaires list and must predict each person’s net worth (in billions USD). The data includes mixed types: structured categorical/numeric fields and free‑text descriptors of the income source. The task is a heavy‑tailed regression problem requiring careful preprocessing, feature engineering, and robust modeling to achieve strong relative accuracy across the entire range of net worth values.

Data description
- Train file: train.csv — columns: Id, Name, Country, Source, Age, Industry, NetWorth. NetWorth is the numeric target in billions USD.
- Test file: test.csv — columns: Id, Name, Country, Source, Age, Industry. NetWorth is withheld.
- Sample submission: sample_submission.csv — columns: Id, NetWorth. Contains random but valid predictions for demonstration.

Notes and guidance
- Use all provided columns except Rank (which is not present in the final files). NetWorth in train.csv is already parsed to numeric billions.
- Data cleaning recommendations:
  - Age: treat missing or non-numeric entries as NaN; impute (e.g., median per Country–Industry) and consider an “Age_missing” indicator.
  - Country and Industry: encode as categorical features (e.g., one‑hot, frequency, or target encoding). Consider grouping ultra‑rare categories to reduce sparsity.
  - Source: normalize and encode free text via TF‑IDF, bag‑of‑words with n‑grams, or compact embeddings trained on the provided corpus. Preserve multi‑term entries (e.g., “beverages, pharmaceuticals”).
  - Optional engineered signals from Name: simple, label‑agnostic indicators such as contains “& family”, name length, or suffixes like “Jr.”. Avoid using raw Name to memorize individuals.
- The split is deterministic and stratified by Industry and NetWorth quantile bins to keep train/test distributions comparable.

Evaluation metric
Submissions are evaluated using Root Mean Squared Logarithmic Error (RMSLE) between the predicted and true net worth values (in billions USD). Lower is better.
- Why RMSLE: Net worth spans roughly 1–177B with a heavy tail. RMSLE evaluates multiplicative error, stabilizes the influence of extreme values, and fairly rewards proportionally accurate estimates across the range.
- Submission format: a CSV file with exactly two columns — Id, NetWorth — covering all Ids in test.csv without duplicates. NetWorth must be non‑negative numeric.

What makes this challenging and meaningful
- Heavy‑tailed target distribution with significant variance in the upper tail.
- High‑cardinality categorical variables (Country, Industry) and noisy multilingual free‑text Source requiring robust text preprocessing.
- Moderate sample size encourages careful regularization and validation.
- Realistic signals capturing geography, sector, and business descriptors.

Suggested baseline approaches
- Linear models with TF‑IDF features for Source combined with categorical encodings.
- Gradient‑boosted trees (e.g., XGBoost/LightGBM/CatBoost) on engineered features.
- Simple neural architectures with embedding layers for categorical variables and text encoders for Source.

Files to produce
- A submission CSV named arbitrarily, containing predictions for all Ids in test.csv with columns: Id, NetWorth.
