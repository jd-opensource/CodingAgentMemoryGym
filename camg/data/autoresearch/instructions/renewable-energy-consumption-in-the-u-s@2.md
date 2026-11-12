# OpenMLE-fast task

Task ID: `renewable-energy-consumption-in-the-u-s@2`

Native metric: `RenewableEnergyForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2203 bytes)
- `data/sample_submission.csv` (2478 bytes); columns: ["id", "forecast"]
- `data/test.csv` (2997 bytes); columns: ["id", "Year", "Month", "Series"]
- `data/train.csv` (270558 bytes); columns: ["Year", "Month", "Sector", "Hydroelectric Power", "Geothermal Energy", "Solar Energy", "Wind Energy", "Wood Energy", "Waste Energy", "Fuel Ethanol, Excluding Denaturant", "Biomass Losses and Co-products", "Biomass Energy", "Total Renewable Energy", "Renewable Diesel Fuel", "Other Biofuels", "Conventional Hydroelectric Power", "Biodiesel"]

## Public description

```
description.txt (45 lines)
sample_submission.csv (53 lines)
test.csv (53 lines)
train.csv (3001 lines)```

-> sample_submission.csv has 52 rows and 2 columns.
Here is some information about the columns:
forecast (float64) has range: 0.43 - 46.31, 0 nan values
id (object) has 52 unique values. Some example values: ['Biodiesel_2023-01', 'Fuel Ethanol, Excluding Denaturant_2023-01', 'Other Biofuels_2023-01', 'Renewable Diesel Fuel_2023-01']

-> test.csv has 52 rows and 4 columns.
Here is some information about the columns:
Month (int64) has range: 1.00 - 12.00, 0 nan values
Series (object) has 4 unique values: ['Biodiesel', 'Fuel Ethanol, Excluding Denaturant', 'Other Biofuels', 'Renewable Diesel Fuel']
Year (int64) has 2 unique values: [2023, 2024]
id (object) has 52 unique values. Some example values: ['Biodiesel_2023-01', 'Fuel Ethanol, Excluding Denaturant_2023-01', 'Other Biofuels_2023-01', 'Renewable Diesel Fuel_2023-01']

-> train.csv has 3000 rows and 17 columns.
Here is some information about the columns:
Biodiesel (float64) has range: 0.00 - 27.87, 0 nan values
Biomass Energy (float64) has range: 0.00 - 233.20, 0 nan values
Biomass Losses and Co-products (float64) has range: 0.00 - 75.37, 0 nan values
Conventional Hydroelectric Power (float64) has range: 0.00 - 117.45, 0 nan values
Fuel Ethanol, Excluding Denaturant (float64) has range: 0.00 - 104.42, 0 nan values
Geothermal Energy (float64) has range: 0.00 - 5.95, 0 nan values
Hydroelectric Power (float64) has range: -0.00 - 2.05, 0 nan values
Month (int64) has range: 1.00 - 12.00, 0 nan values
Other Biofuels (float64) has range: 0.00 - 3.33, 0 nan values
Renewable Diesel Fuel (float64) has range: 0.00 - 22.06, 0 nan values
Sector (object) has 5 unique values: ['Commercial', 'Electric Power', 'Industrial', 'Residential', 'Transportation']
Solar Energy (float64) has range: 0.00 - 54.41, 0 nan values
Total Renewable Energy (float64) has range: 0.00 - 308.18, 0 nan values
Waste Energy (float64) has range: 0.00 - 32.88, 0 nan values
Wind Energy (float64) has range: 0.00 - 157.41, 0 nan values
Wood Energy (float64) has range: 0.00 - 183.63, 0 nan values
Year (int64) has range: 1973.00 - 2022.00, 0 nan values
