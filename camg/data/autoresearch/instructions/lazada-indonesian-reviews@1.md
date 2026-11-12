# OpenMLE-fast task

Task ID: `lazada-indonesian-reviews@1`

Native metric: `IndonesianReviewRatingMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1211 bytes)
- `data/sample_submission.csv` (114605 bytes); columns: ["review_id", "rating"]
- `data/test.csv` (1470046 bytes); columns: ["review_id", "text", "category", "clientType", "boughtFlag", "likeCount", "upVotes", "downVotes", "helpful", "brandName", "price", "averageRating", "totalReviews"]
- `data/train.csv` (5938380 bytes); columns: ["review_id", "text", "category", "clientType", "boughtFlag", "likeCount", "upVotes", "downVotes", "helpful", "brandName", "price", "averageRating", "totalReviews", "rating"]

## Public description

Competition: Indonesian E-commerce Review Rating Prediction (Ordinal)

Problem statement:
Predict the final 1–5 star rating of Lazada Indonesia product reviews from Indonesian text and item metadata. Each example consists of a short review title and/or content, plus contextual features about the product and review.

Public data description:
- Train set (train.csv): rows with known rating labels. Columns include: review_id, text, category, clientType, boughtFlag, likeCount, upVotes, downVotes, helpful, brandName, price, averageRating, totalReviews, rating.
- Test set (test.csv): same columns as train.csv except rating is withheld. The order of rows and review_id values define the evaluation alignment.
- Sample submission (sample_submission.csv): example submission file containing review_id and a valid rating for each test row.

Evaluation metric:
- Primary metric: Quadratic Weighted Kappa (QWK) between true ratings and submitted predictions.
- Submissions must be a CSV with two columns: review_id and rating. Ratings outside [1,5] will be clipped; non-integers will be rounded to the nearest integer.

Files in public/ directory:
- train.csv
- test.csv
- sample_submission.csv
- description.txt
