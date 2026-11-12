# OpenMLE-fast task

Task ID: `rice-dataset-commeo-and-osmancik@1`

Native metric: `RiceVarietyIdentificationMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2950 bytes)
- `data/sample_submission.csv` (9992 bytes); columns: ["row_id", "Cammeo"]
- `data/test.csv` (128845 bytes); columns: ["row_id", "Area", "Perimeter", "Major_Axis_Length", "Minor_Axis_Length", "Eccentricity", "Convex_Area", "Extent"]
- `data/train.csv` (322149 bytes); columns: ["row_id", "Area", "Perimeter", "Major_Axis_Length", "Minor_Axis_Length", "Eccentricity", "Convex_Area", "Extent", "Class"]

## Public description

Rice Variety Identification from Morphological Features (Cammeo vs Osmancik)

Problem statement
- Task: Predict the rice variety (binary classification: Cammeo vs Osmancik) from 7 morphological descriptors measured on individual grains.
- Context: Efficient post-harvest quality control requires accurate identification of rice varieties. The provided features are precise morphometric measurements derived from microscope images.

Data description
- Each row corresponds to one grain and includes:
  - Area: number of pixels within the grain boundary
  - Perimeter: pixel-distance around the boundary
  - Major_Axis_Length: longest line through the grain
  - Minor_Axis_Length: shortest line through the grain
  - Eccentricity: roundness of the ellipse having the same moments as the grain
  - Convex_Area: pixel count of the grain’s convex hull
  - Extent: ratio of grain area to bounding box area
- Target: Class (Cammeo or Osmancik). Present only in training data.
- Scale: 3,810 samples, all 7 numeric features are used.
- Integrity: Features are numeric and finite; row_id is provided for indexing and submission alignment.

Files provided
- train.csv: row_id, all 7 features, and Class (target).
- test.csv: row_id and all 7 features (no Class).
- sample_submission.csv: example of the required submission format.

Train/test split
- Stratified 70/30 split by Class.
- The test set emphasizes mid-range morphology (by Area and Perimeter) to focus evaluation on overlapping cases and reduce trivial thresholding. Both classes are present in train and test.

Submission format
- A CSV with exactly two columns:
  - row_id: integer identifiers matching those in test.csv.
  - Cammeo: predicted probability (between 0 and 1) that the sample is Cammeo.
- The set of row_id values must match test.csv. Ordering does not matter, duplicates are not allowed.

Evaluation metric
- Primary metric: Log Loss (binary cross-entropy) using the submitted Cammeo probabilities evaluated against the hidden test labels.
- Rationale:
  - Rewards calibrated probabilistic predictions and differentiates strong models where accuracy may saturate.
  - Handles mild class imbalance and overlapping feature distributions fairly and precisely.

Notes and recommendations
- Standardize or robust-scale features; consider log transforms for positively skewed variables (Area, Perimeter, Convex_Area).
- Consider domain-inspired features such as:
  - aspect_ratio = Major_Axis_Length / Minor_Axis_Length
  - solidity = Area / Convex_Area
  - circularity = 4π × Area / Perimeter²
- Use stratified K-fold cross-validation without leakage (fit preprocessing on training folds only). Explore class weights, calibrated models, or threshold tuning to improve Log Loss.
- Classical ML (regularized logistic regression, gradient boosting, random forests) and simple neural networks are suitable. Careful preprocessing and probability calibration are key to top performance.
