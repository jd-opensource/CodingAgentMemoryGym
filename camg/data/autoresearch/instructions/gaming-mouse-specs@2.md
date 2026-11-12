# OpenMLE-fast task

Task ID: `gaming-mouse-specs@2`

Native metric: `MouseSensorBrandMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3597 bytes)
- `data/sample_submission.csv` (4324 bytes); columns: ["id", "sensor_brand"]
- `data/test.csv` (49445 bytes); columns: ["id", "Size", "Length (mm)", "Width (mm)", "Height (mm)", "Shape", "Hand compatibility", "Hump placement", "Front flare", "Side curvature", "Thumb rest", "Ring finger rest", "Sensor type", "Sensor position", "DPI", "Polling rate (Hz)", "Tracking speed (IPS)", "Acceleration (G)", "Side buttons", "Middle buttons", "Hot-swap switches", "Switches", "Scroll wheel encoder", "Material", "Connectivity", "Switches brand", "Scroll wheel encoder brand"]
- `data/train.csv` (208461 bytes); columns: ["id", "Size", "Length (mm)", "Width (mm)", "Height (mm)", "Shape", "Hand compatibility", "Hump placement", "Front flare", "Side curvature", "Thumb rest", "Ring finger rest", "Sensor type", "Sensor position", "DPI", "Polling rate (Hz)", "Tracking speed (IPS)", "Acceleration (G)", "Side buttons", "Middle buttons", "Hot-swap switches", "Switches", "Scroll wheel encoder", "Material", "Connectivity", "Switches brand", "Scroll wheel encoder brand", "sensor_brand"]

## Public description

Kaggle Competition: Who Made the Sensor? Inferring Sensor Brand from Mouse Specs

Problem statement
Predict the sensor vendor used in a gaming mouse (target: sensor_brand) from its published specifications. Identity fields (brand/model/name) and the exact sensor model are withheld to prevent memorization, so participants must learn relationships between performance limits, ergonomics, electronics, and connectivity and the likely sensor supplier.

Why this is interesting
- Gaming mice often share sensor suppliers (e.g., PixArt) but have diverse designs and electronics. Vendors exhibit characteristic capability envelopes (e.g., DPI, IPS, acceleration ceilings, polling support) and are correlated with certain build choices.
- The task is a realistic imbalanced multiclass classification problem requiring robust preprocessing, encoding, regularization, and class-imbalance strategies.

Files provided
- train.csv: tabular training data including features and the target column sensor_brand.
- test.csv: tabular test data with the same feature columns as train.csv but without sensor_brand.
- sample_submission.csv: a sample submission with the required columns and example predictions.

Target
- sensor_brand (multiclass string label).

Feature space (columns retained)
All available non-identifying specification fields are kept to maximize learnability while preventing leakage:
- Size
- Length (mm), Width (mm), Height (mm)
- Shape, Hand compatibility, Hump placement, Front flare, Side curvature
- Thumb rest, Ring finger rest
- Sensor type, Sensor position
- DPI, Polling rate (Hz), Tracking speed (IPS), Acceleration (G)
- Side buttons, Middle buttons, Hot-swap switches
- Switches, Scroll wheel encoder, Material, Connectivity
- Switches brand, Scroll wheel encoder brand
Notes:
- Identity/leakage-prone columns are excluded: Brand, Model, Name, Sensor (exact sensor model). Weight (grams) is also excluded to avoid indirect leakage via vendor-specific weight conventions.
- Raw categorical text is intentionally preserved. Participants are encouraged to perform careful cleaning and encoding (e.g., trimming whitespace, mapping Yes/No to booleans, decomposing Sensor position like "Forward (56%)").

Recommended preprocessing (non-exhaustive)
- Trim and standardize text; treat '-' or empty as missing. Cast numeric fields; consider log transforms for DPI/IPS.
- Decompose Sensor position into position_category and position_offset_percent.
- Build volume proxy L×W×H; add a wireless indicator from Connectivity.
- Consider robust encoders (target/leave-one-out with K-fold, CatBoost, entity embeddings) and class weighting.

Evaluation
- Metric: Macro-averaged F1 score over the label set present in the test data. Each class contributes equally, rewarding models that work on minority vendors. The score ranges from 0 to 1.
- Submission format: CSV with two columns: id, sensor_brand. It must include exactly the same ids as in test.csv. Labels are case-sensitive strings.

Rules and caveats
- Only use the provided features; do not attempt to recover identity columns or exact sensor names from external sources. The challenge is to generalize from specifications, not to perform string matching.
- The test set contains only labels that appear at least once in the training set.

Baseline ideas
- Strong baselines include: gradient boosting trees on engineered numeric/categorical features, CatBoost/LightGBM with thoughtful encoding and class weights, or regularized linear models on one-hot/target encoded variables. Ensembling usually helps.

Good luck and happy modeling!
