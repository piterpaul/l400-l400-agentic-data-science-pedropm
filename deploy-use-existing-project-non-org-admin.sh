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
# TO RUN: "source deploy-use-existing-project-non-org-admin"
####################################################################################

# Steps:
# 0 - Login (not necessary if using cloud shell)
# gcloud auth login
# gcloud auth application-default login

# 1 - Create a new project

# 2 - Grant your user Owner IAM access to the new project

# 3 - Run the below script and replace the following variables
gcp_account_name="your-name@your-domain.com"
project_id="my-project"
project_number="000000000000"
vertex_ai_region="${VERTEX_AI_REGION:-us-central1}"

# Ensure terraform / uvx are on PATH (checking ~/.local/bin and ~/.cargo/bin first, or downloading terraform if missing)
export PATH="${HOME}/.local/bin:${HOME}/.cargo/bin:${HOME}/bin:${PATH}"

# Seed local (gitignored) agent-config.json from agent-config.example.json if not yet created
if [ ! -f "agent-config.json" ] && [ -f "agent-config.example.json" ]; then
  cp "agent-config.example.json" "agent-config.json"
fi
if ! command -v terraform >/dev/null 2>&1; then
  echo "Terraform CLI not found on PATH; installing Terraform 1.9.8 into ~/.local/bin/terraform..."
  mkdir -p "${HOME}/.local/bin"
  _tf_arch="amd64"
  if [ "$(uname -m)" = "aarch64" ] || [ "$(uname -m)" = "arm64" ]; then
    _tf_arch="arm64"
  fi
  _tf_os="$(uname -s | tr '[:upper:]' '[:lower:]')"
  _tf_zip="$(mktemp)"
  if curl -fsSL "https://releases.hashicorp.com/terraform/1.9.8/terraform_1.9.8_${_tf_os}_${_tf_arch}.zip" -o "${_tf_zip}"; then
    python3 -c "import zipfile, sys, os; z=zipfile.ZipFile(sys.argv[1]); z.extract('terraform', sys.argv[2]); os.chmod(os.path.join(sys.argv[2], 'terraform'), 0o755)" "${_tf_zip}" "${HOME}/.local/bin"
  fi
  rm -f "${_tf_zip}"
fi


####################################################################################
# Deploy Terraform
####################################################################################
cd terraform 

# Initialize Terraform
terraform init

# Validate
terraform validate

# NOTE: The "Org Id = 0" is a signal to the terraform script that you are not an Org Admin
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

if [ -n "${_adc_tmp}" ] && [ -f "${_adc_tmp}" ]; then
  GOOGLE_APPLICATION_CREDENTIALS="${_adc_tmp}" terraform apply \
    -var="gcp_account_name=${gcp_account_name}" \
    -var="project_id=${project_id}" \
    -var="project_number=${project_number}" \
    -var="vertex_ai_region=${vertex_ai_region}" \
    -var="org_id=0"
  terraform_exit_code=$?
  rm -f "${_adc_tmp}"
else
  terraform apply \
    -var="gcp_account_name=${gcp_account_name}" \
    -var="project_id=${project_id}" \
    -var="project_number=${project_number}" \
    -var="vertex_ai_region=${vertex_ai_region}" \
    -var="org_id=0"
  terraform_exit_code=$?
fi
echo "Terraform exit code: ${terraform_exit_code}"

if [ $terraform_exit_code -eq 0 ]
then
  
  # Write out the output variables 
  terraform output -json > tf-output.json

  # Auto-sync ../agent-config.json from tf-output.json so Checkpoint 01 passes immediately
  VERTEX_AI_REGION_VAL="${vertex_ai_region}" python3 -c '
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
    t0_ds = tf_out.get("citibike_tier0_dataset", {}).get("value", "")
    wk_ds = tf_out.get("l400_ds_work_dataset", {}).get("value", "")
    code_bkt = tf_out.get("terraform-output-bucket", {}).get("value", "")
    vx_region = os.environ.get("VERTEX_AI_REGION_VAL", "us-central1").strip() or "us-central1"
    corp_email = acct
    try:
        out = subprocess.run(["gcloud", "auth", "list", "--format=json"], capture_output=True, text=True, timeout=5)
        if out.returncode == 0 and out.stdout.strip():
            accounts = json.loads(out.stdout)
            g_acc = next((a["account"] for a in accounts if a.get("account", "").endswith("@google.com")), None)
            if g_acc:
                corp_email = g_acc
    except Exception:
        pass
    if rnd:
        cfg["random_string"] = rnd
        cfg["gcs-data-bucket"] = f"l400-agentic-ds-data-{rnd}"
        cfg["gcs-code-bucket"] = code_bkt or f"l400-agentic-ds-code-{rnd}"
    if proj:
        cfg["gcp-project-id"] = proj
    if corp_email:
        cfg["user_email"] = corp_email
    if t0_ds:
        cfg["tier0-bigquery-dataset"] = t0_ds
    if wk_ds:
        cfg["bigquery-dataset"] = wk_ds
    cfg["bigquery-region"] = "US"
    cfg["spark-region"] = os.environ.get("SPARK_REGION", "") or vx_region
    cfg["vertex-ai-region"] = vx_region
    with open(cfg_path, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=4)
        f.write("\n")
    print(f"Updated agent-config.json with gcp-project-id={proj} (random_string={rnd}, spark-region={cfg[\"spark-region\"]}, vertex-ai-region={vx_region})")
    if proj:
        dak_cfg_path = os.path.expanduser("~/.config/data-agent-kit/config.json")
        os.makedirs(os.path.dirname(dak_cfg_path), exist_ok=True)
        dak_cfg = {}
        if os.path.exists(dak_cfg_path):
            try:
                dak_cfg = json.load(open(dak_cfg_path, encoding="utf-8"))
            except Exception:
                dak_cfg = {}
        dak_cfg["projectId"] = proj
        dak_cfg["region"] = vx_region
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
        print(f"Synced Data Agent Kit (~/.config/data-agent-kit/config.json) to projectId={proj}, region={vx_region}")
'

  # Get the name of the bucket the user specified to upload the output file
  terraform_output_bucket=$(terraform output -raw terraform-output-bucket)
  echo "terraform_output_bucket: ${terraform_output_bucket}"

  # Copy TF Output - Check to see if the user did not specify an output bucket
  if [[ $terraform_output_bucket == *"Error"* ]]; 
  then
    echo "No terraform_output_bucket specified.  Not copying tf-output.json"
  else
    echo "Copying tf-output.json: gcloud storage cp tf-output.json gs://${terraform_output_bucket}/terraform/output/"
    gcloud storage cp tf-output.json "gs://${terraform_output_bucket}/terraform/output/"
  fi

  # Copy TF State file - Check to see if the user did not specify an output bucket
  if [[ $terraform_output_bucket == *"Error"* ]]; 
  then
    echo "No terraform_output_bucket specified.  Not copying Terraform State file"
  else
    echo "Copying terraform.tfstate: gcloud storage cp terraform.tfstate gs://${terraform_output_bucket}/terraform/state/"
    gcloud storage cp terraform.tfstate "gs://${terraform_output_bucket}/terraform/state/"
  fi

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

echo "*********************************************************"
echo "Done"
echo "*********************************************************"
