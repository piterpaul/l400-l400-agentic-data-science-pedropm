#!/usr/bin/env python3
"""
Run all 12 lab evaluations in sequential order, or fast-resubmit existing local .zip bundles.

Usage:
  python3 lab-evaluation-verifier/run-all-evals.py
  python3 lab-evaluation-verifier/run-all-evals.py --resubmit-existing
  python3 lab-evaluation-verifier/run-all-evals.py --only 01,06,12
  python3 lab-evaluation-verifier/run-all-evals.py --manual
"""

import glob
import json
import os
import re
import ssl
import subprocess
import sys
import urllib.error
import urllib.request
import uuid

LAB = "L400-agentic-data-science"
DEFAULT_VALIDATOR_URL = os.environ.get(
    "VALIDATOR_URL",
    os.environ.get("URL", "https://lab-evaluation-verifier-verify-463617135523.us-central1.run.app"),
)


def extract_eval_status(output: str, returncode: int) -> str:
    """Extracts PASS/FAIL from validator JSON output, or fallback status."""
    matches = re.findall(r'"pass-fail"\s*:\s*"([^"]+)"', output, flags=re.IGNORECASE)
    if matches:
        return matches[-1].upper()

    if returncode != 0:
        return f"ERROR (exit code {returncode})"

    if "Manual Submission Instructions" in output:
        return "PACKAGED (Manual Upload)"

    return "COMPLETED"


def get_identity_token() -> tuple[str, str]:
    """Retrieves Google Cloud OIDC identity token for authenticating against the validator."""
    corp_suffix = "@" + "google.com"
    try:
        out = subprocess.run(
            ["gcloud", "auth", "list", "--format=json"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if out.returncode == 0 and out.stdout.strip():
            accounts = json.loads(out.stdout)
            corp_acc = next(
                (acc["account"] for acc in accounts if acc.get("account", "").endswith(corp_suffix)),
                None,
            )
            if corp_acc:
                res = subprocess.run(
                    ["gcloud", "auth", "print-identity-token", f"--account={corp_acc}"],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                if res.returncode == 0 and res.stdout.strip():
                    return res.stdout.strip(), corp_acc
    except Exception:
        pass

    try:
        res = subprocess.run(
            ["gcloud", "auth", "print-identity-token"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if res.returncode == 0 and res.stdout.strip():
            return res.stdout.strip(), ""
    except Exception:
        pass

    return "", ""


def submit_existing_zip(validator_url: str, eval_name: str, zip_path: str, token: str = "") -> tuple[int, str]:
    """Submits an already-built local .zip bundle directly to the validator endpoint."""
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
        eval_name.encode("utf-8"),
        f"--{boundary}".encode("utf-8"),
        f'Content-Disposition: form-data; name="files"; filename="{filename}"'.encode("utf-8"),
        b"Content-Type: application/zip",
        b"",
        file_bytes,
        f"--{boundary}--".encode("utf-8"),
        b"",
    ]
    body = bytes([13, 10]).join(body_parts)
    headers = {
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "Content-Length": str(len(body)),
        "User-Agent": "lab-evaluation-client/1.0",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
        headers["X-User-Token"] = token

    req = urllib.request.Request(validator_url, data=body, headers=headers, method="POST")
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        with urllib.request.urlopen(req, context=ctx, timeout=180) as response:
            return response.status, response.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8") if e.fp else str(e)
        return e.code, err_body
    except Exception as e:
        return 0, f"Failed to connect to validator at {validator_url}: {e}"


def eval_name_for_script(script_path: str) -> str:
    """Maps '01-test_terraform_infrastructure.py' -> 'terraform_infrastructure'."""
    stem = os.path.splitext(os.path.basename(script_path))[0]
    m = re.match(r"^[0-9]{2}-(?:test_)?(.+)$", stem)
    return m.group(1) if m else stem


def run_resubmit_existing(script_dir: str, scripts: list[str]) -> int:
    """Fast-resubmits existing local .zip packages in script_dir without re-running BigQuery."""
    print("================================================================================")
    print(" Fast Re-Submit Mode (--resubmit-existing): Submitting Existing Local .zip Files")
    print("================================================================================")

    is_localhost = "localhost" in DEFAULT_VALIDATOR_URL or "127.0.0.1" in DEFAULT_VALIDATOR_URL
    token, auth_acc = ("", "") if is_localhost else get_identity_token()
    if not is_localhost and not token:
        print("ERROR: Could not acquire Google Cloud identity token. Run 'gcloud auth login' first.")
        return 1
    if auth_acc:
        print(f"✔ Authenticated with identity token ({auth_acc}).")

    results: list[tuple[str, str]] = []
    found_any = False
    for script in scripts:
        script_name = os.path.basename(script)
        eval_name = eval_name_for_script(script)
        zip_path = os.path.join(script_dir, f"{eval_name}.zip")
        if not os.path.isfile(zip_path):
            results.append((script_name, "SKIPPED (no local .zip)"))
            continue
        found_any = True
        print("\n--------------------------------------------------------------------------------")
        print(f"Re-submitting existing bundle: {eval_name}.zip ({script_name})")
        print("--------------------------------------------------------------------------------", flush=True)
        http_code, resp_text = submit_existing_zip(DEFAULT_VALIDATOR_URL, eval_name, zip_path, token)
        try:
            parsed = json.loads(resp_text)
            print(json.dumps(parsed, indent=2))
        except Exception:
            print(resp_text)
        status = extract_eval_status(resp_text, 0 if http_code in (200, 201) else 1)
        results.append((script_name, status))

    if not found_any:
        print("\nNo existing *.zip bundles found in lab-evaluation-verifier/.")
        print("Run 'python3 lab-evaluation-verifier/run-all-evals.py' (without --resubmit-existing) to build and submit them.")
        return 1

    print("\n================================================================================")
    print(" Fast Re-Submission Summary")
    print("================================================================================")
    pass_count = 0
    fail_count = 0
    skip_count = 0
    for sname, status in results:
        if status == "PASS":
            pass_count += 1
        elif status.startswith("SKIPPED"):
            skip_count += 1
        elif status.startswith("FAIL") or status.startswith("ERROR"):
            fail_count += 1
        print(f"  {sname:<42} : {status}")
    print("--------------------------------------------------------------------------------")
    print(f"  Submitted: {len(results) - skip_count} | PASS: {pass_count} | FAIL: {fail_count} | SKIPPED: {skip_count}")
    print("================================================================================")
    return 0 if fail_count == 0 else 1


def parse_only_filter(argv: list[str]) -> tuple[set[str], list[str]]:
    """Extracts --only / --only=... checkpoint numbers or names and returns (selected_set, forwarded_argv)."""
    selected: set[str] = set()
    forwarded: list[str] = []
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--only" and i + 1 < len(argv):
            for tok in argv[i + 1].split(","):
                t = tok.strip()
                if t:
                    selected.add(t.zfill(2) if t.isdigit() else t)
            i += 2
            continue
        if arg.startswith("--only="):
            for tok in arg.split("=", 1)[1].split(","):
                t = tok.strip()
                if t:
                    selected.add(t.zfill(2) if t.isdigit() else t)
            i += 1
            continue
        forwarded.append(arg)
        i += 1
    return selected, forwarded


def filter_scripts(scripts: list[str], selected: set[str]) -> list[str]:
    """Filters checkpoint scripts by 2-digit prefix (e.g. '01', '06') or evaluation name."""
    if not selected:
        return scripts
    out = []
    for s in scripts:
        bname = os.path.basename(s)
        prefix = bname[:2]
        ename = eval_name_for_script(s)
        if prefix in selected or ename in selected or bname in selected:
            out.append(s)
    return out


def main() -> None:
    if "-h" in sys.argv or "--help" in sys.argv:
        print(__doc__.strip())
        sys.exit(0)

    selected, forwarded_args = parse_only_filter(sys.argv[1:])
    script_dir = os.path.dirname(os.path.abspath(__file__))
    scripts = filter_scripts(sorted(glob.glob(os.path.join(script_dir, "[0-9][0-9]-*.py"))), selected)

    if not scripts:
        print(f"No evaluation scripts matched in {script_dir} (filter: {sorted(selected)})")
        sys.exit(1)

    if "--resubmit-existing" in forwarded_args:
        sys.exit(run_resubmit_existing(script_dir, scripts))

    print("================================================================================")
    print(f" Running Lab Evaluations ({len(scripts)} script{'s' if len(scripts) != 1 else ''})")
    print("================================================================================")

    results = []
    for script in scripts:
        script_name = os.path.basename(script)
        print("\n--------------------------------------------------------------------------------")
        print(f"Running: {script_name}")
        print("--------------------------------------------------------------------------------", flush=True)
        cmd = [sys.executable, "-u", script] + forwarded_args
        output_lines = []
        with subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        ) as proc:
            assert proc.stdout is not None
            for line in proc.stdout:
                print(line, end="", flush=True)
                output_lines.append(line)
            proc.wait()
            returncode = proc.returncode

        full_output = "".join(output_lines)
        status = extract_eval_status(full_output, returncode)
        results.append((script_name, status))

    print("\n================================================================================")
    print(" Evaluation Run Summary")
    print("================================================================================")
    pass_count = 0
    fail_count = 0
    for sname, status in results:
        if status == "PASS":
            pass_count += 1
        elif status.startswith("FAIL") or status.startswith("ERROR"):
            fail_count += 1
        print(f"  {sname:<42} : {status}")
    print("--------------------------------------------------------------------------------")
    print(f"  Total: {len(results)} | PASS: {pass_count} | FAIL: {fail_count}")
    print("================================================================================")

    sys.exit(0 if fail_count == 0 else 1)


if __name__ == "__main__":
    main()
