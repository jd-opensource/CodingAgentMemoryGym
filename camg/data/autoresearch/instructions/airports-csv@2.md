# OpenMLE-fast task

Task ID: `airports-csv@2`

Native metric: `AirportElevationMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2756 bytes)
- `data/sample_submission.csv` (35241 bytes); columns: ["id", "altitude"]
- `data/test.csv` (177482 bytes); columns: ["id", "name", "city", "country", "iata", "icao", "latitude", "longitude", "timezone_offset", "dst", "timezone", "type", "source"]
- `data/train.csv` (730861 bytes); columns: ["id", "name", "city", "country", "iata", "icao", "latitude", "longitude", "altitude", "timezone_offset", "dst", "timezone", "type", "source"]

## Public description

```
description.txt (34 lines)
sample_submission.csv (1541 lines)
test.csv (1541 lines)
train.csv (6159 lines)```

-> sample_submission.csv has 1540 rows and 2 columns.
Here is some information about the columns:
altitude (float64) has range: -1400.00 - 6065.18, 0 nan values
id (int64) has range: 6.00 - 14107.00, 0 nan values

-> test.csv has 1540 rows and 13 columns.
Here is some information about the columns:
city (object) has 1496 unique values. Some example values: ['Santiago', 'Santa Rosa', 'Murcia', 'New York']
country (object) has 165 unique values. Some example values: ['United States', 'Canada', 'Australia', 'Brazil']
dst (object) has 7 unique values: ['A', 'U', 'N', 'E', 'O', 'S', 'Z', nan]
iata (object) has 1215 unique values. Some example values: ['NAU', 'CLM', 'KBR', 'OVD']
icao (object) has 1539 unique values. Some example values: ['NTGN', 'KCLM', 'FALI', 'UNIP']
id (int64) has range: 6.00 - 14107.00, 0 nan values
latitude (float64) has range: -64.24 - 79.99, 0 nan values
longitude (float64) has range: -179.67 - 177.98, 0 nan values
name (object) has 1539 unique values. Some example values: ['St George Airport', 'Antonio Nery Juarbe Pol Airport', 'Helisul IV Heliport', 'Narrandera Airport']
source (float64) has 0 unique values: [nan]
timezone (object) has 213 unique values. Some example values: ['America/New_York', 'America/Chicago', 'Europe/Berlin', 'America/Anchorage']
timezone_offset (float64) has range: -10.00 - 13.00, 71 nan values
type (object) has 1 unique values: ['airport']

-> train.csv has 6158 rows and 14 columns.
Here is some information about the columns:
altitude (int64) has range: -1266.00 - 14472.00, 0 nan values
city (object) has 5640 unique values. Some example values: ['Columbus', 'London', 'Houston', 'Greenville']
country (object) has 227 unique values. Some example values: ['United States', 'Canada', 'Australia', 'Russia']
dst (object) has 7 unique values: ['E', 'U', 'O', 'N', 'A', 'S', 'Z', nan]
iata (object) has 4857 unique values. Some example values: ['GDW', 'SBK', 'JBQ', 'AOP']
icao (object) has 6158 unique values. Some example values: ['KGDW', 'LFRT', 'MDJB', 'SPAS']
id (int64) has range: 1.00 - 14110.00, 0 nan values
latitude (float64) has range: -90.00 - 89.50, 0 nan values
longitude (float64) has range: -179.88 - 179.95, 0 nan values
name (object) has 6129 unique values. Some example values: ['Capital City Airport', 'Santa Maria Airport', 'Newcastle Airport', 'Faro Airport']
source (float64) has 0 unique values: [nan]
timezone (object) has 293 unique values. Some example values: ['America/New_York', 'America/Chicago', 'Europe/Berlin', 'Europe/Paris']
timezone_offset (float64) has range: -12.00 - 13.00, 282 nan values
type (object) has 1 unique values: ['airport']
