---
schema_version: "1.0"
problem_id: "churn"
target_tier: 1
recommended_rung: 1
source: "built-in-classroom-pack"
---

# Discovery pack — Customer Churn & Retention

`churn` · recorded by **classroom-repo** · version 1 · served 2026-10-27T00:00:00Z

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

> **VP Customer Success, 800-person B2B SaaS, 3,100 accounts** — Net revenue retention slipped from 112 to 97 and the board wants a number by the next meeting. We want a churn model that tells each CSM who to call.
>
> **Director of CRM Analytics, postpaid mobile operator, 18M subscribers** — We already have a churn model at 0.91 AUC. Retention spend is up 30% year on year and churn is flat. Marketing wants a better model.
>
> **Head of Contact Centre Operations, motor insurer** — When someone rings to cancel we get about ninety seconds. I want the agent to see the risk score and the right offer on screen before they say hello.

**Vocabulary is unbound.** The nouns below are the method's neutral words, not this customer's — treat them as placeholders and confirm the real terms early.

**The five specifics.**

- **How many, of the thing being predicted** — *not captured. Ask.*
- **How much history there is, and how much arrives** — *not captured. Ask.*
- **The deadline the run has to hit** — *not captured. Ask.*
- **What being wrong costs, per event or per year** — *not captured. Ask.*
- **Who owns the decision, and who would run this** — *not captured. Ask.*

## 2. Where discovery landed

- **Floor: Tier 1 — Serverless, In-Warehouse** — set by Is there a cancellation date, or is it a guess, Does the money leave with the customer, How much of the loss is failed payments, What actually leaves, Does the system keep dated history, How many customers the team can reach in a week, Who may give money away, Was anyone ever left alone on purpose
- **Ceiling:** nothing heard yet rules out the top of the ladder

## 3. What was asked, and what it steered

### 1. Is there a cancellation date, or is it a guess

**Asked:** When somebody leaves, is there a record of it happening on a particular day — or do you work it out from them going quiet?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** There is a cancellation record with a date on it.
- **Which means:** The comfortable case, and it means the rest of the discovery is about timing rather than definition. Still ask about notice periods: somebody who gave notice a fortnight ago is not a prediction.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Departure is an observed event. Confirm notice periods and reactivation windows.
- **Why it was asked:** Whether the label exists or has to be invented. An invented one carries an arbitrary threshold that no amount of modelling recovers from, and it is the largest single assumption most of these projects make.
- **What it forecloses:** Closes the label definition, the timing question and the whole model family. It also decides whether the honest answer is a churn model or a latent-activity model.

### 2. Does the money leave with the customer

**Asked:** When revenue drops, is it mostly people leaving altogether, or people staying and paying you less?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** People leave. When they go, they go completely.
- **Which means:** Then the ordinary framing holds and the label is the cancellation. Check it against the revenue line anyway, because a matching pair of numbers is the cheapest credibility available in the first meeting.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Loss is dominated by full departures. Check it against the revenue line.
- **Why it was asked:** Whether “churn” is even the right target. A programme aimed at cancellations cannot move a number that is falling because of downgrades, and the two need different signals and different offers.
- **What it forecloses:** Closes the target-variable argument and usually the label-scarcity one with it, because counting reductions as events multiplies a thin label set several times over.

### 3. How much of the loss is failed payments

**Asked:** Of everyone who left last quarter, how many actually chose to — as opposed to a card expiring or a direct debit failing?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** We split those out already. Billing owns them.
- **Which means:** Rare and a good sign. Ask for the share anyway and put it on the weekly board, because a payment gateway change looks exactly like the model decaying and will be blamed on the model.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Payment failures already separated. Keep the share on the weekly board.
- **Why it was asked:** How much of the problem is a data science problem at all. Payment failure is fixed by retries, a card updater and a dunning sequence, and none of that needs a model or a discount.
- **What it forecloses:** Closes the label-purity question, a good part of the scoping, and the “churn is up and nothing is alarming” investigation before it happens.

### 4. What actually leaves

**Asked:** What is the thing that leaves — the whole account, one line on it, or one person inside a company that stays?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** The account. Usage and billing are both at that level.
- **Which means:** The easy case and it is worth confirming rather than assuming. When the two levels match, most of the feature engineering is a group-by and the project is genuinely as simple as it looks.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Departure and usage share a level. Aggregation is a group-by.
- **Why it was asked:** The row you train on, the identity you have to resolve, and whether the usage you can see is even at the same level as the thing you are predicting.
- **What it forecloses:** Closes the aggregation question, the identity-resolution question, and the “one model or two” argument that otherwise resurfaces at build time.

### 5. Does the system keep dated history

**Asked:** Can you tell what a customer’s record looked like on a given day last March, or does the system only hold what is true now?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** We keep dated snapshots. We can rebuild any day.
- **Which means:** The strong answer, and it means features can be rebuilt as they were on the scoring date. Check the snapshots actually go back far enough for the lookback you want, which is a different question.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Point-in-time history available. Rebuild features as-of; check the depth.
- **Why it was asked:** Whether an honest test against the past is possible at all, and therefore Tier 1 against Tier 2. Nothing sells you history you did not keep, so this answer sets the calendar for the whole engagement.
- **What it forecloses:** Closes the leakage argument, the validation-design argument, and most of the debate about how long before there is a number worth showing anybody.

### 6. How many customers the team can reach in a week

**Asked:** How many customers can the people who act on this list actually get to in a week?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** A dialler and an outbound team. Thousands a week.
- **Which means:** Then ranking genuinely pays and the list is worth optimising. It also means treated volume is high enough that a randomly held-back group costs little and settles quickly.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Capacity supports ranking and a randomised holdback at low cost.
- **Why it was asked:** The operating point, and therefore the metric. Everything is judged in the top slice of the list; how the model orders the rest of the base is a number nobody will ever act on.
- **What it forecloses:** Closes the threshold debate, the metric debate, and most arguments about whether a better model is worth funding.

### 7. Who may give money away

**Asked:** Who is allowed to give a customer something to keep them, and how much, before somebody else has to approve it?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** There is a standard offer. Everyone gets the same one.
- **Which means:** Simplest to build and it makes measurement clean, because one treatment means one effect to estimate. Ask what it costs, since a fixed retention offer given to the wrong half of the list is the most expensive kind of waste.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Single fixed offer. One treatment; cost sits in who receives it.
- **Why it was asked:** What the system may actually recommend. A recommendation above the authority line gets overridden by hand every time, and the programme gets blamed on the model rather than the ceiling.
- **What it forecloses:** Closes the offer-design question, the override-logging question, and a good part of the Tier 3 conversation about what belongs in the request path.

### 8. Was anyone ever left alone on purpose

**Asked:** Has any past campaign ever held the offer back from a randomly chosen group, so you could see what happened to them?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Yes, a couple of campaigns kept a control group back.
- **Which means:** Then the effect is estimable and the project can rank on it. Check how the group was chosen: a control picked by excluding the hard cases is not a control, and that is the usual way this answer turns out to be optimistic.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Historical randomisation exists. Verify the control was genuinely random.
- **Why it was asked:** Whether the effect of the offer can be estimated at all, and therefore whether Tier 2 is a build or a research project. It is the single most load-bearing answer on this problem.
- **What it forecloses:** Closes the risk-against-uplift question, the Tier 1 against Tier 2 question, and the awkward one about what the lift number in the board pack has been measuring.

## 4. Still worth asking

*Every question in play has been answered.*

## 5. Not worth asking yet

Each of these is gated behind a branch that is not open. They are listed so the absence is legible: they were not forgotten, they were ruled out.

- **How long does somebody have to go quiet before you would say they have gone?** — closed by *Is there a cancellation date, or is it a guess* → “There is a cancellation record with a date on it”.
- **When a card is declined, what happens next — and how many times?** — closed by *How much of the loss is failed payments* → “We split those out already. Billing owns them”.
- **If the busiest person on an account stopped logging in but everything else carried on, would anybody notice?** — closed by *What actually leaves* → “The account. Usage and billing are both at that level”.
- **Has the group you would train on already been called or emailed by previous retention campaigns?** — closed by *Was anyone ever left alone on purpose* → “Yes, a couple of campaigns kept a control group back”.
- **Is there any sign that people you contacted left more often than similar people you left alone?** — closed by *How many customers the team can reach in a week* → “A dialler and an outbound team. Thousands a week”.
- **Do people leave steadily through the year, or does it cluster around renewal and price-change dates?** — closed by *Does the money leave with the customer* → “People leave. When they go, they go completely”.
- **For the people most at risk, do email and phone still reach them — or have they stopped opening anything you send?** — closed by *How many customers the team can reach in a week* → “A dialler and an outbound team. Thousands a week”.
- **When you hand a list of customers to an ad platform, who turns your records into their users?** — needs “Retention spend leaves the building for an ad platform”, which nothing answered has opened.
- **When an offer needs approving, how long does that take, and does the customer wait on the line for it?** — closed by *Who may give money away* → “There is a standard offer. Everyone gets the same one”.
- **When somebody is flagged, what does the retention rep see next to the name — and could they act on it?** — closed by *Does the system keep dated history* → “We keep dated snapshots. We can rebuild any day”.

## 6. What is being suggested, and why the alternatives are out

### Tier 1 — Serverless, In-Warehouse

A weekly list, ranked by what it is worth

- **What it is:** BigQuery aggregates → BQML boosted tree → scheduled query → work queue with ML.EXPLAIN_PREDICT reasons
- **Google Cloud & open-weight options at this rung:** BigQuery, BigQuery ML, AI.PREDICT, ML.EXPLAIN_PREDICT, AI.CLASSIFY, Scheduled queries, Dataform, BigQuery pipelines
- **What it carries:** Build unchanged from Tier 0, still SQL in BigQuery. What changes is that a trained model now scores rows instead of counting them.
- **Why here:** Volumes are modest and SQL is their language. Rank by risk times account value, cut at weekly capacity, and a score becomes a work queue. ML.EXPLAIN_PREDICT gives per-row drivers a retention rep can act on. AI.CLASSIFY sorts call transcripts into reasons.
- **Where it breaks:** Risk, not persuadability: the top slice is often the least saveable. It assumes the source kept dated history — if it overwrites in place, every test on the past flatters you. Drivers rank tenure and size top, which no retention rep can act on.
- **What would move it up:** A past campaign held a random group back, so the effect is estimable — or the source overwrites in place and features have to be rebuilt from a change log.

Peers at the same price, with a different shape:

- **Reach them where email no longer does** — Scored audience in BigQuery → Data Manager API ingest → Customer Match, suppressed on renewal

#### Architecture Decision Record (ADR) Matrix

A scenario-aware evaluation of the ladder against this customer's constraints. Where an adjacent tier serves as a viable A/B benchmark or a Phase 2 evolution, that role is explicitly called out:

| Rung | Role in this Engagement | Architecture & Stance | Deciding Constraint & Trade-off |
| --- | --- | --- | --- |
| Tier 0 — Out of the Box | **Adjacent Lower Tier (A/B Benchmark)** | Measure it properly before modelling it. Lower complexity and operational overhead. | Below the floor (Tier 1 — Serverless, In-Warehouse), set by Is there a cancellation date, or is it a guess, Does the money leave with the customer, How much of the loss is failed payments, What actually leaves, Does the system keep dated history, How many customers the team can reach in a week, Who may give money away, Was anyone ever left alone on purpose. Viable as an A/B comparator to quantify the performance/accuracy lift of Tier 1 — Serverless, In-Warehouse. |
| Tier 1 — Serverless, In-Warehouse | **Primary Baseline (MVP)** | A weekly list, ranked by what it is worth. Fits all bounded constraints. | Selected target. Fits floor (Tier 1 — Serverless, In-Warehouse). Wins: Volumes are modest and SQL is their language. Rank by risk times account value, cut at weekly capacity, and a score becomes a work queue. ML.EXPLAIN_PREDICT gives per-row drivers a retention rep can act on. AI.CLASSIFY sorts call transcripts into reasons. |
| Tier 2 — Distributed & Custom ML | **Adjacent Higher Tier (Phase 2 Evolution)** | Replay the past, rank on the change you cause. Higher freshness, lower latency, or specialised modeling. | Inside the range, but nothing heard requires it yet. Step-up trigger: A past campaign held a random group back, so the effect is estimable — or the source overwrites in place and features have to be rebuilt from a change log. Propose as Phase 2 expansion once this condition is met. |
| Tier 3 — Real-Time & Specialised | In range, not required | The offer is on screen before they say hello. | Not ruled out, but nothing heard in the room requires it. |

**What a build at this rung is made of.** One place to store it and one engine to work it. The data is in the warehouse, the model is SQL, and the schedule is a line in a timetable.

The menu at this rung, not this design. Each line says what that component is doing *here* -- several of them appear at other rungs doing something else.

- **Where the data sits still** — Whether one copy can serve every reader, or whether you have just signed up to keep two copies honest.
    - **BigQuery standard tables** — The table the model trains on, and the scored table it writes.
    - **Apache Iceberg managed tables** — The landing table when a second engine also reads it.
    - **Cloud Storage and object tables** — SQL reaches unstructured files through a table of pointers.
    - **External tables and BigQuery Omni** — Query it in place to find out whether it is worth landing.
- **How the data gets there** — Whether anything genuinely has to stream, or whether the customer said real time and meant this morning.
    - **Data Transfer Service** — The landing job for a source somebody else already publishes.
    - **Datastream** — Change capture into the warehouse on a rung where nothing streams.
    - **Pub/Sub** — A subscription lands messages in a table with no pipeline to run.
- **Where the logic runs** — Whether the work fits in SQL. Nearly everything else about the build follows from that one answer.
    - **BigQuery SQL and BigQuery ML** — The whole build: the transform, the model and the scoring.
    - **BigQuery DataFrames** — A notebook step inside an otherwise SQL build.
- **What makes it run in order** — Whether this is a timetable or a graph. A graph with a gate in it is a different product from a cron line.
    - **Scheduled queries** — The whole schedule, while the build is still one statement.
    - **Dataform** — The default sequencer at this rung.
    - **BigQuery pipelines** — A scheduled run that is not purely SQL.
    - **Cloud Scheduler, Workflows and Eventarc** — A trigger for a job that has no graph around it.
- **How the answer reaches whoever acts** — Who or what acts on the answer, and whether they can read the place you were going to put it.
    - **A scored table plus Looker** — The scored table, read by whoever acts on it.
    - **BigQuery sharing** — How the scored table reaches a team that is not yours.
    - **A push into the operational system** — A scheduled export into the system that acts.
- **The database the business already runs on** — The read shape at the moment of decision. A key lookup, a real query and a nearest-match are three stores.
    - **Cloud SQL** — Where a scheduled push puts the answer.

**Who operates it.** The team that already writes the SQL. Nothing new to run, and the failure they actually fear is the job silently not running at all.

**Below it, and why that is not enough.**

- Tier 0 — Out of the Box — Measure it properly before modelling it. Out: the floor is Tier 1 — Serverless, In-Warehouse — Is there a cancellation date, or is it a guess, Does the money leave with the customer, How much of the loss is failed payments, What actually leaves, Does the system keep dated history, How many customers the team can reach in a week, Who may give money away, Was anyone ever left alone on purpose.

**Above it, and why that is theatre here.**

- Tier 2 — Distributed & Custom ML — Replay the past, rank on the change you cause. Out: not ruled out, but nothing heard in the room requires it.
- Tier 3 — Real-Time & Specialised — The offer is on screen before they say hello. Out: not ruled out, but nothing heard in the room requires it.

**Below the rung sit the calls no rung makes for you.** The tier does not settle these, and a design that has not stated them has not been made. Nothing on the page asks for them, so they travel unanswered.

- **What one row is** — One account on one date, labelled leaving inside sixty days — or one row per account per month, which is what anything time-shaped needs and what turns 18M rows into 430M.
  Options: One row per account, rebuilt weekly · One row per account per month · One row per line
- **What goes in beside the past** — Which columns are true on the scoring date, and which only appear afterwards. A cancelled direct debit, a closed ticket and “retention offer issued” all land after the decision and all three predict beautifully.
  Options: What the account does · Plus what happened around it · Plus the calendar you control
- **One fit, one each, or one per group** — One fit across 18M accounts, or one per segment — market, product line, tenure band. The rung does not settle it: the pooled fit and the per-segment fan-out both sit on Tier 2.
  Options: One fit, segment as a column · One fit per segment · A separate fit for early life
- **Which methods get a run** — A fixed sixty-day yes-or-no is the reflex. How long until it happens is live here, how much the offer changes it answers a different question, and with no cancel button neither fits — that is a latent-activity model.
  Options: A sixty-day classifier, tree or readable · A curve per account · A caused-change fit
- **How you would know** — Split by time, never at random: a random split shares the same accounts and the same calendar across both halves. And the untreated group is not a validation split — it is customers you knowingly let go.
  Options: A time-split test on the past · A live untreated group · Forward-only measurement
- **What tuning is worth** — The largest knob here is the label, and it is not a setting. Sixty days against ninety, and whether a return inside 90 days retracts the departure — each moves the reported rate more than any search will.
  Options: Defaults, and settle the label instead · A small search once the label holds · Tune the allocator, not the model
- **One winner, or several combined** — Averaging the tree and the readable model is one question; the caused-change fit already combines two response models, treated and untreated, differenced. Risk times account value times lift is neither — that is composition.
  Options: Keep the single winner · Average them · One fit instead of two, for the lift
- **Making the numbers agree** — Retention slipped from 112 to 97, and three separately produced numbers sit under it: full departures, contraction, and failed payments. The board is handed one percentage, and nobody can say which part moved.
  Options: Add the operational counts up · Take the definition finance already uses · Two definitions, scoped separately

**Dataset for the build.** Every workshop build runs on public or shipped tables:

- **Source:** BigQuery public tables
- **Tables:** `firebase-public-project.analytics_153293282.events_*`
- **Grain & size:** One row per mobile game event (user_pseudo_id, event_date, event_timestamp, event_name, nested event_params, user_properties); 5.7M events across 15,175 players from 2018-06-12 to 2018-10-03.
- **Target / label:** Zero active events in the 14 days after a fixed observation cut-off date among players active in the prior 14 days.
- **Tier 1 / Tier 2 build:** Hard Tier 1 builds a point-in-time player feature spine in SQL at the cut-off date and compares a TabFM AI.PREDICT slice against BOOSTED_TREE_CLASSIFIER ranked by retained value; Tier 2 fits a player tenure model (lifelines) from first session to last active day.
- **Caveat:** Aggregating events_* without a strict _TABLE_SUFFIX cut-off leaks post-cutoff activity into the features and inflates validation scores.
- **Setup / verify:** `bq query --use_legacy_sql=false "SELECT MIN(event_date), MAX(event_date), COUNT(DISTINCT user_pseudo_id) FROM `firebase-public-project.analytics_153293282.events_*`"`
- **Agent skills (`bigquery-data-science` & Data Agent Kit):** `uvx bigquery-data-science lookup AI.PREDICT # BQDS: BOOSTED_TREE_CLASSIFIER, LOGISTIC_REG, CONTRIBUTION_ANALYSIS, TRANSFORM, ML.EXPLAIN_PREDICT | Data Agent Kit: bigquery-ai-ml, dataform-bigquery, bigquery-bigframes, ml-best-practices, gcp-pipeline-orchestration`

**The ladder, for reference.** No site is needed to read the tiers above.

- **Tier 0 — Out of the Box** — A model somebody else trained already answers the question. Nothing to fit, nothing to provision, and the bill starts on the first query. The most senior move in the room is often to say so.
- **Tier 1 — Serverless, In-Warehouse** — Bring the model to the data. No cluster, no container, no serving stack. SQL is the interface.
- **Tier 2 — Distributed & Custom ML** — The transformation or the model outgrew SQL. Bring distributed compute to the data, keep the storage where it is.
- **Tier 3 — Real-Time & Specialised** — A hard SLA or a custom objective justifies owning the stack. You are now engineering a system, not training a model.
- **Tier 4 — Hardening for High-Stakes Operation** — Not a rung you buy. It is what changes about a system already at Tier 1, 2 or 3 once being wrong is expensive, contested or unsafe — and what changes is different for every problem in Discovery.

## 7. POC Data Discovery & Profiling Contract (Tier 1)

- **Source Tables (`bigquery-region: "US"`):** `firebase-public-project.analytics_153293282.events_*`
- **Grain & Target:** One row per mobile game event (user_pseudo_id, event_date, event_timestamp, event_name, nested event_params, user_properties); 5.7M events across 15,175 players from 2018-06-12 to 2018-10-03. | Zero active events in the 14 days after a fixed observation cut-off date among players active in the prior 14 days.
- **Data Caveat to Profile & Guard Against:** Aggregating events_* without a strict _TABLE_SUFFIX cut-off leaks post-cutoff activity into the features and inflates validation scores.
- **Verification Command:** `bq query --use_legacy_sql=false "SELECT MIN(event_date), MAX(event_date), COUNT(DISTINCT user_pseudo_id) FROM `firebase-public-project.analytics_153293282.events_*`"`

---

### The same thing, for a program to read

```json
{
  "problem": "churn",
  "ldap": "classroom-repo",
  "version": 1,
  "served_at": "2026-10-27T00:00:00Z",
  "binding": {
    "account": "account",
    "component": "line",
    "departure": "departure",
    "rep": "retention rep",
    "concession": "retention offer",
    "worth": "account value",
    "control": "untreated group",
    "worklist": "work queue"
  },
  "range": {
    "floor": 1,
    "ceiling": 1,
    "clash": false
  },
  "recommended_rung": 1,
  "data": {
    "source": "BigQuery public tables",
    "tables": [
      "firebase-public-project.analytics_153293282.events_*"
    ],
    "grain": "One row per mobile game event (user_pseudo_id, event_date, event_timestamp, event_name, nested event_params, user_properties); 5.7M events across 15,175 players from 2018-06-12 to 2018-10-03.",
    "label": "Zero active events in the 14 days after a fixed observation cut-off date among players active in the prior 14 days.",
    "rungs": "Hard Tier 1 builds a point-in-time player feature spine in SQL at the cut-off date and compares a TabFM AI.PREDICT slice against BOOSTED_TREE_CLASSIFIER ranked by retained value; Tier 2 fits a player tenure model (lifelines) from first session to last active day.",
    "caveat": "Aggregating events_* without a strict _TABLE_SUFFIX cut-off leaks post-cutoff activity into the features and inflates validation scores.",
    "setup": "bq query --use_legacy_sql=false \"SELECT MIN(event_date), MAX(event_date), COUNT(DISTINCT user_pseudo_id) FROM `firebase-public-project.analytics_153293282.events_*`\"",
    "skills": "uvx bigquery-data-science lookup AI.PREDICT # BQDS: BOOSTED_TREE_CLASSIFIER, LOGISTIC_REG, CONTRIBUTION_ANALYSIS, TRANSFORM, ML.EXPLAIN_PREDICT | Data Agent Kit: bigquery-ai-ml, dataform-bigquery, bigquery-bigframes, ml-best-practices, gcp-pipeline-orchestration"
  },
  "questions": [
    {
      "id": "leaving",
      "order": 1,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "event",
        "heard": "There is a cancellation record with a date on it.",
        "means": "The comfortable case, and it means the rest of the discovery is about timing rather than definition. Still ask about notice periods: somebody who gave notice a fortnight ago is not a prediction.",
        "floor": 1,
        "ceiling": null
      }
    },
    {
      "id": "shrink",
      "order": 2,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "leaving",
        "heard": "People leave. When they go, they go completely.",
        "means": "Then the ordinary framing holds and the label is the cancellation. Check it against the revenue line anyway, because a matching pair of numbers is the cheapest credibility available in the first meeting.",
        "floor": 1,
        "ceiling": null
      }
    },
    {
      "id": "involuntary",
      "order": 3,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "separated",
        "heard": "We split those out already. Billing owns them.",
        "means": "Rare and a good sign. Ask for the share anyway and put it on the weekly board, because a payment gateway change looks exactly like the model decaying and will be blamed on the model.",
        "floor": 1,
        "ceiling": null
      }
    },
    {
      "id": "unit",
      "order": 4,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "same",
        "heard": "The account. Usage and billing are both at that level.",
        "means": "The easy case and it is worth confirming rather than assuming. When the two levels match, most of the feature engineering is a group-by and the project is genuinely as simple as it looks.",
        "floor": 1,
        "ceiling": null
      }
    },
    {
      "id": "history",
      "order": 5,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "versioned",
        "heard": "We keep dated snapshots. We can rebuild any day.",
        "means": "The strong answer, and it means features can be rebuilt as they were on the scoring date. Check the snapshots actually go back far enough for the lookback you want, which is a different question.",
        "floor": 1,
        "ceiling": null
      }
    },
    {
      "id": "contacts",
      "order": 6,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "thousands",
        "heard": "A dialler and an outbound team. Thousands a week.",
        "means": "Then ranking genuinely pays and the list is worth optimising. It also means treated volume is high enough that a randomly held-back group costs little and settles quickly.",
        "floor": 1,
        "ceiling": null
      }
    },
    {
      "id": "authority",
      "order": 7,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "fixed",
        "heard": "There is a standard offer. Everyone gets the same one.",
        "means": "Simplest to build and it makes measurement clean, because one treatment means one effect to estimate. Ask what it costs, since a fixed retention offer given to the wrong half of the list is the most expensive kind of waste.",
        "floor": 1,
        "ceiling": null
      }
    },
    {
      "id": "randomised",
      "order": 8,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "yes",
        "heard": "Yes, a couple of campaigns kept a control group back.",
        "means": "Then the effect is estimable and the project can rank on it. Check how the group was chosen: a control picked by excluding the hard cases is not a control, and that is the usual way this answer turns out to be optimistic.",
        "floor": 1,
        "ceiling": null
      }
    },
    {
      "id": "lapse",
      "order": 9,
      "status": "not_in_play",
      "gate": "Leaving is inferred from silence rather than observed",
      "closed_by": {
        "question": "leaving",
        "answer": "event"
      }
    },
    {
      "id": "dunning",
      "order": 10,
      "status": "not_in_play",
      "gate": "A large share of the loss is payment failure, not intent",
      "closed_by": {
        "question": "involuntary",
        "answer": "separated"
      }
    },
    {
      "id": "rollup",
      "order": 11,
      "status": "not_in_play",
      "gate": "Usage is measured below the level that leaves",
      "closed_by": {
        "question": "unit",
        "answer": "same"
      }
    },
    {
      "id": "treated",
      "order": 12,
      "status": "not_in_play",
      "gate": "The people in the training data have already been targeted",
      "closed_by": {
        "question": "randomised",
        "answer": "yes"
      }
    },
    {
      "id": "reminder",
      "order": 13,
      "status": "not_in_play",
      "gate": "Contacting people might remind them to leave",
      "closed_by": {
        "question": "contacts",
        "answer": "thousands"
      }
    },
    {
      "id": "spiky",
      "order": 14,
      "status": "not_in_play",
      "gate": "Money leaves while the customer stays",
      "closed_by": {
        "question": "shrink",
        "answer": "leaving"
      }
    },
    {
      "id": "channels",
      "order": 15,
      "status": "not_in_play",
      "gate": "Contacting people might remind them to leave",
      "closed_by": {
        "question": "contacts",
        "answer": "thousands"
      }
    },
    {
      "id": "matching",
      "order": 16,
      "status": "not_in_play",
      "gate": "Retention spend leaves the building for an ad platform",
      "closed_by": null
    },
    {
      "id": "exception",
      "order": 17,
      "status": "not_in_play",
      "gate": "Some offers need somebody else to approve them",
      "closed_by": {
        "question": "authority",
        "answer": "fixed"
      }
    },
    {
      "id": "reasons",
      "order": 18,
      "status": "not_in_play",
      "gate": "The past cannot be reconstructed from the system of record",
      "closed_by": {
        "question": "history",
        "answer": "versioned"
      }
    }
  ],
  "conflicts": [],
  "still_to_ask": [],
  "counts": {
    "answered": 8,
    "stale": 0,
    "open": 0,
    "not_in_play": 10,
    "dropped": 0
  },
  "schema_version": "1.0",
  "problem_id": "churn",
  "target_tier": 1,
  "derivation": {
    "floor": 1,
    "ceiling": 1,
    "recommended_tier": 1,
    "recommended_rung": 1,
    "clash": false
  }
}
```
