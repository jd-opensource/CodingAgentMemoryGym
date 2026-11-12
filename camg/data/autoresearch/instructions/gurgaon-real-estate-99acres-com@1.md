# OpenMLE-fast task

Task ID: `gurgaon-real-estate-99acres-com@1`

Native metric: `RealEstatePricePredictionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (623 bytes)
- `data/facets/facets/AGE.csv` (127 bytes); columns: ["id", "label"]
- `data/facets/facets/AMENITIES.csv` (1949 bytes); columns: ["id", "category", "type", "label"]
- `data/facets/facets/BATHROOM_NUM.csv` (44 bytes); columns: ["id", "label"]
- `data/facets/facets/BEDROOM_NUM.csv` (70 bytes); columns: ["id", "label"]
- `data/facets/facets/BUILDING_ID.csv` (2489 bytes); columns: ["id", "label"]
- `data/facets/facets/CITY.csv` (21 bytes); columns: ["id", "label"]
- `data/facets/facets/FACING_DIRECTION.csv` (107 bytes); columns: ["id", "label"]
- `data/facets/facets/FEATURES.csv` (233 bytes); columns: ["id", "label"]
- `data/facets/facets/FLOOR_NUM.csv` (598 bytes); columns: ["id", "label"]
- `data/facets/facets/FURNISH.csv` (57 bytes); columns: ["id", "label"]
- `data/facets/facets/LOCALITY_ID.csv` (2244 bytes); columns: ["id", "label"]
- `data/facets/facets/OWNERSHIP_TYPE.csv` (83 bytes); columns: ["id", "label"]
- `data/facets/facets/PROPERTY_TYPE.csv` (174 bytes); columns: ["id", "label"]
- `data/facets/facets/SUB_AVAILABILITY.csv` (284 bytes); columns: ["id", "label"]
- `data/facets/facets/TOTAL_FLOOR.csv` (247 bytes); columns: ["id", "label"]
- `data/sample_submission.csv` (245529 bytes); columns: ["Id", "price_inr"]
- `data/test.csv` (8935794 bytes); columns: ["Id", "AGE", "ALT_TAG", "AMENITIES", "AREA", "BALCONY_NUM", "BATHROOM_NUM", "BEDROOM_NUM", "BROKERAGE", "BUILDING_ID", "BUILDING_NAME", "BUILTUP_SQFT", "CARPET_SQFT", "CITY", "CITY_ID", "CITY_NAME", "CLASS", "CLASS_HEADING", "CLASS_LABEL", "COMMON_FURNISHING_ATTRIBUTES", "CONTACT_COMPANY_NAME", "CONTACT_NAME", "DESCRIPTION", "EXPIRY_DATE", "FACING", "FEATURES", "FLOOR_NUM", "FSL_Data", "FURNISH", "FURNISHING_ATTRIBUTES", "LISTING", "LOCALITY", "LOCALITY_WO_CITY", "MAP_DETAILS", "MAX_AREA_SQFT", "MIN_AREA_SQFT", "OWNTYPE", "POSTING_DATE", "PREFERENCE", "PRIMARY_TAGS", "PRODUCT_TYPE", "PROJ_ID", "PROPERTY_NUMBER", "PROPERTY_TYPE", "PROPERTY_TYPE__U", "PROP_HEADING", "PROP_ID", "PROP_NAME", "QUALITY_SCORE", "REGISTERED_DAYS", "REGISTER_DATE", "REGISTER_DATE__U", "RES_COM", "SECONDARY_AREA", "SECONDARY_TAGS", "SOCIETY_NAME", "SPID", "SUPERAREA_UNIT", "SUPERBUILTUP_SQFT", "SUPER_AREA", "SUPER_SQFT", "TOP_USPS", "TOTAL_FLOOR", "TOTAL_LANDMARK_COUNT", "TRANSACT_TYPE", "UPDATE_DATE", "VALUE_LABEL", "VERIFIED", "location"]
- `data/train.csv` (35592895 bytes); columns: ["Id", "AGE", "ALT_TAG", "AMENITIES", "AREA", "BALCONY_NUM", "BATHROOM_NUM", "BEDROOM_NUM", "BROKERAGE", "BUILDING_ID", "BUILDING_NAME", "BUILTUP_SQFT", "CARPET_SQFT", "CITY", "CITY_ID", "CITY_NAME", "CLASS", "CLASS_HEADING", "CLASS_LABEL", "COMMON_FURNISHING_ATTRIBUTES", "CONTACT_COMPANY_NAME", "CONTACT_NAME", "DESCRIPTION", "EXPIRY_DATE", "FACING", "FEATURES", "FLOOR_NUM", "FSL_Data", "FURNISH", "FURNISHING_ATTRIBUTES", "LISTING", "LOCALITY", "LOCALITY_WO_CITY", "MAP_DETAILS", "MAX_AREA_SQFT", "MIN_AREA_SQFT", "OWNTYPE", "POSTING_DATE", "PREFERENCE", "PRIMARY_TAGS", "PRODUCT_TYPE", "PROJ_ID", "PROPERTY_NUMBER", "PROPERTY_TYPE", "PROPERTY_TYPE__U", "PROP_HEADING", "PROP_ID", "PROP_NAME", "QUALITY_SCORE", "REGISTERED_DAYS", "REGISTER_DATE", "REGISTER_DATE__U", "RES_COM", "SECONDARY_AREA", "SECONDARY_TAGS", "SOCIETY_NAME", "SPID", "SUPERAREA_UNIT", "SUPERBUILTUP_SQFT", "SUPER_AREA", "SUPER_SQFT", "TOP_USPS", "TOTAL_FLOOR", "TOTAL_LANDMARK_COUNT", "TRANSACT_TYPE", "UPDATE_DATE", "VALUE_LABEL", "VERIFIED", "location", "price_inr"]

## Public description

Indian Real Estate Price Prediction Challenge (Multi-City 99acres)

Files provided
- train.csv: Training data with features and the target column price_inr.
- test.csv: Test data with the same feature columns (no target).
- sample_submission.csv: A sample file illustrating the required submission format.
- facets/: Optional mapping dictionaries for decoding categorical IDs.

Submission format
- CSV with exactly two columns: Id, price_inr
- Id must match the Ids provided in test.csv.
- price_inr must be a valid non-negative number for every row.

Evaluation
- Metric: Root Mean Squared Log Error (RMSLE) on price_inr.
