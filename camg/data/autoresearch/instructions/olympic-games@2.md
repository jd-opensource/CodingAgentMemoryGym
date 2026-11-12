# OpenMLE-fast task

Task ID: `olympic-games@2`

Native metric: `OlympicGoldForecastMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (4335 bytes)
- `data/sample_submission.csv` (21307 bytes); columns: ["row_id", "pred"]
- `data/test.csv` (77169 bytes); columns: ["row_id", "Season", "Year", "Country", "Sport", "prev_cs_gold_sum", "prev_cs_medal_sum", "prev_cs_anymed_editions", "prev_cs_had_gold_prev_ed", "prev_cs_years_since_last_gold", "prev_c_all_medals", "prev_c_all_golds", "prev_sport_event_count", "log_population", "log_gdp_per_capita"]
- `data/train.csv` (418209 bytes); columns: ["row_id", "Season", "Year", "Country", "Sport", "prev_cs_gold_sum", "prev_cs_medal_sum", "prev_cs_anymed_editions", "prev_cs_had_gold_prev_ed", "prev_cs_years_since_last_gold", "prev_c_all_medals", "prev_c_all_golds", "prev_sport_event_count", "log_population", "log_gdp_per_capita", "y"]

## Public description

Olympic Country–Sport Gold Prediction per Edition (1896–2014)

Background
National Olympic Committees plan medal targets by sport for each Games. Historical athlete-level medal records can be aggregated into sport-level outcomes for every country and edition. Your task is to forecast which country–sport entries will produce at least one gold medal at a given Olympic edition.

Problem statement
Given historical Olympic results up to, but not including, the target edition and a set of engineered features, predict the probability that a country will win at least one gold medal in a specific sport at that edition. Each row corresponds to a unique (Country, Sport, Year, Season) group that appears in the official medal tables for that edition.

Files
- train.csv: Feature matrix and target for training.
- test.csv: Feature matrix for held-out editions (no target).
- sample_submission.csv: Example submission file with the correct format.

Target
- y: Binary target indicating whether the country won at least one gold medal (1) in the specified sport at that edition; otherwise 0.

Row identifier
- row_id: Unique identifier for each (Country, Sport, Year, Season) row. Use this column to align your predictions in the submission file.

Feature schema (columns)
- Season: "Summer" or "Winter".
- Year: Olympic year of the edition.
- Country: IOC/NOC 3-letter country code (e.g., USA, GRE).
- Sport: High-level sport name (e.g., Athletics, Swimming).
- prev_cs_gold_sum: Cumulative number of gold medals this country previously won in this sport before the current edition.
- prev_cs_medal_sum: Cumulative number of total medals this country previously won in this sport before the current edition.
- prev_cs_anymed_editions: Count of prior editions in which this country won any medal in this sport.
- prev_cs_had_gold_prev_ed: Indicator (0/1) whether this country won gold in this sport in its immediately preceding edition appearance.
- prev_cs_years_since_last_gold: Years since the last gold this country won in this sport before the current edition (large value when none).
- prev_c_all_medals: Country’s cumulative medals across all sports and past editions of the same season (before the current edition).
- prev_c_all_golds: Country’s cumulative golds across all sports and past editions of the same season (before the current edition).
- prev_sport_event_count: Number of distinct medal events contested in this sport in the most recent prior edition of the same season (edition-level context, no target-year outcomes used).
- log_population: Natural log of population (if available).
- log_gdp_per_capita: Natural log of GDP per capita (if available).

Train/test split
- Summer test editions: 2008 and 2012
- Winter test editions: 2010 and 2014
All other editions belong to the training set. Features are computed strictly from data prior to the current edition to prevent leakage.

Evaluation
Submissions must be a CSV with the following columns:
- row_id: Identifier matching test.csv
- pred: Your predicted probability that y=1 for the corresponding row_id (a real number in [0, 1])

Metric: Balanced Log Loss (binary). For each sample i with true label y_i ∈ {0,1} and submitted probability p_i, the per-sample log loss is:
-ℓ_i = y_i * log(p_i) + (1 - y_i) * log(1 - p_i)
Class weights are computed inversely proportional to the class frequencies in the evaluated set. The final score is the weighted mean of per-sample losses, with predictions clipped to [1e-15, 1-1e-15] for numerical stability. Lower is better.

Notes and guidance
- The task is a time-aware binary classification forecasting problem. Use only pre-edition information when creating additional features.
- Categorical encoders, tree-based models, linear models, time-aware cross-validation, and calibration can all be effective.
- The provided features are derived from historical athlete-level results and country macro indicators. You are free to engineer additional features from the provided columns, but do not assume access to athlete- or event-level data.
- The label space is balanced enough for common ML methods; the metric rewards well-calibrated probabilities.

Deliverables
- Submit a CSV with columns [row_id, pred] for every row in test.csv.
- Ensure there are no missing or infinite values and that pred ∈ [0,1].
