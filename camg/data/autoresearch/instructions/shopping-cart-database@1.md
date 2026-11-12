# OpenMLE-fast task

Task ID: `shopping-cart-database@1`

Native metric: `ShoppingCartPriceMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/customers_public.csv` (59992 bytes); columns: ["customer_id", "gender", "age", "zip_code", "city", "state", "country"]
- `data/description.txt` (3438 bytes)
- `data/orders_public.csv` (28623 bytes); columns: ["order_id", "customer_id", "order_date", "delivery_date"]
- `data/products_public.csv` (45418 bytes); columns: ["product_ID", "product_type", "product_name", "size", "colour", "price", "quantity"]
- `data/sample_submission.csv` (21804 bytes); columns: ["sales_id", "price_per_unit"]
- `data/test.csv` (14285 bytes); columns: ["sales_id", "order_id", "product_id", "quantity"]
- `data/test_sales.csv` (14285 bytes); columns: ["sales_id", "order_id", "product_id", "quantity"]
- `data/train.csv` (74238 bytes); columns: ["sales_id", "order_id", "product_id", "price_per_unit", "quantity"]
- `data/train_sales.csv` (74238 bytes); columns: ["sales_id", "order_id", "product_id", "price_per_unit", "quantity"]

## Public description

Title: Line-item Unit Price Prediction (Relational Tabular)

Problem statement
You are given a synthetic e-commerce relational dataset containing customer, order, product, and line-item (sales) tables. For each sales line, predict the realized price_per_unit at the time of purchase. Prices vary by product attributes, size/colour, seasonality (order date), and customer/order context. Your task is to build a model that estimates price_per_unit for each test sales line using the relational structure of the data.

Files
- train_sales.csv: Sales lines for training, including the target column price_per_unit.
- test_sales.csv: Sales lines for testing; identical schema to train_sales.csv except price_per_unit is withheld.
- products_public.csv: Product catalog with attributes (e.g., product_type, product_name, size, colour, base price, inventory quantity).
- orders_public.csv: Orders table with order_date and delivery_date per order_id.
- customers_public.csv: Customer demographics and geography (age, gender, zip_code, city, state, country).
- sample_submission.csv: A valid example submission file providing the expected format.

Target and keys
- Target: price_per_unit (numeric) in train_sales.csv only.
- Join keys:
  - train_sales/test_sales.product_id -> products_public.product_ID
  - train_sales/test_sales.order_id   -> orders_public.order_id
  - orders_public.customer_id         -> customers_public.customer_id
- Row identifier for submission: sales_id in test_sales.csv

Important notes (leakage avoided in provided files)
- The sales total line amount and order payment reference are not provided to avoid trivial leakage of price_per_unit.
- Fine-grained addresses and names are removed; city/state/zip/country provide geographic signal without PII granularity.

Recommended feature engineering (not exhaustive)
- Time features from order_date: year, month, day, day-of-week, week-of-year, quarter, month-end indicator.
- Lead time: (delivery_date - order_date).days.
- Basket context at the order level: number of lines, total quantity, unique products/types/colours, per-type mix, and quantity statistics.
- Product attributes: product_type, product_name, size, colour, base price, inventory quantity.
- Customer features: age, age buckets, gender, geographic encodings.
- Categorical encoding for high-cardinality fields (e.g., product_name, city).

Evaluation
- Metric: Mean Absolute Error (MAE) between your predictions and the ground truth price_per_unit for the test set.
- Lower is better.

Submission format
Submit a single CSV with the following columns and no header extras or index:
- sales_id: integer identifier matching the rows in test_sales.csv
- price_per_unit: your predicted numeric price per unit

Example (see sample_submission.csv for the full file):

sales_id,price_per_unit
4001,103.7
4002,98.2
...

Train/test split policy
- Split is performed by order_id so that all lines from the same order are either entirely in train or entirely in test.
- The test set contains a broad mix of products, sizes, colours, and dates to encourage generalization.

Rules and expectations
- Use only the provided files to build your features.
- Do not attempt to infer hidden labels via external resources.
- Remember that the test labels are withheld; ensure your submission conforms exactly to the required format.

Good luck, and enjoy the challenge of relational feature engineering for price modeling!
