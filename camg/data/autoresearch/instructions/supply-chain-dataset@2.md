# OpenMLE-fast task

Task ID: `supply-chain-dataset@2`

Native metric: `ShipmentRiskClassificationMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (467 bytes)
- `data/sample_submission.csv` (519965 bytes); columns: ["shipment_id", "risk_classification"]
- `data/test.csv` (4569946 bytes); columns: ["shipment_id", "warehouse_inventory_level", "handling_equipment_availability", "order_fulfillment_status", "weather_condition_severity", "shipping_costs", "supplier_reliability_score", "lead_time_days", "historical_demand", "cargo_condition_status", "route_risk_level", "customs_clearance_time", "disruption_likelihood_score", "delay_probability", "delivery_time_deviation", "product_id", "supplier_id", "supplier_country"]
- `data/train.csv` (19231206 bytes); columns: ["shipment_id", "warehouse_inventory_level", "handling_equipment_availability", "order_fulfillment_status", "weather_condition_severity", "shipping_costs", "supplier_reliability_score", "lead_time_days", "historical_demand", "cargo_condition_status", "route_risk_level", "customs_clearance_time", "disruption_likelihood_score", "delay_probability", "delivery_time_deviation", "product_id", "supplier_id", "supplier_country", "risk_classification"]

## Public description

Competition: Shipment Risk Classification for Supply Chain Operations

Files under public/:
- train.csv
- test.csv
- sample_submission.csv
- description.txt

Submission format:
- CSV with exactly two columns: shipment_id and risk_classification.
- shipment_id must match the IDs provided in test.csv.
- risk_classification must be one of: High Risk, Moderate Risk, Low Risk.

Evaluation metric:
- Macro F1 across High Risk, Moderate Risk, Low Risk. Higher is better.
