# OpenMLE-fast task

Task ID: `predict-pet-adoption-status-dataset@1`

Native metric: `PetAdoptionMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2445 bytes)
- `data/sample_submission.csv` (9684 bytes); columns: ["PetID", "AdoptionLikelihood"]
- `data/test.csv` (26339 bytes); columns: ["PetID", "PetType", "Breed", "AgeMonths", "Color", "Size", "WeightKg", "Vaccinated", "HealthCondition", "TimeInShelterDays", "AdoptionFee", "PreviousOwner"]
- `data/train.csv` (108189 bytes); columns: ["PetID", "PetType", "Breed", "AgeMonths", "Color", "Size", "WeightKg", "Vaccinated", "HealthCondition", "TimeInShelterDays", "AdoptionFee", "PreviousOwner", "AdoptionLikelihood"]

## Public description

Competition: Predict Pet Adoption Likelihood

Problem statement:
Shelters seek to understand which pet attributes most influence adoption outcomes. Your task is to build a model that predicts the likelihood that a pet will be adopted (AdoptionLikelihood: 0/1) using only the attributes available at listing time. Submit predicted probabilities for the Likely class (1) on the held-out test set.

Data description:
Tabular data with mixed categorical and numerical features. Each row represents one pet listing.
- Features (inputs): PetID (identifier for mapping; not predictive), PetType, Breed, AgeMonths, Color, Size, WeightKg, Vaccinated (0/1), HealthCondition (0/1), TimeInShelterDays, AdoptionFee, PreviousOwner (0/1).
- Target (to predict): AdoptionLikelihood (0 = Unlikely, 1 = Likely).

Files provided:
- train.csv: Training data including features and the target AdoptionLikelihood.
- test.csv: Test data including features only (AdoptionLikelihood not included).
- sample_submission.csv: Example submission file with the required columns and random valid probabilities.

Submission format:
- A single CSV with exactly two columns in this exact order and spelling: PetID, AdoptionLikelihood.
- PetID must match the IDs and order in test.csv exactly.
- AdoptionLikelihood must be a valid probability in [0, 1] representing the predicted likelihood of class 1.

Evaluation metric:
- Primary metric: ROC AUC computed on the predicted probabilities for class 1 (AdoptionLikelihood).
Why this metric: ROC AUC is threshold-independent, robust under moderate class imbalance, and rewards high-quality ranking across all decision thresholds.

Guidance:
- Thorough data processing is encouraged: type casting, handling categorical encoding, and appropriate scaling for your chosen model.
- Suggested feature engineering ideas: age bucketing, interactions (e.g., PetType×Size, Breed×Vaccinated), log-transform AdoptionFee, and exploration of non-linear relationships.
- Class imbalance exists; consider stratification, class weighting, or loss adjustments in training.
- Avoid leakage: treat all features as available at listing time; use PetID only for submission linkage.

Goal:
Deliver well-calibrated probabilities and strong ranking performance across diverse pet types and attributes. This is a realistic, challenging tabular ML task where careful preprocessing, feature engineering, and model selection can substantially improve results.
