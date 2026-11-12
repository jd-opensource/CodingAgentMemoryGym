# OpenMLE-fast task

Task ID: `video-game-sales@1`

Native metric: `VideoGameSalesMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2636 bytes)
- `data/sample_submission.csv` (15456 bytes); columns: ["Id", "Global_Sales"]
- `data/test.csv` (99412 bytes); columns: ["Id", "Name", "Platform", "Year", "Genre", "Publisher"]
- `data/train.csv` (1001482 bytes); columns: ["Id", "Name", "Platform", "Year", "Genre", "Publisher", "Global_Sales"]

## Public description

Global Video Game Sales Prediction

Overview
Predict cumulative global sales (in millions of units) for individual video game title–platform pairs using only descriptive metadata. You will receive training rows with labels and test rows without labels. Build a model that generalizes to future releases.

Files provided
- train.csv — Columns: Id, Name, Platform, Year, Genre, Publisher, Global_Sales
- test.csv — Columns: Id, Name, Platform, Year, Genre, Publisher
- sample_submission.csv — Columns: Id, Global_Sales

Task details
- Input features available in both train and test: Name (text), Platform (categorical), Year (integer or "Unknown"), Genre (categorical), Publisher (categorical).
- Target to predict: Global_Sales (continuous, in millions of units) for test rows.
- The split is time-aware to emulate real-world forecasting: train contains earlier releases and entries with unknown year; test contains later releases only.

Evaluation metric
- Root Mean Squared Logarithmic Error (RMSLE) on Global_Sales:
  RMSLE = sqrt(mean((log1p(pred) − log1p(true))^2))
- Predictions must be non-negative real numbers. During evaluation, any negative values will be clipped to 0.
- Submission format: CSV with header Id,Global_Sales. Exactly one row per Id in test.csv.

Modeling guidance
- Strong baselines: tree-based models with categorical encoders (e.g., target encoding or CatBoost-like handling) and regularized linear models on character/word n-grams from Name.
- Feature engineering ideas:
  - Name text signals: franchise tokens (e.g., "FIFA", numerals, edition keywords), character n-grams, wordpiece tokenization.
  - Platform lifecycle: interactions between Platform and Year, recency within a platform generation.
  - Genre × Platform and Publisher history effects (frequency/target encoding with appropriate regularization).
  - Robust handling of Unknown years as a separate category.

Submission specification
- Create a CSV named submission.csv with two columns: Id, Global_Sales.
- Id must exactly match the Ids in test.csv; do not add, drop, or reorder rows without preserving Id alignment.
- Global_Sales should be non-negative; use floats in “millions of units”.

Expectations
- Use sound ML practice: preprocessing, careful encoding of high-cardinality categoricals, outlier-aware training objectives or transforms (e.g., modeling log1p of the target), and thorough model evaluation via cross-validation inside the training set.
- Do not rely on any regional sales or rank information; only the columns present in train/test are permitted.

Good luck and have fun building your forecasting model!
