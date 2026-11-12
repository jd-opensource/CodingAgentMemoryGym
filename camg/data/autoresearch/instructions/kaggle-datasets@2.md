# OpenMLE-fast task

Task ID: `kaggle-datasets@2`

Native metric: `KaggleFeaturedDatasetMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3150 bytes)
- `data/sample_submission.csv` (25016 bytes); columns: ["id", "is_featured"]
- `data/test.csv` (1701381 bytes); columns: ["id", "title", "overview", "commonFileTypes", "datasetSize", "licenseName", "licenseShortName", "type", "maintainerOrganization", "creatorName", "ownerName", "creatorUserId", "ownerUserId", "creatorUrl", "ownerUrl", "datasetUrl", "diffType", "currentDatasetVersionNumber", "dateUpdated", "categories"]
- `data/train.csv` (6909295 bytes); columns: ["id", "is_featured", "title", "overview", "commonFileTypes", "datasetSize", "licenseName", "licenseShortName", "type", "maintainerOrganization", "creatorName", "ownerName", "creatorUserId", "ownerUserId", "creatorUrl", "ownerUrl", "datasetUrl", "diffType", "currentDatasetVersionNumber", "dateUpdated", "categories"]

## Public description

Kaggle Featured Dataset Prediction

Problem
Predict whether a newly published public dataset on Kaggle will be featured (highlighted by editors) using only information available at or near publish time.

Files
- train.csv: Training data with id, target, and features
- test.csv: Test data with id and features (no target)
- sample_submission.csv: Example submission file with the required columns

Target
- is_featured: Binary label (1 if the dataset is featured, 0 otherwise)

Features
Each row represents a public Kaggle dataset snapshot. The following columns are provided as inputs:
- id: Dataset identifier
- title: Dataset title (text)
- overview: Dataset overview/description (text)
- commonFileTypes: JSON-like summary of file types and sizes included
- datasetSize: Total size in bytes
- licenseName, licenseShortName: License information
- type: Kaggle dataset type (e.g., fileset)
- maintainerOrganization: Publishing organization, if any
- creatorName, ownerName: Publisher names
- creatorUserId, ownerUserId: Publisher user IDs
- creatorUrl, ownerUrl, datasetUrl: URL slugs (tokenizable strings)
- diffType: Versioning info (e.g., versioned/unversioned)
- currentDatasetVersionNumber: Version number
- dateUpdated: ISO8601 timestamp of last update
- categories: JSON-like list of tag objects (use tag names as inputs)

Notes on leakage avoidance and static inputs
- Engagement counters and downstream curation indicators are not included in the files. The task focuses on pre-engagement, static metadata only.

Evaluation
- Metric: Average Precision (area under the precision–recall curve) on the positive class (is_featured = 1).
- Submissions must contain exactly two columns: id, is_featured. The is_featured column should be a score in [0, 1] indicating the predicted probability (or confidence) that the dataset is featured.

Submission format
- CSV with header and rows for all ids in test.csv
- Columns (in any order):
  - id: integer identifier
  - is_featured: float score in [0, 1]

Recommended approach
- Text processing: Clean and vectorize title and overview (e.g., TF‑IDF n‑grams, or transformer embeddings).
- Parse JSON-like strings: Extract file types and sizes from commonFileTypes; extract tag names from categories.
- Categorical handling: Encode high-cardinality IDs and organization names (e.g., hashing, regularization, or leakage‑safe target encoding using cross‑validation on the training set).
- Time features: Extract year/month/day-of-week from dateUpdated to capture temporal patterns while avoiding pure time-split leakage.
- Modeling: Start with linear models or gradient-boosted trees; improve via text+tabular fusion.

Data split
- Single train/test split stratified by label and balanced across time bins to encourage temporal generalization while ensuring both classes are represented in train and test.

Rules
- Do not use any external information that directly reveals the target for the test set.
- Do not infer labels from file names or hidden artifacts.

Files to produce
- A single CSV named submission.csv (or any name you prefer when uploading) with the exact schema described above.
