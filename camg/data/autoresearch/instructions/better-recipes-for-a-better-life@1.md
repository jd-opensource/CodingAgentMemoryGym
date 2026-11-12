# OpenMLE-fast task

Task ID: `better-recipes-for-a-better-life@1`

Native metric: `RecipeRatingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3105 bytes)
- `data/sample_submission.csv` (3295 bytes); columns: ["id", "rating"]
- `data/test.csv` (211005 bytes); columns: ["id", "name", "ingredients", "directions", "prep_time", "cook_time", "total_time", "servings", "yield"]
- `data/train.csv` (795015 bytes); columns: ["id", "name", "ingredients", "directions", "prep_time", "cook_time", "total_time", "servings", "yield", "rating"]

## Public description

Title: Recipe Rating Prediction from Ingredients and Directions

Problem statement:
Predict the final user rating (1.0–5.0 stars, continuous) of a recipe using its textual content (ingredients and directions) and basic preparation metadata (prep/cook/total time, servings, yield, and name). The task simulates cold-start quality estimation and recommendation, relying only on information available before anyone cooks the recipe.

Data description:
- Training file: train.csv
  - Columns:
    - id: anonymized recipe identifier
    - name: recipe title
    - ingredients: list-like textual ingredients
    - directions: step-by-step textual instructions
    - prep_time, cook_time, total_time: durations as human-readable strings (may contain missing placeholders)
    - servings: number of servings as string (may include ranges)
    - yield: yield text (e.g., 6 servings, 1 9-inch pie; may be empty)
    - rating: target variable (float in [1.0, 5.0])
- Test file: test.csv
  - Same columns as train.csv except rating is not provided.
- Sample submission: sample_submission.csv
  - A valid example with randomized ratings matching the expected format.

Notes:
- ids are anonymized to prevent external lookups; they do not correspond to external URLs.
- Times and quantities are provided as heterogeneous strings; participants are expected to normalize/parse them thoughtfully. Empty values are represented by a placeholder so they are safely read as strings.
- Use only features present in both train.csv and test.csv for modeling.
- Avoid using any external data sources; solve the problem with the provided files only.

Evaluation:
- Metric: Root Mean Squared Error (RMSE) between predictions and ground truth ratings.
- Submission format: a CSV file named submission.csv with two columns:
  - id: matches the ids in test.csv
  - rating: your predicted continuous rating for each id
- RMSE is computed after validating format and clipping predictions to [1.0, 5.0] to ensure numerical stability.

Modeling guidance:
- Text processing: normalize unicode fractions; standardize units; split ingredients into items; tokenize directions into steps; extract cooking verbs, temperatures, durations, and step counts.
- Feature engineering: parse times to minutes; convert servings/yield to numeric estimates and categorical units; encode length/complexity features (ingredients count, steps count, average step length).
- Modeling: start with TF-IDF + linear models; progress to gradient boosting with engineered features; consider transformer-based encoders for ingredients and directions (multi-input fusion).
- Evaluation: pay attention to calibration across the bounded rating range; penalize large errors more heavily under RMSE.

Files provided to participants:
- train.csv: training set with target ratings.
- test.csv: test set without ratings.
- sample_submission.csv: a valid example submission with randomized ratings in the correct format.

Important rules:
- Ensure deterministic preprocessing pipelines fitted on training data only.
- Do not attempt to recover labels via external resources.
