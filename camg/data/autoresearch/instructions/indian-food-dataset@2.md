# OpenMLE-fast task

Task ID: `indian-food-dataset@2`

Native metric: `IndianRecipeCourseMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2567 bytes)
- `data/sample_submission.csv` (26116 bytes); columns: ["id", "Course"]
- `data/test.csv` (4706618 bytes); columns: ["id", "RecipeName", "TranslatedRecipeName", "Ingredients", "TranslatedIngredients", "PrepTimeInMins", "CookTimeInMins", "TotalTimeInMins", "Servings", "Cuisine", "Diet", "Instructions", "TranslatedInstructions"]
- `data/train.csv` (18931632 bytes); columns: ["id", "RecipeName", "TranslatedRecipeName", "Ingredients", "TranslatedIngredients", "PrepTimeInMins", "CookTimeInMins", "TotalTimeInMins", "Servings", "Cuisine", "Diet", "Instructions", "TranslatedInstructions", "Course"]

## Public description

Title: Recipe Course Classification Challenge

Problem statement:
Predict the Course category of a recipe (e.g., Lunch, Snack, Dessert, Appetizer, Breakfast types, etc.) using its text and metadata. Each sample contains multilingual recipe text (original + translated) and structured fields. Your task is to build robust classifiers that infer the course type from ingredients, instructions, names, and contextual features.

Data description:
- train.csv: Training set with features and the target label.
- test.csv: Test set with features only. Predictions are evaluated on this set.
- sample_submission.csv: A sample file illustrating the required submission format.

Columns provided in train/test:
- id: Unique identifier for each recipe.
- RecipeName
- TranslatedRecipeName
- Ingredients
- TranslatedIngredients
- PrepTimeInMins
- CookTimeInMins
- TotalTimeInMins
- Servings
- Cuisine
- Diet
- Instructions
- TranslatedInstructions
- In train.csv only: Course (target label)

Notes:
- The dataset includes both original and translated text fields. Use them together for stronger signals.
- Excluded fields (e.g., URL, source identifiers) are not provided to prevent identity leakage.
- Class distribution is imbalanced. Many classes are large (Lunch, Side Dish, Snack, Dinner, Dessert, Appetizer), while some are scarce (certain breakfast and diet-specific classes). Models should avoid overfitting to majority classes.

Evaluation metric:
- Macro-averaged F1 across all Course classes present in the test set.
- This treats all classes equally and rewards balanced performance, especially on minority classes.

Submission format:
- CSV with two columns: id, Course
- id must exactly match those in test.csv.
- Course must be one of the labels found in train.csv.

Guidelines and recommendations:
- Text processing: normalize case, tokenize recipe names, ingredients, and instructions; consider n-grams, domain vocabulary (e.g., frying/baking cues), and multilingual handling.
- Feature engineering: combine text embeddings/TF‑IDF with tabular features (cuisine, diet, servings, prep/cook/total times).
- Modeling: Multiclass classification with techniques such as linear models on bag-of-words, gradient boosting over engineered features, or transformer-based embeddings fused with tabular features.
- Evaluation: Use stratified validation locally where possible; monitor macro-F1 to ensure minority classes are not ignored.

Files to use:
- train.csv
- test.csv
- sample_submission.csv

Good luck, and enjoy exploring Indian cuisine and recipe understanding!
