# OpenMLE-fast task

Task ID: `daily-potato-prices-and-trade-volume-q1-2025@2`

Native metric: `PotatoVolumeForecastMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3804 bytes)
- `data/panel_daily.csv` (74990 bytes); columns: ["Fecha", "Producto", "Variedad", "Precio Min", "Precio Max", "Precio Prom", "Volumen (TM)"]
- `data/sample_submission.csv` (13439 bytes); columns: ["Fecha", "Variedad", "Volumen (TM)"]
- `data/test.csv` (8256 bytes); columns: ["Fecha", "Variedad"]
- `data/train.csv` (15454 bytes); columns: ["Fecha", "Variedad", "Volumen (TM)"]

## Public description

Competition: Next-day Trade Volume Forecasting by Potato Variety (Peru, 2025)

Background
Local wholesale potato markets in Peru report daily price panels (min/max/average) and traded volumes (metric tons, TM) across multiple varieties. Volumes are volatile and reflect supply–demand dynamics influenced by price, seasonality, and variety-specific behavior.

Task
Given historical daily data, predict the next-day traded volume (TM) for a set of potato varieties. For a target day D and variety v, you must only use information available up to day D-1 (no same-day or future leakage).

Data
You are provided with three CSV files to build features and train your model:
- panel_daily.csv: Daily panel for all varieties with prices and volumes. Columns: Fecha (dd/mm/yyyy), Producto, Variedad, Precio Min, Precio Max, Precio Prom, Volumen (TM). Volumen may be missing on some days/varieties. Prices exist broadly across days. This file is the source for all your feature engineering (lags, rolling stats, calendar features, cross-variety context, etc.).
- train.csv: The training targets index. Each row is a (Fecha, Variedad) pair for which the target is the traded volume on Fecha for that Variedad. You should learn to predict Volumen (TM) on Fecha using only history up to Fecha-1 derived from panel_daily.csv.
- test.csv: The test targets index. Same format as train.csv but with the target withheld. You must submit predictions for these rows.

Important details
- Temporal split: Train targets fall within 2025-01-01 to 2025-03-31; Test targets fall within 2025-04-01 to 2025-05-23.
- Targeted varieties (appear in train and test): PAPA AMARILLA, PAPA BLANCA/VALLE/OTROS, PAPA CANCHAN, PAPA COLOR/VALLE/OTROS, PAPA HUAYRO (ROJO-MORO-NEGRO)RUNT/MARH/U, PAPA UNICA, PAPA YUNGAY.
- Other varieties may appear in panel_daily.csv and can be used to build lagged cross-variety features, but no predictions are required for them.
- Use strictly lagged information: For each (Fecha, Variedad) in train/test, features must be computed only from panel_daily rows with dates strictly earlier than Fecha. Do not use any values from day D itself when predicting day D.
- Data quality tips: Handle missing volumes in lags, ensure non-negative volumes, remove duplicates, parse dates in dd/mm/yyyy, and sort by variety/date when computing rolling features.

Submission format
Submit a CSV with columns: Fecha, Variedad, Volumen (TM)
- Fecha must match the dates in test.csv (format dd/mm/yyyy).
- Variedad must match exactly the strings in test.csv (case-sensitive).
- Volumen (TM) are your predictions (non-negative real numbers). The order of rows does not matter; rows will be matched by keys (Fecha, Variedad).
- Each (Fecha, Variedad) key must appear exactly once; duplicates are not allowed.
- Do not include any extra columns.

Evaluation
Submissions are scored using RMSLE (Root Mean Squared Log Error) between your predictions and the ground truth volumes:
- score = sqrt(mean((log1p(y_pred) - log1p(y_true))^2))
- log1p is used to robustly handle zeros and scale differences across varieties and days.
- Predictions lower than 0 will be clamped to 0 before scoring.

What makes this challenging
- Volumes vary by orders of magnitude across varieties and over time.
- Volume reporting is intermittent for some varieties; robust handling of missing lagged values is needed.
- Good solutions typically build panel time-series features: multi-horizon lags of price and volume, rolling statistics computed strictly from past data, day-of-week/holiday features, and selective cross-variety context from prior days.

Files you will use
- panel_daily.csv
- train.csv
- test.csv
- sample_submission.csv (example predictions file; replace values with your model’s outputs)

Good luck, and forecast responsibly!
