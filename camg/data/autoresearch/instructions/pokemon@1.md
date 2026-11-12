# OpenMLE-fast task

Task ID: `pokemon@1`

Native metric: `PokemonLegendaryMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2490 bytes)
- `data/sample_submission.csv` (1762 bytes); columns: ["Id", "Legendary"]
- `data/test.csv` (6477 bytes); columns: ["Id", "Type 1", "Type 2", "HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed", "Generation"]
- `data/train.csv` (27142 bytes); columns: ["Id", "Type 1", "Type 2", "HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed", "Generation", "Legendary"]

## Public description

Legendary Status Prediction from Base Stats and Types

Overview
Predict the probability that a Pokémon is Legendary based solely on its intrinsic attributes: primary/secondary types, base stats, and generation. The task is a binary classification with pronounced class imbalance. Your submission must provide well-calibrated probabilities for the Legendary class.

Files
- train.csv: Training data with features and the target column Legendary.
- test.csv: Test data with the same feature columns as train.csv (without Legendary).
- sample_submission.csv: Example submission containing valid Ids and random probabilities.

Target
- Legendary: Binary label (1 = Legendary, 0 = non-Legendary).

Features
- Id: An anonymized unique identifier for each Pokémon row.
- Type 1: Primary type as a categorical string (e.g., Grass, Fire, Water).
- Type 2: Secondary type as a categorical string; missing values are provided as the string "None".
- HP, Attack, Defense, Sp. Atk, Sp. Def, Speed: Base stats (integers).
- Generation: Integer generation index (e.g., 1..6).

Design notes
- Each row is a distinct Pokémon form (including mega/alternate forms); treat rows independently.
- Columns excluded to avoid leakage or redundancy: Name, #, Total.

Submission format
- CSV file with exactly two columns and a header:
  - Id: Must match the Ids in test.csv.
  - Legendary: Predicted probability for Legendary (numeric in [0, 1]).
- Do not include any extra columns. Ids must be unique and cover the entire test set.

Evaluation
- Metric: ROC AUC on the Legendary probabilities.
- The leaderboard score is computed by comparing submitted probabilities to the hidden test labels.
- Rationale: ROC AUC is robust to strong class imbalance and scores the ranking quality across thresholds.

Guidance (non-binding)
- Data processing: Encode Type 1/Type 2 and Generation with one-hot or categorical encoders; standardize numeric stats if using linear models.
- Feature engineering: Consider interactions between types, offensive/defensive balance, speed-related thresholds, and generation effects.
- Modeling: Tree ensembles (Gradient Boosting, Random Forest, XGBoost/LightGBM/CatBoost) and regularized logistic models are suitable. Calibrate probabilities if needed.
- Validation: Use stratified CV on the Legendary label; consider generational stratification to maintain distribution coverage.

Deliverable
- Maximize ROC AUC on the test set by submitting a properly formatted CSV as described above.
