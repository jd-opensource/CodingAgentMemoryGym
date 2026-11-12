# OpenMLE-fast task

Task ID: `superstore-dataset@1_duplicate_1`

Native metric: `SuperstoreLossMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2991 bytes)
- `data/sample_submission.csv` (79880 bytes); columns: ["Row ID", "Loss"]
- `data/test.csv` (586327 bytes); columns: ["Row ID", "Order Date", "Ship Mode", "Customer ID", "Segment", "Country", "City", "State", "Postal Code", "Region", "Product ID", "Category", "Sub-Category", "Product Name", "Quantity", "Discount"]
- `data/train.csv` (1194325 bytes); columns: ["Row ID", "Order Date", "Ship Mode", "Customer ID", "Segment", "Country", "City", "State", "Postal Code", "Region", "Product ID", "Category", "Sub-Category", "Product Name", "Quantity", "Discount", "Loss"]

## Public description

Superstore Loss Prediction Challenge

Background
A large retail superstore records detailed information for every order line item, including dates, customer segment, product category, discounts, quantities, and geographic information. Some line items incur a loss (negative profit). Anticipating these loss-making items at the time of order enables better discounting and fulfillment decisions.

Problem Statement
Given tabular features available at order time, predict the probability that a line item will be loss-making. Participants must build models that output calibrated probabilities for each test line item being a loss.

Data Description
The competition dataset is derived from historical superstore order line items. Each row represents a single line item in an order. The following columns are provided:
- Identifiers and timestamps: Row ID, Order Date
- Customer and fulfillment: Ship Mode, Customer ID, Segment, Country, City, State, Postal Code, Region
- Product information: Product ID, Category, Sub-Category, Product Name
- Transactional inputs: Quantity, Discount

Files Provided
- train.csv: Training data with features and the target column Loss (float 0.0 or 1.0), one row per line item.
- test.csv: Test data with the same features as train.csv except the Loss column is omitted.
- sample_submission.csv: Sample submission file containing Row ID and a Loss column with example probability values.

Target Definition
Loss is defined as 1.0 if Profit < 0, else 0.0.

Split Strategy
To emulate real-world deployment and avoid leakage, the split is time-aware by Order Date:
- Train contains orders from 2014–2016.
- Test contains orders from 2017.

Evaluation Metric
Submissions are evaluated using Log Loss on the Loss label. Participants must submit a probability for each test row:
- Lower log loss indicates better performance.
- Predictions must be valid probabilities in [0, 1].

Submission Format
- A CSV file with two columns: Row ID and Loss.
- Row ID must exactly match those in test.csv.
- Loss must be a probability per row (float in [0, 1]).

Modeling Guidance
- Parse and utilize temporal features derived from Order Date (e.g., year, month, weekday).
- Handle high-cardinality categorical variables (e.g., Product ID, Product Name, City, State, Postal Code) via target encoding, hashing, embeddings, or regularized methods.
- Address class imbalance via class weighting or other appropriate techniques; do not alter the test distribution.
- Avoid leakage by not using Sales, Profit, or Ship Date.

Quality and Integrity Notes
- All line items are uniquely identified by Row ID.
- The split is deterministic and contains entire orders strictly within one side of the split by year.
- The label distribution is moderately imbalanced but both classes appear in train and test.

Deliverables
- Submit your probability predictions for Loss using the sample_submission.csv format.
- Use train.csv for model development; do not assume access to hidden columns.
