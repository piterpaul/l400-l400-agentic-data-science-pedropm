# Predictive Maintenance & Asset Reliability — Shipped Generator & Loader

BigQuery's public project (`bigquery-public-data`) has no industrial sensor telemetry + maintenance work-order table. This folder ships a **deterministic stdlib-only Python generator and BigQuery loader** (`generate_and_load.py`) that synthesises a three-table industrial pump fleet dataset with known Weibull time-to-failure parameters and the exact structural traps from the catalog.

---

## 1. Generate and Load into BigQuery

```bash
uv run python labs/data/predictive-maintenance/generate_and_load.py \
  --project "$GOOGLE_CLOUD_PROJECT"
```

To generate the three CSVs locally (`labs/data/predictive-maintenance/out/*.csv`) without calling BigQuery:

```bash
uv run python labs/data/predictive-maintenance/generate_and_load.py --dry-run
```

---

## 2. Tables Created in `<project>.pdm_workshop`

| Table | Rows | Grain & Key Columns | Purpose |
| --- | ---: | --- | --- |
| `assets` | `900` | One row per industrial pump (`asset_id`, `asset_class`, `maker`, `site_id`, `install_date`, `scheduled_swap_weeks`, `rated_load_kw`, `ambient_temp_c`) | Fleet metadata and preventive overhaul policy per asset class |
| `weekly_readings` | `78,947` | One row per active asset-week (`asset_id`, `week_start`, `life_id`, `operating_hours`, `ch1_vibration_mms`, `ch2_bearing_temp_c`, `ch3_current_amps`, `ch4_exhaust_temp_c`, `ch5_oil_particle_count`, `ch6_acoustic_db`, `maker_alarm`, `failed_within_4w`, `duration_weeks`, `event_observed`) | Weekly sensor panel for Hard Tier 1 classification (`failed_within_4w`) and Tier 2 survival (`duration_weeks, event_observed`) |
| `work_orders` | `965` | One row per technician intervention (`work_order_id`, `asset_id`, `filed_date`, `order_type`, `technician_note`) | Unstructured technician text for `AI.GENERATE_TABLE` fault-mode extraction and label auditing |

---

## 3. Built-In Structural Traps (What the Agent Must Catch)

1. **Right-censoring by preventive maintenance (~45% of lives):** `P100` and `P200` units undergo scheduled overhauls around `208` weeks (`scheduled_swap_weeks`). Dropping unfinished lives biases any classifier toward short-lived failures; Tier 2 keeps censored lives via `event_observed = 0`.
2. **Dead sensor flatline (`ch4_exhaust_temp_c`):** On ~8% of assets, `ch4_exhaust_temp_c` freezes at `45.0` °C for six consecutive weeks. A naive tree treats zero variance as healthy stability unless a flatline monitor flags `STDDEV = 0`.
3. **Paperwork filing lag & mixed work orders (`work_orders`):** Technician notes mix genuine bearing/winding failures (`Bearing collapsed...`, `Motor tripped on overload...`) with routine inspections (`Routine inspection, nothing found`) and preventive swaps (`Scheduled 4-year overhaul...`), and `filed_date` lags the true failure week by 2–10 days.
4. **Asset-level + temporal split:** Splitting randomly across asset-weeks leaks the same degrading asset across train and test.
