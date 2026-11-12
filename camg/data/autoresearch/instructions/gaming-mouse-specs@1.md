# OpenMLE-fast task

Task ID: `gaming-mouse-specs@1`

Native metric: `GamingMouseWeightMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3138 bytes)
- `data/sample_submission.csv` (5626 bytes); columns: ["row_id", "Weight (grams)"]
- `data/test.csv` (62587 bytes); columns: ["Size", "Length (mm)", "Width (mm)", "Height (mm)", "Shape", "Hand compatibility", "Hump placement", "Front flare", "Side curvature", "Thumb rest", "Ring finger rest", "Sensor", "Sensor type", "Sensor position", "DPI", "Polling rate (Hz)", "Tracking speed (IPS)", "Acceleration (G)", "Side buttons", "Middle buttons", "Hot-swap switches", "Switches", "Scroll wheel encoder", "Material", "Connectivity", "Sensor brand", "Switches brand", "Scroll wheel encoder brand", "Sensor position category", "Sensor position percent", "Body volume proxy", "Wireless battery proxy", "Material_flag_magnesium", "Material_flag_carbon", "row_id"]
- `data/train.csv` (265622 bytes); columns: ["Size", "Length (mm)", "Width (mm)", "Height (mm)", "Weight (grams)", "Shape", "Hand compatibility", "Hump placement", "Front flare", "Side curvature", "Thumb rest", "Ring finger rest", "Sensor", "Sensor type", "Sensor position", "DPI", "Polling rate (Hz)", "Tracking speed (IPS)", "Acceleration (G)", "Side buttons", "Middle buttons", "Hot-swap switches", "Switches", "Scroll wheel encoder", "Material", "Connectivity", "Sensor brand", "Switches brand", "Scroll wheel encoder brand", "Sensor position category", "Sensor position percent", "Body volume proxy", "Wireless battery proxy", "Material_flag_magnesium", "Material_flag_carbon", "row_id"]

## Public description

Gaming Mouse Weight Prediction Challenge

Overview
Build a model that predicts the weight (in grams) of a gaming mouse from its full specification. Weight influences aim precision and fatigue; it emerges from device dimensions, materials, internal components, and connectivity. Your task is to estimate Weight (grams) for held‑out models using the provided training set and submit predictions for the test set.

Files
- train.csv: Training data including all features and the target column Weight (grams).
- test.csv: Test data with the same feature columns as train.csv except the target. Includes a row_id column to join predictions.
- sample_submission.csv: Example of a valid submission file format with random but valid predictions.

Target
- Weight (grams) — continuous value to be predicted.

Input features
Use the information provided in train.csv and test.csv. They include mixed‑type design and performance attributes such as:
- Dimensional: Size, Length (mm), Width (mm), Height (mm)
- Ergonomics: Shape, Hand compatibility, Hump placement, Front flare, Side curvature, Thumb rest, Ring finger rest
- Performance and components: Sensor, Sensor type, Sensor position (also includes parsed category and percent), DPI, Polling rate (Hz), Tracking speed (IPS), Acceleration (G), Side buttons, Middle buttons, Hot-swap switches, Switches, Scroll wheel encoder
- Materials and build: Material, Connectivity, Sensor brand, Switches brand, Scroll wheel encoder brand
- Engineered features: Body volume proxy, Wireless battery proxy, Material flags, Sensor position category/percent
Note: Identity columns (brand or model names) are intentionally excluded to avoid label leakage and promote generalization from specifications.

Task
- Train any regression model to predict Weight (grams) in test.csv. You may perform data processing and feature engineering. External data and pretraining are allowed if they comply with the dataset license.

Evaluation
- Primary metric: Mean Absolute Error (MAE) in grams between your predictions and the ground truth on the hidden test labels. MAE directly reflects average error in grams and is robust to outliers.

Submission format
- CSV with two columns and header: row_id, Weight (grams)
- One row per test example; row_id values must match those in test.csv exactly.
- Weight (grams) must be numeric and finite.

Suggested approach (non-binding)
- Parsing: treat the original data as semicolon‑separated with some missing values. In train/test, columns are already cleaned and numeric where appropriate.
- Feature engineering ideas: interactions between size and materials, non‑linear transforms, aggregates of dimensional features, and encodings for high‑cardinality categoricals.
- Modeling: tree ensembles (Gradient Boosting, Random Forest, XGBoost/LightGBM/CatBoost) and tabular neural networks can capture non‑linear effects.

Notes
- The official split stratifies by connectivity and weight distribution to support fair comparison across device types.
- All rows in test use only specifications and do not contain identity‑revealing fields.

Good luck and happy modeling!
