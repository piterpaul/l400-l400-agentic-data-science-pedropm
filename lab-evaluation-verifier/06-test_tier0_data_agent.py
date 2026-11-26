#!/usr/bin/env python3
"""
Lab Evaluation: L400-agentic-data-science - tier0_data_agent
Verifies Part 1 stateful BigQuery Conversational Analytics data agent and Tier 1 trigger condition.
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
EVAL_NAME = "tier0_data_agent"
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

def load_agent_evidence() -> dict:
    """Loads artifacts/tier0_data_agent_evidence.json without truncating mid-JSON, then compacts large fields."""
    cand_path = "artifacts/tier0_data_agent_evidence.json" if os.path.exists("artifacts/tier0_data_agent_evidence.json") else ""
    if not cand_path:
        skip_dirs = {".git", ".terraform", ".venv", "venv", "node_modules", "__pycache__", "lab-evaluation-verifier"}
        for root, dirs, files in os.walk("."):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in skip_dirs]
            for f in sorted(files):
                if "data_agent" in f.lower() and f.endswith(".json"):
                    cand_path = os.path.join(root, f)
                    break
            if cand_path:
                break
    if not cand_path or not os.path.exists(cand_path):
        return {}
    try:
        with open(cand_path, "r", encoding="utf-8", errors="ignore") as f:
            data = json.load(f)
        if isinstance(data, dict):
            chat_resp = data.get("last_chat_response")
            if isinstance(chat_resp, list) and len(chat_resp) > 6:
                data["last_chat_response"] = chat_resp[:3] + chat_resp[-3:]
            elif chat_resp and len(json.dumps(chat_resp)) > 16000:
                data["last_chat_response"] = {"summary": str(chat_resp)[:8000]}
            return data
    except Exception:
        pass
    return safe_json_loads(read_file_head(cand_path, 24000), {})


def create_bundle(output_zip_path: str, student_account: str, student_ldap: str):
    project_id, tier0_ds, _, cfg = get_gcp_context()
    agent_evidence = load_agent_evidence()
    if (not isinstance(agent_evidence, dict) or not agent_evidence.get("agent_resource")) and project_id:
        try:
            acc_tok_res = subprocess.run(
                ["gcloud", "auth", "print-access-token"],
                capture_output=True, text=True, timeout=10, env=get_bq_env()
            )
            acc_tok = acc_tok_res.stdout.strip() if acc_tok_res.returncode == 0 else ""
            if acc_tok:
                cand_locs = []
                for loc_cand in [cfg.get("conversational-analytics-region"), "global", "us", cfg.get("vertex-ai-region")]:
                    if loc_cand and str(loc_cand).strip() and str(loc_cand).strip() not in cand_locs:
                        cand_locs.append(str(loc_cand).strip())
                for loc_cand in cand_locs:
                    url = f"https://geminidataanalytics.googleapis.com/v1beta/projects/{project_id}/locations/{loc_cand}/dataAgents"
                    req = urllib.request.Request(
                        url,
                        headers={"Authorization": f"Bearer {acc_tok}", "x-goog-user-project": project_id},
                        method="GET",
                    )
                    try:
                        with urllib.request.urlopen(req, timeout=15) as resp:
                            body = safe_json_loads(resp.read().decode("utf-8"), {})
                            agents_list = body.get("dataAgents", []) if isinstance(body, dict) else []
                            if agents_list:
                                if not isinstance(agent_evidence, dict):
                                    agent_evidence = {}
                                agent_evidence["agent_resource"] = agents_list[0]
                                agent_evidence["discovered_location"] = loc_cand
                                break
                    except Exception:
                        continue
        except Exception:
            pass
    trigger_parts = []
    for p in ["labs/guided/citibike/tier1_trigger.md", "labs/guided/citibike/DESIGN-tier0.md", "DESIGN.md", "labs/guided/citibike/README.md"]:
        txt = read_file_head(p, 10000)
        if txt:
            trigger_parts.append(f"=== {p} ===\n{txt}")
    trigger_doc = "\n\n".join(trigger_parts)
    skill_script = read_file_head(".agents/skills/conversational-analytics-agent/scripts/run.py", 12000)
    resolved_agent_id = (
        (agent_evidence.get("agent_id") if isinstance(agent_evidence, dict) else "")
        or cfg.get("tier0-data-agent-id")
        or "citibike_demand_agent"
    )

    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    signature = calculate_signature(student_ldap, LAB, EVAL_NAME, created_at, SALT)
    manifest_data = {
        "lab": LAB, "evaluation": EVAL_NAME, "created_at": created_at,
        "student_ldap": student_ldap, "workstation_account": student_account, "signature": signature
    }
    evidence = {
        "project_id": project_id,
        "dataset": tier0_ds,
        "agent_id": resolved_agent_id,
        "accepted_agent_id_aliases": ["citibike_demand_agent", "citibike_tier0_agent"],
        "agent_evidence": agent_evidence,
        "tier1_trigger_doc": trigger_doc,
        "skill_script_present": bool(skill_script),
    }
    with zipfile.ZipFile(output_zip_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("manifest.json", json.dumps(manifest_data, indent=2))
        z.writestr("tier0_data_agent_evidence.json", json.dumps(evidence, indent=2))
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
