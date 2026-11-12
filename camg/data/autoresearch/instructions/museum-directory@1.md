# OpenMLE-fast task

Task ID: `museum-directory@1`

Native metric: `MuseumRevenuePredictionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3079 bytes)
- `data/sample_submission.csv` (106748 bytes); columns: ["Id", "Revenue"]
- `data/test.csv` (881919 bytes); columns: ["Id", "Museum Name", "Legal Name", "Alternate Name", "Museum Type", "Institution Name", "Street Address (Administrative Location)", "City (Administrative Location)", "State (Administrative Location)", "Zip Code (Administrative Location)", "Street Address (Physical Location)", "City (Physical Location)", "State (Physical Location)", "Zip Code (Physical Location)", "Phone Number", "Latitude", "Longitude", "Locale Code (NCES)", "County Code (FIPS)", "State Code (FIPS)", "Region Code (AAM)", "Tax Period"]
- `data/train.csv` (3661139 bytes); columns: ["Id", "Museum Name", "Legal Name", "Alternate Name", "Museum Type", "Institution Name", "Street Address (Administrative Location)", "City (Administrative Location)", "State (Administrative Location)", "Zip Code (Administrative Location)", "Street Address (Physical Location)", "City (Physical Location)", "State (Physical Location)", "Zip Code (Physical Location)", "Phone Number", "Latitude", "Longitude", "Locale Code (NCES)", "County Code (FIPS)", "State Code (FIPS)", "Region Code (AAM)", "Tax Period", "Revenue"]

## Public description

Museum Revenue Prediction Challenge

Problem statement
Participants are tasked with building a model that predicts the annual revenue of U.S. museums and related organizations from their descriptive and location metadata. The data include organization names, museum type, administrative and physical addresses, phone numbers, geocoordinates, and other categorical codes. The target variable is Revenue (USD), which is heavy‑tailed with many small organizations and a long high‑revenue tail.

Data description
- Training data (train.csv): Each row corresponds to one organization instance with features and the target column Revenue.
- Test data (test.csv): Same features as train.csv but without the target column.
- Sample submission (sample_submission.csv): Example file showing the required submission format with column names Id and Revenue.

Features come from the original museum directory and include text fields (e.g., Museum Name, Legal Name, Alternate Name, address components), categorical codes (e.g., Museum Type, Locale Code (NCES), County Code (FIPS), State Code (FIPS), Region Code (AAM)), geospatial and numeric fields (Latitude, Longitude), and time indicators (Tax Period). To avoid leakage and trivial identifiers, Income, Employer ID Number, and Museum ID are not included in train/test files. The target column Revenue appears only in train.csv.

Train/test split protocol
- Only rows with valid numeric Revenue are used for training and testing.
- The split is group‑aware by Employer ID Number (EIN): all rows for a given EIN appear exclusively in either train or test to prevent leakage from duplicate or near‑duplicate entries.
- The split ratio is approximately 80%/20% (by EIN groups), with deterministic behavior for reproducibility. Rows with missing EINs are treated as their own groups.

Submission format
- File must contain exactly two columns with headers: Id and Revenue.
- Id must match the Id values provided in test.csv exactly (no missing or duplicate Ids).
- Revenue predictions must be finite, real, and non‑negative numbers.

Evaluation metric
- Root Mean Squared Logarithmic Error (RMSLE) between predictions and ground‑truth revenues:
  RMSLE = sqrt( mean( (log1p(y_pred) − log1p(y_true))^2 ) )
- Rationale: Revenue is extremely skewed; RMSLE emphasizes relative error, handles zeros via log1p, and reduces domination by extreme outliers while remaining sensitive across the entire scale.

What makes this challenge interesting
- Multi‑modal feature engineering: combine text (names and addresses), categorical codes (museum type, locale, FIPS), geospatial features (lat/long), and time (tax period).
- Real‑world noise: duplicates, missing values, and outdated entries.
- Strong yet non‑trivial signals: different museum types, regions, and organizational cues correlate with revenue, but modeling requires careful preprocessing and robust estimation.

Files provided
- train.csv
- test.csv
- sample_submission.csv

Good luck and have fun building robust, fair models for this challenging tabular regression task.
