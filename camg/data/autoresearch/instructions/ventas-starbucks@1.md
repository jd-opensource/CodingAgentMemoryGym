# OpenMLE-fast task

Task ID: `ventas-starbucks@1`

Native metric: `StarbucksPrepTimeMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3125 bytes)
- `data/sample_submission.csv` (22970 bytes); columns: ["ID_Venta", "Demora_Preparación_Min"]
- `data/test.csv` (124604 bytes); columns: ["ID_Venta", "Fecha", "Hora", "Sucursal", "Nombre_Producto", "Categoría_Producto", "Tamaño", "Cantidad", "Precio_Unitario", "Total_Venta", "Método_de_Compra", "Método_de_Pago", "Cliente_Miembro", "Descuento_Miembro", "Promoción_Aplicada", "Empleado_Atendió", "Turno", "Stock_Antes"]
- `data/train.csv` (634273 bytes); columns: ["ID_Venta", "Fecha", "Hora", "Sucursal", "Nombre_Producto", "Categoría_Producto", "Tamaño", "Cantidad", "Precio_Unitario", "Total_Venta", "Método_de_Compra", "Método_de_Pago", "Cliente_Miembro", "Descuento_Miembro", "Promoción_Aplicada", "Empleado_Atendió", "Turno", "Demora_Preparación_Min", "Stock_Antes"]

## Public description

Title: Starbucks Order Prep Time Prediction

Background
Starbucks stores fulfill heterogeneous orders (espresso drinks, tea, bakery, snacks, merchandise) across multiple branches and purchase/payment channels. Preparation time varies with product mix, size, store load, staff, and promotions. Accurately forecasting prep time helps staffing, throughput planning, and customer experience.

Problem statement
Given an order’s details at the moment it is placed, predict the preparation time in minutes (Demora_Preparación_Min).

Files provided
- train.csv: Tabular data with features and the target column Demora_Preparación_Min.
- test.csv: Same features as train.csv but without the target column.
- sample_submission.csv: Example submission with columns [ID_Venta, Demora_Preparación_Min].

Target and features
- Target: Demora_Preparación_Min (continuous, minutes).
- Key feature columns available at order time include: Fecha, Hora, Sucursal, Empleado_Atendió, Turno, Nombre_Producto, Categoría_Producto, Tamaño, Cantidad, Precio_Unitario, Método_de_Compra, Método_de_Pago, Cliente_Miembro, Descuento_Miembro, Promoción_Aplicada, Stock_Antes, ID_Venta.
- Columns recorded after service or that can introduce leakage are excluded from the released train/test: Satisfacción_Cliente, Stock_Después.
- Note: Total_Venta equals Cantidad × Precio_Unitario and adds no new information beyond those two; participants may choose to drop or use it.

Split policy
The data is split chronologically to mimic real deployment and avoid temporal leakage: orders from January to March 2025 are in the training set; orders from April 2025 are in the test set.

Suggested feature engineering
- Temporal features from Fecha and Hora: hour, minute, day-of-week, weekend flag, month, interactions with store/shift.
- Categorical encoding: one-hot for low-cardinality (Sucursal, Método_de_Compra, Método_de_Pago, Cliente_Miembro, Promoción_Aplicada, Turno); regularized target encoding or hashing for higher-cardinality (Nombre_Producto, Empleado_Atendió).
- Size handling: treat missing Tamaño as an explicit category (e.g., "NA").
- Price/quantity: use Precio_Unitario and Cantidad; Total_Venta is redundant.
- Operations proxy: Stock_Antes as an indicator of inventory pressure.

Evaluation metric
Submissions are evaluated with Mean Absolute Error (MAE) on Demora_Preparación_Min for the test set. MAE measures the average absolute difference in minutes between predictions and ground truth, is robust to outliers, and aligns with operational impact.

Submission format
Submit a CSV with two columns:
- ID_Venta: the identifier from test.csv
- Demora_Preparación_Min: your predicted preparation time in minutes (numeric, finite).

Quality and challenge
- The dataset contains 5,000 orders with diverse products, channels, stores, shifts, and promotions.
- Nonlinear interactions and high-cardinality fields make the task challenging yet solvable with tabular ML (e.g., gradient boosting, regularized linear models, neural nets with categorical encoders).
- The time-aware split tests generalization to a future month.
