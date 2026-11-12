# OpenMLE-fast task

Task ID: `agencyperformance@1`

Native metric: `AgencyPerformanceMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2755 bytes)
- `data/sample_submission.csv` (686962 bytes); columns: ["AGENCY_ID", "PRIMARY_AGENCY_ID", "PROD_ABBR", "PROD_LINE", "STATE_ABBR", "STAT_PROFILE_DATE_YEAR", "LOSS_RATIO_NEXT_YEAR"]
- `data/test.csv` (2710911 bytes); columns: ["AGENCY_ID", "PRIMARY_AGENCY_ID", "PROD_ABBR", "PROD_LINE", "STATE_ABBR", "STAT_PROFILE_DATE_YEAR", "RETENTION_POLY_QTY", "POLY_INFORCE_QTY", "PREV_POLY_INFORCE_QTY", "NB_WRTN_PREM_AMT", "WRTN_PREM_AMT", "PREV_WRTN_PREM_AMT", "PRD_ERND_PREM_AMT", "PRD_INCRD_LOSSES_AMT", "MONTHS", "RETENTION_RATIO", "LOSS_RATIO", "AGENCY_APPOINTMENT_YEAR", "ACTIVE_PRODUCERS", "MAX_AGE", "MIN_AGE", "VENDOR_IND", "VENDOR", "PL_START_YEAR", "PL_END_YEAR", "COMMISIONS_START_YEAR", "COMMISIONS_END_YEAR", "CL_START_YEAR", "CL_END_YEAR", "ACTIVITY_NOTES_START_YEAR", "ACTIVITY_NOTES_END_YEAR", "CL_BOUND_CT_MDS", "CL_QUO_CT_MDS", "CL_BOUND_CT_SBZ", "CL_QUO_CT_SBZ", "CL_BOUND_CT_eQT", "CL_QUO_CT_eQT", "PL_BOUND_CT_ELINKS", "PL_QUO_CT_ELINKS", "PL_BOUND_CT_PLRANK", "PL_QUO_CT_PLRANK", "PL_BOUND_CT_eQTte", "PL_QUO_CT_eQTte", "PL_BOUND_CT_APPLIED", "PL_QUO_CT_APPLIED", "PL_BOUND_CT_TRANSACTNOW", "PL_QUO_CT_TRANSACTNOW"]
- `data/train.csv` (18291965 bytes); columns: ["AGENCY_ID", "PRIMARY_AGENCY_ID", "PROD_ABBR", "PROD_LINE", "STATE_ABBR", "STAT_PROFILE_DATE_YEAR", "RETENTION_POLY_QTY", "POLY_INFORCE_QTY", "PREV_POLY_INFORCE_QTY", "NB_WRTN_PREM_AMT", "WRTN_PREM_AMT", "PREV_WRTN_PREM_AMT", "PRD_ERND_PREM_AMT", "PRD_INCRD_LOSSES_AMT", "MONTHS", "RETENTION_RATIO", "LOSS_RATIO", "AGENCY_APPOINTMENT_YEAR", "ACTIVE_PRODUCERS", "MAX_AGE", "MIN_AGE", "VENDOR_IND", "VENDOR", "PL_START_YEAR", "PL_END_YEAR", "COMMISIONS_START_YEAR", "COMMISIONS_END_YEAR", "CL_START_YEAR", "CL_END_YEAR", "ACTIVITY_NOTES_START_YEAR", "ACTIVITY_NOTES_END_YEAR", "CL_BOUND_CT_MDS", "CL_QUO_CT_MDS", "CL_BOUND_CT_SBZ", "CL_QUO_CT_SBZ", "CL_BOUND_CT_eQT", "CL_QUO_CT_eQT", "PL_BOUND_CT_ELINKS", "PL_QUO_CT_ELINKS", "PL_BOUND_CT_PLRANK", "PL_QUO_CT_PLRANK", "PL_BOUND_CT_eQTte", "PL_QUO_CT_eQTte", "PL_BOUND_CT_APPLIED", "PL_QUO_CT_APPLIED", "PL_BOUND_CT_TRANSACTNOW", "PL_QUO_CT_TRANSACTNOW", "LOSS_RATIO_NEXT_YEAR"]

## Public description

Title: Agency-Product-State Next-Year Loss Ratio Forecasting

Problem statement
Forecast the next-year loss ratio for each agency–product–state segment. For a segment observed at year t, predict its loss ratio at year t+1 using only information available up to and including year t.

Data description
- Rows represent segments identified by the columns: AGENCY_ID, PRIMARY_AGENCY_ID, PROD_ABBR, PROD_LINE, STATE_ABBR, STAT_PROFILE_DATE_YEAR.
- Features include exposure/performance (e.g., PRD_ERND_PREM_AMT, PRD_INCRD_LOSSES_AMT, LOSS_RATIO at year t), policy counts and premiums, retention measures, quote/bind counts across systems, producer demographics, vendor indicators, and product/state identifiers.
- MONTHS indicates the number of months observed in the year. Sentinel value 99999 indicates missing for certain numeric fields.

Released files
- train.csv: Segment rows for years t = 2005–2012 with the target column LOSS_RATIO_NEXT_YEAR (the segment’s LOSS_RATIO at t+1, i.e., 2006–2013). Features are constrained to information at year t and earlier.
- test.csv: Segment rows for year t = 2013 with the same feature set (no target). Participants predict LOSS_RATIO_NEXT_YEAR for t+1 = 2014.
- sample_submission.csv: Example submission containing the required ID columns and a prediction column LOSS_RATIO_NEXT_YEAR filled with random valid values.

Submission format
Your submission must be a CSV with exactly these columns:
- AGENCY_ID
- PRIMARY_AGENCY_ID
- PROD_ABBR
- PROD_LINE
- STATE_ABBR
- STAT_PROFILE_DATE_YEAR
- LOSS_RATIO_NEXT_YEAR
Each row corresponds to a row in test.csv with the same ID columns. Predictions must be numeric and finite.

Evaluation
- Metric: Weighted Mean Absolute Error (WMAE) on LOSS_RATIO_NEXT_YEAR.
- For each test row, weight = next-year earned premium (PRD_ERND_PREM_AMT at t+1). Pairs with missing targets or non-positive weights are excluded.
- WMAE = sum_i w_i * |y_i − ŷ_i| / sum_i w_i. Lower is better.

Important notes
- Only full-year observations are used (MONTHS = 12 for year t and the target year t+1). Year 2015 is excluded due to widespread partial-year observations.
- Treat 99999 as missing for numeric fields. Handle missingness explicitly during preprocessing.
- Recommended feature engineering (using only data up to year t): quote-system hit ratios (bound/quote), multi-year trailing averages, growth rates (YoY deltas and ratios), exposure-normalized mixes, agency tenure, and categorical encodings for high-cardinality identifiers.
- The dataset is heterogeneous across agencies, products (PL/CL), states, and time; robust preprocessing and modeling are required. Viable models include regularized linear models and gradient-boosted trees (LightGBM/CatBoost), among others.
