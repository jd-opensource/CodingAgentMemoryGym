# OpenMLE-fast task

Task ID: `trip-advisor-hotel-reviews@1`

Native metric: `TripAdvisorRatingMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2398 bytes)
- `data/sample_submission.csv` (57403 bytes); columns: ["review_id", "Rating"]
- `data/test.csv` (3059100 bytes); columns: ["review_id", "Review"]
- `data/train.csv` (12103644 bytes); columns: ["review_id", "Review", "Rating"]

## Public description

Competition: TripAdvisor Review Rating Prediction (Ordinal NLP)

Problem statement
Predict the exact star rating (1–5) from a hotel review’s free-text. The labels are ordered categories, so larger errors should be penalized more heavily than smaller ones. Build robust NLP models that handle long, noisy text while respecting the ordinal nature of the target.

Data description
- Input text: Review (free text)
- Target label: Rating (integer in {1, 2, 3, 4, 5})

Provided files
- train.csv: Columns [review_id, Review, Rating]
- test.csv: Columns [review_id, Review]
- sample_submission.csv: Columns [review_id, Rating]

Notes
- review_id is a unique, opaque identifier. Use it to merge predictions to test rows.
- The split is stratified by Rating and deterministic. All classes present in test occur in train.
- The dataset contains ~20k reviews with diverse language, variable length, and domain slang.

Recommended approach
Participants are encouraged to explore techniques such as:
- Data processing: Unicode normalization, whitespace cleanup, lowercasing, robust tokenization; handle very long documents via truncation or long-context models.
- Feature engineering: character/word n-grams, TF-IDF, subword tokenization, sentence-level aggregation, domain lexicons.
- Modeling: Linear models and tree-based models on vectorized text; fine-tuned transformers; ordinal methods (e.g., CORN, ordinal regression, thresholded continuous scores).
- Post-processing and calibration: Threshold optimization aligned to the ordinal target.

Evaluation metric
Quadratic Weighted Kappa (QWK) between true and predicted ratings. QWK measures agreement while penalizing larger disagreements more than smaller ones. It ranges from 0 (chance-level agreement) to 1 (perfect agreement) and is well-suited for ordered categories.

Submission format
Submit a CSV with exactly these columns:
- review_id: Must match IDs in test.csv; each must appear exactly once.
- Rating: Integer in {1, 2, 3, 4, 5}.

Rules
- The file must contain predictions for all and only the review_id values from test.csv.
- No duplicate or missing review_id rows.
- No paths or extra columns; Rating must be a valid integer label.
- Row order is not required to match test.csv as long as review_id coverage is exact.

Goal
Maximize QWK on the hidden test set by building high-quality, ordinal-aware models leveraging the full dataset.
