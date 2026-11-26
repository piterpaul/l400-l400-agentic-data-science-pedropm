---
description: Standards for BigQuery AI (TimesFM 2.5 GA, TimesFM 3.0 Preview with covariates, TabFM AI.PREDICT, AI.KEY_DRIVERS), BigQuery ML (ARIMA_PLUS_XREG, BOOSTED_TREE, TRANSFORM), and Open-Weight Foundation Models via bigquery-data-science & Data Agent Kit
---

# BigQuery AI & BigQuery ML Standards

## 0. Skill Routing Across Tiers (`Data Agent Kit` + `bigquery-data-science`)

Never guess `AI.*`/`ML.*` signatures or `CREATE MODEL` options from memory:
- **Tier 0 (Managed Conversational Analytics + Zero-DDL `AI.*` Floor):** `geminidataanalytics.googleapis.com` calls `AI.FORECAST` (`TimesFM 2.5`), `AI.DETECT_ANOMALIES`, and `AI.KEY_DRIVERS` dynamically. Use Data Agent Kit (`bigquery-ai-ml`) and `bigquery-data-science` (`bigquery-ai`) in `agy` to inspect `AI.*` limits and materialize the gap-filled spine and `AI.EVALUATE` holdout floor.
- **Tier 1 (In-Warehouse SQL + BQML):** Use **`bigquery-data-science` (`bigquery-ml`)** (`ARIMA_PLUS_XREG`, `BOOSTED_TREE_*`, `MATRIX_FACTORIZATION`, `ML.EXPLAIN_PREDICT`, `ML.EXPLAIN_FORECAST`) plus Data Agent Kit (`discovering-gcp-data-assets`, `data-autocleaning`, `bigquery-sql`, `dataform-bigquery`, `bigquery-data-transfer-service`, `bigquery-graph-author`, `bigquery-graph-query`).
- **Tier 2 & Tier 3 (Managed Cloud Python, Spark & Streaming — Zero Local Compute):** Pair `bigquery-data-science` (`bigquery-mlops`) with Data Agent Kit (`bigquery-bigframes`, `gcp-spark`, `ml-best-practices`, `gcp-pipeline-orchestration`, `gcp-managed-airflow-dag-authoring`, `gcp-dataflow`, `bigtable-basics`, `cloud-databases-onboarding`). Never fit models locally on the Cloudtop VM (`.to_pandas()` on training data and `master("local")` are banned); execute via `Vertex AI CustomJob`, `bigframes.ml` (`model.to_gbq()`), `Managed Service for Apache Spark Serverless` (`gcloud dataproc batches submit pyspark`), or `BQML`.
- **CLI Lookup:** `uvx bigquery-data-science lookup <SYMBOL>` (`AI.FORECAST`, `AI.PREDICT`, `ARIMA_PLUS_XREG`).

## 1. Tier 0 Foundation Model TVFs (Zero Training)

Always benchmark Tier 0 before training custom models:
- **`AI.FORECAST` (`TimesFM 2.5` GA Default vs `TimesFM 3.0` Preview with Covariates)**:
  - Run on clean calendar spines with explicit zero-fill (`COALESCE(COUNT(*), 0)`).
  - **Default GA (`model => 'TimesFM 2.5'`)**: Univariate (`data_col => 'total_trips'`, `timestamp_col => 'trip_date'`, `horizon => 30`, `confidence_level => 0.95`, optional `id_cols => ['usertype']`, `<= 100M` series). Outputs `forecast_timestamp`, `forecast_value`, `standard_error`, `confidence_level`, `prediction_interval_lower_bound`, `prediction_interval_upper_bound`, `ai_forecast_status`.
  - **Preview (`model => 'TimesFM 3.0'`)**: Univariate (`data_col`) or covariates (`target_cols => ['total_trips']`, `past_covariate_cols => [...]`, `future_covariate_cols => ['temp_f', 'prcp_in', 'is_weekend']`) on `<= 2,048` context points and `<= 1,024` horizon steps. With `target_cols`, returns `STRUCT<value FLOAT64, prediction_interval_lower_bound FLOAT64, prediction_interval_upper_bound FLOAT64>`; alias `trip_date AS forecast_timestamp` and `total_trips.value AS forecast_value`.
- **`AI.DETECT_ANOMALIES` & `AI.EVALUATE` (`TimesFM 2.5` — GA)**: Take historical context (`TABLE` arg 1) + target/holdout (`TABLE` arg 2). `AI.DETECT_ANOMALIES` (`<= 1,024` points/series) returns `is_anomaly`, `anomaly_probability`, `lower_bound`, `upper_bound`. `AI.EVALUATE` returns `mean_absolute_error`, `root_mean_squared_error`, `mean_absolute_percentage_error`.
- **`AI.PREDICT` (`TabFM` — Preview)**: In-context tabular foundation inference (`training_table`, `prediction_table`, `label_col => 'LABEL_COL'`) as an **additive pre-trained option at Tier 0 & Tier 1**:
  - **Empirical Caps (`bigquery-data-science`):** Max **`50` feature columns**, max **`10` classes**, and **`~5,000–8,000` practical training context rows** on on-demand slots.
  - **Task Selection by Type:** `INT64`/`FLOAT64`/`NUMERIC` labels run **Regression** (`predicted_<label>`); `BOOL`/`STRING` labels run **Classification** (`predicted_<label>` + `predicted_<label>_probs`). Cast `0/1` `INT64` binary labels to `BOOL`/`STRING`.
  - **Rejected Types & Latency:** Rejects `DATE`/`DATETIME`/`TIME`/`TIMESTAMP`/`BYTES`/`JSON`/`GEOGRAPHY`/`ARRAY`/`STRUCT` — extract numeric features first and materialize `AI.PREDICT` output once into a table.
- **`AI.KEY_DRIVERS` (GA)**: Model-free driver discovery across `<=12` categorical dimensions on **summable** metrics. For ratios (`clinical-risk`), use Tier 1 `CONTRIBUTION_ANALYSIS` with `ML.GET_INSIGHTS`.

### Guided Tier 0 NYC Citi Bike Reference Patterns (`citibike_tier0`)

In `labs/guided/citibike/tier0_baseline.sql` (`bigquery-public-data.new_york_citibike.citibike_trips` — profile by year/month to bound the contiguous multi-year window `START_DATE..END_DATE` before any feed gap, and set `HOLDOUT_CUTOFF_DATE` 28–30 days prior to `END_DATE`):
- **1. Spines (`daily_trips` & `daily_trips_by_usertype`)**: `UNNEST(GENERATE_DATE_ARRAY(START_DATE, END_DATE, INTERVAL 1 DAY)) AS trip_date` left-joined to daily counts so any multi-day weather/blizzard shutdown dates with zero trips have explicit `0` rows (`COALESCE(d.raw_trips, 0) AS total_trips, COALESCE(d.raw_trips, 0) AS trip_count`, `subscriber_trips`, `customer_trips`), cross-joined with `UNNEST(['Subscriber', 'Customer']) AS usertype`.
- **2. Forecast (`forecast_28d`/`forecast_30d`), Anomalies (`anomalies_2016`/`anomalies_30d`), Rewind Eval (`rewind_eval`/`holdout_eval_summary`), & TabFM (`tabfm_trip_type_preds`)**:
  ```sql
  CREATE OR REPLACE TABLE `PROJECT_ID.citibike_tier0.forecast_30d` AS
  SELECT * FROM AI.FORECAST(
    (SELECT trip_date, usertype, total_trips FROM `PROJECT_ID.citibike_tier0.daily_trips_by_usertype`),
    data_col => 'total_trips', timestamp_col => 'trip_date', id_cols => ['usertype'], model => 'TimesFM 2.5', horizon => 30, confidence_level => 0.95);
  CREATE OR REPLACE TABLE `PROJECT_ID.citibike_tier0.anomalies_30d` AS
  SELECT * FROM AI.DETECT_ANOMALIES(
    (SELECT trip_date, usertype, total_trips FROM `PROJECT_ID.citibike_tier0.daily_trips_by_usertype` WHERE EXTRACT(YEAR FROM trip_date) < EXTRACT(YEAR FROM END_DATE)),
    (SELECT trip_date, usertype, total_trips FROM `PROJECT_ID.citibike_tier0.daily_trips_by_usertype` WHERE EXTRACT(YEAR FROM trip_date) = EXTRACT(YEAR FROM END_DATE)),
    data_col => 'total_trips', timestamp_col => 'trip_date', id_cols => ['usertype'], anomaly_prob_threshold => 0.95);
  CREATE OR REPLACE TABLE `PROJECT_ID.citibike_tier0.holdout_eval_summary` AS
  SELECT * FROM AI.EVALUATE(
    (SELECT trip_date, usertype, total_trips FROM `PROJECT_ID.citibike_tier0.daily_trips_by_usertype` WHERE trip_date <= HOLDOUT_CUTOFF_DATE),
    (SELECT trip_date, usertype, total_trips FROM `PROJECT_ID.citibike_tier0.daily_trips_by_usertype` WHERE trip_date > HOLDOUT_CUTOFF_DATE),
    data_col => 'total_trips', timestamp_col => 'trip_date', id_cols => ['usertype']);
  CREATE OR REPLACE TABLE `PROJECT_ID.citibike_tier0.tabfm_trip_type_preds` AS
  WITH sampled AS (
    SELECT tripduration, start_station_id, end_station_id, EXTRACT(HOUR FROM starttime) AS start_hour, EXTRACT(DAYOFWEEK FROM starttime) AS start_dow,
      usertype, MOD(ABS(FARM_FINGERPRINT(CAST(starttime AS STRING))), 10) AS bucket
    FROM `bigquery-public-data.new_york_citibike.citibike_trips` WHERE DATE(starttime) > HOLDOUT_CUTOFF_DATE AND DATE(starttime) <= END_DATE AND usertype IN ('Subscriber', 'Customer') LIMIT 4000)
  SELECT * FROM AI.PREDICT((SELECT * EXCEPT(bucket) FROM sampled WHERE bucket < 8), (SELECT * EXCEPT(bucket) FROM sampled WHERE bucket >= 8), label_col => 'usertype');
  ```

## 2. Tier 1–3 Skill & Syntax Map Across All 9 Discovery Problems

- **Always Use `TRANSFORM(...)` & Explicit Splits (`DATA_SPLIT_METHOD = 'CUSTOM'` or `'SEQ'`)** in BQML; for `BOOSTED_TREE_REGRESSOR` / `BOOSTED_TREE_CLASSIFIER` on on-demand slots, cap `max_iterations = 20, max_tree_depth = 5, early_stop = TRUE, subsample = 0.8` so training completes in `~3 min` rather than queuing `10–16 min`. Compute `MAE`, `RMSE`, `MAPE` on the exact same holdout split when comparing Tier 0 (`AI.EVALUATE`) vs Tier 1 (`ML.EVALUATE`).
- **9-Problem Skill & Syntax Map (`uvx bigquery-data-science lookup <SYMBOL>` + Data Agent Kit + Open Weights):**
  - `forecasting`: BQDS `AI.FORECAST`, `AI.DETECT_ANOMALIES`, `AI.EVALUATE`, `ARIMA_PLUS_XREG`, `BOOSTED_TREE_REGRESSOR`, `ML.EXPLAIN_FORECAST` | DAK `bigquery-ai-ml`, `dataform-bigquery`, `bigquery-bigframes`, `ml-best-practices`, `gcp-spark` | Open Weights: `google/timesfm-3.0-pytorch`
  - `next-best-offer`: BQDS `AI.KEY_DRIVERS`, `AI.PREDICT`, `BOOSTED_TREE_CLASSIFIER`, `TRANSFORM`, `ML.EXPLAIN_PREDICT` | DAK `bigquery-ai-ml`, `dataform-bigquery`, `bigquery-graph-query`, `ml-best-practices`, `gcp-spark` | Open Weights: `google/tabfm-1.0.0-pytorch`
  - `payment-fraud`: BQDS `AI.KEY_DRIVERS`, `AI.PREDICT`, `BOOSTED_TREE_CLASSIFIER`, `KMEANS`, `PCA`, `ML.EXPLAIN_PREDICT` | DAK `bigquery-ai-ml`, `bigquery-graph-author`, `bigquery-graph-query`, `ml-best-practices`, `gcp-dataflow`, `bigtable-basics` | Open Weights: `google/tabfm-1.0.0-pytorch`
  - `predictive-maintenance`: BQDS `AI.KEY_DRIVERS`, `AI.DETECT_ANOMALIES`, `AI.FORECAST`, `AI.PREDICT`, `BOOSTED_TREE_CLASSIFIER`, `BOOSTED_TREE_REGRESSOR`, `ARIMA_PLUS` | DAK `bigquery-ai-ml`, `data-autocleaning`, `bigquery-bigframes`, `ml-best-practices`, `gcp-spark`, `gcp-dataflow` | Open Weights: `google/timesfm-3.0-pytorch`, `google/tabfm-1.0.0-pytorch`
  - `search-conversion`: BQDS `AI.GENERATE_EMBEDDING`, `VECTOR_SEARCH`, `CREATE VECTOR INDEX`, `AI.SIMILARITY`, `AI.SCORE`, `AI.PREDICT`, `BOOSTED_TREE_CLASSIFIER` | DAK `bigquery-ai-ml`, `bigquery-sql`, `dataform-bigquery`, `ml-best-practices`, `cloud-databases-onboarding` | Open Weights: `google/tabfm-1.0.0-pytorch`
  - `recommender`: BQDS `AI.GENERATE_EMBEDDING`, `AI.SIMILARITY`, `VECTOR_SEARCH`, `AI.PREDICT`, `MATRIX_FACTORIZATION`, `BOOSTED_TREE_CLASSIFIER`, `ML.RECOMMEND` | DAK `bigquery-ai-ml`, `dataform-bigquery`, `ml-best-practices`, `gcp-dataflow`, `bigtable-basics` | Open Weights: `google/tabfm-1.0.0-pytorch`
  - `churn`: BQDS `AI.PREDICT`, `CONTRIBUTION_ANALYSIS`, `BOOSTED_TREE_CLASSIFIER`, `LOGISTIC_REG`, `TRANSFORM`, `ML.EXPLAIN_PREDICT` | DAK `bigquery-ai-ml`, `dataform-bigquery`, `bigquery-bigframes`, `ml-best-practices`, `gcp-pipeline-orchestration` | Open Weights: `google/tabfm-1.0.0-pytorch`
  - `clinical-risk`: BQDS `CONTRIBUTION_ANALYSIS`, `ML.GET_INSIGHTS`, `AI.PREDICT`, `LOGISTIC_REG`, `BOOSTED_TREE_CLASSIFIER`, `TRANSFORM`, `ML.EXPLAIN_PREDICT` | DAK `bigquery-ai-ml`, `data-autocleaning`, `bigquery-sql`, `bigquery-bigframes`, `ml-best-practices` | Open Weights: `google/tabfm-1.0.0-pytorch`
  - `marketing-measurement`: BQDS `AI.FORECAST`, `AI.PREDICT`, `LINEAR_REG`, `ARIMA_PLUS_XREG`, `ML.WEIGHTS`, `ML.EVALUATE` | DAK `bigquery-data-transfer-service`, `dataform-bigquery`, `bigquery-ai-ml`, `ml-best-practices`, `gcp-managed-airflow-dag-authoring` | Open Weights: `google/timesfm-3.0-pytorch`
