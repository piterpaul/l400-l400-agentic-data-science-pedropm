# Google Cloud Argolis Terraform Standards
**Trigger:** Read this file whenever you are asked to write, modify, or plan Terraform infrastructure code, or add new GCP resources.

## 🏗️ 1. Architecture & Repository Layout (CRITICAL)
This project follows the strict Google Cloud Argolis template structure. **Never create a root `main.tf`.**
- **The Orchestrator:** The root Terraform files live in `/terraform/` (e.g., `main.tf`, `variables.tf`). 
- **No Resources in Root:** The `main.tf` file is strictly for **orchestration**. It only configures providers and calls modules. Do not put `resource` blocks here.
- **The Resource Module:** All standard infrastructure (Buckets, VPCs, IAM, PubSub, Dataflow, etc.) MUST be created inside the `/terraform-modules/resources/` module.
- **Existing Modules:** If adding APIs, SQL scripts, or Colab files, use the existing modules (`/terraform-modules/apis-batch-enable/`, `/terraform-modules/sql-scripts/`, etc.).

## 🔐 2. Authentication & Provider Impersonation
- **Service Account Impersonation:** Resources must be deployed using service account impersonation to prevent leaking local keys. 
- When calling modules in `main.tf`, you MUST pass the impersonated provider: 
  `providers = { google = google.service_principal_impersonation }`
- **Never** use the default Compute Engine service account. Use the dedicated deployment service account created in the `service-account` module.

## 🏷️ 3. Naming Conventions & Uniqueness
- **Randomization for Globals:** GCP requires globally unique names for Projects and Storage Buckets. You MUST append the pre-existing random string generator to bucket names (e.g., `name = "${var.l400_ds_work_bucket}-${random_string.project_random.result}"`).
- **Resource Names:** Use `snake_case` for Terraform block labels (e.g., `resource "google_storage_bucket" "google_storage_bucket_dataflow_staging"`).
- **BigQuery:** BigQuery datasets must use underscores, not dashes (e.g., `var.bigquery_l400_ds_work_dataset`).

## 🧱 4. Variable Requirements
- All variables in `variables.tf` MUST include a `description`.
- All required variables MUST include a `validation {}` block to prevent runtime failures (e.g., `condition = length(var.project_id) > 0`).

## 🛑 5. Hard Constraints (SAFETY RULES)
- **NEVER** run `terraform destroy` directly.
- **NEVER** modify `deploy.sh` or `deploy-use-existing-project-non-org-admin.sh` without explicit human permission. These bash scripts wrap the Terraform execution.
- If you need to execute a local API call, use a `null_resource` with a `local-exec` provisioner passing the `data.google_client_config.current.access_token`.

## 🚀 6. Deployment Workflows
**Never run raw `terraform apply` commands.** Deployment is strictly handled via bash wrapper scripts. The primary and preferred method is Option 1. 

**Option 1. Elevated Privileges - Org Level (Primary/Default)**
The system automatically creates the project and deploys the infrastructure.
- **Prerequisites:** Billing Account User (to create the project with billing).
- **Execution:** Run `source deploy.sh` from the root directory.

**Option 2. Owner Project Privileges - Typically Requires Assistance from IT**
- **Prerequisites:** You will need a project pre-created for you (IT can do this). You will need to be an Owner (IAM role) of the project to run the script.
- **Execution:** 
  1. Update the hard-coded values in `deploy-use-existing-project-non-org-admin.sh`
  2. Run `source deploy-use-existing-project-non-org-admin.sh`

## ✅ 7. Definition of Done
If you add a new resource:
1. Did you put it in `/terraform-modules/resources/` (and not `/terraform/main.tf`)?
2. Did you pass variables from `variables.tf` down through `main.tf` into the `resources` module?
3. Did you format the code using `terraform fmt`?

## 🌎 8. Split-Location Architecture & Regional Stockout Resilience (Worldwide Cohorts)
This workspace deliberately separates **BigQuery Data Location (`US` multi-region)** from **Single-Region Cloud Compute Location (`vertex-ai-region`, default `us-central1`)** for all AMER, EMEA, and APAC cohorts:
- **`bigquery-region: "US"` (Always `US` Multi-Region Worldwide):** Keep `citibike_tier0`, `l400_ds_work`, and `l400-agentic-ds-data-<random_string>` in `US` so SQL and Storage API joins against `bigquery-public-data.*` and `firebase-public-project.*` require zero cross-region data copies and stay inside Google's US backbone.
- **`vertex-ai-region: "us-central1"` (Switchable Single-Region Compute for Dataproc Serverless, Vertex AI, & BigFrames):** All model training runs on managed Google Cloud compute (never locally on the Cloudtop VM). Terraform pre-provisions the `default` VPC network, internal Spark firewall rules, Cloud Router + Cloud NAT, and `default` subnets with `private_ip_google_access = true` across 4 US compute regions (`us-central1`, `us-east1`, `us-east4`, `us-west1`).
- **Regional Stockout Fallback (`RESOURCE_EXHAUSTED` / `ZONE_RESOURCE_POOL_EXHAUSTED`):** If `us-central1` experiences a classroom stockout for **Dataproc Serverless (Spark)**, **Vertex AI**, **BigFrames**, or **Dataflow**:
  1. Update `"vertex-ai-region"` in `agent-config.json` (and `"region"` in `~/.config/data-agent-kit/config.json`) to `"us-east1"`, `"us-east4"`, or `"us-west1"`.
  2. Never change `"bigquery-region": "US"`. Single-region compute workers in any US region read and write `US` multi-region BigQuery tables directly via the BigQuery Storage API (`bigquerystorage.googleapis.com`) and `gs://l400-agentic-ds-data-<random_string>` (`US`).
  3. If a regional service requires a same-region staging/deps bucket (such as Vertex AI `staging_bucket` or Dataproc `--deps-bucket`) in the fallback region, create `gs://l400-agentic-ds-code-<random_string>-<region>` in that region (`gcloud storage buckets create gs://l400-agentic-ds-code-<random_string>-<region> --location=<region>`).

## 🔄 9. Post-Deployment: Agent Configuration Update (CRITICAL)
Immediately after successfully deploying the infrastructure via the bash scripts (e.g., `source deploy.sh`), you MUST update the `agent-config.json` file located at the root of the workspace.

**Steps to update `agent-config.json`:**
1. Read the `tf-output.json` file (which is automatically generated by the deploy script in the `terraform/` folder) to extract the newly deployed values, specifically the `random_string` output.
2. Read the existing `agent-config.json` file (or copy `agent-config.example.json` to `agent-config.json` if `agent-config.json` does not exist yet).
3. Update the `"random_string"` key with the actual random string generated by Terraform.
4. For all other values in the JSON, search for the literal placeholder text `{random_string}`. Replace that placeholder with the actual random string value (e.g., `"l400-agentic-ds-{random_string}"` becomes `"l400-agentic-ds-xxxxxxxxxx"`).
5. **CONSTRAINT:** Only update existing keys. DO NOT add new keys to `agent-config.json`. If you cannot find a corresponding value to update, leave the existing value alone. Do not delete keys.
