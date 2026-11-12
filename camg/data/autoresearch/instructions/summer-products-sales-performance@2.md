# OpenMLE-fast task

Task ID: `summer-products-sales-performance@2`

Native metric: `SummerSalesRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (537 bytes)
- `data/merchants_test.csv` (13727 bytes); columns: ["merchant_id", "listedproducts", "rating", "merchantratingscount", "meanproductprices", "meanretailprices", "averagediscount", "meandiscount", "meanproductratingscount", "totalurgencycount", "urgencytextrate"]
- `data/merchants_train.csv` (57767 bytes); columns: ["merchant_id", "listedproducts", "rating", "merchantratingscount", "meanproductprices", "meanretailprices", "averagediscount", "meandiscount", "meanproductratingscount", "totalurgencycount", "urgencytextrate", "totalunitssold"]
- `data/product_catalog_test.csv` (196523 bytes); columns: ["title", "title_orig", "price", "retail_price", "currency_buyer", "uses_ad_boosts", "badges_count", "badge_local_product", "badge_product_quality", "badge_fast_shipping", "tags", "product_color", "product_variation_size_id", "product_variation_inventory", "shipping_option_name", "shipping_option_price", "shipping_is_express", "countries_shipped_to", "inventory_total", "has_urgency_banner", "urgency_text", "origin_country", "merchant_title", "merchant_name", "merchant_info_subtitle", "merchant_id", "merchant_has_profile_picture", "theme", "crawl_month"]
- `data/product_catalog_train.csv` (704012 bytes); columns: ["title", "title_orig", "price", "retail_price", "currency_buyer", "uses_ad_boosts", "badges_count", "badge_local_product", "badge_product_quality", "badge_fast_shipping", "tags", "product_color", "product_variation_size_id", "product_variation_inventory", "shipping_option_name", "shipping_option_price", "shipping_is_express", "countries_shipped_to", "inventory_total", "has_urgency_banner", "urgency_text", "origin_country", "merchant_title", "merchant_name", "merchant_info_subtitle", "merchant_id", "merchant_has_profile_picture", "theme", "crawl_month"]
- `data/sample_submission.csv` (8430 bytes); columns: ["merchant_id", "prediction"]
- `data/tags_global_frequency.csv` (39377 bytes); columns: ["tag", "count"]
- `data/tags_list.csv` (33776 bytes); columns: ["tag"]
- `data/test.csv` (13727 bytes); columns: ["merchant_id", "listedproducts", "rating", "merchantratingscount", "meanproductprices", "meanretailprices", "averagediscount", "meandiscount", "meanproductratingscount", "totalurgencycount", "urgencytextrate"]
- `data/train.csv` (57767 bytes); columns: ["merchant_id", "listedproducts", "rating", "merchantratingscount", "meanproductprices", "meanretailprices", "averagediscount", "meandiscount", "meanproductratingscount", "totalurgencycount", "urgencytextrate", "totalunitssold"]

## Public description

Competition: Merchant-level Summer Sales Forecasting

Files in this public package:
- train.csv
- test.csv
- merchants_train.csv
- merchants_test.csv
- product_catalog_train.csv
- product_catalog_test.csv
- tags_list.csv
- tags_global_frequency.csv
- sample_submission.csv
- description.txt

Target column: totalunitssold (available only in train.csv and merchants_train.csv)
Evaluation: Root Mean Squared Logarithmic Error (RMSLE) on merchant_id.
Submission format: CSV with columns merchant_id,prediction covering exactly the test set.
