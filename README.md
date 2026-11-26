# L400 Agentic Data Science — Student Lab Repository

Companion workspace for **L400 Agentic Data Science** — used **before, during, and after class** to provision your greenfield Google Cloud project, steer the Antigravity coding agent (`agy`), and verify all 12 lab checkpoints.

> **Step-by-Step Classroom & Self-Paced Walkthrough:** Follow [**`LAB_WALKTHROUGH.md`**](LAB_WALKTHROUGH.md) from start (`Checkpoint 01`) to finish (`Checkpoint 12`) alongside the [**Live Classroom Hub UI**](https://data-science-hub-463617135523.us-central1.run.app).
> **Preparing ahead of class?** Start right away with [**Step 0**](#step-0-environment-setup-5-min) below so your repository and Google Cloud project are ready before class begins.

---

## How the Class Works

You pair the **Classroom Hub** (in your browser) with **`agy`** (in this repo) to walk a **4-Step Loop** (`Discover → Design → Build → Verify`) across **two passes** — with all data & ML compute running on managed Google Cloud services (never locally on your Cloudtop VM):

| Stage | Pass 1: Guided Baseline (`Checkpoints 01–06`) | Pass 2: Solo Challenger (`Checkpoints 07–12`) |
| :--- | :--- | :--- |
| **Setup** | **`01`** — Provision greenfield GCP project (`source deploy.sh`). | Reuses the same GCP project (`l400_ds_work` dataset). |
| **1. Discover** | **`02`** — Bound at **Tier 0** & resolve `docs/discovery-pack-tier0.md`. | **`07`** — Bound at **Tier 1 or 2** & resolve `docs/discovery-pack.md`. |
| **2. Design** | **`03`** — Steer `agy` to profile BigQuery data & write `DESIGN-tier0.md`. | **`08`** — Steer `agy` to audit schemas/traps & approve `DESIGN.md`. |
| **3. Build** | **`04–06`** — Calendar spine, zero-DDL BigQuery `AI.*` baseline, & Data Agent. | **`09–11`** — Package `SKILL.md`, build leak-free spine, & train on Cloud runtimes. |
| **4. Verify** | Measure holdout accuracy & document escalation criteria (`tier1_trigger.md`). | **`12`** — Benchmark Pass 2 vs. Pass 1 on the same holdout (`EVALUATION.md`). |

- **`agy` (Coding Agent):** Reads `AGENTS.md`, `agent-config.json`, `.agents/rules/*.md`, and `.agents/skills/`; profiles BigQuery; authors specs, SQL, skills, and cloud jobs.
- **You (Architect):** Frame constraints, review & approve `DESIGN.md` before training, and **always run `lab-evaluation-verifier/` scripts yourself in your terminal** (`agy` never reads or runs `./lab-evaluation-verifier/`).

---

## Step 0: Environment Setup (`~5 min`)

### 1. Create Your Personal Private Repo from This Template
1. On [`cloud-gtm/l400-agentic-data-science-labs`](https://github.com/cloud-gtm/l400-agentic-data-science-labs), click **Use this template** (top right) → **Create a new repository**.
2. **Owner:** Your **personal GitHub handle** (**do NOT select `cloud-gtm`**).
3. **Repository name:** `l400-agentic-data-science-<your-google-ldap>` · **Visibility:** **Private** → **Create repository**.

### 2. Clone into `~/l400/l400-agentic-data-science-labs` & Open as Workspace Root
```bash
mkdir -p ~/l400 && cd ~/l400
git clone https://github.com/<YOUR-GITHUB-HANDLE>/l400-agentic-data-science-<YOUR-LDAP>.git l400-agentic-data-science-labs
cd l400-agentic-data-science-labs
```
Open `~/l400/l400-agentic-data-science-labs` as your workspace folder in VS Code (`code ~/l400/l400-agentic-data-science-labs`) and always start `agy` from this directory.

<details>
<summary><strong>Alternatives: GitHub CLI (<code>gh</code>) or Direct Clone Fallback</strong></summary>

```bash
# Option A — GitHub CLI (gh):
mkdir -p ~/l400 && cd ~/l400
gh repo create l400-agentic-data-science-<YOUR-LDAP> --private --template cloud-gtm/l400-agentic-data-science-labs --clone
mv l400-agentic-data-science-<YOUR-LDAP> l400-agentic-data-science-labs && cd l400-agentic-data-science-labs

# Option B — Direct clone fallback (works if GitHub is not authenticated on Cloudtop):
mkdir -p ~/l400 && cd ~/l400
git clone https://github.com/cloud-gtm/l400-agentic-data-science-labs.git && cd l400-agentic-data-science-labs
```
</details>

### 3. Reset `gcloud` to Your Seed Project (If Coming from Another Lab)
If a prior lab pointed `gcloud` at a shared facilitator project, point back to your `system_check` seed project (`deploy.sh` also auto-resets cross-org projects):
```bash
PROJECT_ID="your-gcp-project-id"
gcloud config set project "${PROJECT_ID}"
gcloud config set billing/quota_project "${PROJECT_ID}"
gcloud auth application-default set-quota-project "${PROJECT_ID}"
```

### 4. Provision Your Greenfield GCP Project
```bash
source deploy.sh
```
- **Provisions:** A fresh Argolis project (`l400-agentic-ds-<id>`), required APIs (BigQuery, Vertex AI, Serverless Spark, Dataflow, Conversational Analytics), `US` BigQuery datasets (`citibike_tier0`, `l400_ds_work`), GCS buckets, and 4-region VPC/NAT networking (`us-central1`, `us-east1`, `us-east4`, `us-west1`).
- **Configures Skills & Local Config:** Generates your gitignored `agent-config.json` from `agent-config.example.json`, syncs `~/.config/data-agent-kit/config.json`, and installs [`bigquery-data-science`](https://github.com/statmike/bigquery-data-science) alongside [`data-agent-kit`](https://github.com/GoogleCloudPlatform/cloud-Agent-Skills-for-Data).
- **Regional Stockout Fallback:** Keep `"bigquery-region": "US"`; switch `"vertex-ai-region"` / `"spark-region"` in `agent-config.json` to `us-east1`, `us-east4`, or `us-west1` (or run `VERTEX_AI_REGION=us-east1 source deploy.sh`) if `us-central1` hits capacity limits.

> **Running Step 0 before class opens?** If the Evaluator reports that evaluations are currently closed at the end of `deploy.sh`, your project is still **100% ready**. Once class starts, record Checkpoint 01 in ~5 seconds without re-running Terraform:
> ```bash
> python3 lab-evaluation-verifier/01-test_terraform_infrastructure.py
> ```

---

## Checkpoints, Re-Submission & Safe Git Backups

Each verifier writes a local, gitignored `lab-evaluation-verifier/<step>.zip` on your Cloudtop and submits it with your `@google` OIDC token:

| Action | Command |
| :--- | :--- |
| **Verify a single checkpoint (`01`–`12`)** | `python3 lab-evaluation-verifier/01-test_terraform_infrastructure.py` |
| **Fast re-submit existing local `.zip` files (`~5s`)** | `python3 lab-evaluation-verifier/run-all-evals.py --resubmit-existing` |
| **Rebuild & submit all 12 checkpoints** | `python3 lab-evaluation-verifier/run-all-evals.py` |
| **Manual browser upload fallback** | Add `--manual`, download `lab-evaluation-verifier/<step>.zip` in VS Code, and upload on the Lab Evaluation Summary Portal. |

**Safe Private GitHub Backups:** `.gitignore` excludes `agent-config.json`, `lab-evaluation-verifier/*.zip`, `artifacts/`, `.env`, and `terraform/*.tfstate*`, so you can push your specs, SQL, and skills to your private repo anytime without leaking project IDs:
```bash
git add -A && git commit -m "Save L400 lab progress" && git push
```

---

## Workspace Map

| Path | Purpose |
| :--- | :--- |
| [`LAB_WALKTHROUGH.md`](LAB_WALKTHROUGH.md) | Step-by-step student & instructor walkthrough (`Checkpoints 01–12`), harness tour, and Cloud Console review map. |
| `AGENTS.md` & `docs/llms.txt` | Master instructions and workspace map read automatically by `agy`. |
| `agent-config.example.json` → `agent-config.json` | Tracked template copied by `deploy.sh` into your local, gitignored `agent-config.json`. |
| `deploy.sh` & `terraform/` | Greenfield Argolis project, APIs, networking, datasets, buckets, and skill setup. |
| `.agents/rules/*.md` | 5 governance rules (`lab_governance`, `data_science`, `bigquery_ai_and_ml`, `agent_skills`, `terraform`). |
| `.agents/skills/` | Shipped skills (`discovery-pack-fetch`, `conversational-analytics-agent`), `bigquery-data-science`, and your Pass 2 skill. |
| `labs/guided/citibike/` | Pass 1 Guided baseline workspace (`Checkpoints 02–06`). |
| `labs/data/` & `data/loader.py` | Dataset loaders for `predictive-maintenance` and `marketing-measurement`. |
| `lab-evaluation-verifier/` | Human-run checkpoint verifiers (`01-test_*.py` .. `12-test_*.py`) and `run-all-evals.py`. |
| [`How-to-Reset-this-Project.md`](How-to-Reset-this-Project.md) | Reset commands to switch Pass 2 tracks or replay from Checkpoint 02 while keeping Terraform intact. |

<details>
<summary><strong>Enterprise Problem Catalog (9 Use Cases Explored in Discovery &amp; Pass 2)</strong></summary>

| Problem ID | Use Case | Dataset Source |
| :--- | :--- | :--- |
| `forecasting` | Demand Forecasting & Inventory Allocation | `bigquery-public-data.new_york_citibike` + `ml_datasets.holidays_and_events_for_forecasting` + `noaa_gsod` |
| `next-best-offer` | Next-Best-Offer & Cross-Sell Propensity | `bigquery-public-data.thelook_ecommerce` |
| `payment-fraud` | Payment Fraud Detection | `bigquery-public-data.ml_datasets.ulb_fraud_detection` |
| `predictive-maintenance` | Predictive Maintenance & Survival Analysis | `python3 data/loader.py --problem predictive-maintenance` |
| `search-conversion` | Search & Browse Conversion | `bigquery-public-data.thelook_ecommerce.events` + `products` |
| `recommender` | Cold-Start Catalog Recommender | `bigquery-public-data.thelook_ecommerce.order_items` + `products` |
| `churn` | Customer Churn & Retention | `firebase-public-project.analytics_153293282.events_*` |
| `clinical-risk` | Clinical Risk Stratification | `bigquery-public-data.fhir_synthea` |
| `marketing-measurement` | Marketing Mix Modeling & Attribution | `python3 data/loader.py --problem marketing-measurement` |

</details>
