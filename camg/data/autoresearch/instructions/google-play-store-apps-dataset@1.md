# OpenMLE-fast task

Task ID: `google-play-store-apps-dataset@1`

Native metric: `GooglePlayInstallsMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1410 bytes)
- `data/sample_submission.csv` (37929 bytes); columns: ["Id", "Installs"]
- `data/test.csv` (255548 bytes); columns: ["App", "Category", "Rating", "Reviews", "Size", "Type", "Price", "Content Rating", "Genres", "Last Updated", "Current Ver", "Android Ver", "Id"]
- `data/train.csv` (1118454 bytes); columns: ["App", "Category", "Rating", "Reviews", "Size", "Installs", "Type", "Price", "Content Rating", "Genres", "Last Updated", "Current Ver", "Android Ver", "Id"]

## Public description

Competition: Predict App Popularity Tier from Google Play Metadata

Problem statement:
Participants must predict the Google Play install bucket (popularity tier) of an app using its store listing metadata. The target classes are the discrete install buckets (e.g., "10,000+", "5,000,000+"), which are inherently ordered by magnitude.

Data provided (under public/):
- train.csv: Tabular training data including the target column Installs.
- test.csv: Test data with the same feature columns as train.csv, excluding Installs.
- sample_submission.csv: A sample file showing the expected submission format.

Features and target:
- Target: Installs (string bucket such as "1+", "10+", "1,000+", ..., "50,000,000+").
- Example feature columns include: Category, Rating, Reviews, Size, Type, Price, Content Rating, Genres, Last Updated, Android Ver.

Submission format:
- CSV file with exactly two columns:
  - Id: The row identifier provided in test.csv.
  - Installs: Your predicted install bucket for each Id.
- Predicted Installs values should be valid bucket strings observed in the training data.

Train/test split details:
- The split is stratified by the target install bucket to preserve class distribution. Rare buckets with only a single sample are kept exclusively in the training set to ensure all test labels exist in the training set.

Files:
- train.csv
- test.csv
- sample_submission.csv

Good luck!
