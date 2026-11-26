---
name: conversational-analytics-agent
description: Creates, queries (:chat), lists, and deletes stateful BigQuery Data Agents via the Conversational Analytics REST API (geminidataanalytics.googleapis.com) using Application Default Credentials.
---

# Conversational Analytics Data Agent Skill (`conversational-analytics-agent`)

Use this skill in **Part 1 (Shared Guided Tier 0 NYC Citi Bike Build)** — or any Tier 0 / Tier 1 verification — to create and chat with a stateful BigQuery Studio Data Agent over `geminidataanalytics.googleapis.com`.

## What It Does
A stateful data agent created at `projects/{project}/locations/global/dataAgents/{data_agent_id}` is a first-class **BigQuery Studio Agent**:
- It appears directly in the Google Cloud Console under **BigQuery → Studio → Left Rail: Agents → My agents**.
- It populates both `staging_context` (the visual Agent Builder editor in BigQuery Studio) and `published_context` (live `:chat` and interactive Console conversations) using the 4-part Context Engineering pattern (`datasource_references`, `system_instruction`, `glossary_terms`, `example_queries`).
- When queried through a stateful conversation (`/v1beta/projects/{project}/locations/global/conversations` + `:chat`) or directly in BigQuery Studio, it generates and executes BigQuery SQL including built-in zero-shot `AI.FORECAST` and `AI.DETECT_ANOMALIES` (`TimesFM 2.5`).
- In **Pass 2 (Solo Tier 1/2)**, you keep this same Conversational Analytics Data Agent as your human interaction layer by pointing its `datasource_references` at your new Tier 1/2 prediction, evaluation, and explanation tables.

## CLI Usage

```bash
# 1. Create/update and chat-verify the Tier 0 NYC Citi Bike data agent + write labs/guided/citibike/tier1_trigger.md:
python3 .agents/skills/conversational-analytics-agent/scripts/run.py \
  --project-id "${GOOGLE_CLOUD_PROJECT}" \
  --dataset-id citibike_tier0 \
  --table-id daily_trips_by_usertype \
  --agent-id citibike_tier0_agent \
  --trigger-doc labs/guided/citibike/tier1_trigger.md

# 2. Ask the data agent a follow-up question via stateful :chat:
python3 .agents/skills/conversational-analytics-agent/scripts/run.py --action ask \
  --prompt "Compare Subscriber and Customer rewind holdout accuracy and show any zero-filled weather shutdown dates."

# 3. List active data agents in your project:
python3 .agents/skills/conversational-analytics-agent/scripts/run.py --action list

# 4. Delete the data agent during clean-room teardown:
python3 .agents/skills/conversational-analytics-agent/scripts/run.py --action delete
```

## Python Import Usage

```python
import sys
import os
import json

sys.path.append(os.path.abspath('.agents/skills/conversational-analytics-agent/scripts'))
import run

with open('agent-config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

agent = run.create_citibike_agent(
    project_id=config["gcp-project-id"],
    dataset_id=config.get("tier0-bigquery-dataset", "citibike_tier0"),
    agent_id=config.get("tier0-data-agent-id", "citibike_tier0_agent"),
)
print(json.dumps(agent, indent=2))
```
