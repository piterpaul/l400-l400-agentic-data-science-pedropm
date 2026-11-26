"""Load Marketing Measurement (MMM) workshop tables into BigQuery.

Loads Google Meridian's Apache-2.0 simulated geo and national panels
(`geo_all_channels.csv` and `national_all_channels.csv`) alongside a
deterministically generated 8-week matched-market switch-off experiment
(`geo_holdout_experiment.csv`) into `<project>.<dataset>`.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import random
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[2]
HOLDOUT_WEEKS = (
    "2023-11-06",
    "2023-11-13",
    "2023-11-20",
    "2023-11-27",
    "2023-12-04",
    "2023-12-11",
    "2023-12-18",
    "2023-12-25",
)
SEED = 20260927
TRUE_CHANNEL0_ROI = 1.62


def build_holdout_csv(geo_csv: Path, out_csv: Path) -> int:
    """Build an 8-week 20-market switch-off holdout table from geo_all_channels.csv."""
    rng = random.Random(SEED)
    with geo_csv.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows = [r for r in reader if r["time"] in HOLDOUT_WEEKS]

    geos = sorted({r["geo"] for r in rows}, key=lambda g: int(g.replace("Geo", "")))
    dark_geos = set(geos[::2])  # 20 treatment_dark markets, 20 control_active markets

    out_csv.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "geo",
        "time",
        "assignment",
        "population",
        "channel0_baseline_spend",
        "channel0_withheld_spend",
        "observed_conversions",
        "counterfactual_conversions",
        "incremental_conversions",
        "revenue_per_conversion",
        "incremental_roi",
    ]
    written = 0
    with out_csv.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            geo = row["geo"]
            is_dark = geo in dark_geos
            base_spend = float(row["Channel0_spend"])
            rev_per_conv = float(row["revenue_per_conversion"])
            counterfactual_conv = float(row["conversions"])
            withheld = base_spend if is_dark else 0.0
            noise = rng.gauss(1.0, 0.04)
            # Diminishing returns (Hill-like curvature) around the true ROI anchor (1.62)
            effective_roi = TRUE_CHANNEL0_ROI * math.pow(max(base_spend, 100.0) / 5000.0, -0.12)
            inc_revenue = withheld * effective_roi * noise
            inc_conv = inc_revenue / max(rev_per_conv, 1e-6)
            observed_conv = max(0.0, counterfactual_conv - inc_conv)
            writer.writerow(
                {
                    "geo": geo,
                    "time": row["time"],
                    "assignment": "treatment_dark" if is_dark else "control_active",
                    "population": int(float(row["population"])),
                    "channel0_baseline_spend": round(base_spend, 2),
                    "channel0_withheld_spend": round(withheld, 2),
                    "observed_conversions": round(observed_conv, 2),
                    "counterfactual_conversions": round(counterfactual_conv, 2),
                    "incremental_conversions": round(inc_conv, 2),
                    "revenue_per_conversion": round(rev_per_conv, 4),
                    "incremental_roi": round(
                        (inc_conv * rev_per_conv) / withheld if withheld > 0 else 0.0, 4
                    ),
                }
            )
            written += 1
    return written


def get_bq_env() -> dict[str, str]:
    """Return environment dict preferring the student's *.altostrat.com account for bq CLI."""
    env = os.environ.copy()
    try:
        res = subprocess.run(
            ["gcloud", "auth", "list", "--format=value(account)"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        for line in res.stdout.splitlines():
            acct = line.strip()
            if acct.endswith(".altostrat.com"):
                env["CLOUDSDK_CORE_ACCOUNT"] = acct
                break
    except Exception:
        pass
    return env


def resolve_defaults(project_arg: str, location_arg: str) -> tuple[str, str]:
    """Resolve project ID and BigQuery location from CLI args, env, or agent-config.json."""
    project = project_arg.strip() or os.environ.get("GOOGLE_CLOUD_PROJECT", "").strip()
    location = location_arg.strip()
    cfg_path = REPO_ROOT / "agent-config.json"
    if cfg_path.exists():
        try:
            cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
            if not project:
                cand = str(cfg.get("gcp-project-id", "")).strip()
                if cand and "{" not in cand and cand != "null":
                    project = cand
            if not location:
                loc = str(cfg.get("bigquery-region", "")).strip()
                if loc and "{" not in loc:
                    location = loc
        except Exception:
            pass
    return project, (location or "US")


def run_bq(cmd: list[str]) -> None:
    """Execute a bq CLI command and raise on non-zero exit."""
    subprocess.run(cmd, check=True, env=get_bq_env())


def main() -> None:
    """Parse arguments, build holdout table, and optionally load into BigQuery."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project",
        default="",
        help="Google Cloud project ID (defaults to GOOGLE_CLOUD_PROJECT or agent-config.json).",
    )
    parser.add_argument(
        "--dataset",
        default="mmm_workshop",
        help="Target BigQuery dataset name (default: mmm_workshop).",
    )
    parser.add_argument(
        "--location",
        default="",
        help="BigQuery dataset location (default: US from agent-config.json).",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=HERE / "out",
        help="Directory for generated geo_holdout_experiment.csv.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Generate geo_holdout_experiment.csv locally without calling bq.",
    )
    args = parser.parse_args()
    project, location = resolve_defaults(args.project, args.location)

    geo_csv = HERE / "geo_all_channels.csv"
    nat_csv = HERE / "national_all_channels.csv"
    holdout_csv = args.out_dir / "geo_holdout_experiment.csv"

    n_holdout = build_holdout_csv(geo_csv, holdout_csv)
    print(f"Generated {holdout_csv} ({n_holdout} rows).")

    if args.dry_run or not project:
        if not project and not args.dry_run:
            raise SystemExit("Pass --project <PROJECT_ID>, set GOOGLE_CLOUD_PROJECT, or populate agent-config.json.")
        return

    run_bq(
        [
            "bq",
            f"--location={location}",
            "mk",
            "--dataset",
            "--force",
            f"{project}:{args.dataset}",
        ]
    )
    for table_name, csv_path in (
        ("geo_all_channels", geo_csv),
        ("national_all_channels", nat_csv),
        ("geo_holdout_experiment", holdout_csv),
    ):
        target = f"{project}:{args.dataset}.{table_name}"
        print(f"Loading {csv_path.name} -> {target} (location={location}) ...")
        run_bq(
            [
                "bq",
                f"--location={location}",
                "load",
                "--replace",
                "--autodetect",
                "--source_format=CSV",
                target,
                str(csv_path),
            ]
        )
    print(f"Loaded 3 tables into {project}.{args.dataset} ({location}).")


if __name__ == "__main__":
    main()
