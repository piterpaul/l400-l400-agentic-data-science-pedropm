"""Deterministic generator and BigQuery loader for Predictive Maintenance.

Generates three CSV tables (`assets.csv`, `weekly_readings.csv`, `work_orders.csv`)
using only the Python standard library (seed 20260927) and optionally loads them
into `<project>.<dataset>` via `bq load`.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import random
import subprocess
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[2]
SEED = 20260927
N_ASSETS = 900
WEEKS = 156
START_DATE = date(2023, 1, 2)
WEIBULL_SHAPE = 1.75
MODELS: dict[str, tuple[str, float, int]] = {
    "P100": ("MakerA", 4.2, 208),
    "P200": ("MakerA", 5.0, 208),
    "Q7": ("MakerB", 3.4, 260),
}
FAIL_NOTES: dict[str, list[str]] = {
    "bearing": [
        "High vibration alarm; drive-end bearing spalled and seal blown. Replaced bearing.",
        "Unit seized under load; inner race fractured and shaft scored. Overhauled assembly.",
    ],
    "winding": [
        "Breaker tripped on thermal overload; stator winding insulation burnt. Replaced motor.",
        "Phase imbalance and earth fault after voltage spike; rewound stator.",
    ],
}
PM_NOTES = [
    "Scheduled 4-year overhaul completed; replaced bearing and seal kit as precaution.",
    "Planned preventive swap at operating-hour limit; no active fault found on strip-down.",
]
INSPECTION_NOTES = [
    "Routine quarterly inspection; strainer cleaned and sensor zero checked.",
    "Operator reported rattle; guard bolt tightened, no mechanical fault found.",
    "Cleared nuisance maker alarm on panel; unit running within normal limits.",
]


def iso_week(offset_weeks: int, extra_days: int = 0) -> str:
    """Return ISO date string for START_DATE + offset_weeks + extra_days."""
    return (START_DATE + timedelta(weeks=offset_weeks, days=extra_days)).isoformat()


def generate_tables(out_dir: Path) -> dict[str, int]:
    """Generate assets.csv, weekly_readings.csv, and work_orders.csv deterministically."""
    rng = random.Random(SEED)
    out_dir.mkdir(parents=True, exist_ok=True)

    assets_rows: list[dict[str, object]] = []
    readings_rows: list[dict[str, object]] = []
    work_orders_rows: list[dict[str, object]] = []

    for idx in range(N_ASSETS):
        asset_id = f"A{idx:04d}"
        asset_class = sorted(MODELS)[idx % len(MODELS)]
        maker, scale_years, swap_weeks = MODELS[asset_class]
        site_id = f"SITE-{(idx % 12) + 1:02d}"
        load_z = rng.gauss(0.0, 1.0)
        amb_z = rng.gauss(0.0, 1.0)
        install_offset = -rng.randint(20, 160)
        has_flatline = rng.random() < 0.08
        flat_start = rng.randint(15, WEEKS - 12) if has_flatline else -1

        assets_rows.append(
            {
                "asset_id": asset_id,
                "asset_class": asset_class,
                "maker": maker,
                "site_id": site_id,
                "install_date": iso_week(install_offset),
                "scheduled_swap_weeks": swap_weeks,
                "rated_load_kw": round(55.0 + 10.0 * load_z, 1),
                "ambient_temp_c": round(22.0 + 4.0 * amb_z, 1),
            }
        )

        # Simulate asset life starting at install_offset
        scale_w = scale_years * 52.0 * math.exp(-(0.42 * load_z + 0.25 * amb_z) / WEIBULL_SHAPE)
        ttf_weeks = int(scale_w * (-math.log(1.0 - rng.random())) ** (1.0 / WEIBULL_SHAPE))
        ttf_weeks = max(24, ttf_weeks)
        fault_mode = "bearing" if rng.random() < 0.65 else "winding"
        end_age = min(ttf_weeks, swap_weeks)
        end_week = install_offset + end_age

        if end_week < 12:
            # Start a fresh life before the observation window so we observe active operation
            install_offset = rng.randint(-40, 10)
            end_age = min(ttf_weeks, swap_weeks)
            end_week = install_offset + end_age

        is_failure = ttf_weeks < swap_weeks and end_week < WEEKS
        is_pm_swap = not is_failure and end_week < WEEKS
        event_observed = 1 if is_failure else 0
        onset_week = end_week - rng.randint(5, 9) if is_failure else end_week + 999

        if is_failure or is_pm_swap:
            lag_days = rng.randint(2, 10)
            note = rng.choice(FAIL_NOTES[fault_mode]) if is_failure else rng.choice(PM_NOTES)
            work_orders_rows.append(
                {
                    "work_order_id": f"WO-{len(work_orders_rows) + 1:05d}",
                    "asset_id": asset_id,
                    "filed_date": iso_week(end_week, extra_days=lag_days),
                    "order_type": "UNPLANNED_FAILURE" if is_failure else "PREVENTIVE_OVERHAUL",
                    "technician_note": note,
                }
            )

        obs_start = max(0, install_offset)
        obs_end = min(end_week, WEEKS)
        duration_weeks = max(1, obs_end - install_offset)

        for w in range(obs_start, obs_end):
            age_w = w - install_offset
            deg = max(0.0, (w - onset_week) / 6.0) if w >= onset_week else 0.0
            season = math.sin(2.0 * math.pi * w / 52.0)

            vib = 2.1 + 0.003 * age_w + 1.85 * deg + rng.gauss(0.0, 0.16)
            bearing_temp = 58.0 + 4.0 * season + 2.5 * amb_z + 11.0 * deg + rng.gauss(0.0, 1.1)
            amps = 82.0 + 9.0 * load_z + 6.5 * deg + rng.gauss(0.0, 1.8)
            exhaust_temp = 45.0 + 5.0 * season + 3.0 * load_z + 9.0 * deg + rng.gauss(0.0, 0.9)
            if has_flatline and flat_start <= w < flat_start + 6:
                exhaust_temp = 45.0
            particles = max(10, int(120 + 0.8 * age_w + 190 * deg + rng.gauss(0.0, 18.0)))
            acoustic = 68.0 + 0.01 * age_w + 7.5 * deg + rng.gauss(0.0, 0.9)
            maker_alarm = 1 if (vib > 3.6 or bearing_temp > 71.0 or rng.random() < 0.03) else 0
            failed_4w = 1 if (is_failure and 0 <= (end_week - w) <= 4) else 0

            readings_rows.append(
                {
                    "asset_id": asset_id,
                    "week_start": iso_week(w),
                    "life_id": 1,
                    "operating_hours": round(age_w * (112.0 + 8.0 * load_z), 1),
                    "ch1_vibration_mms": round(vib, 3),
                    "ch2_bearing_temp_c": round(bearing_temp, 2),
                    "ch3_current_amps": round(amps, 2),
                    "ch4_exhaust_temp_c": round(exhaust_temp, 2),
                    "ch5_oil_particle_count": particles,
                    "ch6_acoustic_db": round(acoustic, 2),
                    "maker_alarm": maker_alarm,
                    "failed_within_4w": failed_4w,
                    "duration_weeks": duration_weeks,
                    "event_observed": event_observed,
                }
            )

            if rng.random() < 0.0025:
                work_orders_rows.append(
                    {
                        "work_order_id": f"WO-{len(work_orders_rows) + 1:05d}",
                        "asset_id": asset_id,
                        "filed_date": iso_week(w, extra_days=rng.randint(0, 4)),
                        "order_type": "ROUTINE_INSPECTION",
                        "technician_note": rng.choice(INSPECTION_NOTES),
                    }
                )

    counts: dict[str, int] = {}
    for name, rows in (
        ("assets", assets_rows),
        ("weekly_readings", readings_rows),
        ("work_orders", work_orders_rows),
    ):
        csv_path = out_dir / f"{name}.csv"
        with csv_path.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        counts[name] = len(rows)
    return counts


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
    """Generate CSVs and optionally load them into BigQuery."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project",
        default="",
        help="Google Cloud project ID (defaults to GOOGLE_CLOUD_PROJECT or agent-config.json).",
    )
    parser.add_argument(
        "--dataset",
        default="pdm_workshop",
        help="Target BigQuery dataset name (default: pdm_workshop).",
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
        help="Directory for generated CSV files.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Generate CSV files locally without calling bq.",
    )
    args = parser.parse_args()
    project, location = resolve_defaults(args.project, args.location)

    counts = generate_tables(args.out_dir)
    for name, count in counts.items():
        print(f"Generated {args.out_dir / f'{name}.csv'}: {count:,} rows")

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
    for name in ("assets", "weekly_readings", "work_orders"):
        csv_path = args.out_dir / f"{name}.csv"
        target = f"{project}:{args.dataset}.{name}"
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
