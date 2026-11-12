# OpenMLE-fast task

Task ID: `netflix-datasets-evaluation@2`

Native metric: `NetflixCountryOriginMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2971 bytes)
- `data/sample_submission.csv` (41648 bytes); columns: ["show_id", "country"]
- `data/test.csv` (615880 bytes); columns: ["show_id", "type", "title", "director", "cast", "date_added", "date_added.1", "release_year", "rating", "duration", "listed_in", "description"]
- `data/train.csv` (2554394 bytes); columns: ["show_id", "type", "title", "director", "cast", "country", "date_added", "date_added.1", "release_year", "rating", "duration", "listed_in", "description"]

## Public description

Netflix Country-of-Origin Multilabel Prediction

Problem statement
Participants are challenged to build a model that predicts the producing countries for each Netflix title using its synopsis and available metadata. Many titles are co-productions spanning multiple countries, so each example may have multiple correct country labels.

Data
Each row represents one Netflix title. The following fields are available:
- show_id: unique identifier
- type: Movie or TV Show
- title: title name
- director: director names (may be missing)
- cast: cast list (may be missing)
- date_added: date when the title was added to Netflix (string format)
- date_added.1: an alternative date format
- release_year: original release year
- rating: age/content rating
- duration: duration string (e.g., "90 min" or "2 Seasons")
- listed_in: genre tags
- description: synopsis text

Target
- country: one or more producing countries (comma-separated). This is the label to be predicted for each title.

Files
- train.csv: full training set with all features and the country label.
- test.csv: test set with all features and without the country label.
- sample_submission.csv: template for submissions. It contains random but valid labels and demonstrates the required format.

Submission format
- A CSV file with exactly two columns: show_id and country.
- The country field must be a comma-separated list of predicted country names. Order does not matter. Whitespace is ignored. Case-insensitive matching is applied during evaluation.

Task characteristics
- Multilabel classification with long-tail label distribution.
- Rich text (description) and sparse metadata (names, dates, durations) can be leveraged.
- Some rows have missing director/cast; models must be robust to missingness.

Metric
- Primary metric: micro-averaged F1 across country labels.
- Rationale: Micro-F1 equitably scores each predicted country instance, balancing precision and recall in the presence of label imbalance and co-productions.

Important notes
- All test labels appear at least once in the training set.
- The test set contains titles with one or more countries. There are no examples with empty country labels.
- The test set preserves overall label frequencies as much as possible while preventing label leakage.

Recommendations for participants
- Text processing on description, title, director, and cast can provide strong signals (e.g., TF-IDF n-grams or transformer-based embeddings).
- Engineer simple numeric features from duration and dates (e.g., minutes, season count, month added).
- Use multilabel-compatible classifiers (e.g., one-vs-rest linear models, classifier chains, or deep models). Consider threshold tuning per label.
- Handle class imbalance with appropriate regularization, class weights, or sampling.

Deliverable
- Submit a CSV following the specified format. The leaderboard is based on micro-F1 computed between your predictions and the hidden ground truth for the test set.
