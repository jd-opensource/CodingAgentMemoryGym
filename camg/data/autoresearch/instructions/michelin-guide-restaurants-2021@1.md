# OpenMLE-fast task

Task ID: `michelin-guide-restaurants-2021@1`

Native metric: `MichelinF1Metrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2869 bytes)
- `data/sample_submission.csv` (111654 bytes); columns: ["id", "Award"]
- `data/test.csv` (719492 bytes); columns: ["id", "Name", "Address", "Location", "Price", "Cuisine", "Longitude", "Latitude", "GreenStar", "FacilitiesAndServices"]
- `data/train.csv` (3132587 bytes); columns: ["id", "Name", "Address", "Location", "Price", "Cuisine", "Longitude", "Latitude", "GreenStar", "FacilitiesAndServices", "Award"]

## Public description

Title: Michelin Distinction Prediction Challenge

Problem statement
Predict the Michelin distinction tier of a restaurant using publicly listed, non-editorial attributes. Given structured, geo, and categorical signals for each restaurant, your task is to classify it into one of five tiers:
- 3 Stars
- 2 Stars
- 1 Star
- Bib Gourmand
- Selected Restaurants

This is a multi-class, imbalanced classification problem that rewards robust feature engineering across heterogeneous signals (categorical, geospatial, list-like attributes, limited text fields) and careful handling of class imbalance.

Files provided
- train.csv: Training set with features and the target column Award.
- test.csv: Test set with the same features as train.csv but without Award.
- sample_submission.csv: A sample submission file showing the required format.

Columns
Each row represents a restaurant. All paths are excluded; values are inline.
- id: Unique restaurant identifier for submission key (string).
- Name: Restaurant name (string).
- Address: Address string (string).
- Location: "City, Country" style location string (string).
- Price: Relative price band represented by € symbols (string, e.g., €, €€, €€€, €€€€).
- Cuisine: Comma-separated cuisines (string).
- Longitude: Longitude in degrees (float).
- Latitude: Latitude in degrees (float).
- GreenStar: 1 if Michelin Green Star, 0 otherwise (integer/binary).
- FacilitiesAndServices: Comma-separated amenities (string).
- Award: Target label present only in train.csv; one of {3 Stars, 2 Stars, 1 Star, Bib Gourmand, Selected Restaurants}.

Notes
- Editorial descriptions are excluded to prevent label leakage.
- Url/Phone/Website are not included as features; the id column replaces Url for uniqueness.
- Expect missing values and noisy category text; robust preprocessing is part of the challenge.

Evaluation
- Primary metric: Macro-averaged F1 score over the 5 classes.
  - For each class, F1 = 2 * precision * recall / (precision + recall), with 0 when a denominator is 0.
  - The final score is the unweighted mean of per-class F1 across the five classes.

Submission format
- A CSV file with exactly two columns, in any order:
  - id
  - Award (predicted label for that id; must be one of the five valid classes listed above)
- It must contain exactly one row for each id in test.csv with no duplicates or extras.

Recommended approaches
- Encode cuisines and facilities (multi-hot, embeddings, target encoding with care).
- Engineer geospatial features (lat/lon, regional bins) and price signals.
- Handle severe class imbalance (class weights, focal loss, resampling, thresholding).
- Tree-based models provide strong baselines; additional gains can come from light text featurization of names/addresses and interaction features.

Final data files
- train.csv
- test.csv
- sample_submission.csv
