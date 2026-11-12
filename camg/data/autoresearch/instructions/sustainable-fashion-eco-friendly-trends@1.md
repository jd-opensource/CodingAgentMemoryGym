# OpenMLE-fast task

Task ID: `sustainable-fashion-eco-friendly-trends@1`

Native metric: `SustainableFashionRatingMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2353 bytes)
- `data/sample_submission.csv` (5943 bytes); columns: ["Id", "Sustainability_Rating"]
- `data/test.csv` (77020 bytes); columns: ["Id", "Country", "Year", "Material_Type", "Eco_Friendly_Manufacturing", "Carbon_Footprint_MT", "Water_Usage_Liters", "Waste_Production_KG", "Recycling_Programs", "Product_Lines", "Average_Price_USD", "Certifications"]
- `data/train.csv` (298607 bytes); columns: ["Country", "Year", "Material_Type", "Eco_Friendly_Manufacturing", "Carbon_Footprint_MT", "Water_Usage_Liters", "Waste_Production_KG", "Recycling_Programs", "Product_Lines", "Average_Price_USD", "Certifications", "Sustainability_Rating"]

## Public description

```
description.txt (49 lines)
sample_submission.csv (1005 lines)
test.csv (1005 lines)
train.csv (3997 lines)```

-> sample_submission.csv has 1004 rows and 2 columns.
Here is some information about the columns:
Id (int64) has range: 0.00 - 1003.00, 0 nan values
Sustainability_Rating (object) has 1 unique values: ['B']

-> test.csv has 1004 rows and 12 columns.
Here is some information about the columns:
Average_Price_USD (float64) has range: 20.33 - 499.94, 0 nan values
Carbon_Footprint_MT (float64) has range: 1.04 - 499.76, 0 nan values
Certifications (object) has 4 unique values: ['B Corp', 'OEKO-TEX', nan, 'GOTS', 'Fair Trade']
Country (object) has 10 unique values. Some example values: ['USA', 'Australia', 'UK', 'Germany']
Eco_Friendly_Manufacturing (object) has 2 unique values: ['No', 'Yes']
Id (int64) has range: 0.00 - 1003.00, 0 nan values
Material_Type (object) has 6 unique values: ['Vegan Leather', 'Bamboo Fabric', 'Tencel', 'Hemp', 'Recycled Polyester', 'Organic Cotton']
Product_Lines (int64) has range: 1.00 - 20.00, 0 nan values
Recycling_Programs (object) has 2 unique values: ['No', 'Yes']
Waste_Production_KG (float64) has range: 1026.38 - 99899.47, 0 nan values
Water_Usage_Liters (float64) has range: 50106.18 - 4995453.48, 0 nan values
Year (int64) has 3 unique values: [2024, 2023, 2022]

-> train.csv has 3996 rows and 12 columns.
Here is some information about the columns:
Average_Price_USD (float64) has range: 20.02 - 499.85, 0 nan values
Carbon_Footprint_MT (float64) has range: 1.32 - 499.93, 0 nan values
Certifications (object) has 4 unique values: ['GOTS', 'Fair Trade', 'B Corp', nan, 'OEKO-TEX']
Country (object) has 10 unique values. Some example values: ['Italy', 'China', 'Germany', 'France']
Eco_Friendly_Manufacturing (object) has 2 unique values: ['No', 'Yes']
Material_Type (object) has 6 unique values: ['Tencel', 'Vegan Leather', 'Bamboo Fabric', 'Recycled Polyester', 'Hemp', 'Organic Cotton']
Product_Lines (int64) has range: 1.00 - 20.00, 0 nan values
Recycling_Programs (object) has 2 unique values: ['No', 'Yes']
Sustainability_Rating (object) has 4 unique values: ['D', 'B', 'A', 'C']
Waste_Production_KG (float64) has range: 1072.89 - 99947.85, 0 nan values
Water_Usage_Liters (float64) has range: 51411.93 - 4999596.61, 0 nan values
Year (int64) has range: 2010.00 - 2021.00, 0 nan values
