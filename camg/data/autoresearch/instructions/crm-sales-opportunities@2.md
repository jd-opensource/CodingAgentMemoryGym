# OpenMLE-fast task

Task ID: `crm-sales-opportunities@2`

Native metric: `SalesOpportunityTimeToCloseMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/accounts.csv` (4670 bytes); columns: ["account", "sector", "year_established", "revenue", "employees", "office_location", "subsidiary_of"]
- `data/description.txt` (3514 bytes)
- `data/products.csv` (171 bytes); columns: ["product", "series", "sales_price"]
- `data/sales_teams.csv` (1284 bytes); columns: ["sales_agent", "manager", "regional_office"]
- `data/sample_submission.csv` (16021 bytes); columns: ["opportunity_id", "days_to_close"]
- `data/test.csv` (75717 bytes); columns: ["opportunity_id", "sales_agent", "product", "account", "engage_date"]
- `data/train.csv` (317592 bytes); columns: ["opportunity_id", "sales_agent", "product", "account", "engage_date", "days_to_close"]

## Public description

```
accounts.csv (86 lines)
description.txt (42 lines)
products.csv (8 lines)
sales_teams.csv (36 lines)
sample_submission.csv (1344 lines)
test.csv (1344 lines)
train.csv (5369 lines)```

-> accounts.csv has 85 rows and 7 columns.
Here is some information about the columns:
account (object) has 85 unique values. Some example values: ['Acme Corporation', 'Betasoloin', 'Betatech', 'Bioholding']
employees (int64) has range: 9.00 - 34288.00, 0 nan values
office_location (object) has 15 unique values. Some example values: ['United States', 'Kenya', 'Philipines', 'Japan']
revenue (float64) has range: 4.54 - 11698.03, 0 nan values
sector (object) has 10 unique values. Some example values: ['retail', 'technolgy', 'medical', 'marketing']
subsidiary_of (object) has 7 unique values: [nan, 'Acme Corporation', 'Massive Dynamic', 'Bubba Gump', 'Inity', 'Sonron', 'Golddex', 'Warephase']
year_established (int64) has range: 1979.00 - 2017.00, 0 nan values

-> products.csv has 7 rows and 3 columns.
Here is some information about the columns:
product (object) has 7 unique values: ['GTX Basic', 'GTX Pro', 'MG Special', 'MG Advanced', 'GTX Plus Pro', 'GTX Plus Basic', 'GTK 500']
sales_price (int64) has 7 unique values: [550, 4821, 55, 3393, 5482, 1096, 26768]
series (object) has 3 unique values: ['GTX', 'MG', 'GTK']

-> sales_teams.csv has 35 rows and 3 columns.
Here is some information about the columns:
manager (object) has 6 unique values: ['Dustin Brinkmann', 'Melvin Marxen', 'Cara Losch', 'Rocco Neubert', 'Celia Rouche', 'Summer Sewald']
regional_office (object) has 3 unique values: ['Central', 'East', 'West']
sales_agent (object) has 35 unique values. Some example values: ['Anna Snelling', 'Cecily Lampkin', 'Versie Hillebrand', 'Lajuana Vencill']

-> sample_submission.csv has 1343 rows and 2 columns.
Here is some information about the columns:
days_to_close (int64) has range: 0.00 - 145.00, 0 nan values
opportunity_id (object) has 1343 unique values. Some example values: ['YJTQSZ9D', 'WIDRX5N6', 'ZLFKHXXI', '0WGAPLOI']

-> test.csv has 1343 rows and 5 columns.
Here is some information about the columns:
account (object) has 85 unique values. Some example values: ['Hottechi', 'Konex', 'Kan-code', 'Condax']
engage_date (object) has 100 unique values. Some example values: ['2017-10-19', '2017-10-02', '2017-09-26', '2017-10-18']
opportunity_id (object) has 1343 unique values. Some example values: ['YJTQSZ9D', 'WIDRX5N6', 'ZLFKHXXI', '0WGAPLOI']
product (object) has 7 unique values: ['GTX Plus Basic', 'GTX Basic', 'GTXPro', 'MG Advanced', 'MG Special', 'GTX Plus Pro', 'GTK 500']
sales_agent (object) has 30 unique values. Some example values: ['Darcel Schlecht', 'Vicki Laflamme', 'Kary Hendrixson', 'Marty Freudenburg']

-> train.csv has 5368 rows and 6 columns.
Here is some information about the columns:
account (object) has 85 unique values. Some example values: ['Kan-code', 'Hottechi', 'Konex', 'Condax']
days_to_close (int64) has range: 1.00 - 138.00, 0 nan values
engage_date (object) has 321 unique values. Some example values: ['2017-07-17', '2017-04-17', '2017-04-23', '2017-04-04']
opportunity_id (object) has 5368 unique values. Some example values: ['USL5PZ4O', '1C1I7A6R', 'EC4QE1BX', 'MV1LWRNH']
product (object) has 7 unique values: ['GTX Plus Basic', 'MG Special', 'GTX Basic', 'GTXPro', 'GTX Plus Pro', 'MG Advanced', 'GTK 500']
sales_agent (object) has 30 unique values. Some example values: ['Darcel Schlecht', 'Anna Snelling', 'Vicki Laflamme', 'Kary Hendrixson']
