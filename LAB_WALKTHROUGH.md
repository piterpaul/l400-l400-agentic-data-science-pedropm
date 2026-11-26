# L400 Agentic Data Science — Step-by-Step Lab Walkthrough

- **Classroom Hub UI:**
  - Open [https://data-science-hub-463617135523.us-central1.run.app](https://data-science-hub-463617135523.us-central1.run.app) *(or the shortlink shared by your instructor)*.
- **Narrative Lecture & Self-Paced Guide:**
  - Want the architectural *why*, classroom stories, Socratic questions, and deep-dive sidebars behind each stage? Read [**`LECTURE_WALKTHROUGH.md`**](LECTURE_WALKTHROUGH.md) alongside this checklist *(every chapter links directly to the matching stage and checkpoint below)*.
- **Need Help?**
  - Raise your hand and **ask an instructor or proctor anytime**.
  - Working self-paced? Expand **`Hints & Alternatives`** on any Hub checkpoint card.
- **How to Pace This Lab (`Checkpoints 01 → 12`):**
  - Walk top-to-bottom alongside the **Classroom Hub**, **Google Cloud Console**, and **`agy`**.
  - Steer `agy` **one checkpoint (and one design turn) at a time** — never ask `agy` to run this whole file at once.
  - Run `python3 lab-evaluation-verifier/XX-test_*.py` **only in your Human Terminal** (`agy` never reads or runs `./lab-evaluation-verifier/`).

---

## Stage 0 — Environment Setup & Checkpoint `01` (`0. Start & Setup`)

- **1. Review Opening Slides (`Hub → 0. Start & Setup`):**
  - Open the Classroom Hub on `0. Start & Setup`.
  - Walk the opening slides (with your instructor or solo).
  - Note the `Discover → Design → Build → Verify` loop across Pass 1 and Pass 2.
- **2. Create Your Private Repo & Clone (`Hub → Step 1A`):**
  - Open [`cloud-gtm/l400-agentic-data-science-labs`](https://github.com/cloud-gtm/l400-agentic-data-science-labs).
  - Click **Use this template → Create a new repository**:
    - **Owner:** Your **personal GitHub handle** *(never `cloud-gtm`)*.
    - **Visibility:** **Private**.
  - Clone to `~/l400/l400-agentic-data-science-labs` and open that folder as your VS Code workspace root.
  - Open **2 terminals** in VS Code:
    - **Terminal 1:** `agy` *(launched in Stage 4)*
    - **Terminal 2:** **Human Terminal** *(for `deploy.sh` and verifiers)*
- **3. Provision Greenfield GCP Project (`Hub → Step 1B`):**
  - Coming from a shared-project lab? Run the 3-line `gcloud` seed reset in [README.md](README.md#3-reset-gcloud-to-your-seed-project-if-coming-from-another-lab).
  - In your Human Terminal, run: `source deploy.sh`
  - Confirm the billing & identity pre-flight prompt.
  - While Terraform runs (~3–4 min), walk **Stage 1** below!
- **4. Link Project ID & Verify `Checkpoint 01`:**
  - Copy the `l400-agentic-ds-<id>` project ID printed by `deploy.sh` (or saved in `agent-config.json`).
  - Paste it into the Hub header pill **`☁️ Set Project ID`**.
  - **Review in Cloud Console (`CP 01`):**
    - Click **`Open Project Console ↗`** on `Checkpoint 01`.
    - Confirm top-right Console avatar matches your `*.altostrat.com` lab login.
    - Navigate: `Top Project Picker -> Organization -> <your-project-id> -> BigQuery -> Studio -> Explorer -> Datasets`
    - Confirm `citibike_tier0` and `l400_ds_work` exist.
  - **Verify (`Human Terminal`):**
    - Confirm `deploy.sh` auto-ran Verifier `01`, or run:
      ```bash
      python3 lab-evaluation-verifier/01-test_terraform_infrastructure.py
      ```
    - Click **`✅ Checkpoints (1/12)` → `🔄 Sync Evaluator`** in the Hub header.

---

## Stage 1 — Up-Front Harness Tour: How This Repo Bounds `agy`

Open these **5 shipped building blocks** in VS Code (or on GitHub) before launching `agy`:

- **`docs/llms.txt` — Compact Navigation Index**
  - ~40-line workspace index read first by LLM agents.
  - Maps core files, datasets, rules, and skills so agents orient immediately instead of grepping blindly.
- **`AGENTS.md` — Master Workflow Contract**
  - Defines `agy`'s role and `Discover → Design → Approval Gate → Build → Verify` sequence.
  - Routes tasks to scoped rules and blocks static keys or schema guessing.
  - Symlinked to `CLAUDE.md`, `.cursorrules`, and `.windsurfrules`.
- **`.agents/rules/*.md` — 5 Always-On Guardrails (`< 12 KB` each)**
  - `lab_governance.md`:
    - Enforces `DESIGN` approval gates, zero local VM compute, and `./lab-evaluation-verifier/` isolation.
  - `data_science_standards.md`:
    - Enforces Tier 0 baseline floor, leak-free splits, raw-data trap checks, and the 3-region split.
  - `bigquery_ai_and_ml_standards.md`:
    - Routes Tier 0 `AI.*` SQL TVFs, fast Tier 1 `BOOSTED_TREE_REGRESSOR` caps, and `e2-standard-4` CustomJobs.
  - `agent_skills_standards.md`:
    - Enforces modular `.agents/skills/<name>/SKILL.md` + `scripts/` packaging.
  - `terraform_standards.md`:
    - Documents 4-region (`us-central1`, `us-east1`, `us-east4`, `us-west1`) stockout-ready infrastructure.
- **`.agents/skills/` — On-Demand Domain Skills**
  - **Shipped in repo:**
    - `discovery-pack-fetch/` *(includes all `9 × 4 = 36` context packs in `packs/`)*
    - `conversational-analytics-agent/` *(registers & chats with BigQuery Data Agents)*
  - **Installed by `deploy.sh`:**
    - [`bigquery-data-science`](https://github.com/statmike/bigquery-data-science) *(4 skills: `bigquery-data-science`, `bigquery-ai`, `bigquery-ml`, `bigquery-mlops`)*
    - [`Data Agent Kit`](https://github.com/GoogleCloudPlatform/data-agent-kit-plugin) *(15 skills: `bigquery-ai-ml`, `ml-best-practices`, `gcp-spark`, `data-autocleaning`, etc.)*
- **`agent-config.json` — Live Environment State *(Gitignored)***
  - Generated from `agent-config.example.json` by `deploy.sh` with your live `gcp-project-id` and datasets.
  - Separates 3 cloud region keys:
    - `bigquery-region`: `"US"` *(multi-region data plane)*
    - `spark-region`: `"us-central1"` *(Serverless Spark batches)*
    - `vertex-ai-region`: `"us-central1"` *(Agent Platform CustomJobs & Model Registry)*

---

## Stage 2 — Method & Discovery Orientation (`Tabs 1 & 2`)

- **1. Walk `1. The Method` on the Hub:**
  - Scan the **4-Tier Escalation Ladder** (`Tier 0 → Tier 3` + `Tier 4` Regulated & Adversarial overlay, with `Tier 0` Conversational Analytics Data Agents as the universal stakeholder interface).
  - Review why **Pass 1 (`Tier 0`)** sets a fast baseline floor before **Pass 2 (`Tier 2`)** earns custom cloud training.
- **2. Walk `2. Discovery & Architectures` on the Hub:**
  - Confirm **NYC Citi Bike Demand Forecasting (`forecasting`)** is active *(used for all 12 graded checkpoints)*.
  - *(Optional)* Expand the **other 8 enterprise archetypes** drawer to explore Keystone Questions and `Tier 0–4` diagrams safely.
  - Click **`🎯 Tier 0 · Pass 1 Class Start`**.
  - Step through the 5-slide use-case deck and Keystone Questions console.
  - Scroll down to **`Checkpoint 02`**.

---

## Stage 3 — Master 12-Checkpoint Map (Clone & Console Reference)

| CP | Pass & Hub Tab | Shipped vs. Added in Your Clone | Cloud Console Review Target | Human Verifier |
| :- | :--- | :--- | :--- | :--- |
| **`01`** | Setup · `0. Start & Setup` | `agent-config.json`, `.agents/skills/*` *(installed)* | `BigQuery -> Studio -> Datasets`: `citibike_tier0`, `l400_ds_work` | `01-test_terraform_infrastructure.py` |
| **`02`** | Pass 1 · `2. Discovery` | **Adds:** `docs/discovery-pack-tier0.md` | — | `02-test_guided_tier0_discovery_pack.py` |
| **`03`** | Pass 1 · `3. Agentic Design` | **Adds:** `labs/guided/citibike/DESIGN-tier0.md` *(2 turns)* | — | `03-test_guided_tier0_design_brief.py` |
| **`04`** | Pass 1 · `4. Agentic Build` | **Adds:** `labs/guided/citibike/tier0_baseline.sql` | `BigQuery -> citibike_tier0`: `daily_trips`, `daily_trips_by_usertype` | `04-test_tier0_calendar_spine.py` |
| **`05`** | Pass 1 · `4. Agentic Build` | *(Materializes BigQuery `AI.*` tables)* | `BigQuery -> citibike_tier0`: `forecast_30d`, `anomalies_30d`, `holdout_eval_summary` | `05-test_tier0_ai_baseline.py` |
| **`06`** | Pass 1 · `4. Agentic Build` | **Adds:** `labs/guided/citibike/tier1_trigger.md`, `artifacts/tier0_data_agent_evidence.json` | `BigQuery -> Agents -> Agent tab -> NYC Citi Bike Tier 0 Demand Agent` | `06-test_tier0_data_agent.py` |
| **`07`** | Pass 2 · `2. Discovery` | **Adds:** `docs/discovery-pack.md` | — | `07-test_discovery_pack_handover.py` |
| **`08`** | Pass 2 · `3. Agentic Design` | **Adds:** `DESIGN.md` *(+ updates `data_science_standards.md`, 2 turns)* | — | `08-test_solution_design_brief.py` |
| **`09`** | Pass 2 · `4. Agentic Build` | **Adds:** `.agents/skills/build-forecasting/SKILL.md` + `scripts/` | — | `09-test_agent_build_skill.py` |
| **`10`** | Pass 2 · `4. Agentic Build` | *(Executes feature spine pipeline into BigQuery)* | `BigQuery -> l400_ds_work`: `feature_spine` *(Schema / Preview)* | `10-test_feature_store_and_trap_guard.py` |
| **`11`** | Pass 2 · `4. Agentic Build` | **Adds:** `artifacts/eval_metrics.json` | **(1)** `BigQuery -> l400_ds_work` (`Tables` & `Models: challenger_xgb`) · **(2)** `Spark Serverless -> Batches` · **(3)** `Agent Platform -> Custom jobs` | `11-test_model_training_and_artifacts.py` |
| **`12`** | Pass 2 · `4. Agentic Build` | **Adds:** `EVALUATION.md`, `docs/agent_critique.md` | `BigQuery -> Agents -> Agent tab -> Details -> Knowledge sources -> View more` | `12-test_baseline_comparison_and_decision.py` |

---

## Stage 4 — Pass 1: Guided Tier 0 Baseline (`Checkpoints 02–06`)

Start **`agy`** inside `~/l400/l400-agentic-data-science-labs` and walk Checkpoints `02–06` one step at a time *(ask an instructor anytime if you hit a snag)*:

### Checkpoint `02` — Resolve Tier 0 Discovery Context Pack
- **Hub:** `2. Discovery & Architectures` → `Checkpoint 02` *(Pass 1: Guided)*
- **Steer `agy`:**
  - Read the `CP 02` Mission Brief on the Hub.
  - Direct `agy` to run `discovery-pack-fetch` for `forecasting` at Tier `0` (`--problem-id forecasting --tier 0 --output docs/discovery-pack-tier0.md`).
  - Have `agy` read the resolved pack and summarize the 4 Discovery Takeaways.
- **Inspect in Clone:**
  - `docs/discovery-pack-tier0.md` *(newly created)*
  - `agent-config.json` *(updated)*
- **Verify (`Human Terminal`):**
  - Run: `python3 lab-evaluation-verifier/02-test_guided_tier0_discovery_pack.py`
  - Click **Continue to `3. Agentic Design`** on the Hub.

### Checkpoint `03` — 2-Turn POC Data Profiling & Tier 0 Design Brief
- **Hub:** `3. Agentic Design` → scan the top **Harness & Skills Toolkit Card**, then scroll to `Checkpoint 03`
- **Steer `agy` (Complete Both Turns Before Verifying):**
  - **Turn 1 (Open Brief):**
    - Have `agy` read `docs/discovery-pack-tier0.md`, `agent-config.json`, and `.agents/rules/*.md`.
    - Ask `agy` to profile `bigquery-public-data.new_york_citibike.citibike_trips` in BigQuery (date bounds, missing calendar days, `Subscriber` vs. `Customer` volume).
    - Have `agy` write the initial draft of `labs/guided/citibike/DESIGN-tier0.md`.
    - **Pause here** and inspect `agy`'s BigQuery profiling findings!
  - **Turn 2 (Expand `Unlock Turn 2 Steering Brief` Drawer):**
    - Direct `agy` to lock in the zero-filled calendar spine, the 30-day chronological holdout split, and the Conversational Analytics Data Agent plan in `DESIGN-tier0.md`.
- **Inspect in Clone:**
  - `labs/guided/citibike/DESIGN-tier0.md` *(confirm `mermaid` pipeline diagram, profiled date range, and zero-fill spec)*
- **Verify (`Human Terminal`):**
  - Run: `python3 lab-evaluation-verifier/03-test_guided_tier0_design_brief.py`
  - Click **Continue to `4. Agentic Build`** on the Hub.

### Checkpoint `04` — Zero-Filled Calendar Spine in BigQuery
- **Hub:** `4. Agentic Build` → `Checkpoint 04`
- **Steer `agy`:**
  - Read the `CP 04` Mission Brief on the Hub.
  - Direct `agy` to author `labs/guided/citibike/tier0_baseline.sql`.
  - Materialize `daily_trips` and `daily_trips_by_usertype` in `citibike_tier0` using a continuous zero-filled calendar spine.
- **Inspect in Clone:**
  - `labs/guided/citibike/tier0_baseline.sql`
- **Review in Cloud Console:**
  - Click **`Open BigQuery Studio ↗`** on the `CP 04` Console Breadcrumb.
  - Navigate: `BigQuery -> Studio -> Explorer -> Datasets -> citibike_tier0`
  - Check `Details / Preview` on `daily_trips` and `daily_trips_by_usertype`.
- **Verify (`Human Terminal`):**
  - Run: `python3 lab-evaluation-verifier/04-test_tier0_calendar_spine.py`

### Checkpoint `05` — Zero-Training BigQuery `AI.*` Baseline & Holdout Floor
- **Hub:** `4. Agentic Build` → `Checkpoint 05`
- **Steer `agy`:**
  - Read the `CP 05` Mission Brief on the Hub.
  - Direct `agy` to extend and execute `tier0_baseline.sql` using zero-shot `AI.FORECAST`, `AI.DETECT_ANOMALIES`, and `AI.EVALUATE` on the 30-day holdout split.
- **Review in Cloud Console:**
  - Click **`Open BigQuery Studio ↗`** on the `CP 05` Console Breadcrumb.
  - Navigate: `BigQuery -> Studio -> Explorer -> Datasets -> citibike_tier0`
  - Preview `forecast_30d`, `anomalies_30d`, and `holdout_eval_summary`.
- **Verify (`Human Terminal`):**
  - Run: `python3 lab-evaluation-verifier/05-test_tier0_ai_baseline.py`

### Checkpoint `06` — Stateful Conversational Analytics Data Agent & Escalation Memo
- **Hub:** `4. Agentic Build` → `Checkpoint 06`
- **Steer `agy`:**
  - Point `agy` at `.agents/skills/conversational-analytics-agent/SKILL.md`.
  - Register the stateful BigQuery Data Agent `citibike_tier0_agent` over your `citibike_tier0` tables.
  - Write `labs/guided/citibike/tier1_trigger.md` recording your measured `Subscriber` vs. `Customer` holdout accuracy and why station grain + weather covariates motivate Pass 2.
- **Inspect in Clone:**
  - `labs/guided/citibike/tier1_trigger.md`
  - `artifacts/tier0_data_agent_evidence.json`
- **Review in Cloud Console:**
  - Click **`Open BigQuery Agents ↗`** on the `CP 06` Console Breadcrumb.
  - Navigate: `BigQuery -> Agents -> Agent tab -> NYC Citi Bike Tier 0 Demand Agent -> + New conversation`
  - Try the 4 copyable prompts on the Hub card to compare:
    - **Governed Scheduled Forecast (`forecast_30d`):** Pre-materialized and reviewed on schedule.
    - **Live On-the-Fly Override (`AI.FORECAST`):** Ad-hoc custom-horizon forecast generated live in chat and compared against `forecast_30d`.
- **Verify (`Human Terminal`):**
  - Run: `python3 lab-evaluation-verifier/06-test_tier0_data_agent.py`
- **Switch to Pass 2:**
  - Click **`Pass 1 Complete → Loop Back to Tab 2 for Pass 2`** at the bottom of `CP 06`.
  - Confirm the top Hub banner now reads **`Pass 2 of 2 · Solo Lab`** on **Demand Forecasting · Tier 2**.

---

## Stage 5 — Pass 2: Solo Tier 2 Multi-Runtime Escalation (`Checkpoints 07–12`)

### Checkpoint `07` — Resolve Tier 2 Discovery Context Pack
- **Hub:** `2. Discovery & Architectures` *(Pass 2: Solo)* → click **`🚀 Tier 2 · Pass 2 Class Target`** if needed → `Checkpoint 07`
- **Steer `agy`:**
  - Read the `CP 07` Mission Brief on the Hub.
  - Direct `agy` to run `discovery-pack-fetch` for `forecasting` at Tier `2` (`--problem-id forecasting --tier 2 --output docs/discovery-pack.md`) while keeping `docs/discovery-pack-tier0.md` intact.
  - Have `agy` summarize the 4 Discovery Takeaways.
- **Inspect in Clone:**
  - `docs/discovery-pack.md` *(compare alongside `docs/discovery-pack-tier0.md`)*
- **Verify (`Human Terminal`):**
  - Run: `python3 lab-evaluation-verifier/07-test_discovery_pack_handover.py`
  - Click **Continue to `3. Agentic Design`** on the Hub.

### Checkpoint `08` — Architect Choices & 2-Turn Root `DESIGN.md` Approval Gate
- **Hub:** `3. Agentic Design` *(Pass 2: Solo)* → `Checkpoint 08`
- **Steer `agy` (Complete Both Turns Before Verifying):**
  - **Select Choices:** Pick your **3 Architect Choices** at the top of `CP 08`.
  - **Turn 1 (Open Brief):**
    - Direct `agy` to profile the station-level Citi Bike + NOAA weather tables in BigQuery and draft root `DESIGN.md`.
    - **Pause here** and inspect `agy`'s raw-data trap findings!
  - **Turn 2 (Expand `Open Turn 2 Mission Brief` Drawer):**
    - Push back on any split, leakage, or weather sentinel gaps.
    - Record the `## Architect's Design Audit & Steering Log` in `DESIGN.md` and refine `.agents/rules/data_science_standards.md` if needed.
- **Inspect in Clone:**
  - `DESIGN.md` *(confirm `mermaid` multi-runtime diagram, bounded station cohort, leak-free split, and audit log)*
- **Verify (`Human Terminal`):**
  - Run: `python3 lab-evaluation-verifier/08-test_solution_design_brief.py`
  - Click **Continue to `4. Agentic Build`** on the Hub.

### Checkpoint `09` — Package Reusable `.agents/skills/build-forecasting/` Skill
- **Hub:** `4. Agentic Build` *(Pass 2: Solo)* → `Checkpoint 09`
- **Steer `agy`:**
  - Direct `agy` to package your approved `DESIGN.md` pipeline into `.agents/skills/build-forecasting/SKILL.md` (valid YAML frontmatter + modular `scripts/`).
  - **Stop before launching training jobs** — verify the skill structure first.
- **Inspect in Clone:**
  - `.agents/skills/build-forecasting/SKILL.md`
  - `.agents/skills/build-forecasting/scripts/`
- **Verify (`Human Terminal`):**
  - Run: `python3 lab-evaluation-verifier/09-test_agent_build_skill.py`

### Checkpoint `10` — Materialize Leak-Free `l400_ds_work.feature_spine`
- **Hub:** `4. Agentic Build` → `Checkpoint 10`
- **Steer `agy`:**
  - Direct `agy` to run the feature-engineering step of `build-forecasting` to materialize `l400_ds_work.feature_spine` in BigQuery (`US`).
  - Have `agy` run a SQL audit confirming zero duplicate keys, clean weather sentinels, and horizon-safe lags.
- **Review in Cloud Console:**
  - Click **`Open BigQuery Studio ↗`** on the `CP 10` Console Breadcrumb.
  - Navigate: `BigQuery -> Studio -> Explorer -> Datasets -> l400_ds_work -> feature_spine`
  - Check `Schema`, `Details`, and `Preview`.
- **Verify (`Human Terminal`):**
  - Run: `python3 lab-evaluation-verifier/10-test_feature_store_and_trap_guard.py`

### Checkpoint `11` — Train Across All 3 Managed Cloud Runtimes & Compare
- **Hub:** `4. Agentic Build` → `Checkpoint 11`
- **Steer `agy`:**
  - Direct `agy` to execute training and evaluation across all 3 managed cloud runtimes:
    1. **BigQuery ML (`challenger_xgb`)**
    2. **Managed Service for Apache Spark Serverless**
    3. **Agent Platform CustomJob (`e2-standard-4`)**
  - Materialize `l400_ds_work.eval_comparison` and write `artifacts/eval_metrics.json`.
  - *Cloud job runtime note:* On a brand-new GCP project, your first Agent Platform `CustomJob` stays in `Pending` for ~6–12 minutes during one-time tenant network peering before running in ~2 minutes, and BigQuery ML `BOOSTED_TREE_REGRESSOR` over the ~888k-row station spine can run ~8–14 minutes — use a generous `>=20-minute` poll timeout and wait until **all 3 cloud jobs reach `Succeeded`** before verifying!
- **Inspect in Clone:**
  - `artifacts/eval_metrics.json`
- **Review All 3 Cloud Runtimes in Console (`CP 11` Breadcrumb Strip):**
  - **1. BigQuery (`US`):** `BigQuery -> Studio -> Datasets -> l400_ds_work` → check `Tables` (`eval_comparison`, `spark_challenger_preds`, `vertex_challenger_preds`) and `Models` (`challenger_xgb`).
  - **2. Spark (`spark-region`):** `Managed Service for Apache Spark -> Serverless -> Batches` → confirm **`Succeeded`**.
  - **3. Agent Platform (`vertex-ai-region`):** `Agent Platform -> Models -> More services -> Training -> Custom jobs` → confirm **`Succeeded`** & `View logs`.
- **Verify (`Human Terminal`):**
  - Run: `python3 lab-evaluation-verifier/11-test_model_training_and_artifacts.py`

### Checkpoint `12` — Executive Showdown, Critique & In-Place Agent Upgrade
- **Hub:** `4. Agentic Build` → `Checkpoint 12`
- **Steer `agy`:**
  - Author root `EVALUATION.md` comparing Pass 1 Tier 0 vs. all Pass 2 challengers and SQL ensemble on the identical 30-day holdout.
  - Author `docs/agent_critique.md`.
  - Update your existing **`NYC Citi Bike Tier 0 Demand Agent` in place** so its `Knowledge sources` include your Pass 2 `l400_ds_work` tables alongside `citibike_tier0`.
- **Inspect in Clone:**
  - `EVALUATION.md`
  - `docs/agent_critique.md`
- **Review in Cloud Console:**
  - Click **`Open BigQuery Agents ↗`** on the `CP 12` Console Breadcrumb.
  - Navigate: `BigQuery -> Agents -> Agent tab -> NYC Citi Bike Tier 0 Demand Agent -> Details (right pane) -> Knowledge sources -> View more`
  - Confirm **1 unified agent** now lists Pass 2 `l400_ds_work` tables (`feature_spine`, `spark_challenger_preds`, `vertex_challenger_preds`, `eval_comparison`) alongside Pass 1's `citibike_tier0` tables.
  - Click **`+ New conversation`** to ask how your Tier 2 challengers and ensemble compare against the Tier 0 baseline floor!
- **Verify (`Human Terminal`):**
  - Run: `python3 lab-evaluation-verifier/12-test_baseline_comparison_and_decision.py`
  - Click **`✅ Checkpoints (12/12)` → `🔄 Sync Evaluator`** in the Hub header!

---

## After Class — Backups, Other 8 Enterprise Archetypes & Teardown

- **Save Your Work to Your Private Repo:**
  - Run: `git add -A && git commit -m "Complete L400 Agentic Data Science lab" && git push`
  - *(Safe: `.gitignore` excludes `agent-config.json`, `artifacts/`, `*.zip`, and Terraform state.)*
- **Explore the Other 8 Enterprise Use Cases:**
  - Open Hub `2. Discovery & Architectures`, expand the 8 additional enterprise archetypes drawer, and see [How-to-Reset-this-Project.md](How-to-Reset-this-Project.md) + `python3 data/loader.py --problem <id>`.
