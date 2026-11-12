# OpenMLE-fast task

Task ID: `yugioh-full-card-database-index-august-1st-2025@2`

Native metric: `YugiohAttackPredictionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (4177 bytes)
- `data/sample_submission.csv` (131456 bytes); columns: ["card_id", "attack"]
- `data/test.csv` (2326814 bytes); columns: ["card_id", "name", "name_official", "description", "sub_type", "attribute", "rank", "rarity", "set_name", "set_id", "set_release", "level_kind", "level_value"]
- `data/train.csv` (9380366 bytes); columns: ["card_id", "name", "name_official", "description", "sub_type", "attribute", "rank", "rarity", "set_name", "set_id", "set_release", "level_kind", "level_value", "attack"]

## Public description

Competition: Predict Monster ATK from Card Text and Metadata

Problem statement
Build a model that predicts a Yu-Gi-Oh! monster card’s Attack (ATK) value from its text and metadata. Each row corresponds to a single printed card (a specific print of a monster). Use the non-ATK fields to learn design patterns that determine ATK, such as Level/Link rating, Attribute, archetype/type-line, and effect text.

Why this is interesting
- Rich NLP + tabular signals: long effect text, archetype/type-lines, attributes, set/rarity and release timing.
- Real design target: ATK is a canonical game stat authored by Konami; learning it from context is challenging and meaningful.
- Scale: Tens of thousands of monster prints; enough data for strong feature engineering and modern text encoders.

Data description
Final files in the competition dataset:
- train.csv: Training rows with features and the target column attack.
- test.csv: Test rows with the same feature columns as train.csv except attack (which is withheld).
- sample_submission.csv: Example submission file with columns [card_id, attack]. The attack values are random placeholders and must be replaced by your predictions.

Columns
All rows in train.csv and test.csv represent MONSTER cards with a numeric ATK. The following feature columns are provided (string unless noted):
- card_id: Unique identifier for a specific monster print (string).
- name: Printed card name.
- name_official: Canonical/official card name.
- description: Effect text or normal card text.
- sub_type: Type-line (e.g., [Dragon／Effect], [Fiend／Link／Effect], [Beast／Normal]).
- attribute: Monster Attribute (e.g., DARK, LIGHT, EARTH...).
- rank: Original level/rank/link string from the source (e.g., "Level 4", "Link 3").
- rarity: Rarity for this print (e.g., C Common, SR Super Rare...).
- set_name: Set name of this print.
- set_id: Set code of this print.
- set_release: Release date for this print (YYYY-MM-DD where available).
- level_kind: Parsed from rank. One of {Level, Rank, Link, UNK}.
- level_value: Parsed integer value from rank where available; otherwise empty.

The training file additionally contains:
- attack: Target ATK value (integer).

Important notes
- Non-monster rows, rows with non-numeric/unknown ATK, and columns that could trivialize the task (e.g., defense) are removed from the provided files.
- The IDs are anonymized; there are no file paths in the CSVs.
- The test.csv file has identical feature schema to train.csv (except attack) and includes the same card_id field used for submission.

Task
Given test.csv, predict the ATK value for each card_id and submit a CSV with the required format.

Submission format
- CSV with exactly two columns and a header row: [card_id, attack].
- card_id must match those in test.csv and be in the same order.
- attack may be integer or float in your file; it will be evaluated numerically. Predictions outside typical ranges are allowed but may harm your score.

Evaluation
- Metric: Mean Absolute Error (MAE) in ATK points between your predictions and the ground truth. Lower is better.
- MAE is robust to outliers and directly interpretable as the average absolute ATK error.

Modeling guidance (non-binding)
- Text processing: normalize quotes, lowercase, tokenize; try TF-IDF n-grams, fastText, or transformer encoders.
- Structure from rank: parse Level/Rank/Link as categorical + integer features; consider a pendulum flag if you derive it from sub_type.
- Useful categorical features: attribute, sub_type, rarity, set_release (bucket to age or year), and name/name_official.
- Consider set_release as a proxy for era mechanics; you may derive temporal features (e.g., year, pre/post Link era).
- Avoid external ATK lookups or resources that directly leak labels.

Train/test split
- Rows are split only among MONSTER prints with numeric ATK.
- The split is stratified by parsed level_kind/level_value to preserve difficulty across scales (e.g., Link 1 vs. Level 10).

File list recap
- train.csv: features + attack target
- test.csv: features only
- sample_submission.csv: [card_id, attack]

Good luck and have fun exploring the design semantics behind ATK!
