# OpenMLE-fast task

Task ID: `protein-and-nutrient-content-of-5000-food-items@1`

Native metric: `FoodNutrientClassificationMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2853 bytes)
- `data/sample_submission.csv` (9015 bytes); columns: ["FDC_ID", "Category"]
- `data/test.csv` (50894 bytes); columns: ["FDC_ID", "Protein_g_per_100g", "Calories_per_100g", "Fat_g_per_100g", "Carbs_g_per_100g", "Fiber_g_per_100g", "Vitamin_A_RAE", "Vitamin_C_mg", "Vitamin_D_µg", "Vitamin_B12_µg", "Calcium_mg", "Iron_mg", "Magnesium_mg", "Potassium_mg", "Zinc_mg", "Calories_per_gram_Protein"]
- `data/train.csv` (220714 bytes); columns: ["FDC_ID", "Protein_g_per_100g", "Calories_per_100g", "Fat_g_per_100g", "Carbs_g_per_100g", "Fiber_g_per_100g", "Vitamin_A_RAE", "Vitamin_C_mg", "Vitamin_D_µg", "Vitamin_B12_µg", "Calcium_mg", "Iron_mg", "Magnesium_mg", "Potassium_mg", "Zinc_mg", "Calories_per_gram_Protein", "Category"]

## Public description

Competition: Nutrient Fingerprints — Classify Food Category from USDA Nutrient Panels

Problem statement
- Given the per-100g nutrient profile of a food item, predict its broad food category. You will build a multi-class classifier over 13+ categories (e.g., vegetables, meat, fruits, eggs, grains, fish, nuts, dairy, legumes, seafood, etc.). The released data excludes textual fields and redundant columns to avoid leakage and focus on measured nutrients.

Files provided
- train.csv: Training data with features and the target label (Category).
- test.csv: Test data with the same features (without labels).
- sample_submission.csv: A valid example submission with random labels.

Data description
- Identifier: FDC_ID (row ID, not a feature).
- Target: Category (string label).
- Features (numeric per 100g):
  - Protein_g_per_100g
  - Calories_per_100g
  - Fat_g_per_100g
  - Carbs_g_per_100g
  - Fiber_g_per_100g
  - Vitamin_A_RAE
  - Vitamin_C_mg
  - Vitamin_D_µg
  - Vitamin_B12_µg
  - Calcium_mg
  - Iron_mg
  - Magnesium_mg
  - Potassium_mg
  - Zinc_mg
  - Calories_per_gram_Protein

Notes on preprocessing
- Obvious anomalies in macros are clipped to reasonable bounds (e.g., negative carbs are set to 0, macros limited to [0, 100] g per 100g).
- Vitamins and minerals are kept as measured; you may consider robust scaling or log transforms due to skew.
- No text fields or redundant columns are included, preventing keyword leakage.

Task and expectations
- Develop an ML pipeline that includes data processing, feature engineering, model training, and model evaluation.
- Consider domain-informed features (e.g., macro ratios, protein-to-calorie efficiency, mineral density) and appropriate scaling/regularization.
- Both classic ML (e.g., logistic regression, SVMs, tree ensembles) and modern tabular methods are applicable.

Evaluation metric
- Macro-averaged F1 score across all categories.
- Why macro F1: Class distribution is imbalanced; this metric weights each class equally, rewarding correct predictions on minority classes as well as dominant ones.

Submission format
- Submit a CSV with exactly two columns: FDC_ID and Category.
- Include one row per test item; IDs must match those in test.csv exactly.
- Category values are free-form strings, but scoring uses the ground-truth label set; ensure you predict only valid categories present in the training data.

Important considerations
- Do not attempt to reconstruct labels from hidden information; focus on nutrient-driven signals.
- There is no validation split provided; perform your own cross-validation within train.csv if needed for model selection.
- Deterministic split ensures reproducibility; every label present in the test set occurs in the training set at least once.

Good luck and have fun building robust, fair models that understand nutrient fingerprints!
