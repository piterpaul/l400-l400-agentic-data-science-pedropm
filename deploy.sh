#!/bin/bash

####################################################################################
# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     https://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
####################################################################################

####################################################################################
# README: This script will use "bash" to deploy the code
#         This will run the "terraform" folder entrypoint (uses service account impersonation)
#         This will create a new GCP project in Terraform
# TO RUN: "source deploy.sh"
####################################################################################
#
# Required software (cloud shell has this installed):
#   - gcloud
#   - gcloud beta (sudo gcloud components install beta)
#   - terraform
#   - .jq (command line JSON parser)
#   - curl
#
# Author: Adam Paternostro
# Terraform for Google: https://registry.terraform.io/providers/hashicorp/google/latest/docs
####################################################################################

# Login to GCP by running BOTH below gcloud auth commands (you only need to do this once which is why they are commented out)
#      These command are not needed when running from a Cloud Shell
# gcloud auth login
# gcloud auth application-default login

# Ensure ~/.local/bin, ~/.cargo/bin, and ~/bin are on PATH, and auto-install terraform into ~/.local/bin if missing
export PATH="${HOME}/.local/bin:${HOME}/.cargo/bin:${HOME}/bin:${PATH}"

# Seed local (gitignored) agent-config.json from agent-config.example.json if not yet created
if [ ! -f "agent-config.json" ] && [ -f "agent-config.example.json" ]; then
  cp "agent-config.example.json" "agent-config.json"
fi
if ! command -v terraform >/dev/null 2>&1; then
  echo "Terraform CLI not found on PATH; installing Terraform v1.9.8 into ~/.local/bin..."
  mkdir -p "${HOME}/.local/bin"
  _tf_tmp="$(mktemp -d)"
  if curl -fsSL -o "${_tf_tmp}/terraform.zip" "https://releases.hashicorp.com/terraform/1.9.8/terraform_1.9.8_linux_amd64.zip"; then
    unzip -q -o "${_tf_tmp}/terraform.zip" -d "${HOME}/.local/bin"
    chmod +x "${HOME}/.local/bin/terraform"
  fi
  rm -rf "${_tf_tmp}"
fi

# Get the account name who logged in above (prefer Argolis *.altostrat.com account if active gcloud is @google.com)
gcp_account_name=$(gcloud auth list --filter=status:ACTIVE --format="value(account)")
if [[ "${gcp_account_name}" == *"@google.com" ]]; then
  _argolis_acct=$(gcloud auth list --format="value(account)" 2>/dev/null | grep -i "altostrat.com" | head -n 1 || true)
  if [ -n "${_argolis_acct}" ]; then
    echo "Detected Argolis account ${_argolis_acct}; setting it as active for Terraform deployment."
    gcp_account_name="${_argolis_acct}"
    CLOUDSDK_CORE_DISABLE_PROMPTS=1 gcloud config set account "${gcp_account_name}" --quiet >/dev/null 2>&1 || true
  fi
fi

# Verify Application Default Credentials (ADC) exist and match the Argolis account (not @google.com)
_adc_tok=$(CLOUDSDK_CORE_DISABLE_PROMPTS=1 gcloud auth application-default print-access-token --quiet 2>/dev/null || true)
_adc_email=""
if [ -n "${_adc_tok}" ]; then
  _adc_email=$(curl -fsSL "https://oauth2.googleapis.com/tokeninfo?access_token=${_adc_tok}" 2>/dev/null | python3 -c "import sys, json; print(json.load(sys.stdin).get('email', ''))" 2>/dev/null || true)
fi
if [ -z "${_adc_tok}" ] || { [[ "${gcp_account_name}" == *"altostrat.com"* ]] && [[ "${_adc_email}" == *"@google.com" ]]; }; then
  echo "⚠️  Application Default Credentials (ADC) are missing or signed in as '${_adc_email:-none}' instead of '${gcp_account_name}'."
  echo "   Terraform requires ADC authenticated with your Argolis account (${gcp_account_name})."
  if [ "${DEPLOY_AUTO_CONFIRM:-0}" != "1" ]; then
    echo "   Launching 'gcloud auth application-default login' — please sign in as ${gcp_account_name}:"
    gcloud auth application-default login
  fi
fi

# Clear any stale project / quota_project from a previous lab (e.g., l400-agentic-data-analytics or l400-agentic-data-eng)
# BEFORE querying organizations or billing accounts so gcloud never sends a disabled or deleted X-Goog-User-Project header.
_prev_gcloud_proj=$(CLOUDSDK_CORE_DISABLE_PROMPTS=1 gcloud config get-value project --quiet 2>/dev/null || true)
unset GOOGLE_CLOUD_PROJECT
unset CLOUDSDK_CORE_PROJECT
unset GOOGLE_CLOUD_QUOTA_PROJECT
unset CLOUDSDK_BILLING_PROJECT
CLOUDSDK_CORE_DISABLE_PROMPTS=1 gcloud config unset project --quiet >/dev/null 2>&1 || true
CLOUDSDK_CORE_DISABLE_PROMPTS=1 gcloud config unset billing/quota_project --quiet >/dev/null 2>&1 || true

# Allow optional compute region override (e.g., VERTEX_AI_REGION=us-east1 SPARK_REGION=us-east1 source deploy.sh during a stockout)
vertex_ai_region="${VERTEX_AI_REGION:-us-central1}"
spark_region="${SPARK_REGION:-${vertex_ai_region}}"
default_zone="${DEFAULT_ZONE:-${vertex_ai_region}-a}"

# Get the Org Id (needed for org policies and creating the GCP project)
org_id=$(CLOUDSDK_CORE_DISABLE_PROMPTS=1 gcloud organizations list --account="${gcp_account_name}" --format="value(name)" --quiet 2>/dev/null | head -n 1)
if [ -z "${org_id}" ]
then
  echo "Org Id could not be automatically read."
  echo "Open this link: https://console.cloud.google.com/cloud-resource-manager/ and copy your org id."
  echo "Your org id will be in the format of xxxxxxxxxxxx"
  read -p "Please enter your org id:" org_id
else
  org_id_length=$(echo -n "${org_id}" | wc -m)
  org_id_length_int=$(expr ${org_id_length} + 0)
  if [ ${org_id_length_int} -gt 13 ]
  then
    echo "You have more than one org id, please manually enter the correct one."
    echo "Your org id will be in the format of xxxxxxxxxxxx"
    read -p "Please enter your org id:" org_id
  else
    echo "Org Id was automatically retrieved."
  fi
fi

# Discover active projects inside the student's OWN Argolis organization (preferring non-l400 seed projects first
# because prior labs like l400-agentic-data-analytics or l400-agentic-data-eng may not have enabled cloudbilling.googleapis.com).
_raw_org_projects=$(CLOUDSDK_CORE_DISABLE_PROMPTS=1 gcloud projects list --account="${gcp_account_name}" --filter="parent.id=${org_id} AND lifecycleState=ACTIVE" --format="value(projectId)" --limit=25 --quiet 2>/dev/null || true)
if [ -z "${_raw_org_projects}" ]; then
  _raw_org_projects=$(CLOUDSDK_CORE_DISABLE_PROMPTS=1 gcloud projects list --account="${gcp_account_name}" --filter="lifecycleState=ACTIVE" --format="value(projectId)" --limit=20 --quiet 2>/dev/null || true)
fi
_seed_first=$(echo "${_raw_org_projects}" | grep -v '^l400-' || true)
_l400_rest=$(echo "${_raw_org_projects}" | grep '^l400-' || true)
_org_projects=$(printf "%s\n%s\n" "${_seed_first}" "${_l400_rest}" | awk 'NF && !seen[$0]++')

# Get the Billing Account (needed for creating the GCP project)
# Strategy 0: Honor explicit BILLING_ACCOUNT_ID environment variable if set
billing_account="${BILLING_ACCOUNT_ID:-}"
_verified_billing_proj=""

# Strategy 1: Inspect billingAccountName attached to the user's active projects in their Argolis org (seed projects first)
if [ -z "${billing_account}" ]; then
  for _bp in ${_org_projects}; do
    _bname=$(CLOUDSDK_CORE_DISABLE_PROMPTS=1 gcloud billing projects describe "${_bp}" --account="${gcp_account_name}" --billing-project="${_bp}" --format="value(billingAccountName)" --quiet 2>/dev/null || CLOUDSDK_CORE_DISABLE_PROMPTS=1 gcloud beta billing projects describe "${_bp}" --account="${gcp_account_name}" --billing-project="${_bp}" --format="value(billingAccountName)" --quiet 2>/dev/null || true)
    if [[ "${_bname}" == billingAccounts/* ]]; then
      billing_account="${_bname#billingAccounts/}"
      _verified_billing_proj="${_bp}"
      echo "Recovered Billing Account (${billing_account}) from existing project ${_bp}."
      break
    fi
  done
fi

# Strategy 2: Try listing open billing accounts using each org project as the billing/quota project
if [ -z "${billing_account}" ]; then
  for _bp in ${_org_projects}; do
    billing_account=$(CLOUDSDK_CORE_DISABLE_PROMPTS=1 gcloud billing accounts list --account="${gcp_account_name}" --billing-project="${_bp}" --filter="open=true" --format="value(ACCOUNT_ID)" --limit=1 --quiet 2>/dev/null || true)
    if [ -n "${billing_account}" ]; then
      _verified_billing_proj="${_bp}"
      echo "Recovered Billing Account (${billing_account}) via quota project ${_bp}."
      break
    fi
  done
fi

# Strategy 3: If all existing projects in the org had cloudbilling.googleapis.com disabled (e.g., coming straight from
# l400-agentic-data-analytics or l400-agentic-data-eng without a seed project that enabled Cloud Billing API),
# automatically enable cloudbilling.googleapis.com on the first active org project and read its billingAccountName.
if [ -z "${billing_account}" ] && [ -n "${_org_projects}" ]; then
  _first_bp=$(echo "${_org_projects}" | head -n 1)
  if [ -n "${_first_bp}" ]; then
    echo "Enabling cloudbilling.googleapis.com on existing project ${_first_bp} to auto-discover Billing Account..."
    CLOUDSDK_CORE_DISABLE_PROMPTS=1 gcloud services enable cloudbilling.googleapis.com --project="${_first_bp}" --account="${gcp_account_name}" --quiet >/dev/null 2>&1 || true
    for _retry in 1 2 3; do
      _bname=$(CLOUDSDK_CORE_DISABLE_PROMPTS=1 gcloud billing projects describe "${_first_bp}" --account="${gcp_account_name}" --billing-project="${_first_bp}" --format="value(billingAccountName)" --quiet 2>/dev/null || true)
      if [[ "${_bname}" == billingAccounts/* ]]; then
        billing_account="${_bname#billingAccounts/}"
        _verified_billing_proj="${_first_bp}"
        echo "Recovered Billing Account (${billing_account}) after enabling Cloud Billing API on ${_first_bp}."
        break
      fi
      billing_account=$(CLOUDSDK_CORE_DISABLE_PROMPTS=1 gcloud billing accounts list --account="${gcp_account_name}" --billing-project="${_first_bp}" --filter="open=true" --format="value(ACCOUNT_ID)" --limit=1 --quiet 2>/dev/null || true)
      if [ -n "${billing_account}" ]; then
        _verified_billing_proj="${_first_bp}"
        echo "Recovered Billing Account (${billing_account}) after enabling Cloud Billing API on ${_first_bp}."
        break
      fi
      sleep 2
    done
  fi
fi

# Strategy 4: Direct open billing accounts list (without --billing-project, for brand-new orgs with zero projects)
if [ -z "${billing_account}" ]; then
  billing_account=$(CLOUDSDK_CORE_DISABLE_PROMPTS=1 gcloud billing accounts list --account="${gcp_account_name}" --filter="open=true" --format="value(ACCOUNT_ID)" --limit=1 --quiet 2>/dev/null || CLOUDSDK_CORE_DISABLE_PROMPTS=1 gcloud beta billing accounts list --account="${gcp_account_name}" --format="value(ACCOUNT_ID)" --limit=1 --quiet 2>/dev/null || true)
fi

# Point gcloud's active project and billing/quota_project at the verified working project (until Terraform creates the new project)
if [ -n "${_verified_billing_proj}" ]; then
  CLOUDSDK_CORE_DISABLE_PROMPTS=1 gcloud config set project "${_verified_billing_proj}" --quiet >/dev/null 2>&1 || true
  CLOUDSDK_CORE_DISABLE_PROMPTS=1 gcloud config set billing/quota_project "${_verified_billing_proj}" --quiet >/dev/null 2>&1 || true
elif [ -n "${_prev_gcloud_proj}" ] && [ "${_prev_gcloud_proj}" != "(unset)" ] && echo "${_org_projects}" | grep -qx "${_prev_gcloud_proj}"; then
  CLOUDSDK_CORE_DISABLE_PROMPTS=1 gcloud config set project "${_prev_gcloud_proj}" --quiet >/dev/null 2>&1 || true
fi

if [ -z "${billing_account}" ]
then
  echo "Billing Account could not be automatically read."
  echo "Tip: If your gcloud CLI was pointed at another user's project, reset it to your seed project with:"
  echo "  gcloud config unset billing/quota_project && gcloud auth application-default set-quota-project <YOUR_SEED_PROJECT_ID>"
  echo "Open this link: https://console.cloud.google.com/billing/ and copy your billing account."
  echo "Your billing account will be in the format of xxxxxx-xxxxxx-xxxxxx"
  read -p "Please enter your billing account:" billing_account
else
  billing_account_length=$(echo -n "${billing_account}" | wc -m)
  billing_account_length_int=$(expr ${billing_account_length} + 0)
  if [ ${billing_account_length_int} != 20 ]
  then
    echo "You have more than one billing account, please manually enter the correct one."
    echo "Your billing account will be in the format of xxxxxx-xxxxxx-xxxxxx"
    read -p "Please enter your billing account:" billing_account
  else
    echo "Billing Account was automatically retrieved."
  fi
fi

echo "gcp_account_name: ${gcp_account_name}"
echo "billing_account:  ${billing_account}"
echo "org_id:           ${org_id}"
echo "compute_region:   ${vertex_ai_region} (BigQuery datasets stay in 'US' multi-region)"

if [ "${DEPLOY_AUTO_CONFIRM:-0}" != "1" ]; then
  echo "*********************************************************"
  read -p "Press [Enter] key if all the above items are set (gcp_account_name, org_id, billing_account). If not press Ctrl+C ..."
  echo "*********************************************************"
fi


####################################################################################
# Deploy Terraform
####################################################################################
currentDir=$(pwd -P)
export TF_LOG=INFO
export TF_LOG_PATH="${currentDir}/tf.log"

cd "./terraform"

# Initialize Terraform
terraform init

# Validate
terraform validate

start=$(date)

echo "terraform apply -var=\"gcp_account_name=${gcp_account_name}\" -var=\"org_id=${org_id}\" -var=\"billing_account=${billing_account}\" -var=\"project_id=l400-agentic-ds\" -var=\"vertex_ai_region=${vertex_ai_region}\" -var=\"default_region=${vertex_ai_region}\" -var=\"default_zone=${default_zone}\""

# Strip any stale quota_project_id from a temporary ADC copy so the impersonated
# service account in the new project never sends X-Goog-User-Project for an old project.
unset GOOGLE_CLOUD_QUOTA_PROJECT
_adc_src="${GOOGLE_APPLICATION_CREDENTIALS:-${HOME}/.config/gcloud/application_default_credentials.json}"
_adc_tmp=""
if [ -f "${_adc_src}" ]; then
  _adc_tmp="$(mktemp)"
  python3 -c '
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
d.pop("quota_project_id", None)
json.dump(d, open(sys.argv[2], "w", encoding="utf-8"))
' "${_adc_src}" "${_adc_tmp}" 2>/dev/null || cp "${_adc_src}" "${_adc_tmp}"
  chmod 600 "${_adc_tmp}"
fi

# Run the Terraform Apply (with automatic 2nd pass on transient API batch / state serialization race)
_run_tf_apply() {
  if [ -n "${_adc_tmp}" ] && [ -f "${_adc_tmp}" ]; then
    GOOGLE_APPLICATION_CREDENTIALS="${_adc_tmp}" terraform apply -auto-approve \
      -var="gcp_account_name=${gcp_account_name}" \
      -var="org_id=${org_id}" \
      -var="billing_account=${billing_account}" \
      -var="project_id=l400-agentic-ds" \
      -var="vertex_ai_region=${vertex_ai_region}" \
      -var="default_region=${vertex_ai_region}" \
      -var="default_zone=${default_zone}"
    return $?
  else
    terraform apply -auto-approve \
      -var="gcp_account_name=${gcp_account_name}" \
      -var="org_id=${org_id}" \
      -var="billing_account=${billing_account}" \
      -var="project_id=l400-agentic-ds" \
      -var="vertex_ai_region=${vertex_ai_region}" \
      -var="default_region=${vertex_ai_region}" \
      -var="default_zone=${default_zone}"
    return $?
  fi
}

_run_tf_apply
terraform_exit_code=$?

if [ $terraform_exit_code -ne 0 ]; then
  echo ""
  echo "================================================================================"
  echo "⚠️  First Terraform pass exited with code ${terraform_exit_code} (often a transient API propagation or batch-enable race)."
  echo "🔄 Waiting 5 seconds and automatically running a 2nd Terraform pass to converge state..."
  echo "================================================================================"
  sleep 5
  _run_tf_apply
  terraform_exit_code=$?
fi

if [ -n "${_adc_tmp}" ] && [ -f "${_adc_tmp}" ]; then
  rm -f "${_adc_tmp}"
fi
echo "Terraform exit code: ${terraform_exit_code}"

echo "Terraform Times"
stop=$(date)
echo "Start time: ${start}"
echo "Stop  time: ${stop}"
echo ""

if [ $terraform_exit_code -eq 0 ]
then
  
  # Write out the output variables 
  terraform output -json > tf-output.json

  # Auto-sync ../agent-config.json from tf-output.json so Checkpoint 01 passes immediately
  python3 -c '
import json, os, subprocess
tf_path, cfg_path, example_path = "tf-output.json", "../agent-config.json", "../agent-config.example.json"
if os.path.exists(tf_path):
    tf_out = json.load(open(tf_path, encoding="utf-8"))
    if os.path.exists(cfg_path):
        cfg = json.load(open(cfg_path, encoding="utf-8"))
    elif os.path.exists(example_path):
        cfg = json.load(open(example_path, encoding="utf-8"))
    else:
        cfg = {}
    rnd = tf_out.get("random_string", {}).get("value", "")
    proj = tf_out.get("project_id", {}).get("value", "")
    acct = tf_out.get("gcp_account_name", {}).get("value", "")
    v_reg = tf_out.get("vertex_ai_region", {}).get("value", "") or os.environ.get("VERTEX_AI_REGION", "us-central1")
    s_reg = os.environ.get("SPARK_REGION", "") or v_reg or "us-central1"
    m_reg = tf_out.get("multi_region", {}).get("value", "") or "US"
    t0_ds = tf_out.get("citibike_tier0_dataset", {}).get("value", "")
    wk_ds = tf_out.get("l400_ds_work_dataset", {}).get("value", "")
    code_bkt = tf_out.get("terraform-output-bucket", {}).get("value", "")
    google_email = ""
    try:
        out = subprocess.check_output(["gcloud", "auth", "list", "--format=value(account)"], text=True)
        for line in out.splitlines():
            if line.strip().endswith("@google.com"):
                google_email = line.strip()
                break
    except Exception:
        pass
    if rnd:
        cfg["random_string"] = rnd
        cfg["gcs-data-bucket"] = f"l400-agentic-ds-data-{rnd}"
        cfg["gcs-code-bucket"] = code_bkt or f"l400-agentic-ds-code-{rnd}"
    if proj:
        cfg["gcp-project-id"] = proj
    if google_email or acct:
        cfg["user_email"] = google_email or acct
    if m_reg:
        cfg["bigquery-region"] = m_reg
    if s_reg:
        cfg["spark-region"] = s_reg
    if v_reg:
        cfg["vertex-ai-region"] = v_reg
    if t0_ds:
        cfg["tier0-bigquery-dataset"] = t0_ds
    if wk_ds:
        cfg["bigquery-dataset"] = wk_ds
    with open(cfg_path, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=4)
        f.write("\n")
    print(f"Updated agent-config.json with gcp-project-id={proj}, bigquery-region={m_reg}, spark-region={s_reg}, vertex-ai-region={v_reg} (random_string={rnd})")
    if proj:
        dak_cfg_path = os.path.join(os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config")), "data-agent-kit/config.json")
        os.makedirs(os.path.dirname(dak_cfg_path), exist_ok=True)
        dak_cfg = {}
        if os.path.exists(dak_cfg_path):
            try:
                dak_cfg = json.load(open(dak_cfg_path, encoding="utf-8"))
            except Exception:
                dak_cfg = {}
        dak_cfg["projectId"] = proj
        dak_cfg["region"] = v_reg or "us-central1"
        dak_cfg.setdefault("services", [
            "BigQuery",
            "Cloud Storage",
            "Apache Spark",
            "Dataflow",
            "Bigtable",
            "Knowledge Catalog",
        ])
        with open(dak_cfg_path, "w", encoding="utf-8") as df:
            json.dump(dak_cfg, df, indent=2)
            df.write("\n")
        print(f"Synced Data Agent Kit (~/.config/data-agent-kit/config.json) to projectId={proj}, region={v_reg}")
'

  deployed_project_id=$(terraform output -raw project_id 2>/dev/null || true)
  deployed_random=$(terraform output -raw random_string 2>/dev/null || true)
  if [ -n "${deployed_project_id}" ]; then
    echo "Setting active gcloud project & quota project to: ${deployed_project_id}"
    CLOUDSDK_CORE_DISABLE_PROMPTS=1 gcloud config set project "${deployed_project_id}" --quiet >/dev/null 2>&1 || true
    CLOUDSDK_CORE_DISABLE_PROMPTS=1 gcloud config set billing/quota_project "${deployed_project_id}" --quiet >/dev/null 2>&1 || true
    CLOUDSDK_CORE_DISABLE_PROMPTS=1 gcloud auth application-default set-quota-project "${deployed_project_id}" --quiet >/dev/null 2>&1 || true
    export GOOGLE_CLOUD_PROJECT="${deployed_project_id}"
  fi

  # Get the name of the bucket the user specified to upload the output file
  terraform_output_bucket=$(terraform output -raw terraform-output-bucket)
  echo "terraform_output_bucket: ${terraform_output_bucket}"

  # Copy TF Output - Check to see if the user did not specify an output bucket
  if [[ $terraform_output_bucket == *"Error"* ]]; 
  then
    echo "No terraform_output_bucket specified.  Not copying tf-output.json"
  else
    echo "Copying tf-output.json: gcloud storage cp tf-output.json gs://${terraform_output_bucket}/terraform/output/"
    gcloud storage cp --account="${gcp_account_name}" --project="${deployed_project_id}" tf-output.json "gs://${terraform_output_bucket}/terraform/output/"
  fi

  # Copy TF State file - Check to see if the user did not specify an output bucket
  if [[ $terraform_output_bucket == *"Error"* ]]; 
  then
    echo "No terraform_output_bucket specified.  Not copying Terraform State file"
  else
    echo "Copying terraform.tfstate: gcloud storage cp terraform.tfstate gs://${terraform_output_bucket}/terraform/state/"
    gcloud storage cp --account="${gcp_account_name}" --project="${deployed_project_id}" terraform.tfstate "gs://${terraform_output_bucket}/terraform/state/"
  fi

  # # Copy the EMPTY org policies over the existing one
  # # Run Terraform apply again to then revert the org policies back to "inherit from parent"
  # if [ -f "../terraform-modules/org-policies/org-policies-original.txt" ]; then
  #   echo "The Org Policies file has already been replaced"
  # else
  #   echo "Replacing the Org Policies file and revoking the policy exceptions used during the deployment"
  #   mv ../terraform-modules/org-policies/org-policies.tf ../terraform-modules/org-policies/org-policies-original.txt
  #   cp ../terraform-modules/org-policies-destroy/org-policies.tf ../terraform-modules/org-policies/org-policies.tf

  #   echo "Start Terraform (Org Policies Revoke)"
  #   echo $(date)
  #   echo ""

  #   start=$(date)

  #   # Run the Terraform Apply (to destroy the org policies)
  #   terraform apply -auto-approve \
  #     -var="gcp_account_name=${gcp_account_name}" \
  #     -var="org_id=${org_id}" \
  #     -var="billing_account=${billing_account}" \
  #     -var="project_id=l400-agentic-ds"

  #   # Move the files back so Git does not check in the wrong file
  #   # Also, if we do another deployment we want to disable the policies so we do not interfere with the deployment
  #   # and then re-enable them.
  #   rm ../terraform-modules/org-policies/org-policies.tf
  #   mv ../terraform-modules/org-policies/org-policies-original.txt ../terraform-modules/org-policies/org-policies.tf

  #   echo "Terraform Times"
  #   stop=$(date)
  #   echo "Start time: ${start}"
  #   echo "Stop  time: ${stop}"
  #   echo ""

  # fi  
fi

cd ..

# 1. Always ensure all 4 bigquery-data-science agent skills are installed in .agents/skills/
#    (Tracked in git as baseline insurance, with automatic repair via uvx -> public PyPI uvx -> git clone fallback)
_bds_missing=0
for _bds_sk in bigquery-data-science bigquery-ai bigquery-ml bigquery-mlops; do
  if [ ! -f ".agents/skills/${_bds_sk}/SKILL.md" ]; then
    _bds_missing=1
    break
  fi
done
if [ "${_bds_missing}" -eq 1 ] || [ "${REFRESH_BDS_SKILLS:-0}" = "1" ]; then
  echo "Installing BigQuery Data Science agent skills (.agents/skills/{bigquery-data-science,bigquery-ai,bigquery-ml,bigquery-mlops})..."
  mkdir -p ".agents/skills"
  if command -v uvx >/dev/null 2>&1; then
    UV_HTTP_TIMEOUT=15 uvx --refresh "bigquery-data-science>=0.10.0" install --target agents >/dev/null 2>&1 \
      || UV_NO_CONFIG=1 UV_HTTP_TIMEOUT=15 uvx --default-index https://pypi.org/simple --refresh "bigquery-data-science>=0.10.0" install --target agents >/dev/null 2>&1 \
      || true
  fi
  _bds_missing=0
  for _bds_sk in bigquery-data-science bigquery-ai bigquery-ml bigquery-mlops; do
    if [ ! -f ".agents/skills/${_bds_sk}/SKILL.md" ]; then
      _bds_missing=1
      break
    fi
  done
  if [ "${_bds_missing}" -eq 1 ] && command -v git >/dev/null 2>&1; then
    _bds_tmp="$(mktemp -d)"
    if GIT_TERMINAL_PROMPT=0 git clone --depth 1 --quiet "${BDS_GIT_REPO_URL:-https://github.com/statmike/bigquery-data-science.git}" "${_bds_tmp}/bds" 2>/dev/null; then
      for _bds_sk in bigquery-data-science bigquery-ai bigquery-ml bigquery-mlops; do
        if [ -d "${_bds_tmp}/bds/skills/${_bds_sk}" ] && { [ ! -f ".agents/skills/${_bds_sk}/SKILL.md" ] || [ "${REFRESH_BDS_SKILLS:-0}" = "1" ]; }; then
          rm -rf ".agents/skills/${_bds_sk}"
          cp -R "${_bds_tmp}/bds/skills/${_bds_sk}" ".agents/skills/${_bds_sk}"
        fi
      done
    fi
    rm -rf "${_bds_tmp}"
  fi
fi
_bds_missing=0
for _bds_sk in bigquery-data-science bigquery-ai bigquery-ml bigquery-mlops; do
  if [ ! -f ".agents/skills/${_bds_sk}/SKILL.md" ]; then
    _bds_missing=1
    break
  fi
done
if [ "${_bds_missing}" -eq 0 ]; then
  echo "✔ BigQuery Data Science agent skills (.agents/skills/{bigquery-data-science,bigquery-ai,bigquery-ml,bigquery-mlops}) present."
else
  echo "⚠️  Some BigQuery Data Science skills could not be downloaded automatically; run 'git pull' or 'uvx bigquery-data-science install --target agents' when online."
fi

# 2. Check if Data Agent Kit is already installed on the Cloudtop (from workstation setup); only install if missing
_dak_found=0
for _p in \
  "${HOME}/.gemini/antigravity-cli/plugins"/data-agent-kit* \
  "${HOME}/.gemini/config/plugins"/data-agent-kit* \
  "${HOME}/.gemini/antigravity/plugins"/data-agent-kit* \
  "${HOME}/.gemini/extensions"/data-agent-kit* \
  "${HOME}/.gemini/antigravity/skills/bigquery-ai-ml" \
  "${HOME}/.gemini/config/skills/bigquery-ai-ml" \
  "${HOME}/.gemini/antigravity-cli/skills/bigquery-ai-ml" \
  ".agents/skills/bigquery-ai-ml"; do
  if [ -e "${_p}" ]; then
    _dak_found=1
    break
  fi
done
if [ "${_dak_found}" -eq 0 ] && command -v agy >/dev/null 2>&1; then
  if agy plugin list 2>/dev/null | grep -qi "data-agent-kit"; then
    _dak_found=1
  fi
fi

if [ "${_dak_found}" -eq 1 ]; then
  echo "✔ Data Agent Kit already installed on Cloudtop; skipping plugin install."
else
  echo "Data Agent Kit not detected on Cloudtop; installing GoogleCloudPlatform/data-agent-kit-plugin..."
  if command -v agy >/dev/null 2>&1; then
    agy plugin install https://github.com/GoogleCloudPlatform/data-agent-kit-plugin </dev/null >/dev/null 2>&1 || true
  fi
fi

# Ensure the 15 core Data Agent Kit skills are also visible in .agents/skills/ for VS Code inspection
if [ ! -d ".agents/skills/bigquery-ai-ml" ] || [ ! -d ".agents/skills/gcp-spark-troubleshooting" ]; then
  _local_dak_skills=""
  for _sd in \
    "${HOME}/.gemini/config/plugins/dak/skills" \
    "${HOME}/.gemini/config/plugins/data-agent-kit-plugin/skills" \
    "${HOME}/.gemini/antigravity-cli/plugins/data-agent-kit-plugin/skills" \
    "${HOME}/.gemini/antigravity/plugins/data-agent-kit-plugin/skills"; do
    if [ -d "${_sd}" ]; then
      _local_dak_skills="${_sd}"
      break
    fi
  done
  if [ -n "${_local_dak_skills}" ]; then
    for _sk in bigquery-ai-ml bigquery-sql data-autocleaning discovering-gcp-data-assets dataform-bigquery bigquery-bigframes ml-best-practices gcp-spark gcp-spark-troubleshooting bigquery-graph-query bigquery-graph-author gcp-dataflow gcp-pipeline-orchestration gcp-managed-airflow-dag-authoring bigtable-basics building-data-apps; do
      if [ -d "${_local_dak_skills}/${_sk}" ] && [ ! -d ".agents/skills/${_sk}" ]; then
        cp -R "${_local_dak_skills}/${_sk}" ".agents/skills/${_sk}"
      fi
    done
  elif command -v git >/dev/null 2>&1; then
    _dak_tmp="$(mktemp -d)"
    if git clone --depth 1 --quiet https://github.com/GoogleCloudPlatform/data-agent-kit-plugin.git "${_dak_tmp}/dak" 2>/dev/null; then
      for _sk in bigquery-ai-ml bigquery-sql data-autocleaning discovering-gcp-data-assets dataform-bigquery bigquery-bigframes ml-best-practices gcp-spark gcp-spark-troubleshooting bigquery-graph-query bigquery-graph-author gcp-dataflow gcp-pipeline-orchestration gcp-managed-airflow-dag-authoring bigtable-basics building-data-apps; do
        if [ -d "${_dak_tmp}/dak/skills/${_sk}" ] && [ ! -d ".agents/skills/${_sk}" ]; then
          cp -R "${_dak_tmp}/dak/skills/${_sk}" ".agents/skills/${_sk}"
        fi
      done
    fi
    rm -rf "${_dak_tmp}"
  fi
fi

echo ""
if [ $terraform_exit_code -ne 0 ] || grep -q "{random_string}" agent-config.json 2>/dev/null; then
  echo "================================================================================"
  echo "❌ ERROR: TERRAFORM DEPLOYMENT DID NOT COMPLETE (exit code: ${terraform_exit_code})"
  echo "================================================================================"
  echo "agent-config.json still contains template placeholders ({random_string} / {ldap})."
  echo "To converge Terraform state and complete deployment without starting over, run:"
  echo "  DEPLOY_AUTO_CONFIRM=1 source deploy.sh"
  echo ""
  echo "If a resource is stuck in a corrupt state, see How-to-Reset-this-Project.md."
  echo "================================================================================"
else
  echo "================================================================================"
  echo "✅ SUCCESS: Greenfield GCP Project Provisioned & agent-config.json Synced!"
  echo "   Project ID:      ${deployed_project_id}"
  echo "   Compute Region:  ${vertex_ai_region} (BigQuery datasets in US multi-region)"
  echo "   Workspace Root:  $(pwd -P)"
  echo "   👉 Next: Paste '${deployed_project_id}' into Checkpoint 01 in the Classroom Hub!"
  echo "================================================================================"
  if [ "${SKIP_AUTO_VERIFY_CP01:-0}" != "1" ] && [ -f "lab-evaluation-verifier/01-test_terraform_infrastructure.py" ]; then
    echo "Running Checkpoint 01 Verifier (01-test_terraform_infrastructure.py) automatically..."
    _cp01_log="$(mktemp)"
    python3 lab-evaluation-verifier/01-test_terraform_infrastructure.py 2>&1 | tee "${_cp01_log}" || true
    if grep -qi "closed for evaluations" "${_cp01_log}" 2>/dev/null; then
      echo ""
      echo "--------------------------------------------------------------------------------"
      echo "ℹ️  PRE-WORK COMPLETE — YOUR INFRASTRUCTURE IS 100% READY!"
      echo "   The Evaluator noted that your classroom cohort window has not opened yet."
      echo "   Nothing needs to be re-deployed! Once your instructor opens your session,"
      echo "   record Checkpoint 01 in ~5 seconds by running:"
      echo "     python3 lab-evaluation-verifier/01-test_terraform_infrastructure.py"
      echo "--------------------------------------------------------------------------------"
    fi
    rm -f "${_cp01_log}"
  fi
  echo "********************************************************************************"
  echo "Done — If using VS Code or agy, make sure $(pwd -P) is open as your workspace folder."
  echo "********************************************************************************"
fi