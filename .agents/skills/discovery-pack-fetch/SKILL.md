---
name: discovery-pack-fetch
description: Resolves and writes the Discovery Context Pack into docs/discovery-pack-tier0.md (Pass 1 Guided Tier 0) or docs/discovery-pack.md (Pass 2 Solo Tier 2 / Tier 1) from the repository's built-in pre-derived packs (.agents/skills/discovery-pack-fetch/packs/), and updates agent-config.json with the selected problem and tier.
---

# Discovery Pack Fetch Skill (`discovery-pack-fetch`)

Use this skill in **Pass 1 (Checkpoint 02)** and **Pass 2 (Checkpoint 07)** to resolve your bounded Discovery Context Pack into `docs/discovery-pack-tier0.md` (Pass 1) or `docs/discovery-pack.md` (Pass 2) and sync `agent-config.json`.

## Built-In Pre-Derived Classroom Packs (Zero Network or Token Dependency)
All **9 enterprise problems × Tiers 0–3** (`36` pre-derived packs) are shipped directly inside this repository at `.agents/skills/discovery-pack-fetch/packs/<problem_id>-tier<0|1|2|3>.md`. By default, `scripts/run.py` resolves and writes the requested pack 100% locally with zero network or identity-token dependency.

*(If you answered custom or expanded follow-up questions in the Classroom Browser UI Step 2.1, you can also click **Download Custom Context Pack (`.md`)** in Step 2.3 of the Browser UI and save it to `docs/discovery-pack.md`.)*

## CLI Usage

```bash
# 1. List all 9 built-in problems and their available Tier 0–3 packs:
python3 .agents/skills/discovery-pack-fetch/scripts/run.py --list

# 2. Pass 1 (Checkpoint 02) — Resolve Demand Forecasting at Tier 0 into docs/discovery-pack-tier0.md:
python3 .agents/skills/discovery-pack-fetch/scripts/run.py \
  --problem-id forecasting \
  --tier 0 \
  --output docs/discovery-pack-tier0.md

# 3. Pass 2 (Checkpoint 07) — Resolve Demand Forecasting (or any of the 9 problems) at Tier 2 into docs/discovery-pack.md:
python3 .agents/skills/discovery-pack-fetch/scripts/run.py \
  --problem-id forecasting \
  --tier 2 \
  --output docs/discovery-pack.md
```
