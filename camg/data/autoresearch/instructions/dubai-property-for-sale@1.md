# OpenMLE-fast task

Task ID: `dubai-property-for-sale@1`

Native metric: `DubaiPropertyPriceMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2495 bytes)
- `data/sample_submission.csv` (285818 bytes); columns: ["Id", "Price"]
- `data/test.csv` (1244788 bytes); columns: ["Id", "Type", "Purpose", "Furnishing", "Beds", "Baths", "Area_sqft", "Address"]
- `data/train.csv` (5399477 bytes); columns: ["Id", "Type", "Purpose", "Furnishing", "Price", "Beds", "Baths", "Area_sqft", "Address"]

## Public description

```
description.txt (39 lines)
sample_submission.csv (10442 lines)
test.csv (10442 lines)
train.csv (41767 lines)```

-> sample_submission.csv has 10441 rows and 2 columns.
Here is some information about the columns:
Id (object) has 10441 unique values. Some example values: ['P0052199', 'P0000001', 'P0000002', 'P0000006']
Price (float64) has range: 40673.44 - 73802547.03, 0 nan values

-> test.csv has 10441 rows and 8 columns.
Here is some information about the columns:
Address (object) has 2457 unique values. Some example values: ['Jade Tower, Majan, Dubai, UAE', 'Binghatti Aquarise, Business Bay, Dubai, UAE', 'Azizi Venice, Dubai South, Dubai, UAE', 'Forest City Tower, Majan, Dubai, UAE']
Area_sqft (object) has 2838 unique values. Some example values: ['1,550 sqft', '770 sqft', '743 sqft', '800 sqft']
Baths (object) has 11 unique values. Some example values: ['2 baths', '1 bath', '3 baths', '4 baths']
Beds (object) has 13 unique values. Some example values: ['1 bed', '2 beds', 'Studio', '3 beds']
Furnishing (object) has 2 unique values: ['Unfurnished', 'Furnished']
Id (object) has 10441 unique values. Some example values: ['P0052199', 'P0000001', 'P0000002', 'P0000006']
Purpose (object) has 1 unique values: ['Sale']
Type (object) has 8 unique values: ['Apartment', 'Villa', 'Penthouse', 'Townhouse', 'Hotel Apartment', 'Residential Floor', 'Villa Compound', 'Residential Building']

-> train.csv has 41766 rows and 9 columns.
Here is some information about the columns:
Address (object) has 3579 unique values. Some example values: ['Binghatti Aquarise, Business Bay, Dubai, UAE', 'Jade Tower, Majan, Dubai, UAE', 'Binghatti Haven, Dubai Sports City, Dubai, UAE', 'Forest City Tower, Majan, Dubai, UAE']
Area_sqft (object) has 4752 unique values. Some example values: ['750 sqft', '773 sqft', '2,208 sqft', '743 sqft']
Baths (object) has 11 unique values. Some example values: ['2 baths', '1 bath', '3 baths', '4 baths']
Beds (object) has 12 unique values. Some example values: ['1 bed', '2 beds', 'Studio', '3 beds']
Furnishing (object) has 2 unique values: ['Unfurnished', 'Furnished']
Id (object) has 41766 unique values. Some example values: ['P0052207', 'P0000003', 'P0000004', 'P0000005']
Price (float64) has range: 305000.00 - 500000000.00, 0 nan values
Purpose (object) has 1 unique values: ['Sale']
Type (object) has 8 unique values: ['Apartment', 'Villa', 'Townhouse', 'Penthouse', 'Residential Floor', 'Hotel Apartment', 'Residential Building', 'Villa Compound']
