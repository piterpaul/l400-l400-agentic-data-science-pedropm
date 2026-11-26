# Marketing Measurement & Incrementality — Shipped Workshop Data

BigQuery's public project (`bigquery-public-data`) has no weekly multi-channel marketing spend and geo-level conversion panel. This folder ships Google Meridian's official simulated geo and national datasets (`Apache-2.0`, see [`LICENSE`](LICENSE)) together with a loader script that adds a paired **8-week matched-market holdout experiment** table and loads all three into `<project>.mmm_workshop`.

---

## 1. Load into BigQuery

```bash
uv run python labs/data/marketing-measurement/load_to_bq.py \
  --project "$GOOGLE_CLOUD_PROJECT"
```

To generate `geo_holdout_experiment.csv` locally without calling BigQuery (e.g. for offline inspection):

```bash
uv run python labs/data/marketing-measurement/load_to_bq.py --dry-run
```

---

## 2. Tables Created in `<project>.mmm_workshop`

| Table | Rows | Grain & Key Columns | Purpose |
| --- | ---: | --- | --- |
| `geo_all_channels` | `6,240` | `40` markets (`Geo0`–`Geo39`) × `156` weeks (`2021-01-25` to `2024-01-15`); 5 paid channels (`Channel0`–`Channel4` impressions & spend, plus `Channel4` reach/frequency), `Organic_channel0_impression`, `Promo`, `competitor_sales_control`, `sentiment_score_control`, `conversions`, `revenue_per_conversion`, `population` | Primary geo-level panel for both Hard Tier 1 and Tier 2 |
| `national_all_channels` | `156` | National weekly roll-up of the same `156` weeks | National aggregate baseline and diagnostic check |
| `geo_holdout_experiment` | `320` | `40` markets × `8` weeks (`2023-11-06` to `2023-12-25`); `assignment` (`treatment_dark` vs `control_active`), `channel0_withheld_spend`, `observed_conversions`, `counterfactual_conversions`, `incremental_conversions`, `incremental_roi` | Matched-market switch-off test anchoring `Channel0`'s causal return (`incremental_roi ≈ 1.62`) |

---

## 3. Built-In Structural Traps (What the Agent Must Catch)

1. **Channel co-movement (`r = 0.27–0.70`):** Paid media channels move together across seasons and markets. Naive OLS (`LINEAR_REG` on raw spend) splits credit arbitrarily across collinear channels.
2. **Promotional confounding (`Promo`):** Promotional weeks coincide with paid spend bursts. Omitting `Promo` or `competitor_sales_control` attributes the promotional spike to paid media.
3. **Carryover (adstock) & diminishing returns (Hill saturation):** Spend in week $t$ drives conversions in weeks $t+1 \dots t+4$ with diminishing marginal return at high spend.
   - **Hard Tier 1** constructs SQL geometric adstock (`SUM(spend * POW(decay, lag)) OVER (...)`) and Hill-style log/power saturation transforms inside BigQuery before fitting `LINEAR_REG`, then compares the naive vs transformed attribution against the holdout experiment.
   - **Tier 2** fits a hierarchical Bayesian geo-level model (`google-meridian` or `PyMC`) with informative priors calibrated to `geo_holdout_experiment`.
