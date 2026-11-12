# OpenMLE-fast task

Task ID: `billionaires-statistics-dataset@1`

Native metric: `BillionaireWorthMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (5832 bytes)
- `data/sample_submission.csv` (19904 bytes); columns: ["id", "finalWorth"]
- `data/test.csv` (153583 bytes); columns: ["id", "category", "age", "country", "city", "source", "industries", "countryOfCitizenship", "selfMade", "status", "gender", "birthDate", "date", "state", "residenceStateRegion", "birthYear", "birthMonth", "birthDay", "cpi_country", "cpi_change_country", "gdp_country", "gross_tertiary_education_enrollment", "gross_primary_education_enrollment_country", "life_expectancy_country", "tax_revenue_country_country", "total_tax_rate_country", "population_country", "latitude_country", "longitude_country"]
- `data/train.csv` (471436 bytes); columns: ["id", "category", "age", "country", "city", "source", "industries", "countryOfCitizenship", "selfMade", "status", "gender", "birthDate", "date", "state", "residenceStateRegion", "birthYear", "birthMonth", "birthDay", "cpi_country", "cpi_change_country", "gdp_country", "gross_tertiary_education_enrollment", "gross_primary_education_enrollment_country", "life_expectancy_country", "tax_revenue_country_country", "total_tax_rate_country", "population_country", "latitude_country", "longitude_country", "finalWorth"]

## Public description

```
description.txt (40 lines)
sample_submission.csv (655 lines)
test.csv (655 lines)
train.csv (1987 lines)```

-> sample_submission.csv has 654 rows and 2 columns.
Here is some information about the columns:
finalWorth (float64) has range: 244.80 - 30520.83, 0 nan values
id (object) has 654 unique values. Some example values: ['BILL_002639', 'BILL_000001', 'BILL_000011', 'BILL_000012']

-> test.csv has 654 rows and 29 columns.
Here is some information about the columns:
age (float64) has range: 20.00 - 101.00, 12 nan values
birthDate (object) has 579 unique values. Some example values: ['1/1/1963 0:00', '1/1/1965 0:00', '1/1/1969 0:00', '1/1/1975 0:00']
birthDay (float64) has range: 1.00 - 31.00, 14 nan values
birthMonth (float64) has range: 1.00 - 12.00, 14 nan values
birthYear (float64) has range: 1921.00 - 2002.00, 14 nan values
category (object) has 18 unique values. Some example values: ['Finance & Investments', 'Manufacturing', 'Technology', 'Fashion & Retail']
city (object) has 279 unique values. Some example values: ['Moscow', 'New York', 'London', 'Mumbai']
country (object) has 48 unique values. Some example values: ['United States', 'China', 'India', 'Russia']
countryOfCitizenship (object) has 51 unique values. Some example values: ['United States', 'China', 'India', 'Russia']
cpi_change_country (float64) has range: -1.90 - 15.20, 44 nan values
cpi_country (float64) has range: 99.55 - 288.57, 44 nan values
date (object) has 2 unique values: ['4/4/2023 5:01', '4/4/2023 9:01']
gdp_country (object) has 45 unique values. Some example values: ['$21,427,700,000,000 ', '$19,910,000,000,000 ', '$2,611,000,000,000 ', '$1,699,876,578,871 ']
gender (object) has 2 unique values: ['M', 'F']
gross_primary_education_enrollment_country (float64) has range: 84.70 - 126.60, 44 nan values
gross_tertiary_education_enrollment (float64) has range: 10.20 - 136.60, 44 nan values
id (object) has 654 unique values. Some example values: ['BILL_002639', 'BILL_000001', 'BILL_000011', 'BILL_000012']
industries (object) has 18 unique values. Some example values: ['Finance & Investments', 'Manufacturing', 'Technology', 'Fashion & Retail']
latitude_country (float64) has range: -40.90 - 61.92, 40 nan values
life_expectancy_country (float64) has range: 54.30 - 84.20, 44 nan values
longitude_country (float64) has range: -106.35 - 174.89, 40 nan values
population_country (float64) has range: 38964.00 - 1397715000.00, 40 nan values
residenceStateRegion (object) has 4 unique values: [nan, 'West', 'Northeast', 'South', 'Midwest']
selfMade (bool) is 71.41% True, 28.59% False
source (object) has 342 unique values. Some example values: ['Real estate', 'Diversified', 'Investments', 'Pharmaceuticals']
state (object) has 35 unique values. Some example values: ['California', 'New York', 'Florida', 'Texas']
status (object) has 6 unique values: ['U', 'D', 'Split Family Fortune', 'E', 'N', 'R']
tax_revenue_country_country (float64) has range: 0.10 - 32.40, 44 nan values
total_tax_rate_country (float64) has range: 15.90 - 65.10, 44 nan values

-> train.csv has 1986 rows and 30 columns.
Here is some information about the columns:
age (float64) has range: 18.00 - 99.00, 53 nan values
birthDate (object) has 1585 unique values. Some example values: ['1/1/1965 0:00', '1/1/1966 0:00', '1/1/1962 0:00', '1/1/1971 0:00']
birthDay (float64) has range: 1.00 - 31.00, 62 nan values
birthMonth (float64) has range: 1.00 - 12.00, 62 nan values
birthYear (float64) has range: 1923.00 - 2004.00, 62 nan values
category (object) has 18 unique values. Some example values: ['Finance & Investments', 'Manufacturing', 'Technology', 'Fashion & Retail']
city (object) has 625 unique values. Some example values: ['New York', 'Beijing', 'Shanghai', 'Hong Kong']
country (object) has 78 unique values. Some example values: ['United States', 'China', 'India', 'Germany']
countryOfCitizenship (object) has 73 unique values. Some example values: ['United States', 'China', 'India', 'Germany']
cpi_change_country (float64) has range: -1.90 - 53.50, 140 nan values
cpi_country (float64) has range: 99.55 - 288.57, 140 nan values
date (object) has 2 unique values: ['4/4/2023 5:01', '4/4/2023 9:01']
finalWorth (int64) has range: 1000.00 - 180000.00, 0 nan values
gdp_country (object) has 68 unique values. Some example values: ['$21,427,700,000,000 ', '$19,910,000,000,000 ', '$2,611,000,000,000 ', '$3,845,630,030,824 ']
gender (object) has 2 unique values: ['M', 'F']
gross_primary_education_enrollment_country (float64) has range: 84.70 - 142.10, 137 nan values
gross_tertiary_education_enrollment (float64) has range: 4.00 - 136.60, 138 nan values
id (object) has 1986 unique values. Some example values: ['BILL_002640', 'BILL_000002', 'BILL_002588', 'BILL_002591']
industries (object) has 18 unique values. Some example values: ['Finance & Investments', 'Manufacturing', 'Technology', 'Fashion & Retail']
latitude_country (float64) has range: -40.90 - 61.92, 124 nan values
life_expectancy_country (float64) has range: 54.30 - 84.20, 138 nan values
longitude_country (float64) has range: -106.35 - 174.89, 124 nan values
population_country (float64) has range: 38019.00 - 1397715000.00, 124 nan values
residenceStateRegion (object) has 5 unique values: ['South', 'West', 'Midwest', 'Northeast', nan, 'U.S. Territories']
selfMade (bool) is 67.72% True, 32.28% False
source (object) has 751 unique values. Some example values: ['Real estate', 'Investments', 'Diversified', 'Pharmaceuticals']
state (object) has 41 unique values. Some example values: ['California', 'New York', 'Florida', 'Texas']
status (object) has 6 unique values: ['D', 'U', 'N', 'Split Family Fortune', 'E', 'R']
tax_revenue_country_country (float64) has range: 0.10 - 37.20, 139 nan values
total_tax_rate_country (float64) has range: 9.90 - 106.30, 138 nan values
