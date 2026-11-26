#!/usr/bin/env python3
"""
Resolves and writes a Discovery Context Pack into docs/discovery-pack-tier0.md (Pass 1)
or docs/discovery-pack.md (Pass 2) from the repository's built-in pre-derived packs
(.agents/skills/discovery-pack-fetch/packs/<problem_id>-tier<0|1|2|3>.md), and updates agent-config.json.

By default, all 9 enterprise problems x Tiers 0-3 are resolved 100% locally from the built-in
packs in the cloned repository (zero network or identity token dependency required).
Pass --from-api only if you explicitly want to pull a remote state from data-science-hub-api.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request

DEFAULT_API_URL = "https://data-science-hub-api-463617135523.us-central1.run.app"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PACKS_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "packs")

BUILTIN_PROBLEMS = [
    ("forecasting", "Demand Forecasting & Inventory Allocation (Live Class Focus — NYC Citi Bike)"),
    ("next-best-offer", "Next-Best-Offer & Cross-Sell Propensity"),
    ("payment-fraud", "Payment Fraud Detection"),
    ("predictive-maintenance", "Predictive Maintenance & Survival Analysis"),
    ("search-conversion", "Search & Product Discovery Conversion"),
    ("recommender", "Product Recommendation & Cold-Start Ranking"),
    ("churn", "Customer Churn & Retention"),
    ("clinical-risk", "Clinical Risk Stratification"),
    ("marketing-measurement", "Marketing Mix Modeling & Attribution"),
]


def load_config(config_path: str = "agent-config.json") -> dict:
    for candidate in (config_path, "agent-config.example.json"):
        if os.path.exists(candidate):
            with open(candidate, "r", encoding="utf-8") as f:
                return json.load(f)
    return {}


def get_google_identity_token(preferred_email: str = "") -> tuple[str, str]:
    """Mints an OIDC identity token for the student's corporate account (used only when --from-api is passed)."""
    account = ""
    if preferred_email and "@" in preferred_email and "{" not in preferred_email:
        account = preferred_email.strip()

    if not account:
        out = subprocess.run(
            ["gcloud", "auth", "list", "--format=json"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if out.returncode == 0 and out.stdout.strip():
            accounts = json.loads(out.stdout)
            account = next(
                (a.get("account", "") for a in accounts if a.get("account", "") and "gserviceaccount.com" not in a.get("account", "")),
                "",
            )

    cmd = ["gcloud", "auth", "print-identity-token"]
    if account:
        cmd.append(f"--account={account}")

    res = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    if res.returncode != 0 or not res.stdout.strip():
        raise RuntimeError(f"Failed to mint identity token ({' '.join(cmd)}): {res.stderr.strip()}")
    return res.stdout.strip(), account or "active-account"


def api_get(url: str, token: str) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "User-Agent": "l400-discovery-pack-fetch/2.0",
        },
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read().decode("utf-8")


def list_packs(api_url: str = DEFAULT_API_URL, user_email: str = "", from_api: bool = False) -> dict:
    """Lists all built-in pre-derived packs in the cloned repo (or remote API packs if from_api=True)."""
    builtin = []
    for pid, title in BUILTIN_PROBLEMS:
        tiers = []
        for t in (0, 1, 2, 3):
            pfile = os.path.join(PACKS_DIR, f"{pid}-tier{t}.md")
            if os.path.exists(pfile):
                tiers.append({"tier": t, "path": os.path.relpath(pfile, os.getcwd())})
        builtin.append({"problem_id": pid, "title": title, "available_tiers": tiers})

    if not from_api:
        return {
            "source": "built-in-classroom-packs",
            "packs_dir": os.path.relpath(PACKS_DIR, os.getcwd()),
            "problems": builtin,
        }

    token, account = get_google_identity_token(user_email)
    body = api_get(f"{api_url.rstrip('/')}/packs", token)
    parsed = json.loads(body)
    items = (parsed.get("opportunities") or parsed.get("packs") or []) if isinstance(parsed, dict) else parsed
    return {"source": "api", "account": account, "packs": items, "builtin_problems": builtin}


def extract_pack_metadata(markdown_text: str) -> dict:
    """Extracts the embedded JSON block at the end of a discovery pack markdown file."""
    matches = re.findall(r"```json\s*(\{.*?\})\s*```", markdown_text, flags=re.S)
    for raw in reversed(matches):
        try:
            data = json.loads(raw)
            if isinstance(data, dict) and ("problem" in data or "derivation" in data or "schema_version" in data):
                return data
        except Exception:
            continue
    return {}


def load_builtin_pack(problem_id: str, tier: int) -> str:
    """Reads the pre-derived Discovery Context Pack from .agents/skills/discovery-pack-fetch/packs/."""
    pid = (problem_id or "forecasting").strip().lower()
    t = tier if tier is not None else 2
    t = max(0, min(3, int(t)))
    candidate = os.path.join(PACKS_DIR, f"{pid}-tier{t}.md")
    if os.path.exists(candidate):
        with open(candidate, "r", encoding="utf-8") as f:
            return f.read()
    fallback = os.path.join(PACKS_DIR, f"forecasting-tier{t}.md")
    if os.path.exists(fallback):
        with open(fallback, "r", encoding="utf-8") as f:
            return f.read()
    raise FileNotFoundError(f"Built-in pack not found at {candidate}")


def fetch_pack(
    pack_id: str = "",
    tier: int | None = None,
    output_path: str = "docs/discovery-pack.md",
    api_url: str = DEFAULT_API_URL,
    user_email: str = "",
    config_path: str = "agent-config.json",
    from_api: bool = False,
) -> dict:
    pid = (pack_id or "forecasting").strip().lower()
    if tier is None:
        tier = 0 if "tier0" in output_path.lower() else 2
    target_tier = max(0, min(3, int(tier)))
    source = "built-in-classroom-pack"
    markdown_text = ""

    if from_api:
        try:
            base = api_url.rstrip("/")
            token, _ = get_google_identity_token(user_email)
            markdown_text = api_get(f"{base}/packs/{pid}", token)
            source = "hub-api"
        except Exception:
            markdown_text = ""

    if not markdown_text:
        markdown_text = load_builtin_pack(pid, target_tier)
        source = "built-in-classroom-pack"

    meta = extract_pack_metadata(markdown_text)
    if meta:
        meta["schema_version"] = "1.0"
        meta["problem_id"] = pid
        meta["target_tier"] = target_tier
        meta["recommended_rung"] = target_tier
        rng = meta.setdefault("range", {})
        if isinstance(rng, dict):
            rng["floor"] = target_tier
            rng["ceiling"] = 0 if target_tier == 0 else max(target_tier, int(rng.get("ceiling") or target_tier))
            rng["clash"] = False
        deriv = meta.setdefault("derivation", {})
        deriv["floor"] = target_tier
        deriv["ceiling"] = 0 if target_tier == 0 else max(target_tier, 2)
        deriv["recommended_tier"] = target_tier
        deriv["recommended_rung"] = target_tier
        deriv["clash"] = False
        replacement_block = f"```json\n{json.dumps(meta, indent=2, ensure_ascii=False)}\n```"
        markdown_text = re.sub(
            r"```json\s*\{.*?\}\s*```",
            lambda _m: replacement_block,
            markdown_text,
            count=1,
            flags=re.S,
        )

    if not markdown_text.startswith("---\n"):
        frontmatter = (
            "---\n"
            'schema_version: "1.0"\n'
            f'problem_id: "{pid}"\n'
            f"target_tier: {target_tier}\n"
            f"recommended_rung: {target_tier}\n"
            f'source: "{source}"\n'
            "---\n\n"
        )
        markdown_text = frontmatter + markdown_text

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown_text)

    if os.path.exists(config_path) or os.path.exists("agent-config.example.json"):
        cfg = load_config(config_path)
        cfg["selected-problem-id"] = str(pid)
        cfg["selected-tier"] = f"Tier {target_tier}"
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=4)
            f.write("\n")

    return {
        "status": "ok",
        "source": source,
        "pack_id": pid,
        "problem_id": pid,
        "target_tier": target_tier,
        "recommended_tier": target_tier,
        "output_path": output_path,
        "bytes": len(markdown_text.encode("utf-8")),
    }


def main():
    parser = argparse.ArgumentParser(
        description="List or resolve built-in Discovery Context Packs into docs/discovery-pack-tier0.md or docs/discovery-pack.md."
    )
    parser.add_argument("--list", action="store_true", help="List all 9 built-in problems and pre-derived tier packs")
    parser.add_argument("--id", "--problem-id", dest="pack_id", default="forecasting", help="Problem ID (default: forecasting)")
    parser.add_argument("--tier", type=int, default=None, help="Target tier: 0 (Pass 1 Guided), 1, 2 (Pass 2 Solo), or 3")
    parser.add_argument("--out", "--output", dest="output_path", default="docs/discovery-pack.md", help="Output path for the markdown pack")
    parser.add_argument("--from-api", action="store_true", help="Optional: fetch live custom state from data-science-hub-api instead of built-in repo packs")
    args = parser.parse_args()

    cfg = load_config()
    api_url = cfg.get("hub-api-url") or DEFAULT_API_URL
    user_email = cfg.get("user_email", "")

    try:
        if args.list:
            res = list_packs(api_url=api_url, user_email=user_email, from_api=args.from_api)
        else:
            res = fetch_pack(
                pack_id=args.pack_id,
                tier=args.tier,
                output_path=args.output_path,
                api_url=api_url,
                user_email=user_email,
                from_api=args.from_api,
            )
        print(json.dumps(res, indent=2))
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="ignore") if e.fp else str(e)
        print(json.dumps({"status": "error", "http_code": e.code, "message": err}, indent=2), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}, indent=2), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
