---
schema_version: "1.0"
problem_id: "predictive-maintenance"
target_tier: 2
recommended_rung: 2
source: "built-in-classroom-pack"
---

# Discovery pack — Predictive Maintenance & Asset Reliability

`predictive-maintenance` · recorded by **classroom-repo** · version 1 · served 2026-10-27T00:00:00Z

Every sentence below was authored in the L400 discovery catalog and selected by the answers a customer engineer recorded in the room. None of it was generated. Where an answer is missing, this pack says so and tells you to go and ask.

**How the tiers work.** Tier 0 to Tier 4, cheapest first. An answer never scores a problem; it sets a floor ("not below this rung") or a ceiling ("above this is theatre"). Two answers can set a floor above a ceiling, and that contradiction is a finding, not an error.

**Why the order.** Questions marked keystone are asked of every customer and asked first, because each one opens or closes a branch of the rest.

> ### 🤖 Agent Directives: System Architecture & Solution Design
> - **Role:** Principal Google Cloud Solutions Architect pair-programming with a Customer Engineer.
> - **Objective:** Author a tailored, production-grade `DESIGN.md` for this customer engagement.
> - **Directives:**
>   1. **Primary Target:** Focus the MVP architecture on the recommended tier in Section 6.
>   2. **Adjacent Tier ADR:** Do not design in isolation. Explicitly contrast the chosen rung with its adjacent alternatives using the ADR Matrix in Section 6, establishing either an A/B comparison or a Phase 2 migration trigger.
>   3. **Honor Customer Constraints:** Adhere strictly to the bounded floor, ceiling, latency clock, and operational ownership recorded below.
>   4. **No Hallucinated Infrastructure:** Propose only Google Cloud components compatible with this tier's operational model.
>   5. **Pre-Trained vs. Custom-Trained Balance:** Treat pre-trained foundation models (`AI.FORECAST` `TimesFM 2.5` / `3.0`, `AI.PREDICT` `TabFM` with `<= 50` columns, `<= 10` classes, `~5k–8k` context rows at Tiers 0–1; Hugging Face / Vertex AI open weights `google/timesfm-3.0-pytorch` and `google/tabfm-1.0.0-pytorch` at Tiers 2–3) as additive baselines or low-latency options alongside custom-trained models (`BQML CREATE MODEL`, `LightGBM`/`XGBoost`, `PySpark`, `Meridian`), never as a blanket replacement when custom training is required.

## 1. The ask

> **VP Manufacturing Operations, three-plant discrete manufacturer** — Unplanned downtime costs us $28,000 an hour. We have ten years of sensor data in the historian. Can AI tell us before something breaks?
>
> **Reliability Engineering Manager, water utility with 900 pump stations** — The maker portal already emails us alarms. There are about 400 a week, the crews stopped reading them in 2024, and now we want AI to tell us which ones are real.
>
> **Director of Fleet Engineering, cold-chain logistics operator, 4,000 reefer trailers** — We need the driver to know before the load spoils. Trailers are on cellular, coverage is patchy through the mountain corridors, and we pay per megabyte.

**Vocabulary is unbound.** The nouns below are the method's neutral words, not this customer's — treat them as placeholders and confirm the real terms early.

**The five specifics.**

- **How many, of the thing being predicted** — *not captured. Ask.*
- **How much history there is, and how much arrives** — *not captured. Ask.*
- **The deadline the run has to hit** — *not captured. Ask.*
- **What being wrong costs, per event or per year** — *not captured. Ask.*
- **Who owns the decision, and who would run this** — *not captured. Ask.*

## 2. Where discovery landed

- **Floor: Tier 2 — Distributed & Custom ML** — set by What the historian actually stored
- **Ceiling: Tier 2 — Distributed & Custom ML** — set by Where must the call be made

## 3. What was asked, and what it steered

### 1. What counts as a failure

**Asked:** What counts as a failure here — the machine stopped, or the machine is still running but running badly? Both are in the history and they give you completely different answers from the same ten years.

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Only a full stop counts. If it kept running, nobody wrote it down.
- **Which means:** The strictest definition and the rarest. Expect tens of events across a decade, not thousands, so the model is fitted on events rather than rows — say that out loud before anyone quotes an accuracy number.
- **Bounds:** none
- **For the brief:** Failure = unplanned stop. Rare-event problem; count the events before choosing a model family.
- **Why it was asked:** The label set, and with it whether this is a rare-event problem at all. Running badly is common, measurable today and worth money; stopped is rare and historical. The first is a stand-in target you can ship this quarter.
- **What it forecloses:** Settles the target before anyone opens the archive, which closes the whole argument about model family — sort, date, or rank — and closes every question about how much breakdown history you need to have.

### 2. Does the repair record hold a real date

**Asked:** When a repair gets written up, what does the date on it mean — when the fault started, when somebody noticed, when it was fixed, or when the paperwork was filed?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** The record is really a parts issue. It says which part went out and to what.
- **Which means:** Better than free text and worse than it looks. Parts records carry good dates and no fault description, and if parts move between machines the history follows the wrong one.
- **Bounds:** none
- **For the brief:** Labels come from parts issue records. Check whether parts move between machines before trusting the history.
- **Why it was asked:** Whether you have a timeline at all. The gap between the fault starting and the form being filed is routinely days, and it lands on the wrong side of every window you draw. Real lines look like Repl brg - see note. Ordered 3/14 fitted 3/22.
- **What it forecloses:** Answers this and you know whether the next month is a modelling month or a month spent sitting with a technician dating a few hundred old records by hand. That closes the schedule argument before it starts.

### 3. What the historian actually stored

**Asked:** When a reading comes off the machine, is every value kept, or does the system only write one down when it has moved by more than some amount? And how fast does the thing you care about actually happen?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** There are short high-speed recordings, but only when something already tripped an alarm.
- **Which means:** Good signal and a trap. A recording triggered by an existing alarm means the alarm is inside the feature, so the model learns the alarm rather than the fault and looks superb until it is live.
- **Bounds:** not below Tier 2 — Distributed & Custom ML
- **For the brief:** Waveform snapshots exist but are alarm-triggered. Treat the trigger as leakage; capture on a timer too.
- **Why it was asked:** Whether the physics is still in the data. A deadband is set to save disk and it deletes at the tag, before storage. A bearing defect tone lives in the kilohertz; a one-minute average of it is a flat line.
- **What it forecloses:** Closes the whole modelling conversation for the fast failure modes in one answer, and closes it in the only direction that helps: towards a hardware quote rather than towards a longer pipeline.

### 4. Who owns the historian

**Asked:** Who actually owns the system the readings sit in — the team that runs the machines, or the team that runs the cloud? And do those two teams share a plan?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Same team. They run the control system and they run the cloud project.
- **Which means:** The best case and the rarest. Sampling rates, new points and the pipeline are all one backlog, so the design can genuinely reach down to the machine instead of stopping at the file.
- **Bounds:** none
- **For the brief:** One team owns both sides. New measurement points are in scope.
- **Why it was asked:** The rung, more often downwards than upwards. The plant-side and cloud-side split decides whether you can add a measurement point, change a sampling rate, or only receive whatever last night’s file happened to contain.
- **What it forecloses:** One answer closes every design that assumes new measurements can be turned on, and every schedule that assumes a change on the plant side happens in the same sprint as a change in the cloud.

### 5. Does the crew still act on alerts

**Asked:** When an alert goes out today, does somebody go and look? Be honest about it — do they work every one, do they work the ones they trust, or has everybody quietly stopped reading them?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** They work every one. It is a small list and it is taken seriously.
- **Which means:** The healthiest starting point on this problem. You are adding order to something that already functions, so the only real risk is making the list longer than the crew can absorb.
- **Bounds:** none
- **For the brief:** Alerts are worked. Preserve list length; add ranking, not volume.
- **Why it was asked:** Whether you have a modelling problem or a trust problem. A crew that stopped reading will not start because the list got cleverer, so the first release has to be shorter than the current one and visibly checked.
- **What it forecloses:** Closes the argument for volume permanently, and closes the question of what success looks like: not a better number, but a list somebody works to the bottom of.

### 6. Where must the call be made

**Asked:** At the moment the warning needs to go out, is the machine reachable? And if it is out of contact for a while, does waiting until it comes back still leave time to do anything?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** They are wired in and always reachable. The plant network is solid.
- **Which means:** Everything can happen centrally, which is cheaper, easier to change and easier to audit. Resist the pull towards putting arithmetic on the machine when nothing forces it.
- **Bounds:** Tier 2 — Distributed & Custom ML is the ceiling
- **For the brief:** Assets are always connected. Score centrally; no on-machine deployment.
- **Why it was asked:** Whether there is a hot path at all, and whose hardware it runs on. Everything below Tier 3 assumes the number can travel; when it cannot, the arithmetic happens at the machine and the cloud becomes a training and version-pushing system.
- **What it forecloses:** Closes the entire cloud-versus-machine debate in one answer, and with it every question about streaming, message brokers and endpoint latency — none of which matter if the link is not there when the answer is needed.

## 4. Still worth asking

**These are instructions, not blanks.** Ask each one. The possible answers below are authored, with what each would rule in or out, so a reply can be recognised rather than interpreted.

### 7. Do you know which machine a given part was fitted to, and when it moved?

**Ask:** Do you know which machine a given part was fitted to, and when it moved? Parts come out of a pool, and a swapped part carries its history with it onto the wrong machine.

What the answers would mean:

- **Every part carries a serial number and the fitting is logged against the machine.** → You can model at the level things actually break at rather than the level they are measured at. That is the difference between a fleet-wide average and something a reliability engineer will defend.
- **The big items are tracked. The small ones come out of a bin and nobody records it.** → Split the scope on the line the tracking already draws. Model the tracked items properly and treat the rest as machine-level context, rather than pretending the whole fleet has the same evidence.
- **Parts come out of a spare pool. Nobody tracks where any of them ends up.** → Everything is machine-level, and the age of a machine no longer means the age of the thing that breaks. Reset-on-repair assumptions become guesses, and any dated estimate inherits that. *(ceiling Tier 2 — Distributed & Custom ML)*
- **Probably in the system somewhere. I could not tell you how good it is.** → Test it rather than ask. Pick twenty machines that had the same part replaced twice and see whether the records tell a story that could physically have happened.

### 10. How many of these can the crew actually get to in a week?

**Ask:** How many of these can the crew actually get to in a week? Not how many they should — how many they do, on a normal week, with everything else they are already committed to.

What the answers would mean:

- **Six crews, four jobs a day. So about a hundred and twenty a week.** → That number is the operating point and it should appear in every later document. The measure is how many of the top hundred and twenty are real, and nothing else is worth reporting.
- **Nobody has counted. There is a backlog and it never gets shorter.** → The backlog is the answer nobody has written down. Count what actually got closed for four weeks and you will find the real cut-off is already being set by what the crew gets round to.
- **Whatever comes in, they deal with. We flex contractors.** → Then ranking is not the point and detection is. Rare, and worth checking against the closure records, because a team that never says no usually has a backlog they have stopped calling one. *(ceiling Tier 1 — Serverless, In-Warehouse)*
- **That varies a lot by region.** → Then it is several operating points, not one. Get the number per region and expect the list to be cut differently in each, which is a scheduling design decision, not a modelling one.

### 14. From the moment you say something, how long is it before the fix can actually happen?

**Ask:** From the moment you say something, how long is it before the fix can actually happen? Add up the part arriving, somebody travelling, and a slot being free.

What the answers would mean:

- **Parts run six weeks and slots book ten days out.** → The useful warning is long, so a weekly cycle is comfortably fast enough and anything faster is spending money on latency nobody can use. Warn too early, though, and the crew learns to ignore it. *(ceiling Tier 2 — Distributed & Custom ML)*
- **A few days. The part is usually in stock and we can move a crew.** → A daily cycle fits, and the interesting design question moves to how early is too early rather than how fast the pipeline runs.
- **The part is on the van. If we know this shift, we fix it this shift.** → Now the pipeline latency is inside the decision, so the measurements have to arrive and be scored within the shift. That is the first honest argument for streaming on this problem. *(floor Tier 2 — Distributed & Custom ML)*
- **It depends on the part. Some things we keep, some we do not.** → Then the window differs per failure mode, and one system serving all of them will be wrong at both ends. Get the lead time per mode and design for the modes that matter most.

## 5. Not worth asking yet

Each of these is gated behind a branch that is not open. They are listed so the absence is legible: they were not forgotten, they were ruled out.

- **What is actually in that file, and can you ask for something to be added to it?** — closed by *Who owns the historian* → “Same team. They run the control system and they run the cloud project”.
- **Is there money this year for new measurement on these machines?** — closed by *What the historian actually stored* → “There are short high-speed recordings, but only when something already tripped an alarm”.
- **Would the crew tick found-or-not on the job before they close it?** — closed by *Does the crew still act on alerts* → “They work every one. It is a small list and it is taken seriously”.
- **Who has to sign before new software runs on one of these?** — closed by *Where must the call be made* → “They are wired in and always reachable. The plant network is solid”.
- **Does whoever schedules the work need a running order, or an actual date with some idea of how confident you are?** — closed by *What counts as a failure* → “Only a full stop counts. If it kept running, nobody wrote it down”.

## 6. What is being suggested, and why the alternatives are out

### Tier 2 — Distributed & Custom ML

Stream the recordings, model time to failure

- **What it is:** Pub/Sub → Dataflow features → Iceberg managed tables; Cloud Scheduler → Managed Spark frequency work → time-to-event fit
- **Google Cloud & open-weight options at this rung:** Pub/Sub, Dataflow, Iceberg managed tables, Managed Service for Apache Spark, Cloud Scheduler
- **What it carries:** Place carried from Tier 1, still a table somebody reads later. The build moved out of SQL, because BigQuery carries no time-to-event model type.
- **Why here:** Dataflow lands windowed features in Iceberg managed tables through the Storage Write API — no small-file problem to solve. Spark gets energy at the defect tones; a time-to-event fit that handles unfinished lives returns a window, not a flag.
- **Where it breaks:** Most of the cost is digging labels out of old paperwork and handling unfinished lives, not modelling. The Dataflow job is a floor you pay whether or not anything is degrading, and you now own two runtimes plus the schema contract between them.
- **What would move it up:** Connection logs show assets dark for longer than the warning a fast mode gives you, so the call has to be made on the machine rather than in the cloud.

Peers at the same price, with a different shape:

- **One big machine instead of a cluster** — BigQuery window features → Agent Platform custom job → survival fit → scored table
- **Health index with no breakdown history** — Iceberg managed tables → Managed Spark features → normal-behaviour model → health index

#### Architecture Decision Record (ADR) Matrix

A scenario-aware evaluation of the ladder against this customer's constraints. Where an adjacent tier serves as a viable A/B benchmark or a Phase 2 evolution, that role is explicitly called out:

| Rung | Role in this Engagement | Architecture & Stance | Deciding Constraint & Trade-off |
| --- | --- | --- | --- |
| Tier 0 — Out of the Box | Ruled out (Insufficient) | Triage the alarms the machine already emits. | Below the floor (Tier 2 — Distributed & Custom ML), set by What the historian actually stored. |
| Tier 1 — Serverless, In-Warehouse | **Adjacent Lower Tier (A/B Benchmark)** | Rolled-up readings, ranked weekly work list. Lower complexity and operational overhead. | Below the floor (Tier 2 — Distributed & Custom ML), set by What the historian actually stored. Viable as an A/B comparator to quantify the performance/accuracy lift of Tier 2 — Distributed & Custom ML. |
| Tier 2 — Distributed & Custom ML | **Primary Baseline (MVP)** | Stream the recordings, model time to failure. Fits all bounded constraints. | Selected target. Fits floor (Tier 2 — Distributed & Custom ML) and ceiling (Tier 2 — Distributed & Custom ML). Wins: Dataflow lands windowed features in Iceberg managed tables through the Storage Write API — no small-file problem to solve. Spark gets energy at the defect tones; a time-to-event fit that handles unfinished lives returns a window, not a flag. |
| Tier 3 — Real-Time & Specialised | Ruled out (Theatre) | Arithmetic at the machine, training in the cloud. | Past the ceiling (Tier 2 — Distributed & Custom ML), set by Where must the call be made. Unjustified operational cost. |

**What a build at this rung is made of.** Storage stays where it is and a second engine arrives beside it, with an artefact you can name, a registry to hold it, and a graph to sequence the steps.

The menu at this rung, not this design. Each line says what that component is doing *here* -- several of them appear at other rungs doing something else.

- **Where the data sits still** — Whether one copy can serve every reader, or whether you have just signed up to keep two copies honest.
    - **BigQuery standard tables** — The offline store the feature code reads and writes.
    - **Apache Iceberg managed tables** — What the distributed engine reads directly, with no export step.
    - **Cloud Storage and object tables** — The raw zone the distributed engine parses before anything is a table.
    - **External tables and BigQuery Omni** — A source in another cloud the transform reads without a migration.
- **How the data gets there** — Whether anything genuinely has to stream, or whether the customer said real time and meant this morning.
    - **Datastream** — Keeps a large mirror current under a transform that runs beside it.
    - **Pub/Sub** — A pipeline drains the topic into windowed features the nightly build reads, with nothing scored on the stream.
    - **Managed Service for Apache Kafka** — Batch consumers read topics the business already publishes.
    - **Dataflow** — Batch movement, written once so the stream can reuse it.
- **Where the logic runs** — Whether the work fits in SQL. Nearly everything else about the build follows from that one answer.
    - **BigQuery DataFrames** — Feature code in Python without standing up a second engine.
    - **Managed Service for Apache Spark** — The transform, and training inside it where that is simpler.
    - **Dataflow** — Batch scoring over a large population, written once.
    - **Cloud Run** — A scoring job that starts, finishes and costs nothing in between.
    - **Agent Platform training** — Where the custom model is produced.
- **What makes it run in order** — Whether this is a timetable or a graph. A graph with a gate in it is a different product from a cron line.
    - **Dataform** — The warehouse half of a graph whose other half runs elsewhere.
    - **BigQuery pipelines** — The warehouse-side steps of a larger build.
    - **Managed Service for Apache Airflow** — The retrain graph and everything that has to happen in order around it.
    - **Agent Platform Pipelines** — Train, evaluate and register as one repeatable run.
    - **Cloud Scheduler, Workflows and Eventarc** — Glue between products where a full graph engine would be too much.
- **How the answer reaches whoever acts** — Who or what acts on the answer, and whether they can read the place you were going to put it.
    - **BigQuery sharing** — The same, once there is a version on the table to keep straight.
    - **A push into the operational system** — A write from the scoring job straight into the operational store.
    - **Agent Platform endpoints and batch inference** — Batch inference fans the artefact out over the population.
    - **A Cloud Run service** — A container that scores and stops.
    - **Feature Store online serving** — One definition, written once and read by the training set.
    - **Agent Retrieval** — The item vectors a training run wrote, indexed in batch so a shortlist is looked up rather than computed.
- **The database the business already runs on** — The read shape at the moment of decision. A key lookup, a real query and a nearest-match are three stores.
    - **Bigtable** — Where the offline job writes what the request path will later read.
    - **AlloyDB** — The operational store the batch job pushes into.
    - **Cloud SQL** — The operational side of a build whose analytics live elsewhere.

**Who operates it.** A real data engineering function. Managed Airflow environments run continuously, so this rung carries a floor cost even in a week when nothing happens.

**Below it, and why that is not enough.**

- Tier 0 — Out of the Box — Triage the alarms the machine already emits. Out: the floor is Tier 2 — Distributed & Custom ML — What the historian actually stored.
- Tier 1 — Serverless, In-Warehouse — Rolled-up readings, ranked weekly work list. Out: the floor is Tier 2 — Distributed & Custom ML — What the historian actually stored.

**Above it, and why that is theatre here.**

- Tier 3 — Real-Time & Specialised — Arithmetic at the machine, training in the cloud. Out: past the ceiling at Tier 2 — Distributed & Custom ML — Where must the call be made.

**Below the rung sit the calls no rung makes for you.** The tier does not settle these, and a design that has not stated them has not been made. Nothing on the page asks for them, so they travel unanswered.

- **What one row is** — One asset per week alive, one whole life from install to failure, or one window of readings. That settles whether this is time-to-event work — and separately, whether the row is the asset or the part fitted to it.
  Options: One asset per week alive · One life, install to failure · One window of readings per scoring run
- **What goes in beside the past** — Whether the fit sees the sensor channel readings alone, or load, speed, ambient and setpoint beside them. Without those a hot machine and a hot day look identical. What the work-order system knows is a third category, and mostly poison.
  Options: Readings alone · Readings plus operating context · Band energies at the defect tones
- **One fit, one each, or one per group** — Nine hundred assets can be nine hundred baselines, one fleet fit with make and working pattern as columns, or one fit per machine type. The dozens of failures you hold, not the asset count, is what decides how far it can be split.
  Options: One baseline per asset · One fit across the fleet · One per machine type
- **Which methods get a run** — A yes-or-no fit over weeks alive, a proper time-to-event fit, and an unsupervised deviation score. Which are even eligible turns on whether anyone wrote down what broke.
  Options: A yes-or-no fit over weeks alive · A time-to-event fit · A deviation score with no labels
- **How you would know** — Held back by asset and by date, scored once per failure rather than once per row, and counted correct only when the warning arrived early enough for somebody to have done something with it.
  Options: Split by asset and by date · Rewind from several dates across seasons · Score against the triage that runs today
- **What tuning is worth** — Three things compete for the same month: the labels dug out of ten years of work-order system text, the inputs, and the settings. On this problem the labels win, and it is not close.
  Options: Leave the defaults · Search the settings · Buy measurement instead
- **One winner, or several combined** — A running-badly score, a deviation score and a dated risk can stay three lists or become one order. Note that the weekly list already merges them by cost times risk in SQL, which is not the same thing as combining models.
  Options: Pick the one that wins at the cut · Blend the scores · Keep them apart, one per failure mode

**Dataset for the build.** Every workshop build runs on public or shipped tables:

- **Source:** Shipped generator + loader
- **Tables:** `.pdm_workshop.assets`, `.pdm_workshop.weekly_readings`, `.pdm_workshop.work_orders`
- **Grain & size:** One row per asset-week (asset_id, week_start, operating_hours, six sensor summaries, maker_alarm, failed_within_4w); 900 assets across 156 weeks (78,947 rows, 4.4 MB) plus 965 technician work orders.
- **Target / label:** Failure within the next four weeks (failed_within_4w = 1) for Tier 1; (duration_weeks, event_observed) for Tier 2.
- **Tier 1 / Tier 2 build:** Hard Tier 1 extracts fault modes from technician work_orders text with AI.GENERATE_TABLE and fits BOOSTED_TREE_CLASSIFIER on a time split against maker_alarm; Tier 2 fits a Weibull or Cox time-to-failure model (lifelines) over (duration_weeks, event_observed).
- **Caveat:** Scheduled four-year swaps cut off 45% of asset lives before failure, ch4_exhaust_temp_c freezes for six weeks on 8% of units, and technician notes mix real bearing faults with routine inspections.
- **Setup / verify:** `uv run python labs/data/predictive-maintenance/generate_and_load.py --project $GOOGLE_CLOUD_PROJECT`
- **Agent skills (`bigquery-data-science` & Data Agent Kit):** `uvx bigquery-data-science lookup AI.GENERATE_TABLE # BQDS: AI.KEY_DRIVERS, AI.FORECAST, AI.DETECT_ANOMALIES, ARIMA_PLUS_XREG, BOOSTED_TREE_CLASSIFIER | Data Agent Kit: bigquery-ai-ml, data-autocleaning, bigquery-bigframes, ml-best-practices, gcp-spark, gcp-dataflow`

**The ladder, for reference.** No site is needed to read the tiers above.

- **Tier 0 — Out of the Box** — A model somebody else trained already answers the question. Nothing to fit, nothing to provision, and the bill starts on the first query. The most senior move in the room is often to say so.
- **Tier 1 — Serverless, In-Warehouse** — Bring the model to the data. No cluster, no container, no serving stack. SQL is the interface.
- **Tier 2 — Distributed & Custom ML** — The transformation or the model outgrew SQL. Bring distributed compute to the data, keep the storage where it is.
- **Tier 3 — Real-Time & Specialised** — A hard SLA or a custom objective justifies owning the stack. You are now engineering a system, not training a model.
- **Tier 4 — Hardening for High-Stakes Operation** — Not a rung you buy. It is what changes about a system already at Tier 1, 2 or 3 once being wrong is expensive, contested or unsafe — and what changes is different for every problem in Discovery.

## 7. POC Data Discovery & Profiling Contract (Tier 2)

- **Source Tables (`bigquery-region: "US"`):** `.pdm_workshop.assets`, `.pdm_workshop.weekly_readings`, `.pdm_workshop.work_orders`
- **Grain & Target:** One row per asset-week (asset_id, week_start, operating_hours, six sensor summaries, maker_alarm, failed_within_4w); 900 assets across 156 weeks (78,947 rows, 4.4 MB) plus 965 technician work orders. | Failure within the next four weeks (failed_within_4w = 1) for Tier 1; (duration_weeks, event_observed) for Tier 2.
- **Data Caveat to Profile & Guard Against:** Scheduled four-year swaps cut off 45% of asset lives before failure, ch4_exhaust_temp_c freezes for six weeks on 8% of units, and technician notes mix real bearing faults with routine inspections.
- **Verification Command:** `uv run python labs/data/predictive-maintenance/generate_and_load.py --project $GOOGLE_CLOUD_PROJECT`

---

### The same thing, for a program to read

```json
{
  "problem": "predictive-maintenance",
  "ldap": "classroom-repo",
  "version": 1,
  "served_at": "2026-10-27T00:00:00Z",
  "binding": {
    "asset": "asset",
    "signal": "sensor channel",
    "failure": "failure",
    "crew": "crew",
    "job": "job",
    "finding": "finding",
    "archive": "historian",
    "worklog": "work-order system",
    "gateway": "gateway"
  },
  "range": {
    "floor": 2,
    "ceiling": 2,
    "clash": false
  },
  "recommended_rung": 2,
  "data": {
    "source": "Shipped generator + loader",
    "tables": [
      ".pdm_workshop.assets",
      ".pdm_workshop.weekly_readings",
      ".pdm_workshop.work_orders"
    ],
    "grain": "One row per asset-week (asset_id, week_start, operating_hours, six sensor summaries, maker_alarm, failed_within_4w); 900 assets across 156 weeks (78,947 rows, 4.4 MB) plus 965 technician work orders.",
    "label": "Failure within the next four weeks (failed_within_4w = 1) for Tier 1; (duration_weeks, event_observed) for Tier 2.",
    "rungs": "Hard Tier 1 extracts fault modes from technician work_orders text with AI.GENERATE_TABLE and fits BOOSTED_TREE_CLASSIFIER on a time split against maker_alarm; Tier 2 fits a Weibull or Cox time-to-failure model (lifelines) over (duration_weeks, event_observed).",
    "caveat": "Scheduled four-year swaps cut off 45% of asset lives before failure, ch4_exhaust_temp_c freezes for six weeks on 8% of units, and technician notes mix real bearing faults with routine inspections.",
    "setup": "uv run python labs/data/predictive-maintenance/generate_and_load.py --project $GOOGLE_CLOUD_PROJECT",
    "skills": "uvx bigquery-data-science lookup AI.GENERATE_TABLE # BQDS: AI.KEY_DRIVERS, AI.FORECAST, AI.DETECT_ANOMALIES, ARIMA_PLUS_XREG, BOOSTED_TREE_CLASSIFIER | Data Agent Kit: bigquery-ai-ml, data-autocleaning, bigquery-bigframes, ml-best-practices, gcp-spark, gcp-dataflow"
  },
  "questions": [
    {
      "id": "failure",
      "order": 1,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "stop",
        "heard": "Only a full stop counts. If it kept running, nobody wrote it down.",
        "means": "The strictest definition and the rarest. Expect tens of events across a decade, not thousands, so the model is fitted on events rather than rows — say that out loud before anyone quotes an accuracy number.",
        "floor": null,
        "ceiling": null
      }
    },
    {
      "id": "onset",
      "order": 2,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "part",
        "heard": "The record is really a parts issue. It says which part went out and to what.",
        "means": "Better than free text and worse than it looks. Parts records carry good dates and no fault description, and if parts move between machines the history follows the wrong one.",
        "floor": null,
        "ceiling": null
      }
    },
    {
      "id": "fidelity",
      "order": 3,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "snapshot",
        "heard": "There are short high-speed recordings, but only when something already tripped an alarm.",
        "means": "Good signal and a trap. A recording triggered by an existing alarm means the alarm is inside the feature, so the model learns the alarm rather than the fault and looks superb until it is live.",
        "floor": 2,
        "ceiling": null
      }
    },
    {
      "id": "owner",
      "order": 4,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "same",
        "heard": "Same team. They run the control system and they run the cloud project.",
        "means": "The best case and the rarest. Sampling rates, new points and the pipeline are all one backlog, so the design can genuinely reach down to the machine instead of stopping at the file.",
        "floor": null,
        "ceiling": null
      }
    },
    {
      "id": "belief",
      "order": 5,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "work",
        "heard": "They work every one. It is a small list and it is taken seriously.",
        "means": "The healthiest starting point on this problem. You are adding order to something that already functions, so the only real risk is making the list longer than the crew can absorb.",
        "floor": null,
        "ceiling": null
      }
    },
    {
      "id": "where",
      "order": 6,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "cloud",
        "heard": "They are wired in and always reachable. The plant network is solid.",
        "means": "Everything can happen centrally, which is cheaper, easier to change and easier to audit. Resist the pull towards putting arithmetic on the machine when nothing forces it.",
        "floor": null,
        "ceiling": 2
      }
    },
    {
      "id": "entity",
      "order": 7,
      "status": "open",
      "options": [
        "Every part carries a serial number and the fitting is logged against the machine.",
        "The big items are tracked. The small ones come out of a bin and nobody records it.",
        "Parts come out of a spare pool. Nobody tracks where any of them ends up.",
        "Probably in the system somewhere. I could not tell you how good it is."
      ]
    },
    {
      "id": "export",
      "order": 8,
      "status": "not_in_play",
      "gate": "The historian team will only hand over an export",
      "closed_by": {
        "question": "owner",
        "answer": "same"
      }
    },
    {
      "id": "capital",
      "order": 9,
      "status": "not_in_play",
      "gate": "The signal that matters was averaged away before it was kept",
      "closed_by": {
        "question": "fidelity",
        "answer": "snapshot"
      }
    },
    {
      "id": "capacity",
      "order": 10,
      "status": "open",
      "options": [
        "Six crews, four jobs a day. So about a hundred and twenty a week.",
        "Nobody has counted. There is a backlog and it never gets shorter.",
        "Whatever comes in, they deal with. We flex contractors.",
        "That varies a lot by region."
      ]
    },
    {
      "id": "dispo",
      "order": 11,
      "status": "not_in_play",
      "gate": "Nobody wrote down whether past alerts were real",
      "closed_by": {
        "question": "belief",
        "answer": "work"
      }
    },
    {
      "id": "signoff",
      "order": 12,
      "status": "not_in_play",
      "gate": "A software change on the asset needs a signature",
      "closed_by": {
        "question": "where",
        "answer": "cloud"
      }
    },
    {
      "id": "output",
      "order": 13,
      "status": "not_in_play",
      "gate": "A schedule downstream reads the output",
      "closed_by": {
        "question": "failure",
        "answer": "stop"
      }
    },
    {
      "id": "window",
      "order": 14,
      "status": "open",
      "options": [
        "Parts run six weeks and slots book ten days out.",
        "A few days. The part is usually in stock and we can move a crew.",
        "The part is on the van. If we know this shift, we fix it this shift.",
        "It depends on the part. Some things we keep, some we do not."
      ]
    }
  ],
  "conflicts": [],
  "still_to_ask": [
    "entity",
    "capacity",
    "window"
  ],
  "counts": {
    "answered": 6,
    "stale": 0,
    "open": 3,
    "not_in_play": 5,
    "dropped": 0
  },
  "schema_version": "1.0",
  "problem_id": "predictive-maintenance",
  "target_tier": 2,
  "derivation": {
    "floor": 2,
    "ceiling": 2,
    "recommended_tier": 2,
    "recommended_rung": 2,
    "clash": false
  }
}
```
