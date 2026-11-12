# OpenMLE-fast task

Task ID: `summer-products-and-sales-in-ecommerce-wish@1`

Native metric: `WishSalesRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (4459 bytes)
- `data/merchants.csv` (65656 bytes); columns: ["merchant_id", "rating", "merchantratingscount", "meanproductprices", "meanretailprices", "averagediscount", "meandiscount", "meanproductratingscount", "totalurgencycount", "urgencytextrate"]
- `data/sample_submission.csv` (11576 bytes); columns: ["product_id", "units_sold"]
- `data/test.csv` (176066 bytes); columns: ["title", "title_orig", "price", "retail_price", "currency_buyer", "uses_ad_boosts", "rating", "rating_count", "rating_five_count", "rating_four_count", "rating_three_count", "rating_two_count", "rating_one_count", "badges_count", "badge_local_product", "badge_product_quality", "badge_fast_shipping", "tags", "product_color", "product_variation_size_id", "product_variation_inventory", "shipping_option_name", "shipping_option_price", "shipping_is_express", "countries_shipped_to", "inventory_total", "has_urgency_banner", "urgency_text", "origin_country", "merchant_title", "merchant_name", "merchant_info_subtitle", "merchant_rating_count", "merchant_rating", "merchant_id", "merchant_has_profile_picture", "product_id", "theme", "crawl_month"]
- `data/train.csv` (710723 bytes); columns: ["title", "title_orig", "price", "retail_price", "currency_buyer", "units_sold", "uses_ad_boosts", "rating", "rating_count", "rating_five_count", "rating_four_count", "rating_three_count", "rating_two_count", "rating_one_count", "badges_count", "badge_local_product", "badge_product_quality", "badge_fast_shipping", "tags", "product_color", "product_variation_size_id", "product_variation_inventory", "shipping_option_name", "shipping_option_price", "shipping_is_express", "countries_shipped_to", "inventory_total", "has_urgency_banner", "urgency_text", "origin_country", "merchant_title", "merchant_name", "merchant_info_subtitle", "merchant_rating_count", "merchant_rating", "merchant_id", "merchant_has_profile_picture", "product_id", "theme", "crawl_month"]
- `data/unique-categories.csv` (33775 bytes); columns: ["tag"]
- `data/unique-categories.sorted-by-count.csv` (39384 bytes); columns: ["count", "keyword"]

## Public description

Competition: Predicting Sales Performance of Summer Products on Wish

Problem statement:
Given product-level attributes captured at crawl time on the Wish platform for items returned by the “summer” query, predict the number of units sold for each product listing. The goal is to build a model that generalizes across merchants and product types to accurately estimate sales counts, enabling better pricing/discount decisions and catalog optimization.

Data description:
- train.csv: Product-level tabular data with all features and the target column units_sold.
- test.csv: Same columns as train.csv except units_sold (the target is withheld).
- merchants.csv: Merchant-level aggregated features that can be joined to train/test via merchant_id. Columns are curated to avoid target leakage.
- unique_categories.csv and unique-categories.sorted-by-count.csv: Canonicalized tag keywords and their global frequencies to help feature engineering from the free-form tags column.
- sample_submission.csv: Example submission file with deterministic random predictions adhering to the required format.

Features overview (non-exhaustive):
- Pricing and discounts: price, retail_price, derived discount potential, shipping_option_price.
- Ratings: rating, rating_count, rating_five_count to rating_one_count (distribution), merchant_rating and merchant_rating_count.
- Merchandising and exposure: uses_ad_boosts, badges_count and badge_* flags, has_urgency_banner, urgency_text.
- Product attributes: title, title_orig, tags (free-form, multi-lingual), product_color, product_variation_size_id, product_variation_inventory, inventory_total, origin_country, theme, crawl_month.
- Shipping: shipping_option_name, shipping_is_express, countries_shipped_to.
- Merchant-level join features (from merchants.csv): rating, merchantratingscount, meanproductprices, meanretailprices, averagediscount, meandiscount, meanproductratingscount, totalurgencycount, urgencytextrate. Note: merchants.csv has no units_sold-derived aggregates to prevent leakage.

Official split:
A single official train/test split is provided. The split preserves scale and diversity of the dataset and is constructed deterministically with merchant-aware logic so that merchants with multiple listings appear in both train and test, where possible.

Evaluation metric:
Root Mean Squared Logarithmic Error (RMSLE) on units_sold.
- Definition: RMSLE = sqrt(mean( (log(1 + y_true) - log(1 + y_pred))^2 ))
- Rationale: Sales counts are heavy-tailed and vary across products and merchants. RMSLE is robust to outliers, penalizes multiplicative errors, and treats over- and under-predictions symmetrically in log space, providing a fair and precise assessment of model quality.

Submission format:
- A CSV file with exactly two columns named: product_id, units_sold
- Must contain one row per product_id in test.csv, no duplicates and no missing rows.
- units_sold predictions must be non-negative finite numbers (float or integer). Negative predictions are invalid.

Recommended approaches:
- Data processing and cleaning: deduplication, robust parsing of multi-lingual titles (French/English), normalization of pricing and discount features, consistent handling of missing values.
- Feature engineering:
  - Pricing: discount_pct = max(0, 1 - price/retail_price), absolute_discount.
  - Ratings distribution: shares per star level, entropy of ratings, rating density.
  - Inventory and shipping: availability and express shipping flags; shipping cost.
  - Merchant join: join merchants.csv on merchant_id for non-leaky aggregate signals.
  - Tags: parse free-form tags; leverage unique_categories files to map to canonical categories and weight by global frequency.
- Modeling: tree-based ensembles (GBDT, XGBoost, LightGBM, CatBoost), regularized linear models with interaction features, and NLP features or embeddings from titles and tags.
- Evaluation: use RMSLE; validate predictions are non-negative and numerically stable.

Files provided:
- train.csv
- test.csv
- merchants.csv
- unique_categories.csv
- unique-categories.sorted-by-count.csv
- sample_submission.csv

Rules and fairness:
- Work strictly within provided files; no external data fetching.
- The merchants.csv file has been curated to exclude any units_sold-derived aggregates (e.g., listedproducts, totalunitssold, meanunitssoldperproduct) to prevent target leakage.
- Single official split only; do not rely on any hidden labels.
