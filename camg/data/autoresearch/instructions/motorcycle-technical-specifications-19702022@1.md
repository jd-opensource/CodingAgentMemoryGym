# OpenMLE-fast task

Task ID: `motorcycle-technical-specifications-19702022@1`

Native metric: `MotorcycleCategoryMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (4114 bytes)
- `data/sample_submission.csv` (142112 bytes); columns: ["id", "Category"]
- `data/test.csv` (4669961 bytes); columns: ["id", "Brand", "Model", "Year", "Rating", "Displacement (ccm)", "Power (hp)", "Torque (Nm)", "Engine cylinder", "Engine stroke", "Gearbox", "Bore (mm)", "Stroke (mm)", "Fuel capacity (lts)", "Fuel system", "Fuel control", "Cooling system", "Transmission type", "Dry weight (kg)", "Wheelbase (mm)", "Seat height (mm)", "Front brakes", "Rear brakes", "Front tire", "Rear tire", "Front suspension", "Rear suspension", "Color options", "raw_Model", "raw_Year", "raw_Rating", "raw_Displacement", "raw_Engine type", "raw_Engine details", "raw_Power", "raw_Top speed", "raw_Bore x stroke", "raw_Fuel system", "raw_Ignition", "raw_Cooling system", "raw_Gearbox", "raw_Transmission type", "raw_Driveline", "raw_Frame type", "raw_Front suspension", "raw_Rear suspension", "raw_Wheels", "raw_Seat", "raw_Dry weight", "raw_Power/weight ratio", "raw_Clutch", "raw_Overall width", "raw_Fuel capacity", "raw_Comments", "raw_Exhaust system", "raw_Compression", "raw_Fuel control", "raw_Lubrication system", "raw_Front tire", "raw_Rear tire", "raw_Front brakes", "raw_Rear brakes", "raw_Weight incl. oil, gas, etc", "raw_Overall length", "raw_Ground clearance", "raw_Wheelbase", "raw_Oil capacity", "raw_Color options", "raw_Starter", "raw_Electrical", "raw_Valves per cylinder", "raw_Diameter", "raw_Carrying capacity", "raw_Modifications compared to previous model", "raw_Seat height", "raw_Overall height", "raw_Fuel consumption", "raw_Greenhouse gases", "raw_Torque", "raw_Max RPM", "raw_Light", "raw_Alternate seat height", "raw_Rake (fork angle)", "raw_0-100 km/h (0-62 mph)", "raw_Front wheel travel", "raw_Rear wheel travel", "raw_Engine oil", "raw_Instruments", "raw_60-140 km/h (37-87 mph), highest gear", "raw_Front percentage of weight", "raw_Trail", "raw_Brake fluid", "raw_Coolant", "raw_Spark plugs", "raw_Idle speed", "raw_Tire pressure front", "raw_Tire pressure rear", "raw_Fork tube size", "raw_Chain links", "raw_Sprockets", "raw_Reserve fuel capacity", "raw_1/4 mile (0.4 km)", "raw_Emission details", "raw_Rear percentage of weight", "raw_Oil filter", "raw_Battery", "raw_Belt teeth", "raw_Belt width", "raw_Pulley teeth", "raw_Chain size", "raw_Factory warranty", "raw_Service interval"]
- `data/train.csv` (19033591 bytes); columns: ["id", "Brand", "Model", "Year", "Category", "Rating", "Displacement (ccm)", "Power (hp)", "Torque (Nm)", "Engine cylinder", "Engine stroke", "Gearbox", "Bore (mm)", "Stroke (mm)", "Fuel capacity (lts)", "Fuel system", "Fuel control", "Cooling system", "Transmission type", "Dry weight (kg)", "Wheelbase (mm)", "Seat height (mm)", "Front brakes", "Rear brakes", "Front tire", "Rear tire", "Front suspension", "Rear suspension", "Color options", "raw_Model", "raw_Year", "raw_Rating", "raw_Displacement", "raw_Engine type", "raw_Engine details", "raw_Power", "raw_Top speed", "raw_Bore x stroke", "raw_Fuel system", "raw_Ignition", "raw_Cooling system", "raw_Gearbox", "raw_Transmission type", "raw_Driveline", "raw_Frame type", "raw_Front suspension", "raw_Rear suspension", "raw_Wheels", "raw_Seat", "raw_Dry weight", "raw_Power/weight ratio", "raw_Clutch", "raw_Overall width", "raw_Fuel capacity", "raw_Comments", "raw_Exhaust system", "raw_Compression", "raw_Fuel control", "raw_Lubrication system", "raw_Front tire", "raw_Rear tire", "raw_Front brakes", "raw_Rear brakes", "raw_Weight incl. oil, gas, etc", "raw_Overall length", "raw_Ground clearance", "raw_Wheelbase", "raw_Oil capacity", "raw_Color options", "raw_Starter", "raw_Electrical", "raw_Valves per cylinder", "raw_Diameter", "raw_Carrying capacity", "raw_Modifications compared to previous model", "raw_Seat height", "raw_Overall height", "raw_Fuel consumption", "raw_Greenhouse gases", "raw_Torque", "raw_Max RPM", "raw_Light", "raw_Alternate seat height", "raw_Rake (fork angle)", "raw_0-100 km/h (0-62 mph)", "raw_Front wheel travel", "raw_Rear wheel travel", "raw_Engine oil", "raw_Instruments", "raw_60-140 km/h (37-87 mph), highest gear", "raw_Front percentage of weight", "raw_Trail", "raw_Brake fluid", "raw_Coolant", "raw_Spark plugs", "raw_Idle speed", "raw_Tire pressure front", "raw_Tire pressure rear", "raw_Fork tube size", "raw_Chain links", "raw_Sprockets", "raw_Reserve fuel capacity", "raw_1/4 mile (0.4 km)", "raw_Emission details", "raw_Rear percentage of weight", "raw_Oil filter", "raw_Battery", "raw_Belt teeth", "raw_Belt width", "raw_Pulley teeth", "raw_Chain size", "raw_Factory warranty", "raw_Service interval"]

## Public description

Motorcycle Market Category Prediction

Problem statement
Given a motorcycle’s technical specifications and textual descriptors for a specific brand-model-year, predict its market Category. The task is a multi-class classification problem with 18+ categories (e.g., Scooter, Sport, Enduro / offroad, Cruiser, Naked, Touring, etc.). Participants should leverage both structured specs and free-text attributes to build robust models.

Data description
You are provided three CSV files to build your solution:
- train.csv: Labeled training data. Each row corresponds to one motorcycle (brand-model-year). Columns include an id column, a rich set of cleaned technical specifications and textual descriptors, and the target column Category.
- test.csv: Unlabeled test data with the same feature columns as train.csv (excluding Category) and an id column aligned to the submission.
- sample_submission.csv: A sample file containing id and a randomly generated Category value from the valid label set; its format matches the required submission format.

Features
- Structured features derived from curated specifications: brand, model, year, rating, displacement, power, torque, engine configuration and stroke, gearbox, bore, stroke, fuel capacity, fuel system, fuel control, cooling, transmission type, dry weight, wheelbase, seat height, brake types, tires, suspensions, and color options.
- Additional features joined from raw scraped data (prefixed as needed to avoid name collisions): engine details, top speed, ignition, driveline, frame type, seat, power/weight ratio, clutch, dimensions (length/width/height), ground clearance, oil capacity, starter, electrical, valves per cylinder, fuel consumption, greenhouse gases, bore×stroke composite string, and more.
- Some text features may have certain obvious category words (e.g., “scooter”, “enduro”, “cruiser”, “naked”, “touring”, “motard”, etc.) masked to reduce trivial label leakage. All raw category columns are removed from features.

Target
- Category (string): the market segment label for the motorcycle.

Submission format
- A single CSV file with the following columns:
  - id: integer identifier corresponding to rows in test.csv.
  - Category: predicted class label (string) for each id.
- The set of valid labels corresponds to the categories present in train.csv. Your predictions must provide exactly one label per id; no probabilities are submitted.

Evaluation metric
- Macro F1 score over the Category classes present in the test set. For each class that appears at least once in the test set, F1 is computed and then averaged across those classes. This metric equally weights minority and majority classes and discourages collapsing to frequent categories.

Rules and considerations
- Do not attempt to infer labels from file names; they have been sanitized and masked for fairness.
- Text fields may include masked tokens like [redacted] where obvious category terms existed.
- No external data is required. You may use standard pre-trained tokenizers or embeddings if desired, but ensure your submission only includes id and Category.

Recommended approach (non-exhaustive)
- Data processing: normalize and parse numeric units; handle missing values with indicators and sensible imputation; standardize categorical vocabularies (e.g., brakes, transmission, cooling).
- Feature engineering: combine structured specs with TF-IDF or simple embedding representations of text fields; consider interactions (e.g., power-to-weight) and normalized dimensions.
- Modeling: strong baselines include gradient-boosted trees for tabular data combined with TF-IDF for text; more advanced approaches can blend multimodal models.
- Imbalanced learning: use stratified CV, class weighting, sampling, and threshold tuning to improve macro F1.

Files provided
- train.csv
- test.csv
- sample_submission.csv

Notes
- The train/test split is stratified by Category to maintain class coverage; test categories are guaranteed to be a subset of training categories.
- Deterministic behavior is used for the split to ensure reproducibility.
