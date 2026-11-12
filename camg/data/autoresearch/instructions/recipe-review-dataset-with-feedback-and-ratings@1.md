# OpenMLE-fast task

Task ID: `recipe-review-dataset-with-feedback-and-ratings@1`

Native metric: `RecipeReviewOrdinalMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2574 bytes)
- `data/sample_submission.csv` (109588 bytes); columns: ["comment_id", "stars"]
- `data/test.csv` (1149466 bytes); columns: ["comment_id", "text", "created_at", "recipe_code", "recipe_number", "recipe_name", "user_id", "user_name", "user_reputation"]
- `data/train.csv` (4221087 bytes); columns: ["comment_id", "text", "created_at", "recipe_code", "recipe_number", "recipe_name", "user_id", "user_name", "user_reputation", "stars"]

## Public description

Title: Recipe Review Ordinal Rating Prediction

Problem statement
Predict the 1–5 star rating that a user assigns to a recipe at the time their review is posted. Use the free-text review and available context present at posting time. The goal is to capture nuanced sentiment and intensity (e.g., mild vs. strong praise/complaints) while generalizing across users, recipes, and temporal drift.

Data
You are provided with tabular files derived from real recipe reviews. Each row represents a single review event. The final competition files are:
- train.csv: features plus the target label (stars)
- test.csv: features only (no stars)
- sample_submission.csv: example submission format

Feature columns available
- comment_id: unique identifier for the review (use as the submission key)
- text: the review text
- created_at: timestamp (UNIX seconds) when the review was submitted
- recipe_code, recipe_number, recipe_name: identifiers and a human-readable recipe name
- user_id, user_name, user_reputation: user identifiers and reputation

Target label
- stars: integer rating in {1, 2, 3, 4, 5}

Train/test split
- Chronological split by created_at to mimic real-world deployment and reduce leakage: the earlier 80% of labeled reviews are in the training set; the most recent 20% are in the test set. All test label classes appear at least once in the training set.

Important notes
- Post-hoc engagement signals (e.g., thumbs_up, thumbs_down, reply_count, best_score) are excluded from features to prevent label leakage.
- The leading unnamed CSV index column (if present) is removed.
- Reviews with stars = 0 or missing text are excluded from the scored data.

Evaluation
- Metric: Quadratic Weighted Kappa (QWK) computed on integer classes {1,2,3,4,5}.
  QWK respects the ordinal nature of ratings and penalizes larger disagreements more than adjacent misclassifications. It is robust under class imbalance typical of review data.

Submission format
- A CSV file with two columns in this order:
  - comment_id
  - stars (predicted integer in {1,2,3,4,5})
- Include predictions for every comment_id in test.csv exactly once.

Modeling guidance (optional)
- Combine text modeling (e.g., TF-IDF, lightweight transformers) with tabular features such as user reputation, recipe identifiers, and time-derived features (e.g., day-of-week, month). Handle HTML entities in text and high-cardinality IDs via hashing/embeddings as desired.
- Ensure deterministic behavior and avoid using any information not available at the time of the review (e.g., future engagement outcomes).
