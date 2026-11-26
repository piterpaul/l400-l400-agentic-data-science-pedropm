#!/usr/bin/env python3
"""
Lab Evaluation: L400-agentic-data-science - baseline_comparison_and_decision
Verifies Tier 1/2 evaluation vs Tier 0 baseline, human critique of agent assumptions (docs/agent_critique.md), and clean-room resource hygiene.
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
EVAL_NAME = "baseline_comparison_and_decision"
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

def prioritize_tables(tables_list: list[dict], max_count: int = 8) -> list[str]:
    """Prioritizes evaluation, comparison, prediction, forecast, and score tables first."""
    priority_keywords = ("eval", "compar", "pred", "forecast", "score", "metric", "roas", "hazard", "rul", "model")
    names = [t.get("table_id", "") for t in tables_list if t.get("table_id")]
    high = [n for n in names if any(k in n.lower() for k in priority_keywords)]
    rest = [n for n in names if n not in high]
    return (high + rest)[:max_count]


def create_bundle(output_zip_path: str, student_account: str, student_ldap: str):
    project_id, _, work_ds, cfg = get_gcp_context()
    eval_rows = run_bq_query(
        project_id,
        f"SELECT * FROM `{project_id}.{work_ds}.eval_comparison` LIMIT 25"
    )
    tables_list = run_bq_query(
        project_id,
        f"SELECT table_id, row_count FROM `{project_id}.{work_ds}.__TABLES__`"
    )
    other_eval_tables = {}
    if isinstance(tables_list, list):
        for tid in prioritize_tables(tables_list, max_count=8):
            if tid and tid != "eval_comparison":
                rows = run_bq_query(
                    project_id,
                    f"SELECT * FROM `{project_id}.{work_ds}.{tid}` LIMIT 15"
                )
                other_eval_tables[tid] = rows
                if isinstance(eval_rows, dict) and "error" in eval_rows and ("eval" in tid.lower() or "compar" in tid.lower()):
                    eval_rows = rows
    evaluation_md = read_file_head("EVALUATION.md", 128000) or read_file_head("docs/EVALUATION.md", 128000)
    critique_only = read_file_head("docs/agent_critique.md", 128000) or read_file_head("agent_critique.md", 128000)
    if not critique_only:
        skip_dirs = {".git", ".terraform", ".venv", "venv", "node_modules", "__pycache__", "lab-evaluation-verifier"}
        for root, dirs, files in os.walk("."):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in skip_dirs]
            for f in sorted(files):
                if "critique" in f.lower() and f.endswith(".md"):
                    cand = os.path.join(root, f)
                    if os.path.getsize(cand) <= 262144:
                        critique_only = read_file_head(cand, 128000)
                        break
            if critique_only:
                break
    design_md = read_file_head("DESIGN.md", 128000)
    critique_md = "\n\n".join(x for x in [evaluation_md, critique_only] if x)
    bq_loc = str(cfg.get("bigquery-region") or "US").strip()
    if project_id and work_ds:
        try:
            ds_show = subprocess.run(
                ["bq", "show", "--format=prettyjson", f"{project_id}:{work_ds}"],
                capture_output=True, text=True, timeout=15, env=get_bq_env()
            )
            if ds_show.returncode == 0 and ds_show.stdout.strip():
                ds_meta = safe_json_loads(ds_show.stdout, {})
                if isinstance(ds_meta, dict) and ds_meta.get("location"):
                    bq_loc = str(ds_meta["location"]).strip()
        except Exception:
            pass
    reservations_check = subprocess.run(
        ["bq", "ls", "--reservation", f"--project_id={project_id}", f"--location={bq_loc}", "--format=prettyjson"],
        capture_output=True, text=True, timeout=20, env=get_bq_env()
    )

    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    signature = calculate_signature(student_ldap, LAB, EVAL_NAME, created_at, SALT)
    manifest_data = {
        "lab": LAB, "evaluation": EVAL_NAME, "created_at": created_at,
        "student_ldap": student_ldap, "workstation_account": student_account, "signature": signature
    }
    evidence = {
        "project_id": project_id,
        "dataset": work_ds,
        "selected_problem": cfg.get("selected-problem-id", ""),
        "selected_tier": cfg.get("selected-tier", ""),
        "eval_comparison": eval_rows,
        "other_eval_tables": other_eval_tables,
        "evaluation_md": evaluation_md,
        "agent_critique_md": critique_md,
        "design_md": design_md,
        "active_reservations": safe_json_loads(reservations_check.stdout, []),
    }
    with zipfile.ZipFile(output_zip_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("manifest.json", json.dumps(manifest_data, indent=2))
        z.writestr("baseline_and_critique_evidence.json", json.dumps(evidence, indent=2))
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
