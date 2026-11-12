# OpenMLE-fast task

Task ID: `park-biodiversity@1`

Native metric: `ParkBiodiversityMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3172 bytes)
- `data/sample_submission.csv` (170565 bytes); columns: ["row_id", "abundance"]
- `data/test.csv` (1461378 bytes); columns: ["row_id", "park_code", "park_name", "state", "acres", "latitude", "longitude", "category", "order", "family", "genus", "scientific_name", "common_names", "nativeness", "seasonality", "conservation_status"]
- `data/train.csv` (6761399 bytes); columns: ["row_id", "park_code", "park_name", "state", "acres", "latitude", "longitude", "category", "order", "family", "genus", "scientific_name", "common_names", "nativeness", "seasonality", "conservation_status", "abundance"]

## Public description

Competition: Predict Species Abundance in US National Parks

Overview
You are given tabular records of plant and animal species verified as present in US national parks. For each species–park record, predict the abundance class describing how common the species is within that park. The target is ordinal with five ordered categories: Rare < Occasional < Uncommon < Common < Abundant.

Why this is challenging and meaningful
- Abundance is ordered and imbalanced across parks and taxa.
- Records combine taxonomy, nativeness, seasonality, conservation status, and park geospatial attributes, requiring careful data processing and feature engineering.
- The test set consists of entire parks held out from training, measuring generalization to unseen parks and ecosystems and preventing same-park leakage.

Files provided
- train.csv: Feature columns plus the target column abundance.
- test.csv: Feature columns only. Predict abundance for these rows.
- sample_submission.csv: Example submission with row_id and abundance. Replace abundance with your predictions.

Columns
- row_id: Unique identifier for each species–park record (neutral; carries no label information).
- park_code: Park code (e.g., ACAD).
- park_name: Park name.
- state: US state(s) of the park.
- acres: Park area in acres.
- latitude, longitude: Park centroid coordinates.
- category: Taxonomic class (e.g., Mammal, Bird, Plant).
- order: Taxonomic order.
- family: Taxonomic family.
- genus: Derived from the first token of scientific_name.
- scientific_name: Latin binomial or trinomial.
- common_names: Comma-separated English common names (text).
- nativeness: Whether the species is Native, Not Native, or Unknown.
- seasonality: Nature of presence when available (e.g., Resident, Breeder, Migratory, Vagrant).
- conservation_status: USFWS status when present (e.g., Endangered, Species of Concern); may be empty.
- abundance (train.csv only): Target class in {Rare, Occasional, Uncommon, Common, Abundant}.

Task and submission format
- Predict the abundance for each row in test.csv.
- Valid predictions must be exactly one of: Rare, Occasional, Uncommon, Common, Abundant.
- Submit a CSV with two columns: row_id, abundance. The row_id values must exactly match those in test.csv.

Evaluation
- Metric: Quadratic Weighted Kappa (QWK) computed on the ordered classes Rare < Occasional < Uncommon < Common < Abundant.
- QWK penalizes distant misclassifications more than near ones and adjusts for chance agreement, making it suitable for ordinal, imbalanced targets.
- Higher is better; scores range from 0 to 1.

Guidance
- The split is at the park level: all species from held-out parks appear exclusively in the test set.
- Use the full data; do not subset. Robust feature engineering is beneficial (e.g., encoding high-cardinality taxonomy, extracting genus, leveraging text in common_names, and geospatial features).
- Handle missing values explicitly and encode categorical variables carefully. Consider ordinal-aware modeling strategies.
- Suitable approaches include gradient-boosted trees, regularized linear models, deep tabular networks, and hybrid text–tabular architectures.
