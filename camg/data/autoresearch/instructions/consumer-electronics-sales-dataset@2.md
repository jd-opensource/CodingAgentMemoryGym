# OpenMLE-fast task

Task ID: `consumer-electronics-sales-dataset@2`

Native metric: `ConsumerElectronicsSatisfactionMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2305 bytes)
- `data/sample_submission.csv` (12385 bytes); columns: ["Id", "CustomerSatisfaction"]
- `data/test.csv` (87043 bytes); columns: ["Id", "ProductCategory", "ProductBrand", "ProductPrice", "CustomerAge", "CustomerGender", "PurchaseFrequency"]
- `data/train.csv` (362833 bytes); columns: ["Id", "ProductCategory", "ProductBrand", "ProductPrice", "CustomerAge", "CustomerGender", "PurchaseFrequency", "CustomerSatisfaction"]

## Public description

Predict post‑purchase customer satisfaction (1–5) from consumer electronics sales records.

Problem statement
Participants must build a model that predicts a customer’s post‑purchase satisfaction rating (integer 1–5) using product attributes, customer demographics, and purchase behavior. The task is an ordinal classification problem: misclassifying by 2 points is worse than by 1.

Files provided
- train.csv: Training data with features and the target column CustomerSatisfaction.
- test.csv: Test data with the same features as train.csv, without CustomerSatisfaction.
- sample_submission.csv: A sample submission file with the correct format and randomly generated valid labels.

Columns
- Id: Unique row identifier.
- ProductCategory: Categorical product category (e.g., Smartphones, Laptops, Tablets, Headphones, Smart Watches).
- ProductBrand: Categorical brand (e.g., Apple, Samsung, Sony, HP, Other Brands).
- ProductPrice: Numeric price in USD.
- CustomerAge: Integer age of the customer.
- CustomerGender: Binary indicator (0 = Male, 1 = Female).
- PurchaseFrequency: Integer average number of purchases per year.
- CustomerSatisfaction (train.csv only): Integer in {1, 2, 3, 4, 5}.

Target
- Predict CustomerSatisfaction for each row in test.csv as an integer in {1, 2, 3, 4, 5}.

Evaluation
- Primary metric: Quadratic Weighted Kappa (QWK), computed between your integer predictions and the ground-truth labels. QWK accounts for the ordinal nature of the labels by penalizing larger disagreements more than smaller ones and is robust to near‑uniform class frequencies.

Submission format
- CSV file with exactly two columns and a header: Id,CustomerSatisfaction
- One row per Id present in test.csv.
- CustomerSatisfaction must be an integer in {1,2,3,4,5}.

Modeling guidance (informative, not mandatory)
- Treat the task as ordinal classification or calibrated regression to optimize QWK.
- Effective preprocessing often includes: encoding of ProductCategory and ProductBrand; scaling or transformation of ProductPrice, CustomerAge, and PurchaseFrequency; interaction features such as Brand×Category; and non-linear transforms (e.g., log‑price).
- Consider stratified cross‑validation on the training data.

Final data files
- train.csv
- test.csv
- sample_submission.csv
