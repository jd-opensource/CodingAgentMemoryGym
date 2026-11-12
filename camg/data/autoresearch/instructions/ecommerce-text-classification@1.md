# OpenMLE-fast task

Task ID: `ecommerce-text-classification@1`

Native metric: `ECommerceTextClassificationMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2835 bytes)
- `data/sample_submission.csv` (240888 bytes); columns: ["id", "label"]
- `data/test.csv` (7508489 bytes); columns: ["id", "text"]
- `data/train.csv` (29822734 bytes); columns: ["id", "text", "label"]

## Public description

E-commerce Product Category Classification from Noisy Descriptions

Background
Marketplaces receive heterogeneous, often noisy product descriptions with a mix of marketing phrases, specifications, sizes, and seller-added tags. Automatically assigning products to the correct catalog category improves search, recommendations, and inventory management at scale.

Problem statement
Given a product’s free‑text description, predict its category among four classes:
- Electronics
- Household
- Books
- Clothing & Accessories

You must build models that generalize beyond simple keyword spotting and handle long, noisy descriptions with overlapping vocabulary.

Data description
- The dataset contains over 50k e-commerce product descriptions labeled with one of the four target categories.
- Texts vary in length and cleanliness (marketing fluff, specs, and seller tags are present). Duplicate descriptions exist by design (e.g., the same product sold by different sellers). This reflects real-world catalog behavior.
- Train/test split is stratified by label and constructed with duplicate‑aware grouping to avoid leakage: identical descriptions (after simple normalization) are kept entirely within either train or test.

Files
- train.csv: id,text,label
- test.csv: id,text
- sample_submission.csv: id,label

Important notes
- Train/test split is group‑wise by identical normalized description (lowercased, trimmed, whitespace‑collapsed). Identical texts never cross the split. Duplicates are retained within a split.
- All provided text is raw; you are free to tokenize, normalize, truncate (for efficiency), and engineer features.
- Labels are consistent and come from the four categories listed above.

Evaluation
Submissions are evaluated using macro‑averaged F1 score across the four classes. Macro‑F1 computes F1 per class and averages them, giving equal weight to each class. This choice is robust to the dataset’s moderate class imbalance and aligns with catalog quality, where both false assignments and misses matter.

Submission format
- A CSV file with two columns and a header: id,label
- The id values must exactly match those in test.csv (order does not matter, but all must be present exactly once).
- The label values must be one of: Electronics, Household, Books, Clothing & Accessories.

Starter ideas (non‑exhaustive)
- Strong classical baselines: word/character TF‑IDF with linear models (logistic regression, linear SVM).
- Deep models: pretrained transformers with appropriate truncation, long‑text handling strategies, and domain‑specific tokenization.
- Feature engineering: n‑grams, subwords/characters, simple rules for common artifacts (SKUs/specs), ensembling.

Good luck, and build models that truly generalize beyond memorization while handling noisy, real‑world text at scale.
