# OpenMLE-fast task

Task ID: `historical-sales-data-on-daily-basis-of-a-company@1`

Native metric: `DailySalesForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3581 bytes)
- `data/sample_submission.csv` (18035 bytes); columns: ["Date", "Article_ID", "Country_Code", "Predicted"]
- `data/test.csv` (14857 bytes); columns: ["Date", "Article_ID", "Country_Code"]
- `data/train.csv` (272367 bytes); columns: ["Date", "Article_ID", "Country_Code", "Sold_Units"]

## Public description

Historical Hierarchical Sales Forecasting (Daily, Article × Country)

Problem statement
You are given daily online sales of a company across multiple countries and articles from 2017-01-01 to 2019-02-13. Many dates per series are not recorded in the raw logs; those correspond to zero sales and must be treated as such. Your task is to forecast Sold_Units for a fixed future horizon at the base level (Article_ID × Country_Code). Your predictions will be evaluated not only at the base level but also when aggregated to countries and to the global total.

Deliverables
- Submit a CSV with rows for each required (Date, Article_ID, Country_Code) in the forecast horizon and a Predicted column.
- Column order must be exactly: Date, Article_ID, Country_Code, Predicted.
- Date must be formatted as YYYY-MM-DD.

Data description
- train.csv: Fully expanded daily panel from 2017-01-01 to 2018-12-31 for all observed Article_ID × Country_Code series. Missing dates in the raw logs are filled with Sold_Units = 0. Columns: Date, Article_ID, Country_Code, Sold_Units.
- test.csv: The keys for the forecast horizon from 2019-01-01 to 2019-02-13 (44 consecutive days). Columns: Date, Article_ID, Country_Code.
- sample_submission.csv: A valid sample submission with plausible predictions for the required keys.

Modeling guidance
- Use all of the provided training data. Build features and models that account for intermittent demand, weekly seasonality, and cross-series information if you like (e.g., pooled models).
- Useful approaches include exponential smoothing/ETS, ARIMA/SARIMA, Prophet, Croston/TSB for intermittent demand, gradient boosting or tree-based models with calendar and lag features, and neural time-series models.
- Ensure your base-level forecasts remain reasonable when aggregated to countries and the global total; the metric rewards coherence.

Evaluation metric: Hierarchical Weighted RMSSE (WRMSSE)
Your submission is evaluated across three levels and averaged:
- Level 2 (base): Article_ID × Country_Code series.
- Level 1: Country totals (aggregate across articles within each country).
- Level 0: Global total (aggregate across all countries and articles).

For any series s, RMSSE is computed as:
- Numerator: RMSE over the 44-day forecast horizon.
- Denominator: Root mean squared first difference of the corresponding training series for s (a scale/volatility term). When the training series is flat or undefined, a robust fallback scale is used to avoid division by zero.

Level weights within each level are proportional to the series’ total Sold_Units over the training window and normalized to sum to 1. The final score is the simple average of the three level-wise weighted scores. Lower is better.

Constraints and rules
- Use only the provided data files to train your models; external data is not required or expected.
- Do not assume that missing dates imply anything other than zero sales.
- Do not rely on file names or any artifacts that might leak labels—only use the contents of train.csv.

Files provided to participants
- train.csv
- test.csv
- sample_submission.csv

Submission format
- CSV with columns: Date, Article_ID, Country_Code, Predicted.
- Exactly one row per key in test.csv; no duplicates or extra rows.

Tips
- Calendar-based features (weekday, month, holidays by country if modeled generatively), rolling lags, and cross-series pooling can improve performance.
- Consider models that can handle zero-inflation and spikes.
- Coherent forecasting strategies (e.g., reconciliation) may help under hierarchical scoring.
