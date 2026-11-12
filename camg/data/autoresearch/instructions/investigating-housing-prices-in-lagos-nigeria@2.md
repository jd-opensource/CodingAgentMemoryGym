# OpenMLE-fast task

Task ID: `investigating-housing-prices-in-lagos-nigeria@2`

Native metric: `LagosNeighborhoodMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3133 bytes)
- `data/sample_submission.csv` (72180 bytes); columns: ["id", "Neighboorhood"]
- `data/test.csv` (484813 bytes); columns: ["id", "Property_name", "Address", "ContractType"]
- `data/train.csv` (2045264 bytes); columns: ["id", "Property_name", "Address", "ContractType", "Neighboorhood"]

## Public description

Competition: Lagos Neighborhood Inference from Listing Text

Problem statement
Predict the neighborhood (Neighboorhood) of Lagos real-estate listings using only the free‑text Property_name and Address and a ContractType flag (rent or sale). Listings contain noisy, repetitive phrasing and references to estates, landmarks, and roads. To prevent trivial leakage, explicit neighborhood mentions and common aliases have been deterministically masked with the token [NEIGH]. Your job is to build robust text models that recognize the remaining linguistic and contextual cues.

Files you will use
- train.csv: id, Property_name, Address, ContractType, Neighboorhood
- test.csv: id, Property_name, Address, ContractType
- sample_submission.csv: id, Neighboorhood

Target
- Neighboorhood: multiclass label covering many Lagos areas with a long‑tail distribution.

Input features
- Property_name: free‑text listing title (masked for explicit neighborhood mentions).
- Address: free‑text address/description (masked for explicit neighborhood mentions).
- ContractType: categorical text in {rent, sale}.
- Note: Numeric price is intentionally excluded to avoid indirect leakage via price-by-neighborhood distributions.

Evaluation
- Metric: Macro F1 across all neighborhoods present in the test set.
- Definition: Compute F1 for each class separately (zero_division=0 when a class isn’t predicted) and report the unweighted mean across classes.
- Rationale: Macro F1 treats all neighborhoods fairly despite strong class imbalance and encourages balanced performance rather than focusing on dominant classes.

Submission format
- A CSV with columns: id, Neighboorhood.
- Every id from test.csv must appear exactly once. Extra or missing ids lead to invalid submissions.

Masking details
- Explicit neighborhood tokens and common aliases have been replaced with [NEIGH] in both Property_name and Address. The masking is case-insensitive and robust to hyphen/space variants (e.g., Lekki, Lekki Phase 1, Ibeju-Lekki, Ajah, Yaba, Ikoyi, VI/Victoria Island, Ikeja, Gbagada, Kosofe/Ikosi, Shomolu, Alapere, Ilupeju, Isolo, Igando, Ojo, Ojodu, Magodo, Ikota, Jakande, Chevron, Sangotedo, Oral Estate, etc.). This leaves genuine predictive signal such as estates, roads, landmarks, and nearby localities.

Recommended approach
- Text processing: basic normalization; consider robust tokenization and handling of misspellings/abbreviations.
- Feature engineering: character/word n‑grams; TF‑IDF; subword embeddings; transformer encoders; concatenating Property_name and Address; include ContractType.
- Modeling: multiclass classification with techniques that address imbalance (class weights, focal loss, sampling/thresholding strategies).
- Validation: stratified cross‑validation by Neighboorhood is recommended. Consider grouping highly similar titles/addresses to reduce leakage within folds.

Rules and constraints
- Do not submit files with duplicated or missing ids.
- External data is not required; the released texts are already masked to reduce leakage.

Good luck building robust text models for Lagos real‑estate listings!
