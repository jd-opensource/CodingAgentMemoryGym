# OpenMLE-fast task

Task ID: `summer-products-sales-performance@1`

Native metric: `SummerProductsSalesMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3154 bytes)
- `data/sample_submission.csv` (11212 bytes); columns: ["listing_id", "units_sold"]
- `data/test.csv` (198125 bytes); columns: ["listing_id", "title", "title_orig", "price", "retail_price", "currency_buyer", "uses_ad_boosts", "rating", "rating_count", "rating_five_count", "rating_four_count", "rating_three_count", "rating_two_count", "rating_one_count", "badges_count", "badge_local_product", "badge_product_quality", "badge_fast_shipping", "tags", "product_color", "product_variation_size_id", "product_variation_inventory", "shipping_option_name", "shipping_option_price", "shipping_is_express", "countries_shipped_to", "inventory_total", "has_urgency_banner", "urgency_text", "origin_country", "merchant_title", "merchant_name", "merchant_info_subtitle", "merchant_rating_count", "merchant_rating", "merchant_id", "merchant_has_profile_picture"]
- `data/train.csv` (799757 bytes); columns: ["listing_id", "title", "title_orig", "price", "retail_price", "currency_buyer", "units_sold", "uses_ad_boosts", "rating", "rating_count", "rating_five_count", "rating_four_count", "rating_three_count", "rating_two_count", "rating_one_count", "badges_count", "badge_local_product", "badge_product_quality", "badge_fast_shipping", "tags", "product_color", "product_variation_size_id", "product_variation_inventory", "shipping_option_name", "shipping_option_price", "shipping_is_express", "countries_shipped_to", "inventory_total", "has_urgency_banner", "urgency_text", "origin_country", "merchant_title", "merchant_name", "merchant_info_subtitle", "merchant_rating_count", "merchant_rating", "merchant_id", "merchant_has_profile_picture"]

## Public description

Summer Products Demand Forecasting

Problem
E-commerce sellers need to estimate demand for newly listed summer items to make inventory and promotion decisions. Given listing-time metadata (titles, tags, pricing, shipping options, badges, seller profile signals, etc.), predict the number of units each product listing will sell. This is a listing-level regression task with a long-tailed target.

Files provided
- train.csv: Training listings with features and the target units_sold. Includes a unique listing_id for each row.
- test.csv: Test listings with the same columns as train.csv except units_sold is withheld. Includes listing_id for submission matching.
- sample_submission.csv: Example submission file showing the required columns and formatting.

Target
- units_sold (non-negative numeric count)

Key columns and signals (non-exhaustive)
- Pricing and discounts: price, retail_price, currency_buyer, shipping_option_price, shipping_is_express
- Merchant profile: merchant_id, merchant_name, merchant_rating, merchant_rating_count, merchant_has_profile_picture
- Product attributes: title, title_orig, tags, product_color, product_variation_size_id, product_variation_inventory, inventory_total
- Badges/flags: uses_ad_boosts, has_urgency_banner, badges_count, badge_local_product, badge_product_quality, badge_fast_shipping
- Social proof: rating, rating_count, rating_five_count, rating_four_count, rating_three_count, rating_two_count, rating_one_count
- Logistics and reach: origin_country, shipping_option_name, countries_shipped_to
Notes
- Identifiers are provided via listing_id. Raw URLs and externally scrapeable fields are excluded.
- Column availability matches between train.csv and test.csv with the exception of the missing target in test.csv.

Submission format
- A CSV file with exactly two columns in this order:
  1) listing_id: identifier that must exactly match the IDs in test.csv
  2) units_sold: your predicted non-negative numeric count for each listing
- All test listing_id values must be present exactly once. Extra/missing/duplicate IDs, NaN/Inf, or non-numeric predictions invalidate the submission.

Evaluation
- Root Mean Squared Logarithmic Error (RMSLE) on units_sold.
- For each row i with true value y_i and your prediction p_i:
  - y_i_clamped = max(0, y_i)
  - p_i_clamped = max(0, p_i)
  - rmsle = sqrt( mean( (log1p(p_i_clamped) - log1p(y_i_clamped))^2 ) )
- RMSLE treats relative errors fairly across low and high sellers and handles zeros robustly.

Modeling guidance (optional)
- The target is heavy-tailed; log1p-transforming the target internally or using models that handle skew can help.
- Combine structured features with text features from title/tags (e.g., TF-IDF or hashed n-grams) and robust encoders for high-cardinality categoricals.
- Useful engineered features may include discount ratios, price-to-retail ratios, shipping cost flags, and rarity signals derived from tags.

What to submit
- Train your model on train.csv to predict units_sold, and create a submission CSV with the required columns for all rows in test.csv. Ordering of rows does not matter as long as listing_id matches.
