# Pass 1: Guided Tier 0 Lab — Demand Forecasting Baseline (`Checkpoints 01–06`)

In **Pass 1**, everyone in the classroom walks the **4-Step Agentic Loop** (`Discover → Design → Build → Verify`) together on **Demand Forecasting** at **Tier 0** before moving on to **Pass 2 (Solo Challenger)**.

> **Live Classroom Guidance:** Follow the step-by-step architectural guides in the **Classroom & Field Guide Hub** (shared by your instructor when your session opens). Remember: steer `agy` in your workspace root to author and run your data science deliverables, and **always run `python3 lab-evaluation-verifier/NN-test_*.py` yourself in your human terminal** (`agy` never reads or runs `./lab-evaluation-verifier/`).

---

## Why We Start at Tier 0

Never approve a custom Tier 1 (`CREATE MODEL`) or Tier 2 (cloud Python / Spark custom training) build until you have established a **Tier 0 zero-training baseline** on clean, point-in-time historical data and measured on a holdout window where Tier 0 succeeds and where it falls short.

At **Tier 0**, a managed **BigQuery Conversational Analytics Data Agent (`geminidataanalytics.googleapis.com`)** can invoke zero-DDL `AI.FORECAST` and `AI.DETECT_ANOMALIES` over governed tables. Because a managed data agent will not automatically profile raw source tables for calendar gaps or run a deterministic historical rewind holdout for you, in Pass 1 you steer `agy` (consulting `.agents/rules/*.md`, **`bigquery-data-science`**, and **Data Agent Kit**) to prepare and evaluate the governed Tier 0 baseline in your greenfield project's `citibike_tier0` dataset:

1. **Checkpoint 02 — Discover (`02-test_guided_tier0_discovery_pack.py`):**
   Bound the Tier 0 baseline in Discovery and resolve `docs/discovery-pack-tier0.md` using `.agents/skills/discovery-pack-fetch/`.
2. **Checkpoint 03 — Design (`03-test_guided_tier0_design_brief.py`):**
   Steer `agy` in a 2-turn discovery-first flow: profile the raw `bigquery-public-data.new_york_citibike.citibike_trips` table live in BigQuery (discovering its contiguous historical date bounds, rider segments, and whether every calendar day is present), then author and review `labs/guided/citibike/DESIGN-tier0.md` before writing pipeline SQL.
3. **Checkpoint 04 — Calendar Spine (`04-test_tier0_calendar_spine.py`):**
   Steer `agy` to author `labs/guided/citibike/tier0_baseline.sql` and materialize contiguous, zero-filled daily tables (`daily_trips` and `daily_trips_by_usertype`) in `citibike_tier0`.
4. **Checkpoint 05 — Zero-Shot Foundation Model Baseline (`05-test_tier0_ai_baseline.py`):**
   Evaluate BigQuery AI foundation models (`AI.FORECAST`, `AI.DETECT_ANOMALIES`, `AI.EVALUATE`, and `AI.PREDICT`) over your governed spine and holdout window in `citibike_tier0`.
5. **Checkpoint 06 — Conversational Analytics Data Agent & Escalation Trigger (`06-test_tier0_data_agent.py`):**
   Provision and test your stateful BigQuery Conversational Analytics Data Agent over `citibike_tier0` via `.agents/skills/conversational-analytics-agent/` and document your empirical escalation criteria in `labs/guided/citibike/tier1_trigger.md`.
