# OpenMLE-fast task

Task ID: `formula-1-drivers-dataset@1`

Native metric: `F1CareerPointsMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2950 bytes)
- `data/sample_submission.csv` (1757 bytes); columns: ["Driver_ID", "Points"]
- `data/test.csv` (16924 bytes); columns: ["Driver_ID", "Driver", "Nationality", "Seasons", "Race_Entries", "Race_Starts", "Pole_Positions", "Race_Wins", "Podiums", "Fastest_Laps", "Active", "Decade", "Years_Active"]
- `data/train.csv` (71299 bytes); columns: ["Driver_ID", "Driver", "Nationality", "Seasons", "Race_Entries", "Race_Starts", "Pole_Positions", "Race_Wins", "Podiums", "Fastest_Laps", "Active", "Decade", "Years_Active", "Points"]

## Public description

Formula 1 Era-Aware Career Points Prediction

Problem statement
Build a machine learning model that predicts a Formula 1 driver’s total career points (Points) from driver-level tabular features. The mapping from performance statistics to points is era-dependent due to evolving rules (e.g., scoring top 6 vs. top 10, fastest lap bonus, season length). This nonstationarity, combined with heavy-tailed targets and sparse careers, makes precise prediction challenging yet tractable.

Data provided
- train.csv: Driver-level features and the target column Points.
- test.csv: Driver-level features for held-out drivers (no target column); includes Driver_ID for submission matching.
- sample_submission.csv: Example submission with the correct format.

Rows represent unique drivers. Columns included:
- Driver_ID: anonymized identifier used for submission matching (string)
- Driver: driver name (string)
- Nationality: driver nationality (string)
- Seasons: stringified list of years competed (e.g., "[2005, 2006]")
- Race_Entries, Race_Starts, Pole_Positions, Race_Wins, Podiums, Fastest_Laps: performance counts (numeric)
- Active: whether the driver was active at the 2023 Bahrain GP snapshot (binary indicator encoded as true/false)
- Decade: primary decade marker for the driver’s career (numeric)
- Years_Active: total count of active seasons (numeric)
- Points (train.csv only): total career points (float)

Columns intentionally excluded due to target leakage or derivation: Championships, Champion, Championship Years, Pole_Rate, Start_Rate, Win_Rate, Podium_Rate, FastLap_Rate, Points_Per_Entry.

Modeling guidance
- Parse Seasons to engineer temporal features: first/last year, span length, gaps, era bins (e.g., pre-1990, 1990s, 2000s, 2010s, 2020s), fraction of seasons per era.
- Encode categorical features (Nationality; Driver if used as identifier for baselines). Avoid memorization on Driver.
- Coerce numeric columns, handle missing values, and consider log1p/scaling for skewed counts.
- Era awareness is essential: leverage Decade and season-derived signals to reflect changing points systems.

Evaluation metric
- Mean Absolute Error (MAE) on Points.
- Robust and fair: MAE emphasizes absolute accuracy and is less dominated by extreme outliers than RMSE, suitable for heavy-tailed totals.

Submission format
- Submit a CSV with exactly two columns and a header: Driver_ID, Points
- Driver_ID values must exactly match those in test.csv (no duplicates, no missing or extra IDs).
- Points must be finite numeric values (no NaN/Inf).
- Scoring aligns by Driver_ID; order does not matter.

Why this challenge is meaningful
- High-quality use of the full driver-level dataset.
- Requires modeling a nonstationary relationship between performance and points across eras.
- Encourages feature engineering from raw seasonal data and robust regression techniques.

Good luck, and enjoy building era-aware models for F1 career points!
