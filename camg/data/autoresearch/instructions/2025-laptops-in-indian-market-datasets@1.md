# OpenMLE-fast task

Task ID: `2025-laptops-in-indian-market-datasets@1`

Native metric: `LaptopPriceMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2920 bytes)
- `data/sample_submission.csv` (25114 bytes); columns: ["id", "price"]
- `data/test.csv` (648953 bytes); columns: ["id", "name", "name_raw", "brand", "os", "os_raw", "cpu_brand", "cpu_name", "cpu_type", "cpu_cores", "cpu_threads", "cpu1", "cpu2", "gpu_brand", "gpu_name", "gpu_vram", "gpu_text", "ram_capacity", "ram_ddr_type", "ram_text", "hdd", "ssd", "hdd_raw", "ssd_raw", "screen_size", "aspect_ratio_category", "screen_res", "ppi", "display", "touchscreen", "is_gaming"]
- `data/train.csv` (2629998 bytes); columns: ["id", "name", "name_raw", "brand", "os", "os_raw", "cpu_brand", "cpu_name", "cpu_type", "cpu_cores", "cpu_threads", "cpu1", "cpu2", "gpu_brand", "gpu_name", "gpu_vram", "gpu_text", "ram_capacity", "ram_ddr_type", "ram_text", "hdd", "ssd", "hdd_raw", "ssd_raw", "screen_size", "aspect_ratio_category", "screen_res", "ppi", "display", "touchscreen", "is_gaming", "price"]

## Public description

# Indian Laptop Price Prediction 2025

Problem statement
Predict the retail price (INR) of laptops sold in the Indian market as of 2025. You are provided with structured specifications and raw listing text. Build models that generalize across brands, CPU/GPU tiers, RAM/storage/display configurations, and noisy listing language.

Data overview
Final training and test files contain a multi-modal set of features:
- Structured specs (from cleaned data): brand, os, cpu_brand, cpu_name, cpu_type, cpu_cores, cpu_threads, gpu_brand, gpu_name, gpu_vram (GB), ram_capacity (GB), ram_ddr_type, hdd (GB), ssd (GB), screen_size (inches), aspect_ratio_category, screen_res (categorical bands), ppi (numeric when available), touchscreen (0/1).
- Raw text (from uncleaned listings): name_raw, cpu1 (generation/model), cpu2 (core/thread text), ram_text, hdd_raw, ssd_raw, gpu_text, display (size + resolution + touch indicator), os_raw, warranty.
- Cleaned name string (name) is also provided; use both name and name_raw for text features.
- Convenience flag: is_gaming (inferred from discrete GPU or listing text) to assist stratification-aware modeling.

Target
- price (INR) in the training file.
- In the test file, participants must predict price for each row.

Files provided
- train.csv: Features + price.
- test.csv: Features only (no price).
- sample_submission.csv: id, price. A valid example submission with random numeric predictions.

Split policy and leakage control
- Train/test split is deterministic, group-aware by normalized product name to prevent identical models crossing splits.
- Stratification by brand and gaming flag is applied at the group level to balance distribution.
- Opaque or potentially leaky fields (spec_score, user_rating) are excluded.

Evaluation
- Metric: Root Mean Squared Log Error (RMSLE) on price.
- Definition: sqrt(mean((log1p(y_pred) - log1p(y_true))^2))).
- Rationale: Prices span a wide range; RMSLE rewards proportional accuracy and reduces outsized influence of premium outliers while remaining sensitive to errors across the spectrum.

Modeling guidance
- Make use of both structured features and raw text. Suggested techniques:
  - Robust preprocessing and entity resolution between name and specs.
  - Feature engineering: CPU/GPU families and suffixes, integrated vs discrete GPU, RAM/SSD/HDD quantities, display resolution and size interactions, touch flag.
  - Text features: token/n-gram features from name, cpu1, gpu_text, display.
  - Models: gradient boosting, regularized linear models, tabular deep nets with embeddings; optionally combine text via TF-IDF or embeddings.

Submission format
- CSV with columns: id, price.
- Exactly one row per test id. Price must be non-negative finite numeric.

Notes
- Keep numeric precision and handle missing values robustly (e.g., gpu_vram=0 may indicate integrated GPU).
- Do not include any filesystem paths in the CSV files.
