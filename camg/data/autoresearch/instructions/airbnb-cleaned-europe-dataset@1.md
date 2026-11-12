# OpenMLE-fast task

Task ID: `airbnb-cleaned-europe-dataset@1`

Native metric: `AirbnbPriceRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3470 bytes)
- `data/sample_submission.csv` (202133 bytes); columns: ["Id", "Price"]
- `data/test.csv` (1433664 bytes); columns: ["Id", "City", "Day", "Room Type", "Shared Room", "Private Room", "Person Capacity", "Superhost", "Multiple Rooms", "Business", "Cleanliness Rating", "Guest Satisfaction", "Bedrooms", "City Center (km)", "Metro Distance (km)", "Attraction Index", "Normalised Attraction Index", "Restraunt Index", "Normalised Restraunt Index"]
- `data/train.csv` (6348442 bytes); columns: ["Id", "City", "Price", "Day", "Room Type", "Shared Room", "Private Room", "Person Capacity", "Superhost", "Multiple Rooms", "Business", "Cleanliness Rating", "Guest Satisfaction", "Bedrooms", "City Center (km)", "Metro Distance (km)", "Attraction Index", "Normalised Attraction Index", "Restraunt Index", "Normalised Restraunt Index"]

## Public description

Title: European Airbnb Price Prediction Challenge

Problem statement
Pricing short-term rentals depends on location, accessibility, property attributes, host characteristics, and local demand. You are given a multi-city tabular dataset of Airbnb listings across nine European cities. Your task is to predict the nightly Price of a listing from its attributes.

Files provided
- train.csv: Listing Id, all features, and the target Price.
- test.csv: Listing Id and all features (without Price).
- sample_submission.csv: Example submission file with columns Id and Price.

Target
- Price (continuous, non-negative): nightly price in the local currency (as provided in the source data).

Features
All columns except Price are features. Columns include a mix of categorical, boolean, and numeric variables:
- Categorical:
  - City: name of the city (Rome, Paris, Lisbon, Athens, Budapest, Vienna, Barcelona, Berlin, Amsterdam)
  - Day: Weekday or Weekend
  - Room Type: Entire home/apt, Private room, Shared room
- Boolean (0/1 after preprocessing):
  - Shared Room: listing is a shared room
  - Private Room: listing is a private room
  - Superhost: host is a Superhost
  - Multiple Rooms: host offers multiple rooms
  - Business: business-ready listing
- Numeric:
  - Person Capacity: maximum number of guests
  - Cleanliness Rating: cleanliness score (typically 1–10)
  - Guest Satisfaction: aggregated guest ratings
  - Bedrooms: number of bedrooms
  - City Center (km): distance to city center
  - Metro Distance (km): distance to nearest metro/subway
  - Attraction Index: density/score of nearby attractions
  - Normalised Attraction Index: scaled attraction index
  - Restraunt Index: density/score of nearby restaurants
  - Normalised Restraunt Index: scaled restaurant index

Evaluation
- Metric: Root Mean Squared Logarithmic Error (RMSLE)
  - RMSLE is computed as the root mean squared error between log1p(y_true) and log1p(y_pred), where y_true and y_pred are the true and predicted Price values.
  - Submissions must contain non-negative Price predictions; negative values are invalid and will be rejected during format validation.

Submission format
- A CSV file with two columns and header: Id,Price
- Id must match exactly the Id values in test.csv, with each Id appearing once.
- Price must be a numeric, non-negative value.

Data split and identifiers
- The official split is 80/20 (train/test), stratified by the combination of City and Room Type to preserve distribution across cities and listing types.
- Each row is assigned a deterministic integer Id. Ids are unique across the combined dataset and appear in both train.csv and test.csv for their respective rows.

Modeling tips (informational)
- The price distribution is heavy-tailed; training on log1p(Price) often improves performance. Convert predictions back with expm1 for submission.
- Tree-based gradient boosting models (LightGBM, XGBoost, CatBoost) typically perform well. Linear models with appropriate encoding/regularization can be competitive.
- Categorical encoding (one-hot or native categorical support) is required for categorical features. Booleans are provided as 0/1.
- Consider interactions such as capacity × bedrooms × distance to center and nonlinear effects of attraction indices.

Final deliverables required from participants
- A single CSV file named arbitrarily, with header and exactly the two columns Id,Price as specified above.

Good luck and have fun modeling!
