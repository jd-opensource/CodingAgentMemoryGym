# OpenMLE-fast task

Task ID: `real-estate-goldmine-dubai-uae-rental-market@1`

Native metric: `DubaiRentEstimationMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3157 bytes)
- `data/sample_submission.csv` (357275 bytes); columns: ["Id", "Rent"]
- `data/test.csv` (2119975 bytes); columns: ["Id", "Address", "Beds", "Baths", "Type", "Area_in_sqft", "Furnishing", "Posted_date", "Age_of_listing_in_days", "Location", "City", "Latitude", "Longitude"]
- `data/train.csv` (8860025 bytes); columns: ["Id", "Address", "Beds", "Baths", "Type", "Area_in_sqft", "Furnishing", "Posted_date", "Age_of_listing_in_days", "Location", "City", "Latitude", "Longitude", "Rent"]

## Public description

```
description.txt (54 lines)
sample_submission.csv (14750 lines)
test.csv (14750 lines)
train.csv (58994 lines)```

-> sample_submission.csv has 14749 rows and 2 columns.
Here is some information about the columns:
Id (int64) has range: 15.00 - 73733.00, 0 nan values
Rent (float64) has range: 2734.85 - 2086059.61, 0 nan values

-> test.csv has 14749 rows and 13 columns.
Here is some information about the columns:
Address (object) has 2688 unique values. Some example values: ['Khalifa City, Abu Dhabi', 'Mohammed Bin Zayed City, Abu Dhabi', 'Muwaileh Building, Muwailih Commercial, Sharjah', 'Muwaileh 3 Building, Muwailih Commercial, Sharjah']
Age_of_listing_in_days (int64) has range: 11.00 - 2276.00, 0 nan values
Area_in_sqft (int64) has range: 112.00 - 168046.00, 0 nan values
Baths (int64) has range: 1.00 - 11.00, 0 nan values
Beds (int64) has range: 0.00 - 11.00, 0 nan values
City (object) has 8 unique values: ['Sharjah', 'Abu Dhabi', 'Ajman', 'Dubai', 'Al Ain', 'Ras Al Khaimah', 'Umm Al Quwain', 'Fujairah']
Furnishing (object) has 2 unique values: ['Unfurnished', 'Furnished']
Id (int64) has range: 15.00 - 73733.00, 0 nan values
Latitude (float64) has range: 15.18 - 25.92, 137 nan values
Location (object) has 342 unique values. Some example values: ['Al Reem Island', 'Jumeirah Village Circle (JVC)', 'Downtown Dubai', 'Khalifa City']
Longitude (float64) has range: 43.35 - 56.35, 137 nan values
Posted_date (object) has 390 unique values. Some example values: ['2024-04-03', '2024-04-04', '2024-03-27', '2024-03-18']
Type (object) has 9 unique values: ['Apartment', 'Villa', 'Townhouse', 'Penthouse', 'Hotel Apartment', 'Villa Compound', 'Residential Building', 'Residential Plot', 'Residential Floor']

-> train.csv has 58993 rows and 14 columns.
Here is some information about the columns:
Address (object) has 4286 unique values. Some example values: ['Khalifa City, Abu Dhabi', 'Mohammed Bin Zayed City, Abu Dhabi', 'Madinat Al Riyadh, Abu Dhabi', 'Muwaileh 3 Building, Muwailih Commercial, Sharjah']
Age_of_listing_in_days (int64) has range: 11.00 - 1789.00, 0 nan values
Area_in_sqft (int64) has range: 74.00 - 210254.00, 0 nan values
Baths (int64) has range: 1.00 - 11.00, 0 nan values
Beds (int64) has range: 0.00 - 12.00, 0 nan values
City (object) has 8 unique values: ['Dubai', 'Abu Dhabi', 'Sharjah', 'Ajman', 'Ras Al Khaimah', 'Al Ain', 'Umm Al Quwain', 'Fujairah']
Furnishing (object) has 2 unique values: ['Furnished', 'Unfurnished']
Id (int64) has range: 1.00 - 73742.00, 0 nan values
Latitude (float64) has range: 15.18 - 25.92, 582 nan values
Location (object) has 433 unique values. Some example values: ['Al Reem Island', 'Jumeirah Village Circle (JVC)', 'Downtown Dubai', 'Khalifa City']
Longitude (float64) has range: 43.35 - 56.36, 582 nan values
Posted_date (object) has 520 unique values. Some example values: ['2024-04-03', '2024-03-27', '2024-04-04', '2024-03-20']
Rent (int64) has range: 0.00 - 55000000.00, 0 nan values
Type (object) has 9 unique values: ['Apartment', 'Villa', 'Townhouse', 'Hotel Apartment', 'Villa Compound', 'Penthouse', 'Residential Plot', 'Residential Building', 'Residential Floor']
