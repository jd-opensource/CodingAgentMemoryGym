# OpenMLE-fast task

Task ID: `all-natural-disasters-19002021-eosdis@1`

Native metric: `GlobalDisasterImpactMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (4654 bytes)
- `data/sample_submission.csv` (58101 bytes); columns: ["Event_ID", "Total Affected"]
- `data/test.csv` (475781 bytes); columns: ["Event_ID", "Year", "Seq", "Glide", "Disaster Group", "Disaster Subgroup", "Disaster Type", "Disaster Subtype", "Disaster Subsubtype", "Event Name", "Location", "Country", "ISO", "Region", "Continent", "Latitude", "Longitude", "Origin", "Associated Dis", "Associated Dis2", "Dis Mag Value", "Dis Mag Scale", "River Basin", "Start Year", "Start Month", "Start Day", "End Year", "End Month", "End Day", "CPI", "Adm Level", "DurationDays"]
- `data/train.csv` (2495890 bytes); columns: ["Event_ID", "Year", "Seq", "Glide", "Disaster Group", "Disaster Subgroup", "Disaster Type", "Disaster Subtype", "Disaster Subsubtype", "Event Name", "Location", "Country", "ISO", "Region", "Continent", "Latitude", "Longitude", "Origin", "Associated Dis", "Associated Dis2", "Dis Mag Value", "Dis Mag Scale", "River Basin", "Start Year", "Start Month", "Start Day", "End Year", "End Month", "End Day", "CPI", "Adm Level", "DurationDays", "Total Affected"]

## Public description

Global Disaster Impact Prediction (EM-DAT/EOSDIS)

Problem statement
- Task: Predict the number of people affected (Total Affected) for each natural disaster event using ex-ante event metadata.
- Context: Events span the globe and multiple hazard types. Accurate impact estimation supports planning and resource allocation.
- Type: Tabular regression with a time-based generalization target.

Files provided
- train.csv: Training set with features and the target column.
- test.csv: Test set with the same feature schema (no target).
- sample_submission.csv: A valid example submission format.

Target and identifiers
- ID column: Event_ID (unique identifier per disaster event).
- Target column (train only): Total Affected (non-negative float).

Feature schema (columns in train.csv and test.csv)
- Event_ID: unique event identifier (string).
- Year: event year as recorded (integer, may be missing for some entries).
- Seq: sequence number within the year (integer, may be missing).
- Glide: GLIDE number if available (string, may be missing).
- Disaster Group, Disaster Subgroup, Disaster Type, Disaster Subtype, Disaster Subsubtype: hazard taxonomy (categorical strings).
- Event Name: short event name/label (string, optional text feature).
- Location: event location descriptor (string, optional text feature).
- Country, ISO, Region, Continent: geography metadata (categorical strings).
- Latitude, Longitude: coordinates in decimal degrees (floats; may be missing; clipped to valid ranges).
- Origin: event origin type (categorical string).
- Associated Dis, Associated Dis2: associated disaster flags/links (categorical strings; presence can be used as binary features).
- Dis Mag Value: magnitude value (float; unit depends on Dis Mag Scale; no cross-unit conversion applied).
- Dis Mag Scale: magnitude scale (e.g., Richter, Kph, Km2) — use together with Dis Mag Value (categorical string).
- River Basin: basin name if applicable (categorical string).
- Start Year, Start Month, Start Day: start date components (integers; may be missing).
- End Year, End Month, End Day: end date components (integers; may be missing).
- CPI: consumer price index (float; macro covariate; coverage varies).
- Adm Level: administrative level metadata (categorical string).
- DurationDays: engineered feature = difference (in days) between end and start dates when available; otherwise missing.

Train/test split
- Chronological split to evaluate generalization:
  - Train: events with Start Year ≤ 2015.
  - Test: events with Start Year between 2016 and 2021 inclusive.
- No validation set is provided; participants may create their own validation via cross-validation or time-based folds.

Evaluation metric
- Root Mean Squared Logarithmic Error (RMSLE) on Total Affected.
- Computation: For each event, use log(1 + x) to handle zeros and heavy tails.
  RMSLE = sqrt(mean((log(1 + y_true) − log(1 + y_pred))^2)).
- Submission requirements:
  - CSV with exactly two columns in this order: [Event_ID, Total Affected].
  - Event_IDs must match the IDs and order in test.csv.
  - Predictions must be numeric, finite, and non-negative.

Guidance and constraints
- The target distribution is heavy-tailed and multi-modal across hazard types and regions; RMSLE emphasizes multiplicative accuracy and fairness across scales.
- Use ex-ante metadata only (the provided features are curated to avoid outcome leakage). Outcome variables and post-event decision fields have been excluded from the feature files.
- Handle missing values thoughtfully. Do not impute the target. Numeric types may require conversion; categorical features can be encoded via target-aware strategies (e.g., one-hot, frequency, embeddings).
- Suggested feature engineering:
  - DurationDays, seasonality features from months, hemispheric season via latitude sign, interactions between hazard taxonomy and magnitude scale.
  - Geospatial encodings (e.g., country/region embeddings or external shapefile-based features are optional if desired).
- Modeling approaches: Gradient boosting, regularized linear models with log-transform targets, neural networks for mixed tabular/text, and ensembles. Evaluate with time-aware validation.

Deliverables
- Submit a file following the submission requirements above. The public leaderboard is computed using RMSLE against the hidden test labels.

Goal
- Build models that generalize to recent years and accurately estimate Total Affected from heterogeneous, partially missing event metadata. This is a challenging but solvable ML task designed to reward robust data processing, careful feature engineering, and sound model training and evaluation.
