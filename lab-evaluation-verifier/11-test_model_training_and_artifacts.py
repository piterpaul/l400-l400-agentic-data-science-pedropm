#!/usr/bin/env python3
"""
Lab Evaluation: L400-agentic-data-science - model_training_and_artifacts
Verifies trained BigQuery ML model or Tier 2 Python model artifacts in the student's BigQuery dataset.
Supports both Automatic submission (Cloud Run validator) and Manual submission (web upload).
"""

import os
import re
import sys
import json
import uuid
import hashlib
import zipfile
import subprocess
import urllib.request
import urllib.error
import ssl
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

LAB = "L400-agentic-data-science"
EVAL_NAME = "model_training_and_artifacts"
ZIP_FILENAME = f"{EVAL_NAME}.zip"
DEFAULT_VALIDATOR_URL = os.environ.get(
    "VALIDATOR_URL",
    os.environ.get("URL", "https://lab-evaluation-verifier-verify-463617135523.us-central1.run.app")
)
SALT = os.environ.get("EVAL_SIGNATURE_SALT", "argolis-eval-verifier-salt-2026")
PRIORITY_TABLE_KEYWORDS = (
    "eval", "compar", "spark", "vertex", "pred", "forecast",
    "score", "metric", "roas", "hazard", "rul", "model",
)
IN_PROGRESS_DATAPROC_STATES = frozenset({"PENDING", "RUNNING", "CANCELLING", "SETUP_DONE"})
IN_PROGRESS_VERTEX_STATES = frozenset({
    "JOB_STATE_QUEUED", "JOB_STATE_PENDING", "JOB_STATE_RUNNING",
    "JOB_STATE_CANCELLING", "JOB_STATE_PAUSED",
})
CLOUD_JOB_LIST_LIMIT = 15
MAX_DISCOVERY_PACK_HEAD_CHARS = 8000


def extract_ldap(account_str: str) -> str:
    """Extracts base corporate LDAP identity from Google email or Argolis account."""
    if not account_str:
        return ""
    acc = str(account_str).strip().lower()
    if "@" not in acc:
        return acc
    user, domain = acc.split("@", 1)
    if "altostrat.com" in domain:
        parts = domain.split(".")
        if parts[0] != "altostrat":
            return parts[0]
        return user
    return user


def is_service_account(acc: str) -> bool:
    """Checks if an account string represents a GCP service account rather than a human student."""
    if not acc:
        return False
    acc_lower = str(acc).strip().lower()
    return (
        "gserviceaccount.com" in acc_lower
        or "cloudtop" in acc_lower
        or acc_lower.startswith("service-")
    )


def get_student_identity() -> tuple[str, str]:
    """Discovers active gcloud account and extracts LDAP identity."""
    account = ""
    try:
        result = subprocess.run(
            ["gcloud", "config", "get-value", "account"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0 and result.stdout.strip() and result.stdout.strip() != "(unset)":
            candidate = result.stdout.strip()
            if not is_service_account(candidate):
                account = candidate
    except Exception:
        pass

    if not account:
        try:
            out = subprocess.run(["gcloud", "auth", "list", "--format=json"], capture_output=True, text=True, timeout=5)
            if out.returncode == 0 and out.stdout.strip():
                accounts = json.loads(out.stdout)
                google_acc = next((a["account"] for a in accounts if a.get("account", "").endswith("@google.com")), None)
                if google_acc:
                    account = google_acc
                else:
                    argolis_acc = next((a["account"] for a in accounts if "altostrat.com" in a.get("account", "") and not is_service_account(a.get("account", ""))), None)
                    if argolis_acc:
                        account = argolis_acc
        except Exception:
            pass

    if not account:
        os_user = os.environ.get("USER", "").strip()
        if os_user and not is_service_account(os_user):
            account = f"{os_user}@google.com"
        else:
            account = "unknown@example.com"

    student_ldap = extract_ldap(account)
    return account, student_ldap


def get_gcp_context():
    """Reads project and dataset configurations from agent-config.json, terraform/tf-output.json, or gcloud."""
    cfg = {}
    if os.path.exists("agent-config.json"):
        try:
            with open("agent-config.json", "r", encoding="utf-8") as f:
                cfg = json.load(f)
        except Exception:
            cfg = {}

    project_id = cfg.get("gcp-project-id", "")
    if not project_id or "{" in project_id or "Set by the agent" in project_id or project_id == "null":
        if os.path.exists("terraform/tf-output.json"):
            try:
                with open("terraform/tf-output.json", "r", encoding="utf-8") as f:
                    tf_out = json.load(f)
                    tf_proj = tf_out.get("project_id", {}).get("value", "")
                    if tf_proj:
                        project_id = tf_proj
            except Exception:
                pass
    if not project_id or "{" in project_id or project_id == "null":
        try:
            res = subprocess.run(["gcloud", "config", "get-value", "project"], capture_output=True, text=True, timeout=5)
            if res.returncode == 0 and res.stdout.strip() and res.stdout.strip() != "(unset)":
                project_id = res.stdout.strip()
        except Exception:
            project_id = ""

    tier0_dataset = cfg.get("tier0-bigquery-dataset") or "citibike_tier0"
    work_dataset = cfg.get("bigquery-dataset") or "l400_ds_work"
    return project_id, tier0_dataset, work_dataset, cfg


def safe_json_loads(text: str, default=None):
    """Safely decodes JSON text, returning default if empty or invalid."""
    if not text or not str(text).strip():
        return default if default is not None else {}
    try:
        return json.loads(text)
    except Exception:
        return default if default is not None else {"raw_output": str(text).strip()}


def get_bq_env():
    """Returns environment dict with CLOUDSDK_CORE_ACCOUNT set to the Argolis account if present."""
    env = os.environ.copy()
    try:
        out = subprocess.run(["gcloud", "auth", "list", "--format=json"], capture_output=True, text=True, timeout=5)
        if out.returncode == 0 and out.stdout.strip():
            accounts = json.loads(out.stdout)
            argolis_acc = next(
                (a["account"] for a in accounts if "altostrat.com" in a.get("account", "") and not is_service_account(a.get("account", ""))),
                None,
            )
            if argolis_acc:
                env["CLOUDSDK_CORE_ACCOUNT"] = argolis_acc
    except Exception:
        pass
    return env


def run_bq_query(project_id: str, sql: str, location: str = ""):
    """Runs a BigQuery SQL query and returns parsed JSON rows or error dict."""
    if not project_id:
        return {"error": "Missing project_id"}
    cmd = ["bq", "query", f"--project_id={project_id}"]
    if location:
        cmd.append(f"--location={location}")
    cmd.extend(["--use_legacy_sql=false", "--format=prettyjson", sql])
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=60, env=get_bq_env())
    if p.returncode == 0 and p.stdout.strip():
        return safe_json_loads(p.stdout, [])
    return {"error": (p.stderr or p.stdout or "Query failed").strip()}


def read_file_head(path: str, max_chars: int = 128000) -> str:
    if not os.path.exists(path):
        return ""
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read(max_chars)
    except Exception as e:
        return f"Error reading {path}: {e}"


def calculate_signature(student_ldap: str, lab: str, evaluation: str, created_at: str, salt: str) -> str:
    """Generates SHA-256 signature for bundle anti-tampering."""
    raw = f"{student_ldap.strip().lower()}:{lab.strip().lower()}:{evaluation.strip().lower()}:{created_at.strip().lower()}:{salt}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def get_identity_token() -> tuple[str, str]:
    """Retrieves Google identity token for authenticating directly against Cloud Run."""
    try:
        out = subprocess.run(["gcloud", "auth", "list", "--format=json"], capture_output=True, text=True, timeout=5)
        if out.returncode == 0:
            accounts = json.loads(out.stdout)
            google_acc = next((acc["account"] for acc in accounts if acc.get("account", "").endswith("@google.com")), None)
            if google_acc:
                res = subprocess.run(
                    ["gcloud", "auth", "print-identity-token", f"--account={google_acc}"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if res.returncode == 0 and res.stdout.strip():
                    return res.stdout.strip(), google_acc
    except Exception:
        pass

    try:
        res = subprocess.run(
            ["gcloud", "auth", "print-identity-token"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if res.returncode == 0 and res.stdout.strip():
            active_acc = ""
            try:
                acc_res = subprocess.run(["gcloud", "config", "get-value", "account"], capture_output=True, text=True, timeout=3)
                if acc_res.returncode == 0:
                    active_acc = acc_res.stdout.strip()
            except Exception:
                pass
            return res.stdout.strip(), active_acc
    except Exception:
        pass

    return "", ""


def submit_bundle(validator_url: str, zip_path: str, token: str = ""):
    """Submits the zip bundle to the Cloud Run validator endpoint."""
    boundary = f"----WebKitFormBoundary{uuid.uuid4().hex}"
    filename = os.path.basename(zip_path)

    with open(zip_path, "rb") as f:
        file_bytes = f.read()

    body_parts = [
        f"--{boundary}".encode("utf-8"),
        b'Content-Disposition: form-data; name="lab"',
        b"",
        LAB.encode("utf-8"),
        f"--{boundary}".encode("utf-8"),
        b'Content-Disposition: form-data; name="evaluation"',
        b"",
        EVAL_NAME.encode("utf-8"),
        f"--{boundary}".encode("utf-8"),
        f'Content-Disposition: form-data; name="files"; filename="{filename}"'.encode("utf-8"),
        b"Content-Type: application/zip",
        b"",
        file_bytes,
        f"--{boundary}--".encode("utf-8"),
        b""
    ]
    body = bytes([13, 10]).join(body_parts)

    headers = {
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "Content-Length": str(len(body)),
        "User-Agent": "lab-evaluation-client/1.0"
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
        headers["X-User-Token"] = token

    req = urllib.request.Request(
        validator_url,
        data=body,
        headers=headers,
        method="POST"
    )

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        with urllib.request.urlopen(req, context=ctx, timeout=180) as response:
            resp_body = response.read().decode("utf-8")
            status = response.status
            return status, resp_body
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8") if e.fp else str(e)
        return e.code, err_body
    except Exception as e:
        return 0, f"Failed to connect to validator at {validator_url}: {e}"


def print_manual_instructions(zip_filename: str):
    """Prints manual instructions for downloading and uploading the bundle."""
    print("=======================================================")
    print(" [Manual Submission Instructions]")
    print(f" 1. In VS Code file explorer: Right-click '{zip_filename}'")
    print(" 2. Select 'Download...' to save it to your local machine")
    print(" 3. Open the Lab Verifier Summary Portal in your browser")
    print(" 4. Click 'Manual Upload' at the top of the page")
    print(f" 5. Drag and drop '{zip_filename}' into the drop zone")
    print("=======================================================")

def prioritize_tables(tables_list: list[dict], max_count: int = 10) -> list[str]:
    """Prioritizes evaluation, runtime prediction, and forecast tables first."""
    names = [table.get("table_id", "") for table in tables_list if table.get("table_id")]
    high = [name for name in names if any(keyword in name.lower() for keyword in PRIORITY_TABLE_KEYWORDS)]
    rest = [name for name in names if name not in high]
    return (high + rest)[:max_count]


def resolve_effective_tier(config: dict) -> int:
    """Resolves target architectural tier (1 or 2) from config or discovery pack."""
    raw_tier = str(config.get("selected-tier", "")).strip().lower()
    if raw_tier in ("1", "tier 1", "tier1", "tier-1"):
        return 1
    if raw_tier in ("2", "tier 2", "tier2", "tier-2", "3", "tier 3", "tier3"):
        return 2
    pack_head = read_file_head("docs/discovery-pack.md", max_chars=MAX_DISCOVERY_PACK_HEAD_CHARS)
    if re.search(r"target_tier:\s*1\b", pack_head) or re.search(r"recommended_rung:\s*1\b", pack_head):
        return 1
    return 2


def extract_bqml_model_names(parsed_models: object) -> list[str]:
    """Extracts registered BigQuery ML model IDs from bq ls -m or __TABLES__ rows."""
    if not isinstance(parsed_models, list):
        return []
    model_names: list[str] = []
    for item in parsed_models:
        if not isinstance(item, dict):
            continue
        model_ref = item.get("modelReference")
        model_id = ""
        if isinstance(model_ref, dict):
            model_id = str(model_ref.get("modelId") or "").strip()
        if not model_id:
            model_id = str(item.get("table_id") or item.get("id") or "").strip()
        if model_id and model_id not in model_names:
            model_names.append(model_id)
    return model_names


def summarize_dataproc_batches(
    dataproc_batches: list[dict],
) -> tuple[list[dict], list[dict], list[str]]:
    """Separates Dataproc Serverless batches into succeeded, non-succeeded, and active."""
    succeeded: list[dict] = []
    non_succeeded: list[dict] = []
    in_progress: list[str] = []
    for item in dataproc_batches:
        if not isinstance(item, dict):
            continue
        raw_name = str(item.get("name") or "")
        batch_id = raw_name.split("/")[-1] if raw_name else "unknown-batch"
        region = str(item.get("_region") or "")
        state = str(item.get("state") or "UNKNOWN")
        state_message = str(item.get("stateMessage") or "").strip()
        summary = {
            "batch_id": batch_id,
            "region": region,
            "state": state,
            "create_time": str(item.get("createTime") or ""),
            "state_time": str(item.get("stateTime") or ""),
            "state_message": state_message,
        }
        if state == "SUCCEEDED":
            succeeded.append(summary)
        else:
            non_succeeded.append(summary)
            if state in IN_PROGRESS_DATAPROC_STATES:
                in_progress.append(
                    f"Managed Service for Apache Spark batch '{batch_id}' ({region}) is still {state} — wait for SUCCEEDED."
                )
    return succeeded, non_succeeded, in_progress


def summarize_vertex_custom_jobs(
    vertex_custom_jobs: list[dict],
) -> tuple[list[dict], list[dict], list[str]]:
    """Separates Agent Platform CustomJobs into succeeded, non-succeeded, and active."""
    succeeded: list[dict] = []
    non_succeeded: list[dict] = []
    in_progress: list[str] = []
    for item in vertex_custom_jobs:
        if not isinstance(item, dict):
            continue
        raw_name = str(item.get("name") or "")
        job_id = raw_name.split("/")[-1] if raw_name else "unknown-job"
        display_name = str(item.get("displayName") or job_id)
        region = str(item.get("_region") or "")
        state = str(item.get("state") or "UNKNOWN")
        raw_error = item.get("error")
        if isinstance(raw_error, dict):
            error_message = str(raw_error.get("message") or "").strip()
        else:
            error_message = str(raw_error or "").strip()
        summary = {
            "job_id": job_id,
            "display_name": display_name,
            "region": region,
            "state": state,
            "create_time": str(item.get("createTime") or ""),
            "end_time": str(item.get("endTime") or ""),
            "error_message": error_message,
        }
        if state == "JOB_STATE_SUCCEEDED":
            succeeded.append(summary)
        else:
            non_succeeded.append(summary)
            if state in IN_PROGRESS_VERTEX_STATES:
                in_progress.append(
                    f"Agent Platform CustomJob '{display_name}' ({job_id} in {region}) is still {state} — wait for JOB_STATE_SUCCEEDED."
                )
    return succeeded, non_succeeded, in_progress


def collect_custom_skill_scripts(max_files: int = 8) -> dict:
    """Reads head of student-created build skill scripts and workspace scripts to verify cloud runtime usage."""
    shipped_skills = {
        "bigquery-ai", "bigquery-ai-ml", "bigquery-bigframes", "bigquery-data-science",
        "bigquery-data-transfer-service", "bigquery-graph-author", "bigquery-graph-query",
        "bigquery-ml", "bigquery-mlops", "bigquery-sql",
        "bigtable-basics", "building-data-apps", "cloud-databases-onboarding",
        "conversational-analytics-agent", "data-autocleaning", "dataform-bigquery",
        "discovery-pack-fetch", "discovering-gcp-data-assets", "gcp-dataflow",
        "gcp-managed-airflow-dag-authoring", "gcp-pipeline-orchestration", "gcp-spark",
        "ml-best-practices", "model-Context-Protocol-MCP"
    }
    scripts_out = {}
    skills_root = ".agents/skills"
    if os.path.isdir(skills_root):
        for entry in sorted(os.listdir(skills_root)):
            if entry in shipped_skills:
                continue
            skill_dir = os.path.join(skills_root, entry)
            if not os.path.isdir(skill_dir):
                continue
            for root, _, files in os.walk(skill_dir):
                for fname in sorted(files):
                    if fname.endswith((".py", ".sql", ".sh", ".md")) and len(scripts_out) < max_files:
                        rel_path = os.path.join(root, fname)
                        scripts_out[rel_path] = read_file_head(rel_path, max_chars=64000)

    skip_dirs = {
        ".git", ".terraform", ".venv", "venv", "node_modules", "__pycache__",
        "lab-evaluation-verifier", "terraform", "terraform-modules", ".agents", ".claude"
    }
    shipped_files = {"labs/guided/citibike/tier0_baseline.sql", "data/loader.py"}
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in skip_dirs]
        for fname in sorted(files):
            if fname.endswith((".py", ".sql", ".sh")) and len(scripts_out) < max_files:
                rel_path = os.path.normpath(os.path.join(root, fname))
                if rel_path not in shipped_files and not rel_path.startswith("deploy"):
                    scripts_out[rel_path] = read_file_head(rel_path, max_chars=64000)
    return scripts_out


def get_dataset_location(project_id: str, dataset_id: str, cfg: dict, bq_env: dict) -> str:
    """Detects the actual BigQuery location of dataset_id (e.g. US, EU, us-central1) dynamically."""
    if project_id and dataset_id:
        try:
            res = subprocess.run(
                ["bq", "show", "--format=prettyjson", f"{project_id}:{dataset_id}"],
                capture_output=True, text=True, timeout=15, env=bq_env
            )
            if res.returncode == 0 and res.stdout.strip():
                meta = safe_json_loads(res.stdout, {})
                if isinstance(meta, dict) and meta.get("location"):
                    return str(meta["location"]).strip()
        except Exception:
            pass
    return str(cfg.get("bigquery-region") or "US").strip()


def discover_candidate_compute_regions(cfg: dict, scripts_map: dict) -> list[str]:
    """Discovers all candidate GCP compute regions across config, env vars, DAK config, scripts, and US fallbacks."""
    candidates = []

    def add_region(r: str):
        if not r:
            return
        val = str(r).strip().lower()
        if re.match(r"^(?:us|europe|asia|northamerica|southamerica|australia|me)-[a-z]+[0-9]+$", val):
            if val not in candidates:
                candidates.append(val)

    add_region(cfg.get("spark-region", ""))
    add_region(cfg.get("vertex-ai-region", ""))
    add_region(os.environ.get("SPARK_REGION", ""))
    add_region(os.environ.get("VERTEX_AI_REGION", ""))
    add_region(os.environ.get("GOOGLE_CLOUD_REGION", ""))
    add_region(os.environ.get("CLOUDSDK_COMPUTE_REGION", ""))
    add_region(os.environ.get("CLOUDSDK_DATAPROC_REGION", ""))

    dak_cfg_path = os.path.expanduser("~/.config/data-agent-kit/config.json")
    if os.path.isfile(dak_cfg_path):
        try:
            with open(dak_cfg_path, "r", encoding="utf-8") as f:
                dak_cfg = json.load(f)
                add_region(dak_cfg.get("region", ""))
        except Exception:
            pass

    design_text = read_file_head("DESIGN.md", 128000)
    combined_text = "\n".join([design_text] + list(scripts_map.values()))
    for match in re.findall(r"\b(?:us|europe|asia|northamerica|southamerica|australia|me)-[a-z]+[0-9]+\b", combined_text.lower()):
        add_region(match)

    for fallback_reg in ("us-central1", "us-east1", "us-east4", "us-west1"):
        add_region(fallback_reg)

    return candidates[:8]


def analyze_script_runtime_patterns(scripts_map: dict) -> dict:
    """Inspects student build scripts for cloud runtime usage vs banned local VM training."""
    cloud_indicators = []
    local_antipatterns = []
    combined = "\n".join(scripts_map.values())
    if re.search(r"CREATE\s+(?:OR\s+REPLACE\s+)?(?:TEMP\s+)?MODEL", combined, re.I):
        cloud_indicators.append("BigQuery ML (CREATE MODEL: ARIMA_PLUS / ARIMA_PLUS_XREG / BOOSTED_TREE / RANDOM_FOREST)")
    if re.search(r"AI\.(?:FORECAST|PREDICT|EVALUATE|DETECT_ANOMALIES|GENERATE_EMBEDDING)", combined, re.I):
        cloud_indicators.append("BigQuery AI Foundation TVF (AI.FORECAST TimesFM 2.5/3.0 / AI.PREDICT TabFM)")
    if re.search(r"bigframes\.ml|bigframes\.pandas|bpd\.read_gbq|\.to_gbq\(", combined, re.I):
        cloud_indicators.append("BigFrames Cloud Python (bigframes.ml / bigframes.pandas)")
    if re.search(r"dataproc\s+batches\s+submit|DataprocSparkSession|ManagedSparkSession|google\.cloud\.dataproc|applyInPandas|SparkXGBRegressor|pyspark\.ml", combined, re.I):
        cloud_indicators.append("Google Cloud Managed Service for Apache Spark (Serverless Spark / PySpark applyInPandas / SparkML)")
    if re.search(r"aiplatform\.Custom|vertexai|gcloud\s+ai\s+custom-jobs", combined, re.I):
        cloud_indicators.append("Vertex AI Custom Training Job (statsmodels Theta/Holt-Winters / statsforecast / XGBoost)")
    if re.search(r"ThetaModel|AutoTheta|ExponentialSmoothing|AutoETS|HoltWinters", combined, re.I):
        cloud_indicators.append("Python Statistical Forecasting (Theta / Holt-Winters via statsmodels / statsforecast)")

    if re.search(r"\.master\(\s*['\"]local", combined, re.I):
        local_antipatterns.append("SparkSession.builder.master('local') detected (must use Dataproc Serverless)")
    has_local_sklearn_fit = bool(
        re.search(r"\b(?:sklearn|lightgbm|xgboost|catboost)\b", combined, re.I)
        and re.search(r"\.to_pandas\(\)", combined, re.I)
        and not cloud_indicators
    )
    if has_local_sklearn_fit:
        local_antipatterns.append("Local .to_pandas() + local model fitting without a cloud runtime")

    return {
        "cloud_indicators_in_scripts": cloud_indicators,
        "local_compute_antipatterns": local_antipatterns,
    }


def create_bundle(output_zip_path: str, student_account: str, student_ldap: str) -> tuple[str, str, dict]:
    """Collects BigQuery, Spark, and Agent Platform job evidence into output_zip_path."""
    project_id, _, work_dataset, config = get_gcp_context()
    bq_env = get_bq_env()
    bq_location = get_dataset_location(project_id, work_dataset, config, bq_env)
    scripts_map = collect_custom_skill_scripts()
    candidate_regions = discover_candidate_compute_regions(config, scripts_map)
    compute_region = candidate_regions[0] if candidate_regions else "us-central1"
    effective_tier = resolve_effective_tier(config)

    models_list = subprocess.run(
        ["bq", f"--project_id={project_id}", "ls", "-m", "--format=prettyjson", f"{project_id}:{work_dataset}"],
        capture_output=True, text=True, timeout=30, env=bq_env
    )
    routines_and_tables = run_bq_query(
        project_id,
        f"SELECT table_id, type AS table_type, row_count FROM `{project_id}.{work_dataset}.__TABLES__`",
        location=bq_location,
    )
    parsed_models = safe_json_loads(models_list.stdout, [])
    if not parsed_models and isinstance(routines_and_tables, list):
        parsed_models = [
            table for table in routines_and_tables
            if str(table.get("table_type")) in ("4", "MODEL")
        ]
    bqml_model_names = extract_bqml_model_names(parsed_models)

    def query_bq_training_jobs(view_name: str, location_name: str):
        return run_bq_query(
            project_id,
            f"""
            SELECT
              job_id,
              creation_time,
              statement_type,
              SUBSTR(query, 1, 240) AS query_snippet
            FROM `region-{location_name.lower()}.INFORMATION_SCHEMA.{view_name}`
            WHERE creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
              AND (
                statement_type = 'CREATE_MODEL'
                OR REGEXP_CONTAINS(UPPER(query), r'CREATE\\s+(OR\\s+REPLACE\\s+)?(TEMP\\s+)?MODEL|ML\\.(EVALUATE|PREDICT|FORECAST|EXPLAIN_PREDICT|EXPLAIN_FORECAST|RECOMMEND|WEIGHTS)|AI\\.(FORECAST|PREDICT|EVALUATE|DETECT_ANOMALIES|GENERATE_EMBEDDING)|BIGFRAMES')
                OR REGEXP_CONTAINS(LOWER(TO_JSON_STRING(labels)), r'bigframes|dataproc|spark|vertex|bqml')
              )
            ORDER BY creation_time DESC
            LIMIT 15
            """,
            location=location_name,
        )

    bq_cloud_training_jobs = query_bq_training_jobs("JOBS_BY_PROJECT", bq_location)
    if (isinstance(bq_cloud_training_jobs, dict) and "error" in bq_cloud_training_jobs) or not bq_cloud_training_jobs:
        fallback_jobs = query_bq_training_jobs("JOBS_BY_USER", bq_location)
        if isinstance(fallback_jobs, list) and fallback_jobs:
            bq_cloud_training_jobs = fallback_jobs
        elif isinstance(bq_cloud_training_jobs, dict) and "error" in bq_cloud_training_jobs:
            bq_cloud_training_jobs = []

    eval_table = run_bq_query(
        project_id,
        f"SELECT * FROM `{project_id}.{work_dataset}.eval_comparison` LIMIT 20",
        location=bq_location,
    )
    sample_table_rows = {}
    if isinstance(routines_and_tables, list):
        for table_name in prioritize_tables(routines_and_tables, max_count=10):
            if table_name and table_name != "eval_comparison":
                rows = run_bq_query(
                    project_id,
                    f"SELECT * FROM `{project_id}.{work_dataset}.{table_name}` LIMIT 10",
                    location=bq_location,
                )
                sample_table_rows[table_name] = rows
                if isinstance(eval_table, dict) and "error" in eval_table and ("eval" in table_name.lower() or "compar" in table_name.lower()):
                    eval_table = rows

    dataproc_batches: list[dict] = []
    dataproc_sessions: list[dict] = []
    vertex_custom_jobs: list[dict] = []
    limit_flag = f"--limit={CLOUD_JOB_LIST_LIMIT}"
    if project_id and candidate_regions:
        def poll_region(region_name: str) -> tuple[list[dict], list[dict], list[dict]]:
            batch_items: list[dict] = []
            session_items: list[dict] = []
            vertex_items: list[dict] = []
            try:
                batches_proc = subprocess.run(
                    ["gcloud", "dataproc", "batches", "list", f"--project={project_id}", f"--region={region_name}", "--format=json", limit_flag],
                    capture_output=True, text=True, timeout=15, env=bq_env
                )
                if batches_proc.returncode == 0 and batches_proc.stdout.strip():
                    parsed_batches = safe_json_loads(batches_proc.stdout, [])
                    if isinstance(parsed_batches, list):
                        for item in parsed_batches:
                            if isinstance(item, dict):
                                item["_region"] = region_name
                                batch_items.append(item)
            except Exception:
                pass
            try:
                sessions_proc = subprocess.run(
                    ["gcloud", "dataproc", "sessions", "list", f"--project={project_id}", f"--region={region_name}", "--format=json", limit_flag],
                    capture_output=True, text=True, timeout=15, env=bq_env
                )
                if sessions_proc.returncode == 0 and sessions_proc.stdout.strip():
                    parsed_sessions = safe_json_loads(sessions_proc.stdout, [])
                    if isinstance(parsed_sessions, list):
                        for item in parsed_sessions:
                            if isinstance(item, dict):
                                item["_region"] = region_name
                                session_items.append(item)
            except Exception:
                pass
            try:
                vertex_proc = subprocess.run(
                    ["gcloud", "ai", "custom-jobs", "list", f"--project={project_id}", f"--region={region_name}", "--format=json", limit_flag],
                    capture_output=True, text=True, timeout=15, env=bq_env
                )
                if vertex_proc.returncode == 0 and vertex_proc.stdout.strip():
                    parsed_vertex = safe_json_loads(vertex_proc.stdout, [])
                    if isinstance(parsed_vertex, list):
                        for item in parsed_vertex:
                            if isinstance(item, dict):
                                item["_region"] = region_name
                                vertex_items.append(item)
            except Exception:
                pass
            return batch_items, session_items, vertex_items

        with ThreadPoolExecutor(max_workers=min(8, len(candidate_regions))) as pool:
            for batch_result, session_result, vertex_result in pool.map(poll_region, candidate_regions):
                dataproc_batches.extend(batch_result)
                dataproc_sessions.extend(session_result)
                vertex_custom_jobs.extend(vertex_result)

    (
        succeeded_dataproc_batches,
        failed_or_incomplete_dataproc_batches,
        in_progress_dataproc,
    ) = summarize_dataproc_batches(dataproc_batches)
    (
        succeeded_vertex_custom_jobs,
        failed_or_incomplete_vertex_custom_jobs,
        in_progress_vertex,
    ) = summarize_vertex_custom_jobs(vertex_custom_jobs)
    succeeded_dataproc_sessions = [
        item for item in dataproc_sessions
        if isinstance(item, dict) and str(item.get("state") or "") in ("ACTIVE", "TERMINATED", "SUCCEEDED")
    ]

    dataproc_batch_succeeded = len(succeeded_dataproc_batches) > 0
    vertex_custom_job_succeeded = len(succeeded_vertex_custom_jobs) > 0
    in_progress_cloud_jobs = in_progress_dataproc + in_progress_vertex

    unrecovered_failed_jobs: list[str] = []
    if failed_or_incomplete_dataproc_batches and not dataproc_batch_succeeded:
        for batch in failed_or_incomplete_dataproc_batches:
            detail = batch["state_message"] or "inspect logs in Managed Service for Apache Spark -> Serverless -> Batches"
            unrecovered_failed_jobs.append(
                f"Managed Service for Apache Spark batch '{batch['batch_id']}' ({batch['region']}) is {batch['state']}: {detail}"
            )
    if failed_or_incomplete_vertex_custom_jobs and not vertex_custom_job_succeeded:
        for job in failed_or_incomplete_vertex_custom_jobs:
            detail = job["error_message"] or "inspect logs in Agent Platform -> Models -> More services -> Training -> Custom jobs"
            unrecovered_failed_jobs.append(
                f"Agent Platform CustomJob '{job['display_name']}' ({job['job_id']} in {job['region']}) is {job['state']}: {detail}"
            )

    missing_tier2_runtimes: list[str] = []
    if effective_tier >= 2:
        if not dataproc_batch_succeeded:
            missing_tier2_runtimes.append(
                "Missing a SUCCEEDED Managed Service for Apache Spark Serverless batch (Menu -> Managed Service for Apache Spark -> Serverless -> Batches)."
            )
        if not vertex_custom_job_succeeded:
            missing_tier2_runtimes.append(
                "Missing a JOB_STATE_SUCCEEDED Agent Platform CustomJob (Menu -> Agent Platform -> Models -> More services -> Training -> Custom jobs)."
            )

    script_analysis = analyze_script_runtime_patterns(scripts_map)
    detected_cloud_runtimes: list[str] = []
    if bqml_model_names:
        detected_cloud_runtimes.append(
            f"BigQuery Registered Models ({len(bqml_model_names)} in {work_dataset} [{bq_location}]: {bqml_model_names})"
        )
    if isinstance(bq_cloud_training_jobs, list) and len(bq_cloud_training_jobs) > 0:
        detected_cloud_runtimes.append(
            f"BigQuery Cloud Training/TVF Jobs ({len(bq_cloud_training_jobs)} in region-{bq_location.lower()})"
        )
    if succeeded_dataproc_batches:
        spark_regions = sorted({batch["region"] for batch in succeeded_dataproc_batches})
        detected_cloud_runtimes.append(
            f"Managed Service for Apache Spark Serverless Batches (SUCCEEDED: {len(succeeded_dataproc_batches)} across {spark_regions})"
        )
    if succeeded_dataproc_sessions:
        session_regions = sorted({str(item.get("_region") or "") for item in succeeded_dataproc_sessions})
        detected_cloud_runtimes.append(
            f"Managed Service for Apache Spark Interactive Sessions ({len(succeeded_dataproc_sessions)} across {session_regions})"
        )
    if succeeded_vertex_custom_jobs:
        vertex_regions = sorted({job["region"] for job in succeeded_vertex_custom_jobs})
        detected_cloud_runtimes.append(
            f"Agent Platform (Vertex AI) Custom Jobs (JOB_STATE_SUCCEEDED: {len(succeeded_vertex_custom_jobs)} across {vertex_regions})"
        )

    if effective_tier >= 2:
        cloud_execution_verified = bool(
            dataproc_batch_succeeded
            and vertex_custom_job_succeeded
            and not in_progress_cloud_jobs
            and not unrecovered_failed_jobs
            and not script_analysis["local_compute_antipatterns"]
        )
    else:
        has_tier1_cloud_execution = bool(
            bqml_model_names
            or (isinstance(bq_cloud_training_jobs, list) and len(bq_cloud_training_jobs) > 0)
            or dataproc_batch_succeeded
            or len(succeeded_dataproc_sessions) > 0
            or vertex_custom_job_succeeded
        )
        cloud_execution_verified = bool(
            has_tier1_cloud_execution
            and not in_progress_cloud_jobs
            and not unrecovered_failed_jobs
            and not script_analysis["local_compute_antipatterns"]
        )

    eval_metrics_json = safe_json_loads(read_file_head("artifacts/eval_metrics.json", max_chars=16000), {})

    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    signature = calculate_signature(student_ldap, LAB, EVAL_NAME, created_at, SALT)
    manifest_data = {
        "lab": LAB, "evaluation": EVAL_NAME, "created_at": created_at,
        "student_ldap": student_ldap, "workstation_account": student_account, "signature": signature
    }
    cloud_verification_summary = {
        "effective_tier": effective_tier,
        "cloud_execution_verified": cloud_execution_verified,
        "bqml_model_names": bqml_model_names,
        "dataproc_batch_succeeded": dataproc_batch_succeeded,
        "succeeded_dataproc_batches": succeeded_dataproc_batches,
        "failed_or_incomplete_dataproc_batches": failed_or_incomplete_dataproc_batches,
        "vertex_custom_job_succeeded": vertex_custom_job_succeeded,
        "succeeded_vertex_custom_jobs": succeeded_vertex_custom_jobs,
        "failed_or_incomplete_vertex_custom_jobs": failed_or_incomplete_vertex_custom_jobs,
        "in_progress_cloud_jobs": in_progress_cloud_jobs,
        "unrecovered_failed_jobs": unrecovered_failed_jobs,
        "missing_tier2_runtimes": missing_tier2_runtimes,
        "detected_cloud_runtimes": detected_cloud_runtimes,
        "script_cloud_indicators": script_analysis["cloud_indicators_in_scripts"],
        "local_compute_antipatterns": script_analysis["local_compute_antipatterns"],
    }
    evidence = {
        "project_id": project_id,
        "dataset": work_dataset,
        "bigquery_dataset_location": bq_location,
        "primary_compute_region": compute_region,
        "checked_compute_regions": candidate_regions,
        "selected_problem": config.get("selected-problem-id", ""),
        "selected_tier": config.get("selected-tier", f"Tier {effective_tier}"),
        "cloud_runtime_verification": cloud_verification_summary,
        "bqml_models": parsed_models,
        "bq_cloud_training_jobs": bq_cloud_training_jobs,
        "dataproc_batches": dataproc_batches,
        "dataproc_sessions": dataproc_sessions,
        "vertex_custom_jobs": vertex_custom_jobs,
        "build_skill_scripts": scripts_map,
        "eval_metrics_json": eval_metrics_json,
        "tables_summary": routines_and_tables,
        "eval_comparison_rows": eval_table,
        "sample_table_rows": sample_table_rows,
    }
    with zipfile.ZipFile(output_zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("manifest.json", json.dumps(manifest_data, indent=2))
        archive.writestr("model_training_evidence.json", json.dumps(evidence, indent=2))
    return created_at, signature, cloud_verification_summary


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    zip_path = os.path.join(script_dir, ZIP_FILENAME)

    print("=======================================================")
    print(f" Lab Evaluation: {LAB} - {EVAL_NAME}")
    print("=======================================================")

    student_account, student_ldap = get_student_identity()
    created_at, signature, cloud_summary = create_bundle(zip_path, student_account, student_ldap)

    print(f"✔ Created evaluation package: {ZIP_FILENAME}")
    print(f"  Student Identity: {student_ldap} ({student_account})")
    print(f"  Timestamp:        {created_at}")
    print(f"  Target Tier:      Tier {cloud_summary['effective_tier']}")
    print(f"  BQML Models:      {cloud_summary['bqml_model_names'] or 'none detected'}")
    print(f"  Managed Spark:    {len(cloud_summary['succeeded_dataproc_batches'])} SUCCEEDED batch(es)")
    print(f"  Agent Platform:   {len(cloud_summary['succeeded_vertex_custom_jobs'])} JOB_STATE_SUCCEEDED CustomJob(s)")
    for active_warning in cloud_summary["in_progress_cloud_jobs"]:
        print(f"  ⚠ IN PROGRESS:    {active_warning}")
    for failed_warning in cloud_summary["unrecovered_failed_jobs"]:
        print(f"  ✖ FAILED JOB:     {failed_warning}")
    for missing_warning in cloud_summary["missing_tier2_runtimes"]:
        print(f"  ✖ MISSING:        {missing_warning}")
    print("")

    force_manual = "--manual" in sys.argv or os.environ.get("MANUAL") == "1"
    is_localhost = "localhost" in DEFAULT_VALIDATOR_URL or "127.0.0.1" in DEFAULT_VALIDATOR_URL
    token, auth_account = ("", "") if (is_localhost or force_manual) else get_identity_token()

    can_submit = not force_manual and (is_localhost or bool(token))

    if can_submit:
        if token:
            acc_label = f" ({auth_account})" if auth_account else ""
            print(f"✔ Authenticated with Google Cloud identity token{acc_label}.")
        print(f"Submitting {ZIP_FILENAME} to validator ({DEFAULT_VALIDATOR_URL})...")
        print("")
        status, response_text = submit_bundle(DEFAULT_VALIDATOR_URL, zip_path, token)
        try:
            parsed = json.loads(response_text)
            print(json.dumps(parsed, indent=2))
        except Exception:
            print(response_text)

        if status not in (200, 201):
            print("")
            print("Automatic submission did not succeed. You can submit manually:")
            print_manual_instructions(ZIP_FILENAME)
    else:
        if force_manual:
            print("Manual submission mode requested (--manual/MANUAL=1).")
        else:
            print("ℹ Google Cloud identity token could not be acquired (ensure 'gcloud auth login' has been run).")
            print("Proceeding with manual web submission.")
            print("")
        print_manual_instructions(ZIP_FILENAME)

    print("\nDone!")


if __name__ == "__main__":
    main()
