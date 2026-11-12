# OpenMLE-fast task

Task ID: `ebay-laptops-and-netbooks-sales@1`

Native metric: `EbayLaptopPriceMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (4679 bytes)
- `data/sample_submission.csv` (8071 bytes); columns: ["id", "Price"]
- `data/supplemental_unclean.csv` (4139874 bytes); columns: ["Brand", "Price", "Rating", "Ratings Count", "Condition", "Seller Note", "Processor", "Screen Size", "Manufacturer Color", "Color", "Ram Size", "SSD Capacity", "GPU", "Processor Speed", "Type", "Release Year", "Maximum Resolution", "Model", "OS", "Features", "Hard Drive Capacity", "Country Region Of Manufacture", "Storage Type"]
- `data/test.csv` (390165 bytes); columns: ["id", "Brand", "Currency", "Color", "Features", "Condition", "Condition Description", "Seller Note", "GPU", "Processor", "Processor Speed", "Processor Speed Unit", "Type", "Width of the Display", "Height of the Display", "OS", "Storage Type", "Hard Drive Capacity", "Hard Drive Capacity Unit", "SSD Capacity", "SSD Capacity Unit", "Screen Size (inch)", "Ram Size", "Ram Size Unit"]
- `data/train.csv` (1669252 bytes); columns: ["id", "Brand", "Price", "Currency", "Color", "Features", "Condition", "Condition Description", "Seller Note", "GPU", "Processor", "Processor Speed", "Processor Speed Unit", "Type", "Width of the Display", "Height of the Display", "OS", "Storage Type", "Hard Drive Capacity", "Hard Drive Capacity Unit", "SSD Capacity", "SSD Capacity Unit", "Screen Size (inch)", "Ram Size", "Ram Size Unit"]

## Public description

Ebay Laptop Price Prediction (Tabular + Text)

Problem statement
Given an eBay laptop/netbook listing with structured specifications and free-text notes, predict its listing price in USD. Prices vary widely with brand, condition, specs, and presentation. Your task is to build a robust model that maps the available attributes to the numeric Price.

Files provided
- train.csv: Labeled training data containing one row per listing with an id column, all features, and the target column Price (USD).
- test.csv: Unlabeled test data with the same feature columns and id, but without Price.
- sample_submission.csv: Example submission file with id and a placeholder Price for each test row.
- supplemental_unclean.csv: A supplemental corpus containing richer and sometimes noisier attributes (e.g., Model, Release Year, Ratings, Manufacturer Color, Maximum Resolution, and longer text). No labels should be taken from this file.

Data description (core columns in train.csv/test.csv)
- id: Unique identifier for each listing (string/integer).
- Brand: Manufacturer (e.g., Dell, HP, Lenovo, Acer, etc.).
- Price: Target (USD). Present only in train.csv.
- Currency: Currency symbol. Filtered to USD in the provided split.
- Color: Color string.
- Features: Comma-separated feature tags (e.g., Bluetooth, Touchscreen, Webcam...).
- Condition: Condition category (e.g., New, Used, Refurbished variants).
- Condition Description: Free text describing condition. Currency-like strings are redacted to prevent leakage.
- Seller Note: Free text from the seller. Currency-like strings are redacted to prevent leakage.
- GPU: GPU text (e.g., Intel UHD 620, NVIDIA, AMD...).
- Processor: CPU text (e.g., Intel Core i5 8th generation).
- Processor Speed (+ Unit): Numeric plus unit (GHz where available).
- Type: Notebook/Laptop, 2-in-1, etc.
- Width of the Display, Height of the Display: Resolution integers.
- OS: Operating system (Windows, Chrome OS, etc.).
- Storage Type: HDD/SSD/eMMC/Hybrid.
- Hard Drive Capacity (+ Unit): HDD capacity and unit.
- SSD Capacity (+ Unit): SSD capacity and unit.
- Screen Size (inch): Diagonal screen size (float).
- Ram Size (+ Unit): RAM capacity and unit.

Supplemental file (supplemental_unclean.csv)
The supplemental file includes additional, sometimes richer attributes that are not fully normalized in the main files, for example:
- Model (string), Release Year (numeric), Rating and Ratings Count, Manufacturer Color, Maximum Resolution (string), Country/Region of Manufacture, longer Seller Notes, and other details. You may parse, standardize, and join these to train/test to improve your features. Do not use any price-like fields from the supplemental file as labels.

Train/test split policy
- The train/test split is deterministic and aims to reduce near-duplicate leakage by grouping listings that likely correspond to the same underlying model/configuration (based on brand, resolution, screen size, and processor family when available). Entire groups are placed wholly in either train or test where possible. Rows without a reliable group are split deterministically at random.

Target and evaluation
- Target: Price (USD), a positive real number.
- Metric: Root Mean Squared Logarithmic Error (RMSLE) between your predictions and the ground truth.
    RMSLE = sqrt( mean( (log1p(y_pred_clipped) - log1p(y_true))^2 ) ),
    where y_pred_clipped = max(y_pred, 1e-9). This emphasizes relative error and is robust to price outliers.
- Submission format: A CSV with two columns and a header: id,Price. The id must match the ids from test.csv and Price must be a valid positive number. No extra columns.

Notes and guidance
- Use both tabular and text features. Effective solutions commonly include:
  - Standardizing units (e.g., map TB→GB; parse Processor Speed to GHz),
  - Extracting specs from text (e.g., GPU vendor, CPU family/generation),
  - Engineering resolution features (pixels, aspect ratio), storage flags (has_hdd/has_ssd/has_emmc), and combined capacities,
  - Tokenizing multi-valued Features into boolean indicators,
  - Leveraging free-text fields via TF-IDF or other text encoders after cleaning boilerplate and currency-like strings.
- The supplemental file can be used to enrich feature engineering, e.g., to infer model families, release years, or typical configurations. It is not required to train a model.
- All files are provided ready to use; you do not need to reference original raw filenames.

Baseline expectations
- Simple baselines (one-hot/tabular encoders + TF-IDF + linear models/GBDTs) should achieve reasonable RMSLE. More advanced preprocessing and multimodal fusion can yield stronger performance.
