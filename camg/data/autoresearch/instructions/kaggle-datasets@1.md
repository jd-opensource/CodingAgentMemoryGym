# OpenMLE-fast task

Task ID: `kaggle-datasets@1`

Native metric: `MultiLabelTaggingMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3043 bytes)
- `data/sample_submission.csv` (41955 bytes); columns: ["id", "labels"]
- `data/test.csv` (276777 bytes); columns: ["id", "title", "overview", "commonFileTypes", "datasetSize", "licenseName", "licenseShortName", "type", "maintainerOrganization", "creatorName", "ownerName", "creatorUserId", "ownerUserId", "dateUpdated", "datasetUrl", "diffType", "currentDatasetVersionNumber"]
- `data/train.csv` (1158860 bytes); columns: ["id", "title", "overview", "commonFileTypes", "datasetSize", "licenseName", "licenseShortName", "type", "maintainerOrganization", "creatorName", "ownerName", "creatorUserId", "ownerUserId", "dateUpdated", "datasetUrl", "diffType", "currentDatasetVersionNumber", "labels"]

## Public description

Kaggle Dataset Auto-Tagging (MAP@5)

Problem statement
Predict the most relevant taxonomy tags for a Kaggle dataset using only its static metadata and textual description available at publish time. For each dataset, submit a ranked list (up to 5) of tag predictions.

Data description
Files provided to participants:
- train.csv: Training rows with features and the ground-truth tags in a single column named labels (space-separated tokens).
- test.csv: Test rows with the same feature columns as train.csv but without labels.
- sample_submission.csv: A template demonstrating the required submission format (id, labels) with 5 example tags per row.

Each row represents a Kaggle dataset snapshot. Features come only from static, non-engagement metadata, such as:
- Text: title, overview
- Structured: commonFileTypes, datasetSize, licenseName, licenseShortName, type, maintainerOrganization, creatorName, ownerName, creatorUserId, ownerUserId, datasetUrl (slug tokens), diffType, currentDatasetVersionNumber, dateUpdated
Fields that encode post-publication outcomes or curation (e.g., views, downloads, votes, featured flags, discussion/script links, avatar/thumbnail URLs, collaborator/hidden/private flags) are excluded to avoid leakage.

Target labels
- The labels column contains the taxonomy tag names associated with the dataset (multi-label).
- Labels are lowercased and normalized to snake_case (non-alphanumeric characters → underscore; multiple underscores collapsed; trimmed).
- The label space includes tags that occur sufficiently often in the corpus to support reliable evaluation. All ground-truth labels in test appear at least once in training.

Submission format
- CSV with two columns: id, labels
- labels contains up to 5 tag tokens separated by spaces, ordered from most to least likely. Fewer than 5 are allowed.
- Duplicate tokens in a row are ignored; only the first occurrence counts.
- Using tokens not present in training is allowed but yields no credit.
- The set of ids must match test.csv exactly, each appearing once.

Evaluation
Mean Average Precision at 5 (MAP@5) is used.
- For each row, compute the average precision of the top-5 predictions against the ground-truth labels for that row.
- The final score is the mean across all test rows.

Practical guidance
- Strong baselines: TF–IDF + linear classifiers on title + overview text, augmented with parsed features from commonFileTypes (file types, counts, total size), datasetUrl slug tokens, type, license, datasetSize, currentDatasetVersionNumber, creator/owner IDs, and dateUpdated (e.g., year/month).
- More advanced models can fuse text encoders (e.g., transformer embeddings) with tabular features for improved performance.
- No engagement/counter fields or curation flags are present; models should rely on text and static metadata only.

Files to use
- train.csv (features + labels)
- test.csv (features only)
- sample_submission.csv (submission template)

Good luck building a multi-label ranking model that understands both text and metadata!
