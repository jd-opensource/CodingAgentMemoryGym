# OpenMLE-fast task

Task ID: `investigating-housing-prices-in-lagos-nigeria@1`

Native metric: `LagosHousingPriceMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3850 bytes)
- `data/sample_submission.csv` (99823 bytes); columns: ["ListingID", "Price"]
- `data/test.csv` (608886 bytes); columns: ["ListingID", "ContractType", "Property_name", "Address", "Neighboorhood", "Neighborhood_raw", "Neighborhood_std", "PropertyType", "Bedrooms", "IsFurnished", "HasEstateKeyword"]
- `data/train.csv` (2547993 bytes); columns: ["ListingID", "ContractType", "Price", "Property_name", "Address", "Neighboorhood", "Neighborhood_raw", "Neighborhood_std", "PropertyType", "Bedrooms", "IsFurnished", "HasEstateKeyword"]

## Public description

Lagos Listing Price Forecast (Rent + Sale)

Problem statement
- Predict the listing price (numeric) for Lagos properties using noisy free-text descriptions and location information. Each row is a listing with textual features (Property_name and Address), a contract type label (rent or sale), and a neighborhood name. Prices span several orders of magnitude across diverse property types and neighborhoods.
- Your task is to build models that robustly estimate prices across both rental and sales markets.

Files provided
- train.csv: training data with target column Price and the following features per listing:
  - ListingID: unique identifier for each listing.
  - ContractType: "rent" or "sale".
  - Property_name: free-text title/description of the listing.
  - Address: free-text location text.
  - Neighboorhood: original neighborhood string as provided.
  - Neighborhood_raw: a copy of the original neighborhood string.
  - Neighborhood_std: lightly standardized neighborhood string (case and punctuation normalization).
  - PropertyType: simple type parsed from Property_name (e.g., Flat/Apartment, Duplex, Land, Office, Shop, Bungalow, House, Mini Flat).
  - Bedrooms: parsed numeric bedroom count when detectable; NaN otherwise.
  - IsFurnished: 1 if text indicates furnished/serviced; otherwise 0.
  - HasEstateKeyword: 1 if the word "estate" appears in Property_name; otherwise 0.
- test.csv: same columns as train.csv except does not include Price.
- sample_submission.csv: a file showing the required submission format with plausible random predictions.

Target
- Price: a positive numeric value in local currency units, reflecting either rental asking price (typically per year) or sale price.

Evaluation
- Root Mean Squared Logarithmic Error (RMSLE) on Price is used to evaluate submissions:
  - We compute RMSLE = sqrt(mean((log1p(y_true) - log1p(y_pred))^2)).
  - RMSLE is robust to heavy tails and focuses on relative error, which is appropriate for prices that vary by orders of magnitude.
  - Predictions must be non-negative real numbers.

Rules and notes
- Use any combination of text and tabular modeling. Strong baselines include gradient-boosted trees with TF-IDF or target-encoded features, regularized linear models on text features, and deep text+tabular hybrids.
- Feature engineering ideas:
  - Tokenize and vectorize Property_name and Address (e.g., word/character n-grams).
  - Use Neighborhood_std and ContractType as categorical signals.
  - Leverage parsed features (PropertyType, Bedrooms, IsFurnished, HasEstateKeyword).
  - Create additional robust features (length of text, keyword flags, neighborhood buckets).
- Data cleaning tips:
  - Text is noisy and inconsistent; normalize casing and whitespace, but avoid aggressive relabeling.
  - Prices are positive and heavy-tailed; apply log-transform for modeling.
- The dataset combines rental and sale listings; ensure your model handles scale differences (ContractType is provided).

Submission format
- A single CSV with two columns in this order:
  - ListingID
  - Price
- ListingID values must match those in test.csv exactly and be unique. Price values must be non-negative real numbers.

Data split
- A single train/test split is provided. Listings are grouped by internal identifiers to avoid leakage, and the split is stratified by contract type and neighborhood frequency buckets to ensure diverse coverage.

Tips for strong performance
- Use log1p(Price) as the modeling target and invert the transform for predictions.
- Combine text (TF-IDF) with categorical/tabular features in a single model or a stacking/ensemble.
- Pay attention to rare neighborhoods and property types; regularization and robust encodings help.
- Validate locally by making a further split of the training data (e.g., time-independent stratified split) and tracking RMSLE.
