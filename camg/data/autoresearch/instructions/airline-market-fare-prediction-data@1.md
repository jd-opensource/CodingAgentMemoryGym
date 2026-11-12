# OpenMLE-fast task

Task ID: `airline-market-fare-prediction-data@1`

Native metric: `AirlineFarePredictionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (296 bytes)
- `data/sample_submission.csv` (303783 bytes); columns: ["row_id", "Average_Fare"]
- `data/test.csv` (3074639 bytes); columns: ["row_id", "MktCoupons", "OriginCityMarketID", "DestCityMarketID", "OriginAirportID", "DestAirportID", "Carrier", "NonStopMiles", "RoundTrip", "ODPairID", "Pax", "CarrierPax", "Market_share", "Market_HHI", "LCC_Comp", "Multi_Airport", "Circuity", "Slot", "Non_Stop", "MktMilesFlown", "OriginCityMarketID_freq", "DestCityMarketID_freq", "OriginAirportID_freq", "DestAirportID_freq", "Carrier_freq", "ODPairID_freq"]
- `data/train.csv` (12894006 bytes); columns: ["row_id", "MktCoupons", "OriginCityMarketID", "DestCityMarketID", "OriginAirportID", "DestAirportID", "Carrier", "NonStopMiles", "RoundTrip", "ODPairID", "Pax", "CarrierPax", "Average_Fare", "Market_share", "Market_HHI", "LCC_Comp", "Multi_Airport", "Circuity", "Slot", "Non_Stop", "MktMilesFlown", "OriginCityMarketID_freq", "DestCityMarketID_freq", "OriginAirportID_freq", "DestAirportID_freq", "Carrier_freq", "ODPairID_freq"]

## Public description

Airline Market Average Fare Prediction

Files in this directory:
- train.csv: Training data with features, target Average_Fare, and row_id.
- test.csv: Test data with features and row_id (no target).
- sample_submission.csv: Example submission containing row_id and predictions for Average_Fare.
