# How to Reset This Project

Use this runbook to reset generated artifacts and BigQuery datasets between runs without destroying your greenfield Argolis GCP project (`terraform/`).

---

## Option 1: Reset Pass 2 Only (Switch Solo Problem Track — Checkpoints `07–12`)

If you completed Pass 1 (`Checkpoints 01–06`) and want to switch to a different Pass 2 catalog problem or tier without touching your Guided Tier 0 NYC Citi Bike baseline:

```bash
# 1. Remove Pass 2 generated documents and evaluation bundles
rm -f docs/discovery-pack.md \
      DESIGN.md \
      EVALUATION.md \
      docs/EVALUATION.md \
      docs/agent_critique.md \
      lab-evaluation-verifier/discovery_pack_handover.zip \
      lab-evaluation-verifier/solution_design_brief.zip \
      lab-evaluation-verifier/agent_build_skill.zip \
      lab-evaluation-verifier/feature_store_and_trap_guard.zip \
      lab-evaluation-verifier/model_training_and_artifacts.zip \
      lab-evaluation-verifier/baseline_comparison_and_decision.zip

# 2. Recreate an empty l400_ds_work dataset in BigQuery
PROJECT_ID=$(python3 -c "import json; print(json.load(open('agent-config.json')).get('gcp-project-id',''))")
bq rm -r -f -d "${PROJECT_ID}:l400_ds_work"
bq --location=US mk -d "${PROJECT_ID}:l400_ds_work"
```

---

## Option 2: Full Lab Reset (Restart from Checkpoint `02`, Keep Terraform Project)

If you want to replay the entire lab from Pass 1 (`Checkpoint 02`) while keeping your provisioned Argolis project (`terraform/terraform.tfstate` and `agent-config.json`):

```bash
# 1. Delete all generated Pass 1 and Pass 2 artifacts
rm -rf artifacts
rm -f docs/discovery-pack-tier0.md \
      docs/discovery-pack.md \
      labs/guided/citibike/DESIGN-tier0.md \
      labs/guided/citibike/tier0_baseline.sql \
      labs/guided/citibike/tier1_trigger.md \
      DESIGN.md \
      EVALUATION.md \
      docs/EVALUATION.md \
      docs/agent_critique.md \
      lab-evaluation-verifier/*.zip

# 2. Recreate empty citibike_tier0 and l400_ds_work datasets in BigQuery
PROJECT_ID=$(python3 -c "import json; print(json.load(open('agent-config.json')).get('gcp-project-id',''))")
bq rm -r -f -d "${PROJECT_ID}:citibike_tier0"
bq rm -r -f -d "${PROJECT_ID}:l400_ds_work"
bq --location=US mk -d "${PROJECT_ID}:citibike_tier0"
bq --location=US mk -d "${PROJECT_ID}:l400_ds_work"
```

---

## Option 3: Maintainer Prep Before Committing for CE Use

Before pushing changes to the template repository, ensure none of the student-generated deliverables are tracked:
- `docs/discovery-pack-tier0.md` and `docs/discovery-pack.md` must **not** exist
- `.agents/rules/` must contain the 5 shipped workspace governance `.md` files (`lab_governance.md`, `data_science_standards.md`, `bigquery_ai_and_ml_standards.md`, `agent_skills_standards.md`, `terraform_standards.md`)
- `.agents/skills/` must contain `discovery-pack-fetch`, `conversational-analytics-agent`, and all 4 `bigquery-data-science` skills (`bigquery-data-science`, `bigquery-ai`, `bigquery-ml`, `bigquery-mlops`), while the 15 Data Agent Kit skills are installed dynamically by `deploy.sh` and gitignored
- `labs/guided/citibike/DESIGN-tier0.md`, `labs/guided/citibike/tier0_baseline.sql`, and `labs/guided/citibike/tier1_trigger.md` must **not** exist
- `DESIGN.md`, `EVALUATION.md`, `docs/agent_critique.md`, and `artifacts/` must **not** exist
- `agent-config.json` must **not** be tracked (it is gitignored; `agent-config.example.json` holds the tracked placeholder template)
- `lab-evaluation-verifier/*.zip` and `terraform/tf-output.json` must **not** exist
