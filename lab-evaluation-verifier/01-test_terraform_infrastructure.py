#!/usr/bin/env python3
"""
Lab Evaluation: L400-agentic-data-science - terraform_infrastructure
Verifies Step 0 Greenfield Argolis Terraform infrastructure, agent-config.json update, and live BigQuery datasets (citibike_tier0 and l400_ds_work).
Supports both Automatic submission (Cloud Run validator) and Manual submission (web upload).
"""

import os
import sys
import json
import uuid
import hashlib
import zipfile
import subprocess
import urllib.request
import urllib.error
import ssl
from datetime import datetime, timezone

LAB = "L400-agentic-data-science"
EVAL_NAME = "terraform_infrastructure"
ZIP_FILENAME = f"{EVAL_NAME}.zip"
DEFAULT_VALIDATOR_URL = os.environ.get(
    "VALIDATOR_URL",
    os.environ.get("URL", "https://lab-evaluation-verifier-verify-463617135523.us-central1.run.app")
)
SALT = os.environ.get("EVAL_SIGNATURE_SALT", "argolis-eval-verifier-salt-2026")


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
    """Reads project and dataset configurations from agent-config.json, agent-config.example.json, terraform/tf-output.json, or gcloud."""
    cfg = {}
    for candidate_cfg in ("agent-config.json", "agent-config.example.json"):
        if os.path.exists(candidate_cfg):
            try:
                with open(candidate_cfg, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                break
            except Exception:
                cfg = {}

    project_id = cfg.get("gcp-project-id", "")
    rnd_cfg = cfg.get("random_string", "")
    if (
        not project_id
        or "{" in project_id
        or "Set by the agent" in project_id
        or project_id == "null"
        or "Set by the agent" in str(rnd_cfg)
    ):
        if os.path.exists("terraform/tf-output.json"):
            try:
                with open("terraform/tf-output.json", "r", encoding="utf-8") as f:
                    tf_out = json.load(f)
                tf_proj = tf_out.get("project_id", {}).get("value", "")
                tf_rnd = tf_out.get("random_string", {}).get("value", "")
                tf_acct = tf_out.get("gcp_account_name", {}).get("value", "")
                tf_t0 = tf_out.get("citibike_tier0_dataset", {}).get("value", "")
                tf_wk = tf_out.get("l400_ds_work_dataset", {}).get("value", "")
                tf_code = tf_out.get("terraform-output-bucket", {}).get("value", "")
                if tf_proj:
                    project_id = tf_proj
                    cfg["gcp-project-id"] = tf_proj
                if tf_rnd:
                    cfg["random_string"] = tf_rnd
                    cfg["gcs-data-bucket"] = f"l400-agentic-ds-data-{tf_rnd}"
                    cfg["gcs-code-bucket"] = tf_code or f"l400-agentic-ds-code-{tf_rnd}"
                if tf_acct and ("{" in cfg.get("user_email", "") or not cfg.get("user_email") or "Set by" in cfg.get("user_email", "")):
                    corp_email = tf_acct
                    try:
                        out = subprocess.run(["gcloud", "auth", "list", "--format=json"], capture_output=True, text=True, timeout=5)
                        if out.returncode == 0 and out.stdout.strip():
                            accounts = json.loads(out.stdout)
                            g_acc = next((a["account"] for a in accounts if a.get("account", "").endswith("@google.com")), None)
                            if g_acc:
                                corp_email = g_acc
                    except Exception:
                        pass
                    cfg["user_email"] = corp_email
                if tf_t0:
                    cfg["tier0-bigquery-dataset"] = tf_t0
                if tf_wk:
                    cfg["bigquery-dataset"] = tf_wk
                cfg.setdefault("bigquery-region", "US")
                cfg.setdefault("vertex-ai-region", "us-central1")
                cfg.setdefault("spark-region", cfg.get("vertex-ai-region", "us-central1"))
                with open("agent-config.json", "w", encoding="utf-8") as wf:
                    json.dump(cfg, wf, indent=4)
                    wf.write("\n")
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


def run_bq_query(project_id: str, sql: str):
    """Runs a BigQuery SQL query and returns parsed JSON rows or error dict."""
    if not project_id:
        return {"error": "Missing project_id"}
    cmd = ["bq", "query", f"--project_id={project_id}", "--use_legacy_sql=false", "--format=prettyjson", sql]
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

def create_bundle(output_zip_path: str, student_account: str, student_ldap: str):
    project_id, tier0_ds, work_ds, cfg = get_gcp_context()
    bds_skills = ("bigquery-data-science", "bigquery-ai", "bigquery-ml", "bigquery-mlops")
    if any(not os.path.isfile(f".agents/skills/{sk}/SKILL.md") for sk in bds_skills):
        try:
            subprocess.run(
                ["uvx", "bigquery-data-science", "install", "--target", "agents"],
                capture_output=True, text=True, timeout=45
            )
        except Exception:
            pass
    if any(not os.path.isfile(f".agents/skills/{sk}/SKILL.md") for sk in bds_skills):
        try:
            import shutil
            import tempfile
            with tempfile.TemporaryDirectory() as tmp_d:
                clone_dir = os.path.join(tmp_d, "bds")
                env_git = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}
                r_git = subprocess.run(
                    ["git", "clone", "--depth", "1", "--quiet", "https://github.com/statmike/bigquery-data-science.git", clone_dir],
                    capture_output=True, text=True, timeout=45, env=env_git
                )
                if r_git.returncode == 0:
                    os.makedirs(".agents/skills", exist_ok=True)
                    for sk in bds_skills:
                        src_sk = os.path.join(clone_dir, "skills", sk)
                        dst_sk = os.path.join(".agents", "skills", sk)
                        if os.path.isdir(src_sk) and not os.path.isfile(os.path.join(dst_sk, "SKILL.md")):
                            if os.path.exists(dst_sk):
                                shutil.rmtree(dst_sk, ignore_errors=True)
                            shutil.copytree(src_sk, dst_sk)
        except Exception:
            pass
    bq_datasets = []
    if project_id:
        p = subprocess.run(
            ["bq", "ls", "--format=prettyjson", f"--project_id={project_id}"],
            capture_output=True, text=True, timeout=30, env=get_bq_env()
        )
        if p.returncode == 0 and p.stdout.strip():
            bq_datasets = safe_json_loads(p.stdout, [])
        else:
            bq_datasets = {"error": (p.stderr or p.stdout or "bq ls failed").strip()}
    else:
        bq_datasets = {"error": "Missing project_id in agent-config.json / tf-output.json / gcloud config"}

    tf_output = safe_json_loads(read_file_head("terraform/tf-output.json", 16000), {})

    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    signature = calculate_signature(student_ldap, LAB, EVAL_NAME, created_at, SALT)
    manifest_data = {
        "lab": LAB, "evaluation": EVAL_NAME, "created_at": created_at,
        "student_ldap": student_ldap, "workstation_account": student_account, "signature": signature
    }
    evidence = {
        "project_id": project_id,
        "tier0_dataset": tier0_ds,
        "work_dataset": work_ds,
        "agent_config": cfg,
        "tf_output": tf_output,
        "live_bq_datasets": bq_datasets,
    }
    with zipfile.ZipFile(output_zip_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("manifest.json", json.dumps(manifest_data, indent=2))
        z.writestr("live_bq_datasets.json", json.dumps(bq_datasets, indent=2))
        z.writestr("terraform_infrastructure_evidence.json", json.dumps(evidence, indent=2))
        for tf_path in ["terraform/main.tf", "terraform/variables.tf", "terraform-modules/resources/resources.tf", "agent-config.json"]:
            if os.path.isfile(tf_path) and os.path.getsize(tf_path) <= 262144:
                z.write(tf_path, tf_path)
    return created_at, signature


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    zip_path = os.path.join(script_dir, ZIP_FILENAME)

    print("=======================================================")
    print(f" Lab Evaluation: {LAB} - {EVAL_NAME}")
    print("=======================================================")

    student_account, student_ldap = get_student_identity()
    created_at, signature = create_bundle(zip_path, student_account, student_ldap)

    print(f"✔ Created evaluation package: {ZIP_FILENAME}")
    print(f"  Student Identity: {student_ldap} ({student_account})")
    print(f"  Timestamp:        {created_at}")
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
