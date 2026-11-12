# OpenMLE-fast task

Task ID: `smart-agricultural-production-optimizing-engine@1`

Native metric: `CropRecommendationMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (474 bytes)
- `data/sample_submission.csv` (209182 bytes); columns: ["id", "apple", "banana", "blackgram", "chickpea", "coconut", "coffee", "cotton", "grapes", "jute", "kidneybeans", "lentil", "maize", "mango", "mothbeans", "mungbean", "muskmelon", "orange", "papaya", "pigeonpeas", "pomegranate", "rice", "watermelon"]
- `data/test.csv` (31756 bytes); columns: ["id", "N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
- `data/train.csv` (141058 bytes); columns: ["id", "N", "P", "K", "temperature", "humidity", "ph", "rainfall", "label"]

## Public description

Title: Crop Recommendation under Soil and Weather Constraints

Files in this competition (relative to public/):
- train.csv: Training data with features and labels. Columns: id, N, P, K, temperature, humidity, ph, rainfall, label
- test.csv: Test data with features only (no labels). Columns: id, N, P, K, temperature, humidity, ph, rainfall
- sample_submission.csv: Example submission file. Columns: id plus one column per crop class (probabilities that sum to 1 per row).
