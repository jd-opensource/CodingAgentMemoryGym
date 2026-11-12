# OpenMLE-fast task

Task ID: `michelin-guide-restaurants-2021@2`

Native metric: `MichelinGreenStarMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3246 bytes)
- `data/sample_submission.csv` (106202 bytes); columns: ["Id", "GreenStar"]
- `data/test.csv` (804714 bytes); columns: ["Id", "Name", "Address", "Location", "Price", "Cuisine", "Longitude", "Latitude", "WebsiteUrl", "FacilitiesAndServices"]
- `data/train.csv` (3245135 bytes); columns: ["Id", "Name", "Address", "Location", "Price", "Cuisine", "Longitude", "Latitude", "WebsiteUrl", "FacilitiesAndServices", "GreenStar"]

## Public description

Competition: Michelin Green Star Prediction

Problem statement
Predict whether a restaurant holds a Michelin Green Star using public, non-leaky tabular attributes. This is a binary classification task: GreenStar ∈ {0,1}. The class is highly imbalanced (positives are a small minority), so probability calibration and ranking quality matter.

Data description
Each row represents one restaurant curated from the Michelin Guide. The data has been cleaned (rows with missing labels removed) and de-duplicated. A pseudonymous Id is provided per row.

Files
- train.csv: training data with labels
- test.csv: test data without labels
- sample_submission.csv: sample submission format with random predictions

Columns
- Id: unique identifier for a restaurant (string)
- Name: restaurant name (string)
- Address: street address (string)
- Location: city and country (string)
- Price: price band as symbols (string)
- Cuisine: primary and secondary cuisines, comma-separated (string)
- Longitude: longitude in WGS84 (float)
- Latitude: latitude in WGS84 (float)
- WebsiteUrl: restaurant website URL where available (string)
- FacilitiesAndServices: comma-separated list of facilities/services (string)
- GreenStar: binary target indicating Michelin Green Star (only in train.csv)

Notes on feature availability
- To ensure a fair and challenging problem, the Award and Description fields are not included, as they correlate strongly with the target or may contain direct editorial hints. The Id is pseudonymous and does not expose the source URL.

Evaluation
- Metric: Average Precision (area under the Precision–Recall curve for the positive class).
- Submission file: a CSV with two columns and header: Id,GreenStar. The GreenStar column should contain a score in [0,1] representing the predicted probability of GreenStar = 1.
- Scoring details:
  1) Submissions are aligned to the official test set by Id.
  2) Scores are clipped to [0,1] if necessary and robustly handled if NaN/Inf appear.
  3) Average Precision is computed by ranking rows by descending predicted score and averaging precision at the ranks of the positive instances.

Submission format
- Required columns (exact names): Id,GreenStar
- Number of rows must equal test.csv.
- All Id values must be present exactly once and match those in test.csv.
- GreenStar values must be numeric; higher means more likely to be Green Star.

Train/test split
- The official split is a single, deterministic, stratified split by GreenStar (e.g., ~80/20). Both train and test contain positives and negatives. Participants may perform their own cross-validation on train.csv.

Suggested modeling directions
- Address severe class imbalance (e.g., class weighting, focal loss, calibrated probabilities, threshold tuning).
- Engineer geospatial features (e.g., geohash/binning/region indicators), categorical encodings for cuisines/facilities/price, and weak signals from Name/Address tokens and website TLDs.
- Handle rare categories, normalize Unicode text, and consider interaction features between geography, price, and cuisine.

Goal
Build a robust classifier that generalizes across countries and cuisines to identify sustainability-leading restaurants based on publicly available attributes.
