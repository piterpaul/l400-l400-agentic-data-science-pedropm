#!/usr/bin/env python3
"""Unified dispatcher for loading shipped L400 workshop datasets into BigQuery.

Dispatches `--problem predictive-maintenance` to `labs/data/predictive-maintenance/generate_and_load.py`
and `--problem marketing-measurement` to `labs/data/marketing-measurement/load_to_bq.py`.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

PROBLEM_SCRIPTS: dict[str, tuple[Path, str]] = {
    "predictive-maintenance": (
        REPO_ROOT / "labs" / "data" / "predictive-maintenance" / "generate_and_load.py",
        "pdm_workshop",
    ),
    "marketing-measurement": (
        REPO_ROOT / "labs" / "data" / "marketing-measurement" / "load_to_bq.py",
        "mmm_workshop",
    ),
}


def main() -> None:
    """Parse arguments and invoke the target shipped-dataset loader."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--problem",
        required=True,
        choices=sorted(PROBLEM_SCRIPTS.keys()),
        help="Catalog problem ID whose shipped dataset should be generated and loaded.",
    )
    parser.add_argument(
        "--project",
        default="",
        help="Google Cloud project ID (defaults to GOOGLE_CLOUD_PROJECT or agent-config.json).",
    )
    parser.add_argument(
        "--dataset",
        default="",
        help="Target BigQuery dataset name (defaults to pdm_workshop or mmm_workshop).",
    )
    parser.add_argument(
        "--location",
        default="",
        help="BigQuery dataset location (defaults to US from agent-config.json).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Generate CSV files locally without calling bq.",
    )
    args = parser.parse_args()

    script_path, default_dataset = PROBLEM_SCRIPTS[args.problem]
    cmd = [sys.executable, str(script_path)]
    if args.project:
        cmd.extend(["--project", args.project])
    cmd.extend(["--dataset", args.dataset or default_dataset])
    if args.location:
        cmd.extend(["--location", args.location])
    if args.dry_run:
        cmd.append("--dry-run")

    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
