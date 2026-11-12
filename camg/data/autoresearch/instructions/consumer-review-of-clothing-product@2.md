# OpenMLE-fast task

Task ID: `consumer-review-of-clothing-product@2`

Native metric: `ClothingReviewRatingMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2607 bytes)
- `data/sample_submission.csv` (116038 bytes); columns: ["review_id", "Cons_rating"]
- `data/test.csv` (2409437 bytes); columns: ["review_id", "Title", "Review"]
- `data/train.csv` (9875589 bytes); columns: ["review_id", "Title", "Review", "Cons_rating"]

## Public description

Title: Ordinal Review Rating Prediction (1–5 stars) from Clothing Product Text

Problem statement
Given the Title and Review text of clothing product reviews, predict the ordinal star rating Cons_rating on a 1–5 scale. Ratings are strongly imbalanced and the textual signal is often subtle, requiring robust modeling of sentiment intensity and domain-specific context.

Data description
- train.csv: Columns [review_id, Title, Review, Cons_rating]. Title and Review are free-form text fields; Cons_rating is an integer in {1,2,3,4,5}.
- test.csv: Columns [review_id, Title, Review] with the same formatting as train.csv but without labels.
- sample_submission.csv: A template showing the expected submission format.

Input details
- Title and Review are the only inputs guaranteed at inference time. Either field may be empty, but never both. Casing and punctuation are preserved.
- Text lengths vary widely (short titles to long reviews). Participants may apply any text processing they deem appropriate (cleaning, tokenization, truncation, long-sequence models, etc.).

Evaluation metric
- Primary metric: Quadratic Weighted Kappa (QWK) on integer ratings 1–5.
- Rationale: QWK respects ordinality, penalizing larger disagreements more heavily than smaller ones. It mitigates issues from class imbalance better than accuracy while rewarding calibrated ordinal predictions.

Submission format
- A single CSV with columns [review_id, Cons_rating].
- review_id must match exactly the IDs provided in test.csv; each ID appears once.
- Cons_rating must be an integer in {1,2,3,4,5} for every row.

Official split
- One official train/test split is provided. Exact duplicate texts (identical Title+Review after whitespace normalization) are grouped to prevent train/test leakage. The split is stratified by Cons_rating to preserve label distribution.

Guidance for participants
- This is an ordinal prediction task. Strong baselines include TF‑IDF + linear models; higher performance can come from pretrained transformers with ordinal-aware heads or calibrated regression.
- Address class imbalance via stratified validation, loss reweighting, or calibration. Consider techniques that respect ordinality (ordinal regression, pairwise ranking, or mapping regression outputs to integer classes).
- Be careful with preprocessing: retain meaningful punctuation and casing; normalize whitespace; handle long sequences and rare tokens.

Notes
- The final files focus on text-only inference to avoid leakage from auxiliary metadata. No additional labels or product attributes are included in train/test files.
