# OpenMLE-fast task

Task ID: `myanimelist-dataset@2`

Native metric: `AnimeRatingClassificationMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (4062 bytes)
- `data/sample_submission.csv` (43109 bytes); columns: ["anime_id", "Rating"]
- `data/test.csv` (2559800 bytes); columns: ["anime_id", "Name", "English name", "Other name", "Genres", "Synopsis", "Type", "Episodes", "Aired", "Premiered", "Status", "Producers", "Licensors", "Studios", "Source", "Duration"]
- `data/train.csv` (10341273 bytes); columns: ["anime_id", "Name", "English name", "Other name", "Genres", "Synopsis", "Type", "Episodes", "Aired", "Premiered", "Status", "Producers", "Licensors", "Studios", "Source", "Duration", "Rating"]

## Public description

Competition title: Anime Age Rating Prediction (Content-Based)

Background
MyAnimeList (MAL) assigns age ratings (G, PG, PG-13, R, R+, Rx) to anime based on content suitability. Automatically inferring age rating from an anime’s synopsis and metadata supports moderation and cataloging at scale. This competition challenges participants to build robust models that predict the MAL age rating category from textual synopsis and structured metadata.

Problem statement
Given an anime’s synopsis and metadata, predict its MAL age rating category. This is a multiclass classification task. The target label is Rating with classes: G, PG, PG-13, R, R+, Rx. Items with UNKNOWN or unrated values are excluded from the dataset.

Data description
The dataset contains thousands of anime entries with text and tabular metadata. The final competition files are:
- train.csv: Labeled training data with features and the target column Rating.
- test.csv: Unlabeled test data with the same features but without the Rating column.
- sample_submission.csv: A sample submission file containing example predictions in the required format.

Columns included in train.csv and test.csv (train additionally includes Rating):
- anime_id: Unique identifier of the anime.
- Name: Original title.
- English name: English title.
- Other name: Alternate title(s).
- Genres: Comma-separated genres.
- Synopsis: Plot summary text.
- Type: TV, Movie, OVA, ONA, Special, Music, etc.
- Episodes: Number of episodes (numeric where available).
- Aired: Airing dates.
- Premiered: Season and year.
- Status: Airing status.
- Producers: Production companies.
- Licensors: Licensors.
- Studios: Animation studios.
- Source: Source material (manga, light novel, original, etc.).
- Duration: Episode duration.

Columns intentionally excluded to avoid bias and leakage from audience behavior:
- Score, Rank, Popularity, Favorites, Scored By, Members. Image URLs are also excluded.

What you need to build
- Data processing: Clean and normalize text (Synopsis) and parse metadata. Handle missing values and inconsistent formats.
- Feature engineering: Create informative features from text (e.g., TF-IDF, pretrained embeddings) and categorical/numeric metadata (e.g., multi-hot genres, type/source/studio encodings, episode counts, durations).
- Model training: Train a multiclass classifier that integrates text and tabular features. Approaches include linear models, gradient boosting, and transformer-based NLP.
- Model evaluation: Use cross-validation or validation splits to tune models, with Macro-F1 as the main objective.

Evaluation metric
Submissions are evaluated using Macro-averaged F1 across the classes present in the test set:
- For each class c, compute F1_c = 2 * (precision_c * recall_c) / (precision_c + recall_c), using 0 when precision or recall are undefined.
- The leaderboard score is the arithmetic mean of F1_c over all labels present in the test set.
Macro-F1 treats all classes equally and counters class imbalance, rewarding models that perform well across both common and rare ratings. There is no ordinal relationship among labels; treat them as categorical.

Submission format
- A CSV file with exactly two columns: anime_id and Rating.
- anime_id must match the IDs in test.csv exactly and appear once each, in the same order as test.csv.
- Rating must be one of the valid class labels {G, PG, PG-13, R, R+, Rx}.

Train/test split
The data is split deterministically and stratified by Rating to preserve label proportions while ensuring that every test label appears in the training set. The test set is held out for evaluation; only train.csv, test.csv, and sample_submission.csv are provided.

Notes
- Handle missing values robustly; many metadata fields can be empty or contain UNKNOWN.
- This is a content-based task; do not rely on audience-derived aggregates (they are excluded).
- Images are not provided.
- You may use any ML techniques and external pretraining for text embeddings, provided predictions are produced strictly from train.csv/test.csv inputs.
