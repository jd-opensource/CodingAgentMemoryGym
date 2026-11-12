# OpenMLE-fast task

Task ID: `statistical-performance@1`

Native metric: `StatisticalPerformanceIndexMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (796 bytes)
- `data/sample_submission.csv` (5032 bytes); columns: ["row_id", "SPI_INDEX"]
- `data/test.csv` (91382 bytes); columns: ["row_id", "country", "iso3c", "date", "SPI.INDEX.PIL1", "SPI.INDEX.PIL2", "SPI.INDEX.PIL3", "SPI.INDEX.PIL4", "SPI.INDEX.PIL5", "SPI.INDEX", "SPI.DIM1.5.INDEX", "SPI.DIM2.1.INDEX", "SPI.DIM2.2.INDEX", "SPI.DIM2.4.INDEX", "SPI.DIM3.1.INDEX", "SPI.DIM3.2.INDEX", "SPI.DIM3.3.INDEX", "SPI.DIM3.4.INDEX", "SPI.DIM4.1.CEN.INDEX", "SPI.DIM4.1.SVY.INDEX", "SPI.DIM4.2.INDEX", "SPI.DIM4.3.INDEX", "SPI.DIM5.1.INDEX", "SPI.DIM5.2.INDEX", "SPI.DIM5.5.INDEX", "SPI.D1.5.POV", "SPI.D1.5.CHLD.MORT", "SPI.D1.5.DT.TDS.DPPF.XP.ZS", "SPI.D1.5.SAFE.MAN.WATER", "SPI.D1.5.LFP", "SPI.D2.1.GDDS", "SPI.D2.2.Machine.readable", "SPI.D2.2.Non.proprietary", "SPI.D2.2.Download.options", "SPI.D2.2.Metadata.available", "SPI.D2.2.Terms.of.use", "SPI.D2.2.Openness.subscore", "SPI.D2.4.NADA", "SPI.D3.1.POV", "SPI.D3.2.HNGR", "SPI.D3.3.HLTH", "SPI.D3.4.EDUC", "SPI.D3.5.GEND", "SPI.D3.6.WTRS", "SPI.D3.7.ENRG", "SPI.D3.8.WORK", "SPI.D3.9.INDY", "SPI.D3.10.NEQL", "SPI.D3.11.CITY", "SPI.D3.12.CNSP", "SPI.D3.15.LAND", "SPI.D3.16.INST", "SPI.D3.17.PTNS", "SPI.D3.13.CLMT", "SPI.D3.NA", "SPI.D4.1.1.POPU", "SPI.D4.1.2.AGRI", "SPI.D4.1.3.BIZZ", "SPI.D4.1.4.HOUS", "SPI.D4.1.5.AGSVY", "SPI.D4.1.6.LABR", "SPI.D4.1.7.HLTH", "SPI.D4.1.8.BZSVY", "SPI.D4.2.3.CRVS", "SPI.D4.3.GEO.first.admin.level", "SPI.D5.1.DILG", "SPI.D5.2.1.SNAU", "SPI.D5.2.2.NABY", "SPI.D5.2.3.CNIN", "SPI.D5.2.4.CPIBY", "SPI.D5.2.5.HOUS", "SPI.D5.2.6.EMPL", "SPI.D5.2.7.CGOV", "SPI.D5.2.8.FINA", "SPI.D5.2.9.MONY", "SPI.D5.2.10.GSBP", "SPI.D5.5.DIFI", "income", "region", "weights", "population"]
- `data/train.csv` (583095 bytes); columns: ["country", "iso3c", "date", "SPI.INDEX.PIL1", "SPI.INDEX.PIL2", "SPI.INDEX.PIL3", "SPI.INDEX.PIL4", "SPI.INDEX.PIL5", "SPI.INDEX", "SPI.DIM1.5.INDEX", "SPI.DIM2.1.INDEX", "SPI.DIM2.2.INDEX", "SPI.DIM2.4.INDEX", "SPI.DIM3.1.INDEX", "SPI.DIM3.2.INDEX", "SPI.DIM3.3.INDEX", "SPI.DIM3.4.INDEX", "SPI.DIM4.1.CEN.INDEX", "SPI.DIM4.1.SVY.INDEX", "SPI.DIM4.2.INDEX", "SPI.DIM4.3.INDEX", "SPI.DIM5.1.INDEX", "SPI.DIM5.2.INDEX", "SPI.DIM5.5.INDEX", "SPI.D1.5.POV", "SPI.D1.5.CHLD.MORT", "SPI.D1.5.DT.TDS.DPPF.XP.ZS", "SPI.D1.5.SAFE.MAN.WATER", "SPI.D1.5.LFP", "SPI.D2.1.GDDS", "SPI.D2.2.Machine.readable", "SPI.D2.2.Non.proprietary", "SPI.D2.2.Download.options", "SPI.D2.2.Metadata.available", "SPI.D2.2.Terms.of.use", "SPI.D2.2.Openness.subscore", "SPI.D2.4.NADA", "SPI.D3.1.POV", "SPI.D3.2.HNGR", "SPI.D3.3.HLTH", "SPI.D3.4.EDUC", "SPI.D3.5.GEND", "SPI.D3.6.WTRS", "SPI.D3.7.ENRG", "SPI.D3.8.WORK", "SPI.D3.9.INDY", "SPI.D3.10.NEQL", "SPI.D3.11.CITY", "SPI.D3.12.CNSP", "SPI.D3.15.LAND", "SPI.D3.16.INST", "SPI.D3.17.PTNS", "SPI.D3.13.CLMT", "SPI.D3.NA", "SPI.D4.1.1.POPU", "SPI.D4.1.2.AGRI", "SPI.D4.1.3.BIZZ", "SPI.D4.1.4.HOUS", "SPI.D4.1.5.AGSVY", "SPI.D4.1.6.LABR", "SPI.D4.1.7.HLTH", "SPI.D4.1.8.BZSVY", "SPI.D4.2.3.CRVS", "SPI.D4.3.GEO.first.admin.level", "SPI.D5.1.DILG", "SPI.D5.2.1.SNAU", "SPI.D5.2.2.NABY", "SPI.D5.2.3.CNIN", "SPI.D5.2.4.CPIBY", "SPI.D5.2.5.HOUS", "SPI.D5.2.6.EMPL", "SPI.D5.2.7.CGOV", "SPI.D5.2.8.FINA", "SPI.D5.2.9.MONY", "SPI.D5.2.10.GSBP", "SPI.D5.5.DIFI", "income", "region", "weights", "population", "SPI_INDEX_NEXT"]

## Public description

```
description.txt (47 lines)
sample_submission.csv (188 lines)
test.csv (188 lines)
train.csv (1239 lines)```

-> sample_submission.csv has 187 rows and 2 columns.
The columns are: row_id, SPI_INDEX

-> test.csv has 187 rows and 81 columns.
The columns are: row_id, country, iso3c, date, SPI.INDEX.PIL1, SPI.INDEX.PIL2, SPI.INDEX.PIL3, SPI.INDEX.PIL4, SPI.INDEX.PIL5, SPI.INDEX, SPI.DIM1.5.INDEX, SPI.DIM2.1.INDEX, SPI.DIM2.2.INDEX, SPI.DIM2.4.INDEX, SPI.DIM3.1.INDEX... and 66 more columns

-> train.csv has 1238 rows and 81 columns.
The columns are: country, iso3c, date, SPI.INDEX.PIL1, SPI.INDEX.PIL2, SPI.INDEX.PIL3, SPI.INDEX.PIL4, SPI.INDEX.PIL5, SPI.INDEX, SPI.DIM1.5.INDEX, SPI.DIM2.1.INDEX, SPI.DIM2.2.INDEX, SPI.DIM2.4.INDEX, SPI.DIM3.1.INDEX, SPI.DIM3.2.INDEX... and 66 more columns
