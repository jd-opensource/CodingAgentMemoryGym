# OpenMLE-fast task

Task ID: `us-collegiate-sports-dataset@1`

Native metric: `CollegiateSportsBudgetMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3207 bytes)
- `data/sample_submission.csv` (425378 bytes); columns: ["id", "total_exp_menwomen"]
- `data/test.csv` (2883490 bytes); columns: ["id", "year", "unitid", "institution_name", "city_txt", "state_cd", "zip_text", "classification_code", "classification_name", "classification_other", "ef_male_count", "ef_female_count", "ef_total_count", "sector_cd", "sector_name", "sportscode", "partic_men", "partic_women", "partic_coed_men", "partic_coed_women", "sum_partic_men", "sum_partic_women", "sports"]
- `data/train.csv` (12221845 bytes); columns: ["id", "year", "unitid", "institution_name", "city_txt", "state_cd", "zip_text", "classification_code", "classification_name", "classification_other", "ef_male_count", "ef_female_count", "ef_total_count", "sector_cd", "sector_name", "sportscode", "partic_men", "partic_women", "partic_coed_men", "partic_coed_women", "sum_partic_men", "sum_partic_women", "sports", "total_exp_menwomen"]

## Public description

BudgetEx — Predict Collegiate Sports Program Expenditures (2015–2019)

Problem statement
Participants must build a machine learning model to predict the combined sports program expenditures (total_exp_menwomen) for US colleges and universities, at the institution–sport–year level. Each row represents a single sport at an institution in a given academic year. Expenditures vary widely by sport, institution type, and geography, and are influenced by participation and enrollment.

Task
- Type: Tabular regression
- Target: total_exp_menwomen (USD), strictly positive
- Input features: Institutional identifiers and attributes, geography, year, enrollment counts, sport identifiers, and participation counts.

Data description
Each row corresponds to a unique institution–sport–year record spanning 2015 to 2019.
Features provided (non-exhaustive):
- year, unitid, institution_name
- city_txt, state_cd, zip_text
- classification_code, classification_name, classification_other
- sector_cd, sector_name
- sportscode, sports
- ef_male_count, ef_female_count, ef_total_count
- partic_men, partic_women, partic_coed_men, partic_coed_women
- sum_partic_men, sum_partic_women

Excluded financial fields
To prevent label leakage, the following columns are removed from both train and test:
- exp_men, exp_women, rev_men, rev_women, total_rev_menwomen

Files
- train.csv: Labeled training data including the target column total_exp_menwomen and an id column.
- test.csv: Unlabeled test data with the same feature columns as train.csv (excluding the target) and an id column.
- sample_submission.csv: A valid example submission with columns [id, total_exp_menwomen].

Train/test split
- Time-forward split: The test set consists of the most recent year in the dataset (2019). The training set contains the remaining years with valid targets.
- Disjointness: Train and test rows are disjoint and identified by a unique id column.
- Coverage: All sports and institution classifications present in the test set also appear in the training set.

Evaluation
- Metric: Root Mean Squared Logarithmic Error (RMSLE), computed as the square root of the mean squared error between log1p(predicted) and log1p(actual).
- Rationale: Expenditures are heavily skewed across institutions and sports. RMSLE emphasizes relative error and stabilizes the impact of large budgets while remaining sensitive to smaller programs.

Submission format
- A CSV file with exactly two columns: id and total_exp_menwomen.
- Each id must appear exactly once and match the ids in test.csv.
- Predictions must be finite, numeric, and nonnegative.

Recommendations for modeling
- Handle missing values and parse "NA" as missing.
- Engineer features from participation and enrollment (e.g., totals, ratios, per-capita measures).
- Consider one-hot encoding high-cardinality categorical variables (institution, sport, classification, state), or use models that can natively handle categorical features.
- Use time-aware or grouped validation (e.g., out-of-year or institution-grouped CV) to avoid leakage due to repeated institutions across years.
- Avoid using excluded financial columns or any transformation that reconstructs the target.
