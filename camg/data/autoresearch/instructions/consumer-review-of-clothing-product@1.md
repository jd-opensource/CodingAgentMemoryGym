# OpenMLE-fast task

Task ID: `consumer-review-of-clothing-product@1`

Native metric: `ClothingReviewClassificationMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2510 bytes)
- `data/sample_submission.csv` (135892 bytes); columns: ["id", "label"]
- `data/test.csv` (2521778 bytes); columns: ["id", "Title", "Review", "Cons_rating", "Materials", "Construction", "Color", "Finishing", "Durability"]
- `data/train.csv` (10405373 bytes); columns: ["id", "Title", "Review", "Cons_rating", "Materials", "Construction", "Color", "Finishing", "Durability", "label"]

## Public description

Title: Clothing Category Prediction from Consumer Reviews

Problem statement:
Given free-form Title and Review text describing clothing products, predict the product category label for each review. Categories include common apparel types (e.g., Dresses, Pants, Knits, Sweaters, etc.). Reviews are noisy, with misspellings, shorthand, and varied writing styles. Participants should build robust NLP models that leverage text along with optional structured signals to accurately classify each item into its correct category.

Data description:
- train.csv: Labeled training data containing the following columns:
  - id: Unique identifier for each record
  - Title: Short headline written by the reviewer (may be empty)
  - Review: Main review text
  - Cons_rating: Integer rating (e.g., 1–5)
  - Materials, Construction, Color, Finishing, Durability: Binary aspect flags extracted from reviews
  - label: Target category for classification (valid categories are all unique values appearing in this column)
- test_data.csv: Unlabeled test data with the same feature columns as train.csv, except without the label column.
- sample_submission.csv: A sample file demonstrating the expected submission format.

Task:
Train a machine learning model that predicts the category label for each row in the test data using the provided text fields and any additional features you find useful. The dataset contains multiple apparel categories with class imbalance and linguistic noise; careful preprocessing, feature engineering, and model selection are important.

Submission format:
- A CSV file with two columns: id and label
- id must match the values in test_data.csv exactly, and each id must appear once
- label must be a valid category string (case-sensitive) consistent with the categories present in train.csv

Evaluation metric:
- Macro F1 score across all categories
- F1 is computed per class and averaged equally, rewarding performance on minority classes
- Invalid labels or missing ids will result in a rejected submission

Notes and recommendations:
- Text cleaning, tokenization, and embeddings can substantially improve performance
- Consider using the numeric rating and aspect flags as auxiliary features
- Ensure predictions are valid category strings and avoid NaNs or empty labels
- Calibrate decision thresholds to optimize macro F1 under class imbalance
- You may use any modeling approach (e.g., classic bag-of-words, TF-IDF + linear models, pretrained language models, or multimodal features)
