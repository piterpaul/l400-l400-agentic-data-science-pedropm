---
schema_version: "1.0"
problem_id: "churn"
target_tier: 3
recommended_rung: 3
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

- **Floor: Tier 2 — Distributed & Custom ML** — set by Does the system keep dated history, Do people leave steadily through the year, or does it cluster around renewal and price-change dates?, When an offer needs approving, how long does that take, and does the customer wait on the line for it?, Neither the past state nor the past experiment exists, and no rung recovers either
- **Ceiling:** nothing heard yet rules out the top of the ladder

> **Together, not apart.** Neither the past state nor the past experiment exists, and no rung recovers either. The first deliverable is change capture plus an experiment design; the first defensible number is quarters away. Say that in the first meeting, or somebody will believe a number nobody can trace.

> **Together, not apart.** A third of the loss is a payment problem and nothing about the spend has ever been measured. Retry logic and a card updater will beat any model funded this year, and they belong to billing. Fix that first; it buys the credibility to ask for the experiment.

## 3. What was asked, and what it steered

### 1. Is there a cancellation date, or is it a guess

**Asked:** When somebody leaves, is there a record of it happening on a particular day — or do you work it out from them going quiet?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** They just stop using it. There is no cancel button.
- **Which means:** Then churn does not exist here, only quiet, and any cut-off you pick invents the label. Say so early: it moves the work from prediction to estimating whether somebody is dormant or gone, which is a different family entirely.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Non-contractual. Churn must be inferred; the threshold is the main assumption.
- **Why it was asked:** Whether the label exists or has to be invented. An invented one carries an arbitrary threshold that no amount of modelling recovers from, and it is the largest single assumption most of these projects make.
- **What it forecloses:** Closes the label definition, the timing question and the whole model family. It also decides whether the honest answer is a churn model or a latent-activity model.

### 2. Does the money leave with the customer

**Asked:** When revenue drops, is it mostly people leaving altogether, or people staying and paying you less?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** They stay. They just drop to a cheaper plan, or hand back seats.
- **Which means:** This is the most common answer in subscription businesses and the most commonly mis-scoped. The board number is revenue retention; a cancellation model does not move it. Count reductions as events and the whole project changes shape.
- **Bounds:** not below Tier 0 — Out of the Box
- **For the brief:** Loss is dominated by contraction, not departure. Target reductions as events.
- **Why it was asked:** Whether “churn” is even the right target. A programme aimed at cancellations cannot move a number that is falling because of downgrades, and the two need different signals and different offers.
- **What it forecloses:** Closes the target-variable argument and usually the label-scarcity one with it, because counting reductions as events multiplies a thin label set several times over.

### 3. How much of the loss is failed payments

**Asked:** Of everyone who left last quarter, how many actually chose to — as opposed to a card expiring or a direct debit failing?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Now you mention it, a big chunk. Maybe a third.
- **Which means:** Then a third of the loss is being handed to a marketing budget that cannot touch it. The cheapest win available here is retry logic and a card updater, and it will beat anything you model this quarter.
- **Bounds:** not below Tier 0 — Out of the Box
- **For the brief:** Roughly a third involuntary. Route to billing ops before any modelling.
- **Why it was asked:** How much of the problem is a data science problem at all. Payment failure is fixed by retries, a card updater and a dunning sequence, and none of that needs a model or a discount.
- **What it forecloses:** Closes the label-purity question, a good part of the scoping, and the “churn is up and nothing is alarming” investigation before it happens.

### 4. What actually leaves

**Asked:** What is the thing that leaves — the whole account, one line on it, or one person inside a company that stays?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** The account leaves, but usage is per seat, or per SIM.
- **Which means:** The usual case and the usual trap. Averaging lines up to the account hides the thing you want: the one person who mattered stopped logging in while automated traffic kept the total flat.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Usage sits below the departing level. Keep component detail; do not average up.
- **Why it was asked:** The row you train on, the identity you have to resolve, and whether the usage you can see is even at the same level as the thing you are predicting.
- **What it forecloses:** Closes the aggregation question, the identity-resolution question, and the “one model or two” argument that otherwise resurfaces at build time.

### 5. Does the system keep dated history

**Asked:** Can you tell what a customer’s record looked like on a given day last March, or does the system only hold what is true now?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** The CRM shows the current state. It just gets updated.
- **Which means:** The common answer and the one that quietly decides the architecture. Change capture buys history from today forward and none for the past, so the honest number is quarters away rather than weeks.
- **Bounds:** not below Tier 2 — Distributed & Custom ML
- **For the brief:** Source overwrites in place. Change capture starts history now; no test on the past.
- **Why it was asked:** Whether an honest test against the past is possible at all, and therefore Tier 1 against Tier 2. Nothing sells you history you did not keep, so this answer sets the calendar for the whole engagement.
- **What it forecloses:** Closes the leakage argument, the validation-design argument, and most of the debate about how long before there is a number worth showing anybody.

### 6. How many customers the team can reach in a week

**Asked:** How many customers can the people who act on this list actually get to in a week?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** It is automated. Email and text, so effectively unlimited.
- **Which means:** Then capacity is not the constraint but goodwill is, and the failure mode inverts: contacting people who had forgotten they were paying is how you cause the thing you are measuring.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** No capacity limit. The binding constraint is contact fatigue, not throughput.
- **Why it was asked:** The operating point, and therefore the metric. Everything is judged in the top slice of the list; how the model orders the rest of the base is a number nobody will ever act on.
- **What it forecloses:** Closes the threshold debate, the metric debate, and most arguments about whether a better model is worth funding.

### 7. Who may give money away

**Asked:** Who is allowed to give a customer something to keep them, and how much, before somebody else has to approve it?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Anything meaningful goes to an underwriter or a manager.
- **Which means:** Then the constraint is approval, not latency, and no amount of speed helps. Design the system to recommend inside the authority line and to flag the exception separately, rather than proposing things that get refused.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Meaningful offers need second approval. Recommend inside authority; flag exceptions.
- **Why it was asked:** What the system may actually recommend. A recommendation above the authority line gets overridden by hand every time, and the programme gets blamed on the model rather than the ceiling.
- **What it forecloses:** Closes the offer-design question, the override-logging question, and a good part of the Tier 3 conversation about what belongs in the request path.

### 8. Was anyone ever left alone on purpose

**Asked:** Has any past campaign ever held the offer back from a randomly chosen group, so you could see what happened to them?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** No. If we thought they were at risk, we called them.
- **Which means:** The normal answer, and it means the effect of every past campaign is unknown. Nothing recovers it after the fact. The deliverable becomes an experiment design, and saying so in week one is worth more than fitting the model anyway.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** No historical randomisation. First deliverable is an experiment, not a model.
- **Why it was asked:** Whether the effect of the offer can be estimated at all, and therefore whether Tier 2 is a build or a research project. It is the single most load-bearing answer on this problem.
- **What it forecloses:** Closes the risk-against-uplift question, the Tier 1 against Tier 2 question, and the awkward one about what the lift number in the board pack has been measuring.

### 9. How long does somebody have to go quiet before you would say they have gone?

**Asked:** How long does somebody have to go quiet before you would say they have gone?

- **Heard:** Ninety days. It is written down and everyone uses it.
- **Which means:** Then use theirs even if you would have picked differently, because a number the business already argues with beats a better one nobody recognises. Show the sensitivity alongside it.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Silence threshold agreed and documented. Use it; publish the sensitivity.
- **Why it was asked:** The threshold that invents the label, and therefore every number downstream of it. Two teams picking 60 and 90 days will report churn rates that differ by half, and both will be defensible.

### 10. When a card is declined, what happens next — and how many times?

**Asked:** When a card is declined, what happens next — and how many times?

- **Heard:** Smart retries, a card updater, and a proper email sequence.
- **Which means:** Then the easy money is gone and the remaining involuntary loss is genuinely hard. Ask for the recovery rate so it can be excluded honestly rather than blamed on the model later.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Dunning is mature. Exclude recovered failures; get the recovery rate.
- **Why it was asked:** Whether the cheapest fix in this whole problem has already been taken. Retry schedules and a card updater routinely recover a large share of failures, and nobody needs a model or a discount to do it.

### 11. If the busiest person on an account stopped logging in but everything else carried on, would anybody notice?

**Asked:** If the busiest person on an account stopped logging in but everything else carried on, would anybody notice?

- **Heard:** Yes. We watch the main users individually.
- **Which means:** Good, and unusual. Ask whether that is a dashboard somebody reads or a field the model gets, because the two are very different and only one of them scales.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Component-level activity tracked. Confirm it reaches the model, not a dashboard.
- **Why it was asked:** Whether the feature set can see the thing that actually predicts loss. It is the difference between a signal that leads by a quarter and one that arrives with the cancellation.

### 12. Has the group you would train on already been called or emailed by previous retention campaigns?

**Asked:** Has the group you would train on already been called or emailed by previous retention campaigns?

- **Heard:** Yes, and we know who was contacted and when.
- **Which means:** Then the treated can be excluded or modelled explicitly, which is the difference between a usable dataset and a misleading one. Ask whether the log covers every channel, including the ones another team runs.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Treatment history logged. Exclude or model it; confirm all channels are covered.
- **Why it was asked:** Whether the labels describe customers or describe the last campaign’s targeting rules. A model fitted to already-treated outcomes partly learns whoever built the old list.

### 13. Is there any sign that people you contacted left more often than similar people you left alone?

**Asked:** Is there any sign that people you contacted left more often than similar people you left alone?

- **Heard:** We have seen that. Certain segments react badly to contact.
- **Which means:** Then somebody has already done the hard thinking and the finding should be a suppression rule, not folklore. Get the segment written into the list build before it is rediscovered next year.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Adverse reaction observed in some segments. Encode as a suppression rule.
- **Why it was asked:** Whether contact is safe to scale. Some customers have forgotten they are paying, and a well-meant message is the reminder that ends it — an effect a risk model cannot see, because it scores those people as safe.

### 14. Do people leave steadily through the year, or does it cluster around renewal and price-change dates?

**Asked:** Do people leave steadily through the year, or does it cluster around renewal and price-change dates?

- **Heard:** It spikes at renewal. Months eleven to thirteen, every time.
- **Which means:** Then the shape is how long until it happens rather than yes-or-no, and the useful output is a curve per account rather than a probability. Note the cost: BigQuery has no built-in model for this, so it leaves SQL.
- **Bounds:** not below Tier 2 — Distributed & Custom ML
- **For the brief:** Risk spikes at renewal. The question is when, not whether; no BQML model type.
- **Why it was asked:** Whether a fixed-window classifier is the right shape at all. When risk spikes at an anniversary, a flat sixty-day question asked every week is answering the wrong question fifty times.

### 15. For the people most at risk, do email and phone still reach them — or have they stopped opening anything you send?

**Asked:** For the people most at risk, do email and phone still reach them — or have they stopped opening anything you send?

- **Heard:** The ones we most want to reach ignore everything.
- **Which means:** Then paid media becomes the delivery path, and that changes the architecture: an audience leaves BigQuery for an ad platform, and somebody has to remove people the moment they renew or the spend continues on customers you already kept.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Direct channels exhausted. Needs an audience export with renewal suppression.
- **Why it was asked:** Whether the programme has a delivery path at all for its highest-value segment. Ranking is worthless if the top of the list is unreachable, and that is frequently exactly who it is.

### 17. When an offer needs approving, how long does that take, and does the customer wait on the line for it?

**Asked:** When an offer needs approving, how long does that take, and does the customer wait on the line for it?

- **Heard:** A team leader can approve it while the call is live.
- **Which means:** Then the screen has to carry the approval path, not just the recommendation, and the interesting engineering is the workflow rather than the score. Log the approval as part of the treatment.
- **Bounds:** not below Tier 2 — Distributed & Custom ML
- **For the brief:** Live approval path. Build the workflow into the screen; log approvals as treatment.
- **Why it was asked:** Whether speed is worth paying for. If the meaningful offer takes a manager two minutes, the milliseconds argument is settled and the money belongs somewhere else.

### 18. When somebody is flagged, what does the retention rep see next to the name — and could they act on it?

**Asked:** When somebody is flagged, what does the retention rep see next to the name — and could they act on it?

- **Heard:** They see the specific thing that is wrong. Open tickets, usage drop.
- **Which means:** The right answer, and it means the explanation layer has to be filtered rather than raw. Tenure and company size explain a lot and can be acted on by nobody.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Per-row reasons required, filtered to things a rep can actually change.
- **Why it was asked:** Whether the output is usable. A probability with no reason attached gets ignored within a month, and the programme dies of indifference rather than of inaccuracy.

## 4. Still worth asking

*Every question in play has been answered.*

## 5. Not worth asking yet

Each of these is gated behind a branch that is not open. They are listed so the absence is legible: they were not forgotten, they were ruled out.

- **When you hand a list of customers to an ad platform, who turns your records into their users?** — needs “Retention spend leaves the building for an ad platform”, which nothing answered has opened.

## 6. What is being suggested, and why the alternatives are out

### Tier 2 — Distributed & Custom ML

Replay the past, rank on the change you cause

- **What it is:** Datastream append-only capture → Iceberg managed tables → BigQuery DataFrames as-of replay → uplift or a panel fit
- **Google Cloud & open-weight options at this rung:** Datastream, Iceberg managed tables, BigQuery DataFrames, Data Science Agent, Managed Service for Apache Airflow, Managed Service for Apache Spark
- **What it carries:** Place unchanged from Tier 1, still a scored table. What moves is the build, out of SQL and into BigQuery DataFrames over Iceberg managed tables.
- **Why here:** Change capture lands the history the source overwrote, so replaying features as they stood removes leakage structurally rather than by discipline. Ranking on the change the offer causes targets the people it moves.
- **Where it breaks:** Uplift needs treatment randomised in the past; with no historical holdback nothing recovers it. Cost is the monthly panel at 12–36 times the customer table, rebuilt every retrain. There is no BQML model type for when-it-happens fits, so that leaves SQL.
- **What would move it up:** The cancellation queue overtakes the outbound list as the place saves actually happen, so the offer has to be chosen inside a call the customer started.

Peers at the same price, with a different shape:

- **The replay and the curve on Managed Spark** — Datastream → Iceberg → Managed Spark replay → survival and uplift fits → scored table in BigQuery

#### Architecture Decision Record (ADR) Matrix

A scenario-aware evaluation of the ladder against this customer's constraints. Where an adjacent tier serves as a viable A/B benchmark or a Phase 2 evolution, that role is explicitly called out:

| Rung | Role in this Engagement | Architecture & Stance | Deciding Constraint & Trade-off |
| --- | --- | --- | --- |
| Tier 0 — Out of the Box | Ruled out (Insufficient) | Measure it properly before modelling it. | Below the floor (Tier 2 — Distributed & Custom ML), set by Does the system keep dated history, Do people leave steadily through the year, or does it cluster around renewal and price-change dates?, When an offer needs approving, how long does that take, and does the customer wait on the line for it?, Neither the past state nor the past experiment exists, and no rung recovers either. |
| Tier 1 — Serverless, In-Warehouse | **Adjacent Lower Tier (A/B Benchmark)** | A weekly list, ranked by what it is worth. Lower complexity and operational overhead. | Below the floor (Tier 2 — Distributed & Custom ML), set by Does the system keep dated history, Do people leave steadily through the year, or does it cluster around renewal and price-change dates?, When an offer needs approving, how long does that take, and does the customer wait on the line for it?, Neither the past state nor the past experiment exists, and no rung recovers either. Viable as an A/B comparator to quantify the performance/accuracy lift of Tier 2 — Distributed & Custom ML. |
| Tier 2 — Distributed & Custom ML | **Primary Baseline (MVP)** | Replay the past, rank on the change you cause. Fits all bounded constraints. | Selected target. Fits floor (Tier 2 — Distributed & Custom ML). Wins: Change capture lands the history the source overwrote, so replaying features as they stood removes leakage structurally rather than by discipline. Ranking on the change the offer causes targets the people it moves. |
| Tier 3 — Real-Time & Specialised | **Adjacent Higher Tier (Phase 2 Evolution)** | The offer is on screen before they say hello. Higher freshness, lower latency, or specialised modeling. | Inside the range, but nothing heard requires it yet. Step-up trigger: The cancellation queue overtakes the outbound list as the place saves actually happen, so the offer has to be chosen inside a call the customer started. Propose as Phase 2 expansion once this condition is met. |

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

- Tier 0 — Out of the Box — Measure it properly before modelling it. Out: the floor is Tier 2 — Distributed & Custom ML — Does the system keep dated history, Do people leave steadily through the year, or does it cluster around renewal and price-change dates?, When an offer needs approving, how long does that take, and does the customer wait on the line for it?, Neither the past state nor the past experiment exists, and no rung recovers either.
- Tier 1 — Serverless, In-Warehouse — A weekly list, ranked by what it is worth. Out: the floor is Tier 2 — Distributed & Custom ML — Does the system keep dated history, Do people leave steadily through the year, or does it cluster around renewal and price-change dates?, When an offer needs approving, how long does that take, and does the customer wait on the line for it?, Neither the past state nor the past experiment exists, and no rung recovers either.

**Above it, and why that is theatre here.**

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

## 7. POC Data Discovery & Profiling Contract (Tier 3)

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
    "floor": 3,
    "ceiling": 3,
    "clash": false
  },
  "recommended_rung": 3,
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
        "key": "infer",
        "heard": "They just stop using it. There is no cancel button.",
        "means": "Then churn does not exist here, only quiet, and any cut-off you pick invents the label. Say so early: it moves the work from prediction to estimating whether somebody is dormant or gone, which is a different family entirely.",
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
        "key": "downgrade",
        "heard": "They stay. They just drop to a cheaper plan, or hand back seats.",
        "means": "This is the most common answer in subscription businesses and the most commonly mis-scoped. The board number is revenue retention; a cancellation model does not move it. Count reductions as events and the whole project changes shape.",
        "floor": 0,
        "ceiling": null
      }
    },
    {
      "id": "involuntary",
      "order": 3,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "third",
        "heard": "Now you mention it, a big chunk. Maybe a third.",
        "means": "Then a third of the loss is being handed to a marketing budget that cannot touch it. The cheapest win available here is retry logic and a card updater, and it will beat anything you model this quarter.",
        "floor": 0,
        "ceiling": null
      }
    },
    {
      "id": "unit",
      "order": 4,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "below",
        "heard": "The account leaves, but usage is per seat, or per SIM.",
        "means": "The usual case and the usual trap. Averaging lines up to the account hides the thing you want: the one person who mattered stopped logging in while automated traffic kept the total flat.",
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
        "key": "overwrite",
        "heard": "The CRM shows the current state. It just gets updated.",
        "means": "The common answer and the one that quietly decides the architecture. Change capture buys history from today forward and none for the past, so the honest number is quarters away rather than weeks.",
        "floor": 2,
        "ceiling": null
      }
    },
    {
      "id": "contacts",
      "order": 6,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "automated",
        "heard": "It is automated. Email and text, so effectively unlimited.",
        "means": "Then capacity is not the constraint but goodwill is, and the failure mode inverts: contacting people who had forgotten they were paying is how you cause the thing you are measuring.",
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
        "key": "exception",
        "heard": "Anything meaningful goes to an underwriter or a manager.",
        "means": "Then the constraint is approval, not latency, and no amount of speed helps. Design the system to recommend inside the authority line and to flag the exception separately, rather than proposing things that get refused.",
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
        "key": "never",
        "heard": "No. If we thought they were at risk, we called them.",
        "means": "The normal answer, and it means the effect of every past campaign is unknown. Nothing recovers it after the fact. The deliverable becomes an experiment design, and saying so in week one is worth more than fitting the model anyway.",
        "floor": 1,
        "ceiling": null
      }
    },
    {
      "id": "lapse",
      "order": 9,
      "status": "answered",
      "answer": {
        "key": "agreed",
        "heard": "Ninety days. It is written down and everyone uses it.",
        "means": "Then use theirs even if you would have picked differently, because a number the business already argues with beats a better one nobody recognises. Show the sensitivity alongside it.",
        "floor": 1,
        "ceiling": null
      }
    },
    {
      "id": "dunning",
      "order": 10,
      "status": "answered",
      "answer": {
        "key": "mature",
        "heard": "Smart retries, a card updater, and a proper email sequence.",
        "means": "Then the easy money is gone and the remaining involuntary loss is genuinely hard. Ask for the recovery rate so it can be excluded honestly rather than blamed on the model later.",
        "floor": 1,
        "ceiling": null
      }
    },
    {
      "id": "rollup",
      "order": 11,
      "status": "answered",
      "answer": {
        "key": "tracked",
        "heard": "Yes. We watch the main users individually.",
        "means": "Good, and unusual. Ask whether that is a dashboard somebody reads or a field the model gets, because the two are very different and only one of them scales.",
        "floor": 1,
        "ceiling": null
      }
    },
    {
      "id": "treated",
      "order": 12,
      "status": "answered",
      "answer": {
        "key": "flagged",
        "heard": "Yes, and we know who was contacted and when.",
        "means": "Then the treated can be excluded or modelled explicitly, which is the difference between a usable dataset and a misleading one. Ask whether the log covers every channel, including the ones another team runs.",
        "floor": 1,
        "ceiling": null
      }
    },
    {
      "id": "reminder",
      "order": 13,
      "status": "answered",
      "answer": {
        "key": "seen",
        "heard": "We have seen that. Certain segments react badly to contact.",
        "means": "Then somebody has already done the hard thinking and the finding should be a suppression rule, not folklore. Get the segment written into the list build before it is rediscovered next year.",
        "floor": 1,
        "ceiling": null
      }
    },
    {
      "id": "spiky",
      "order": 14,
      "status": "answered",
      "answer": {
        "key": "anniversary",
        "heard": "It spikes at renewal. Months eleven to thirteen, every time.",
        "means": "Then the shape is how long until it happens rather than yes-or-no, and the useful output is a curve per account rather than a probability. Note the cost: BigQuery has no built-in model for this, so it leaves SQL.",
        "floor": 2,
        "ceiling": null
      }
    },
    {
      "id": "channels",
      "order": 15,
      "status": "answered",
      "answer": {
        "key": "burned",
        "heard": "The ones we most want to reach ignore everything.",
        "means": "Then paid media becomes the delivery path, and that changes the architecture: an audience leaves BigQuery for an ad platform, and somebody has to remove people the moment they renew or the spend continues on customers you already kept.",
        "floor": 1,
        "ceiling": null
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
      "status": "answered",
      "answer": {
        "key": "inline",
        "heard": "A team leader can approve it while the call is live.",
        "means": "Then the screen has to carry the approval path, not just the recommendation, and the interesting engineering is the workflow rather than the score. Log the approval as part of the treatment.",
        "floor": 2,
        "ceiling": null
      }
    },
    {
      "id": "reasons",
      "order": 18,
      "status": "answered",
      "answer": {
        "key": "actionable",
        "heard": "They see the specific thing that is wrong. Open tickets, usage drop.",
        "means": "The right answer, and it means the explanation layer has to be filtered rather than raw. Tenure and company size explain a lot and can be acted on by nobody.",
        "floor": 1,
        "ceiling": null
      }
    }
  ],
  "conflicts": [
    "Neither the past state nor the past experiment exists, and no rung recovers either. The first deliverable is change capture plus an experiment design; the first defensible number is quarters away. Say that in the first meeting, or somebody will believe a number nobody can trace.",
    "A third of the loss is a payment problem and nothing about the spend has ever been measured. Retry logic and a card updater will beat any model funded this year, and they belong to billing. Fix that first; it buys the credibility to ask for the experiment."
  ],
  "still_to_ask": [],
  "counts": {
    "answered": 17,
    "stale": 0,
    "open": 0,
    "not_in_play": 1,
    "dropped": 0
  },
  "schema_version": "1.0",
  "problem_id": "churn",
  "target_tier": 3,
  "derivation": {
    "floor": 3,
    "ceiling": 3,
    "recommended_tier": 3,
    "recommended_rung": 3,
    "clash": false
  }
}
```
