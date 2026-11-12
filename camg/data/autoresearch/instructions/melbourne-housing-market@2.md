# OpenMLE-fast task

Task ID: `melbourne-housing-market@2`

Native metric: `MelbourneAuctionUnsoldMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (4001 bytes)
- `data/sample_submission.csv` (303933 bytes); columns: ["Id", "Unsold_Prob"]
- `data/test.csv` (2118186 bytes); columns: ["Id", "Suburb", "Rooms", "Type", "SellerG", "Date", "Distance", "Postcode", "Regionname", "Propertycount", "Bedroom2", "Bathroom", "Car", "Landsize", "BuildingArea", "YearBuilt", "CouncilArea", "Lattitude", "Longtitude"]
- `data/train.csv` (5576708 bytes); columns: ["Id", "Suburb", "Rooms", "Type", "SellerG", "Date", "Distance", "Postcode", "Regionname", "Propertycount", "Bedroom2", "Bathroom", "Car", "Landsize", "BuildingArea", "YearBuilt", "CouncilArea", "Lattitude", "Longtitude", "Unsold"]

## Public description

Melbourne Auction Outcome Prediction

Background
Melbourne’s property market features weekly auctions where homes may sell or fail to sell (passed in, vendor bid, withdrawn, etc.). Understanding which listings are at risk of not selling helps agents and sellers plan strategies, set expectations, and allocate resources. This competition focuses on predicting the probability that a property will be unsold at auction using tabular, geospatial, and temporal information.

Problem Statement
Given listing characteristics, location, and timing, predict the probability that a property will be unsold at auction. The target is a binary label derived from the auction method codes, but this target-defining field is excluded from the provided features to prevent leakage. Participants should build robust ML pipelines that handle missing values, high-cardinality categoricals, geospatial signals, and temporal distribution shifts.

Files Provided
- train.csv: Training data with features and the binary target column Unsold (1 = unsold outcome, 0 = sold outcome).
- test.csv: Test data with the same features as train.csv but without the Unsold column.
- sample_submission.csv: Example submission file with the correct format.

Data Description
Features are tabular, categorical, numerical, geospatial, and temporal. The typical columns include:
- Id: Unique integer identifier for each listing.
- Suburb: Suburb name.
- Rooms: Number of rooms.
- Type: Property type (e.g., h, u, t).
- SellerG: Real estate agent/agency.
- Date: Date of the auction/listing.
- Distance: Distance from Melbourne CBD in kilometers.
- Postcode: Postal code.
- Regionname: General region classification.
- Propertycount: Number of properties in the suburb.
- Bedroom2: Scraped number of bedrooms (alternate source).
- Bathroom: Number of bathrooms.
- Car: Number of car spots.
- Landsize: Land size (m²).
- BuildingArea: Building size (m²).
- YearBuilt: Year the home was built.
- CouncilArea: Governing council for the area.
- Lattitude, Longtitude: Geospatial coordinates.

Target
- Unsold: Binary indicator (1 = unsold outcome, 0 = sold outcome). This is derived from auction method codes (sold = {S, SP, SA, SN, PN, SS}; unsold = {PI, VB, NB, W}). The auction method itself is not included among features to avoid leakage.

Train/Test Split
- Time-aware split: Training examples are from dates up to and including 2017-12-31; Test examples are from dates on or after 2018-01-01. Duplicate properties observed multiple times are deduplicated by keeping the earliest observation per property.

Evaluation Metric
- Leaderboard metric: ROC-AUC (area under the receiver operating characteristic curve) for the Unsold class (positive = 1). This metric is threshold-independent and robust to class imbalance and base-rate shifts across time.

Submission Format
Submit a CSV file with the following columns:
- Id: Must match the Ids in test.csv.
- Unsold_Prob: A floating-point probability (0 to 1) indicating the predicted likelihood that the listing is unsold.

Example (sample_submission.csv):
Id,Unsold_Prob
1000001,0.42
1000002,0.18
...

Guidelines and Considerations
- Do not attempt to recover or use the auction method codes; they define the target and are deliberately excluded.
- Price is excluded to prevent target-adjacent leakage; focus on pre-auction characteristics.
- Handle missingness systematically (imputation + indicators), especially for Landsize, BuildingArea, YearBuilt, Bathroom, and Car.
- Engineer meaningful features: temporal (week, month, quarter), geospatial (distance to CBD, region encodings), interactions (Type × Regionname, etc.), and encodings for high-cardinality categoricals (SellerG, CouncilArea, Postcode).
- Use robust modeling techniques (e.g., gradient-boosted trees, calibrated classifiers) and pay attention to class imbalance.

Goal
Build a model that generalizes across time and regions, producing well-calibrated unsold probabilities for the listings in test.csv. Good luck!
