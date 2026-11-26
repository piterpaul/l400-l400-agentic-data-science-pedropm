# Agent Skills & Python Scripting Standards
**Trigger:** Read this file whenever you are asked to write a new Python script, CLI automation, or an Agent Skill (`SKILL.md` / `run.py`).

## 🌐 1. Dependency Preferences (The REST API & CLI Default)
- **Highly Preferred:** Default to using Google Cloud REST APIs (with `google-auth` and `requests` or `urllib.request`) or the `bq` / `gcloud` CLI so scripts run cleanly without heavy dependencies.
- **Fallback (If Necessary):** For Tier 2 statistical/ML workloads (`lifelines`, `lightgbm`, `scikit-learn`, `pandas`, `google-cloud-bigquery`), run via `uv run` or the course virtual environment (`~/.venv`).
- **Never** use `pip` directly if `uv` is available; never use static API keys or service-account JSON key files.

## 🛠️ 2. Dual-Identity Authentication Pattern (CRITICAL)
On the L400 course Cloud Workstation:
1. **Google Cloud Resources (BigQuery, Conversational Analytics API, Vertex AI):**
   - Authenticate via Application Default Credentials (`google.auth.default()`) or `gcloud auth print-access-token`, which runs as the student's active **Argolis** identity against `config["gcp-project-id"]`.
   - Always include header `"x-goog-user-project": config["gcp-project-id"]` when calling REST APIs like `geminidataanalytics.googleapis.com`.
2. **Course Services (`lab-evaluation-verifier`):**
   - Authenticate using an OIDC identity token minted for the student's **`@google.com`** corporate identity (`config["user_email"]`):
     `gcloud auth print-identity-token --account=<user_email>` (with **no** `--audiences` flag).

## 📂 3. Skill Directory Structure
Every skill in `.agents/skills/[skill-name]/` must follow this structure:
- `SKILL.md`: YAML frontmatter (`name`, `description`) + usage instructions and examples.
- `scripts/run.py`: Modular, executable Python implementation.
- `scripts/requirements.txt`: Required packages (`google-auth`, `requests`).

## 📥 4. Configuration Loading Pattern (CRITICAL)
**NEVER hardcode project IDs, dataset names, regions, or user emails.** Always read `agent-config.json` from the workspace root:

```python
import json

with open("agent-config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

project_id = config["gcp-project-id"]
dataset = config["bigquery-dataset"]
bigquery_region = config.get("bigquery-region", "US")
spark_region = config.get("spark-region") or config.get("vertex-ai-region", "us-central1")
vertex_region = config.get("vertex-ai-region", "us-central1")
user_email = config["user_email"]
```
- **3-Service Regional Rule:** Pass `bigquery_region` (`"US"`) to BigQuery CLI/SDK calls (`bq --location=US ...`), `spark_region` (`"us-central1"`, or fallback `"us-east1"` / `"us-east4"` / `"us-west1"`) to **Managed Service for Apache Spark (`Serverless -> Batches`)** (`gcloud dataproc batches submit pyspark --region=...`), and `vertex_region` (`"us-central1"` or fallback) to **Agent Platform (Vertex AI) Custom Jobs (`Models -> More services -> Training -> Custom jobs`)** (`gcloud ai custom-jobs create --region=...`) and Model Registry.

## 🚀 5. Cloud Job Execution, Container Image & Completion Polling Rules (CRITICAL)
When building and executing a Pass 2 **Tier 2** challenger tournament, **both** the Managed Service for Apache Spark Serverless batch **and** the Agent Platform (Vertex AI) CustomJob must complete (`SUCCEEDED` / `JOB_STATE_SUCCEEDED`) and materialize their BigQuery prediction tables before Checkpoint 11 can pass:

1. **Agent Platform (Vertex AI) CustomJobs (`gcloud ai custom-jobs create --region=$VERTEX_REGION`):**
   - **Machine Type (`machineType`):** ALWAYS use `"e2-standard-4"` (or `"e2-standard-8"`). **NEVER** use legacy `"n1-standard-4"`, which suffers from 10–15+ minute worker pool queue starvation across regional pools.
   - **Container Image (`imageUri`):** ALWAYS use `"python:3.11-slim"` and install Python wheels at container boot (`pip install -q --no-cache-dir google-cloud-bigquery google-cloud-bigquery-storage google-cloud-storage pyarrow db-dtypes pandas numpy scikit-learn xgboost statsmodels`) over the pre-provisioned Cloud NAT. **NEVER** guess deprecated or removed `us-docker.pkg.dev/vertex-ai/training/scikit-learn-cpu.*` or `xgboost-cpu.*` image tags.
   - **Worker Service Account (`serviceAccount`):** Look up `PROJECT_NUMBER=$(gcloud projects describe "$PROJECT_ID" --format="value(projectNumber)")` and set `serviceAccount: ${PROJECT_NUMBER}-compute@developer.gserviceaccount.com` in the CustomJob YAML spec so the worker has IAM access to BigQuery and Cloud Storage.
   - **Output Table:** Write holdout predictions from inside the container to `<project>.<dataset>.vertex_challenger_preds`.
2. **Managed Service for Apache Spark Serverless (`gcloud dataproc batches submit pyspark --region=$SPARK_REGION --version=2.3 --deps-bucket=gs://...`):**
   - Read `<project>.<dataset>.feature_spine` via the built-in `spark-bigquery` connector and write holdout predictions directly to `<project>.<dataset>.spark_challenger_preds` (`writeMethod="direct"`).
3. **Regional Staging Bucket Alignment:**
   - Dataproc `--deps-bucket` and Vertex `baseOutputDirectory.outputUriPrefix` must reside in the same region as the compute job. If `spark-region` or `vertex-ai-region` differs from `gcs-code-bucket`'s location (e.g., after switching to `us-east1`), auto-create `gs://${PROJECT_ID}-stage-${REGION}` (`gcloud storage buckets create gs://${PROJECT_ID}-stage-${REGION} --location=${REGION} --uniform-bucket-level-access`) while keeping all BigQuery datasets in `US`.
4. **Concurrent Launch, Mandatory Completion Polling & Output Review:**
   - Launch BigQuery ML (`CREATE OR REPLACE MODEL <dataset>.challenger_xgb ...` in `US`), the Serverless Spark batch (`--async`), and the Agent Platform CustomJob concurrently (e.g., `concurrent.futures.ThreadPoolExecutor`).
   - Poll `gcloud dataproc batches describe` until `state == "SUCCEEDED"` AND `gcloud ai custom-jobs describe` until `state == "JOB_STATE_SUCCEEDED"`. Never treat job submission alone as completion; if either job enters `FAILED` / `JOB_STATE_FAILED`, inspect its logs/error message, fix the root cause, and re-run until **both** jobs succeed and populate `spark_challenger_preds` and `vertex_challenger_preds`, then assemble `<project>.<dataset>.eval_comparison` and `artifacts/eval_metrics.json`.
