# OpenMLE-fast task

Task ID: `flight-delay-dataset-20182022@2`

Native metric: `FlightDelayRegressionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2618 bytes)
- `data/sample_submission.csv` (184749 bytes); columns: ["id", "ArrDelay"]
- `data/test.csv` (796976 bytes); columns: ["id", "Year", "Quarter", "Month", "DayofMonth", "DayOfWeek", "FlightDate", "Marketing_Airline_Network", "Operating_Airline", "IATA_Code_Marketing_Airline", "IATA_Code_Operating_Airline", "Flight_Number_Marketing_Airline", "Flight_Number_Operating_Airline", "Origin", "OriginAirportID", "OriginCityMarketID", "OriginState", "Dest", "DestAirportID", "DestCityMarketID", "DestState", "Distance", "DistanceGroup", "CRSElapsedTime", "CRSDepTime", "CRSArrTime", "DepTimeBlk", "ArrTimeBlk"]
- `data/train.csv` (3295093 bytes); columns: ["id", "Year", "Quarter", "Month", "DayofMonth", "DayOfWeek", "FlightDate", "Marketing_Airline_Network", "Operating_Airline", "IATA_Code_Marketing_Airline", "IATA_Code_Operating_Airline", "Flight_Number_Marketing_Airline", "Flight_Number_Operating_Airline", "Origin", "OriginAirportID", "OriginCityMarketID", "OriginState", "Dest", "DestAirportID", "DestCityMarketID", "DestState", "Distance", "DistanceGroup", "CRSElapsedTime", "CRSDepTime", "CRSArrTime", "DepTimeBlk", "ArrTimeBlk", "ArrDelay"]

## Public description

Flight Arrival Delay Regression (2018–2022)

Problem
Predict the realized arrival delay in minutes for each completed (non‑cancelled, non‑diverted) U.S. domestic flight using only information available before departure. The target ArrDelay is a continuous value (negative = early arrival, positive = late arrival).

Files provided
- train.csv: Training data with features and the target ArrDelay.
- test.csv: Test data with the same features and an id for each flight. The target is hidden.
- sample_submission.csv: Example submission file containing id and a placeholder ArrDelay prediction.

Target
- ArrDelay: Realized arrival delay in minutes (can be negative for early arrivals). Rows include only completed flights; cancelled or diverted flights are excluded.

Key columns
- id: Unique identifier for each flight built from schedule information: FlightDate + "_" + Operating_Airline + "_" + Flight_Number_Operating_Airline + "_" + Origin + "_" + Dest + "_" + CRSDepTime.
- Pre‑departure features (subset of schedule/identifier fields that are available before takeoff):
  - Year, Quarter, Month, DayofMonth, DayOfWeek, FlightDate
  - Marketing_Airline_Network, Operating_Airline, IATA_Code_Marketing_Airline, IATA_Code_Operating_Airline
  - Flight_Number_Marketing_Airline, Flight_Number_Operating_Airline
  - Origin, OriginAirportID, OriginCityMarketID, OriginState
  - Dest, DestAirportID, DestCityMarketID, DestState
  - Distance, DistanceGroup, CRSElapsedTime, CRSDepTime, CRSArrTime, DepTimeBlk, ArrTimeBlk

Important: Only pre‑departure information is included. Realized operational timings and delay breakdowns are excluded to avoid label leakage.

Train/test split
- Train period: 2018-01-01 through 2021-12-31 (inclusive)
- Test period: 2022-01-01 through 2022-07-31 (inclusive)
The split is chronological to reflect real-world deployment and distribution shift.

Evaluation
- Metric: Mean Absolute Error (MAE) in minutes between your prediction and the true ArrDelay on the test set.
- Submission format: A CSV file with two columns and a header:
  - id
  - ArrDelay
The id values must match those in test.csv; order does not matter. Predictions must be finite numeric values.

Notes and tips
- The target has heavy tails, seasonality, airline/route heterogeneity, and non‑stationarity due to COVID-era disruptions. Robust models and careful feature engineering are encouraged.
- Feature ideas include time-of-day encodings, route/airline identifiers, and historical aggregates computed only from training years.
- Early arrivals are common; models should handle negative values naturally.
