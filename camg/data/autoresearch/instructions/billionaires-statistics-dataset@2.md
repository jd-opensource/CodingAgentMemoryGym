# OpenMLE-fast task

Task ID: `billionaires-statistics-dataset@2`

Native metric: `BillionairesSelfMadeMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (5242 bytes)
- `data/sample_submission.csv` (13909 bytes); columns: ["row_id", "selfMade"]
- `data/test.csv` (109107 bytes); columns: ["row_id", "category", "age", "country", "city", "source", "industries", "countryOfCitizenship", "gender", "birthDate", "state", "residenceStateRegion", "birthYear", "birthMonth", "birthDay", "cpi_country", "cpi_change_country", "gdp_country", "gross_tertiary_education_enrollment", "gross_primary_education_enrollment_country", "life_expectancy_country", "tax_revenue_country_country", "total_tax_rate_country", "population_country", "latitude_country", "longitude_country"]
- `data/train.csv` (439064 bytes); columns: ["row_id", "category", "age", "country", "city", "source", "industries", "countryOfCitizenship", "selfMade", "gender", "birthDate", "state", "residenceStateRegion", "birthYear", "birthMonth", "birthDay", "cpi_country", "cpi_change_country", "gdp_country", "gross_tertiary_education_enrollment", "gross_primary_education_enrollment_country", "life_expectancy_country", "tax_revenue_country_country", "total_tax_rate_country", "population_country", "latitude_country", "longitude_country"]

## Public description

```
description.txt (38 lines)
sample_submission.csv (529 lines)
test.csv (529 lines)
train.csv (2113 lines)```

-> sample_submission.csv has 528 rows and 2 columns.
Here is some information about the columns:
row_id (int64) has range: 102112.00 - 102639.00, 0 nan values
selfMade (float64) has range: 0.00 - 1.00, 0 nan values

-> test.csv has 528 rows and 26 columns.
Here is some information about the columns:
age (float64) has range: 20.00 - 99.00, 12 nan values
birthDate (object) has 476 unique values. Some example values: ['1/1/1971 0:00', '1/1/1969 0:00', '1/1/1955 0:00', '1/1/1962 0:00']
birthDay (float64) has range: 1.00 - 31.00, 13 nan values
birthMonth (float64) has range: 1.00 - 12.00, 13 nan values
birthYear (float64) has range: 1923.00 - 2002.00, 13 nan values
category (object) has 18 unique values. Some example values: ['Finance & Investments', 'Technology', 'Manufacturing', 'Fashion & Retail']
city (object) has 253 unique values. Some example values: ['New York', 'Beijing', 'Shanghai', 'Hong Kong']
country (object) has 46 unique values. Some example values: ['United States', 'China', 'India', 'Switzerland']
countryOfCitizenship (object) has 49 unique values. Some example values: ['United States', 'China', 'India', 'Russia']
cpi_change_country (float64) has range: -1.90 - 53.50, 35 nan values
cpi_country (float64) has range: 99.55 - 288.57, 35 nan values
gdp_country (object) has 42 unique values. Some example values: ['$21,427,700,000,000 ', '$19,910,000,000,000 ', '$2,611,000,000,000 ', '$703,082,435,360 ']
gender (object) has 2 unique values: ['M', 'F']
gross_primary_education_enrollment_country (float64) has range: 84.70 - 126.60, 34 nan values
gross_tertiary_education_enrollment (float64) has range: 10.10 - 113.10, 34 nan values
industries (object) has 18 unique values. Some example values: ['Finance & Investments', 'Technology', 'Manufacturing', 'Fashion & Retail']
latitude_country (float64) has range: -38.42 - 61.92, 33 nan values
life_expectancy_country (float64) has range: 54.30 - 84.20, 34 nan values
longitude_country (float64) has range: -106.35 - 138.25, 33 nan values
population_country (float64) has range: 38964.00 - 1397715000.00, 33 nan values
residenceStateRegion (object) has 4 unique values: [nan, 'West', 'South', 'Northeast', 'Midwest']
row_id (int64) has range: 102112.00 - 102639.00, 0 nan values
source (object) has 294 unique values. Some example values: ['Real estate', 'Investments', 'Diversified', 'Pharmaceuticals']
state (object) has 29 unique values. Some example values: ['California', 'New York', 'Florida', 'Texas']
tax_revenue_country_country (float64) has range: 0.10 - 32.40, 34 nan values
total_tax_rate_country (float64) has range: 9.90 - 106.30, 34 nan values

-> train.csv has 2112 rows and 27 columns.
Here is some information about the columns:
age (float64) has range: 18.00 - 101.00, 53 nan values
birthDate (object) has 1671 unique values. Some example values: ['1/1/1965 0:00', '1/1/1967 0:00', '1/1/1964 0:00', '1/1/1966 0:00']
birthDay (float64) has range: 1.00 - 31.00, 63 nan values
birthMonth (float64) has range: 1.00 - 12.00, 63 nan values
birthYear (float64) has range: 1921.00 - 2004.00, 63 nan values
category (object) has 18 unique values. Some example values: ['Finance & Investments', 'Manufacturing', 'Technology', 'Fashion & Retail']
city (object) has 637 unique values. Some example values: ['New York', 'Hong Kong', 'Moscow', 'London']
country (object) has 74 unique values. Some example values: ['United States', 'China', 'India', 'Germany']
countryOfCitizenship (object) has 73 unique values. Some example values: ['United States', 'China', 'India', 'Germany']
cpi_change_country (float64) has range: -1.90 - 53.50, 149 nan values
cpi_country (float64) has range: 99.55 - 288.57, 149 nan values
gdp_country (object) has 64 unique values. Some example values: ['$21,427,700,000,000 ', '$19,910,000,000,000 ', '$2,611,000,000,000 ', '$3,845,630,030,824 ']
gender (object) has 2 unique values: ['F', 'M']
gross_primary_education_enrollment_country (float64) has range: 84.70 - 142.10, 147 nan values
gross_tertiary_education_enrollment (float64) has range: 4.00 - 136.60, 148 nan values
industries (object) has 18 unique values. Some example values: ['Finance & Investments', 'Manufacturing', 'Technology', 'Fashion & Retail']
latitude_country (float64) has range: -40.90 - 61.92, 131 nan values
life_expectancy_country (float64) has range: 54.30 - 84.20, 148 nan values
longitude_country (float64) has range: -106.35 - 174.89, 131 nan values
population_country (float64) has range: 38019.00 - 1397715000.00, 131 nan values
residenceStateRegion (object) has 5 unique values: [nan, 'Midwest', 'South', 'West', 'Northeast', 'U.S. Territories']
row_id (int64) has range: 100000.00 - 102111.00, 0 nan values
selfMade (int64) has 2 unique values: [1, 0]
source (object) has 796 unique values. Some example values: ['Real estate', 'Diversified', 'Investments', 'Pharmaceuticals']
state (object) has 42 unique values. Some example values: ['California', 'New York', 'Florida', 'Texas']
tax_revenue_country_country (float64) has range: 0.10 - 37.20, 149 nan values
total_tax_rate_country (float64) has range: 11.30 - 106.30, 148 nan values
