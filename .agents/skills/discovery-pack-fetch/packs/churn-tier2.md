---
schema_version: "1.0"
problem_id: "churn"
target_tier: 2
recommended_rung: 2
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

- **Floor: Tier 2 — Distributed & Custom ML** — set by Does the system keep dated history, Neither the past state nor the past experiment exists, and no rung recovers either
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

## 4. Still worth asking

**These are instructions, not blanks.** Ask each one. The possible answers below are authored, with what each would rule in or out, so a reply can be recognised rather than interpreted.

### 9. How long does somebody have to go quiet before you would say they have gone?

**Ask:** How long does somebody have to go quiet before you would say they have gone?

**Why it matters:** The threshold that invents the label, and therefore every number downstream of it. Two teams picking 60 and 90 days will report churn rates that differ by half, and both will be defensible.

What the answers would mean:

- **Ninety days. It is written down and everyone uses it.** → Then use theirs even if you would have picked differently, because a number the business already argues with beats a better one nobody recognises. Show the sensitivity alongside it. *(floor Tier 1 — Serverless, In-Warehouse)*
- **Finance and the product team use different windows.** → Then there are two churn rates in the building and the meeting will find that out eventually. Getting one written down is a cheap, visible win and it is a prerequisite for anything you measure. *(floor Tier 1 — Serverless, In-Warehouse)*
- **It depends. Some customers only use us a few times a year.** → Then a fixed window is wrong by construction and the honest shape is a latent-activity model: how likely somebody is still alive, given how they used to behave. That is a different family and it needs saying early. *(floor Tier 2 — Distributed & Custom ML)*
- **We have never had to put a number on it.** → Then plot the gap between visits for people who came back and for people who did not. The two curves usually separate somewhere obvious, and that is your threshold with evidence behind it.

### 10. When a card is declined, what happens next — and how many times?

**Ask:** When a card is declined, what happens next — and how many times?

**Why it matters:** Whether the cheapest fix in this whole problem has already been taken. Retry schedules and a card updater routinely recover a large share of failures, and nobody needs a model or a discount to do it.

What the answers would mean:

- **Smart retries, a card updater, and a proper email sequence.** → Then the easy money is gone and the remaining involuntary loss is genuinely hard. Ask for the recovery rate so it can be excluded honestly rather than blamed on the model later. *(floor Tier 1 — Serverless, In-Warehouse)*
- **It retries a couple of times and then gives up.** → Then retry timing alone is worth more this quarter than any ranking you could build. It is somebody else’s system, which is exactly why it never gets fixed, and naming it is worth the meeting. *(floor Tier 0 — Out of the Box)*
- **The subscription just cancels.** → Then a measurable share of reported churn is a billing configuration. Put a number on it before the retention programme is scoped, because it will change what the programme is for. *(floor Tier 0 — Out of the Box)*
- **Billing handles that. I have never seen it.** → Get whoever owns billing into the room once. The conversation is short, it is the highest-return hour of the engagement, and it usually reframes the size of the prize.

### 11. If the busiest person on an account stopped logging in but everything else carried on, would anybody notice?

**Ask:** If the busiest person on an account stopped logging in but everything else carried on, would anybody notice?

**Why it matters:** Whether the feature set can see the thing that actually predicts loss. It is the difference between a signal that leads by a quarter and one that arrives with the cancellation.

What the answers would mean:

- **Yes. We watch the main users individually.** → Good, and unusual. Ask whether that is a dashboard somebody reads or a field the model gets, because the two are very different and only one of them scales. *(floor Tier 1 — Serverless, In-Warehouse)*
- **No. We look at total usage on the account.** → Then the earliest signal is invisible by construction. Automated traffic and background integrations hold the total up long after the people stopped caring, which is why aggregate usage so often looks fine right up to the cancellation. *(floor Tier 1 — Serverless, In-Warehouse)*
- **The person who signed the deal left. That is our real signal.** → Worth taking seriously: in business-to-business this often leads everything the product telemetry shows, and it lives in the CRM rather than the product. It is also a feature nobody thinks to ask the CRM for. *(floor Tier 1 — Serverless, In-Warehouse)*
- **I am not sure we could tell.** → One query against the last dozen departures answers it: did per-person activity fall before the total did? If it did, that gap is the whole value of the project.

### 12. Has the group you would train on already been called or emailed by previous retention campaigns?

**Ask:** Has the group you would train on already been called or emailed by previous retention campaigns?

**Why it matters:** Whether the labels describe customers or describe the last campaign’s targeting rules. A model fitted to already-treated outcomes partly learns whoever built the old list.

What the answers would mean:

- **Yes, and we know who was contacted and when.** → Then the treated can be excluded or modelled explicitly, which is the difference between a usable dataset and a misleading one. Ask whether the log covers every channel, including the ones another team runs. *(floor Tier 1 — Serverless, In-Warehouse)*
- **Probably, but there is no record of who.** → Then the labels are contaminated in a way you cannot undo, and every test against the past is measuring the old campaign as much as the customer. Start logging now and be explicit that the first honest evaluation is forward-looking. *(floor Tier 1 — Serverless, In-Warehouse)*
- **No, this would be the first programme.** → Unusually clean and worth exploiting immediately: design the randomisation into the first campaign while nobody has a habit to defend. It is far easier now than after a quarter of good results. *(floor Tier 1 — Serverless, In-Warehouse)*
- **Several teams send things. I could not tell you.** → That is itself the finding, and it usually means the contact log lives in three tools. Consolidating it is unglamorous, is a prerequisite for every number that follows, and nobody else will volunteer to do it.

### 13. Is there any sign that people you contacted left more often than similar people you left alone?

**Ask:** Is there any sign that people you contacted left more often than similar people you left alone?

**Why it matters:** Whether contact is safe to scale. Some customers have forgotten they are paying, and a well-meant message is the reminder that ends it — an effect a risk model cannot see, because it scores those people as safe.

What the answers would mean:

- **We have seen that. Certain segments react badly to contact.** → Then somebody has already done the hard thinking and the finding should be a suppression rule, not folklore. Get the segment written into the list build before it is rediscovered next year. *(floor Tier 1 — Serverless, In-Warehouse)*
- **We have never looked at it that way.** → One comparison against any untouched group answers it. In subscription businesses with low engagement this is a real and expensive effect, and it is invisible to every metric currently on the board. *(floor Tier 1 — Serverless, In-Warehouse)*
- **We could not check. We contact everyone at risk.** → Then this joins the list of things that need the untreated group, and it strengthens the case for one considerably: it is no longer only about proving value, it is about not causing harm. *(floor Tier 1 — Serverless, In-Warehouse)*
- **I would not know where to start.** → Start with the lowest-risk band you contacted anyway, which most programmes do by accident. Their outcome against the rest is a rough answer available from data you already have.

### 14. Do people leave steadily through the year, or does it cluster around renewal and price-change dates?

**Ask:** Do people leave steadily through the year, or does it cluster around renewal and price-change dates?

**Why it matters:** Whether a fixed-window classifier is the right shape at all. When risk spikes at an anniversary, a flat sixty-day question asked every week is answering the wrong question fifty times.

What the answers would mean:

- **It spikes at renewal. Months eleven to thirteen, every time.** → Then the shape is how long until it happens rather than yes-or-no, and the useful output is a curve per account rather than a probability. Note the cost: BigQuery has no built-in model for this, so it leaves SQL. *(floor Tier 2 — Distributed & Custom ML)*
- **Fairly steady. People drop off all year round.** → Then the ordinary fixed-window classifier is the right shape and the simplest tier holds. Worth confirming against a curve rather than an opinion, because renewal spikes are easy to miss in a monthly average. *(floor Tier 1 — Serverless, In-Warehouse)*
- **It follows our own price rises, mostly.** → Then the strongest predictor is a calendar the business controls, which is good news and awkward news at once. It makes the model useful and it makes the honest recommendation partly a pricing conversation. *(floor Tier 1 — Serverless, In-Warehouse)*
- **Nobody has plotted it.** → A retention curve by cohort answers it in one query and no model. It is also the most persuasive single chart available in an early meeting, because everybody in the room can read it.

### 15. For the people most at risk, do email and phone still reach them — or have they stopped opening anything you send?

**Ask:** For the people most at risk, do email and phone still reach them — or have they stopped opening anything you send?

**Why it matters:** Whether the programme has a delivery path at all for its highest-value segment. Ranking is worthless if the top of the list is unreachable, and that is frequently exactly who it is.

What the answers would mean:

- **They open things. Email still works for us.** → Then the ordinary path holds and the list can go to the CRM. Ask for open rates in the top risk band specifically rather than overall, because the average hides the segment that matters.
- **The ones we most want to reach ignore everything.** → Then paid media becomes the delivery path, and that changes the architecture: an audience leaves BigQuery for an ad platform, and somebody has to remove people the moment they renew or the spend continues on customers you already kept. *(floor Tier 1 — Serverless, In-Warehouse)*
- **Half of them have opted out of marketing entirely.** → Then consent is the binding constraint before any channel question, and the suppression layer is a governance artefact rather than a filter. Find out who owns it, because it is rarely the team in the room. *(floor Tier 1 — Serverless, In-Warehouse)*
- **Marketing owns the sending. I see the list go out.** → Then nobody in the room can tell you whether the programme lands, and the ranking work is being judged on a delivery step it does not control. Get the two teams in one meeting before building anything.

### 17. When an offer needs approving, how long does that take, and does the customer wait on the line for it?

**Ask:** When an offer needs approving, how long does that take, and does the customer wait on the line for it?

**Why it matters:** Whether speed is worth paying for. If the meaningful offer takes a manager two minutes, the milliseconds argument is settled and the money belongs somewhere else.

What the answers would mean:

- **A team leader can approve it while the call is live.** → Then the screen has to carry the approval path, not just the recommendation, and the interesting engineering is the workflow rather than the score. Log the approval as part of the treatment. *(floor Tier 2 — Distributed & Custom ML)*
- **No. It goes to a queue and somebody rings them back.** → Then the ninety-second budget was never the constraint and the whole latency argument dissolves. Say so: it moves the project from a streaming build to a decent list and a better offer policy.
- **Most cases fit within what the agent can already give.** → Then design for the common case and treat exceptions as an escape hatch. It also means the offer policy can be precomputed, which removes most of the request-path complexity people assume they need. *(floor Tier 1 — Serverless, In-Warehouse)*
- **That is an operations question.** → It is, and it is the one that decides how much this costs to build. Sit with the queue for an hour before designing anything; it is the cheapest research available on this problem.

### 18. When somebody is flagged, what does the retention rep see next to the name — and could they act on it?

**Ask:** When somebody is flagged, what does the retention rep see next to the name — and could they act on it?

**Why it matters:** Whether the output is usable. A probability with no reason attached gets ignored within a month, and the programme dies of indifference rather than of inaccuracy.

What the answers would mean:

- **They see the specific thing that is wrong. Open tickets, usage drop.** → The right answer, and it means the explanation layer has to be filtered rather than raw. Tenure and company size explain a lot and can be acted on by nobody. *(floor Tier 1 — Serverless, In-Warehouse)*
- **Just the score. They work out the rest themselves.** → Then the experienced people will substitute their own judgement, which is often fine, and the model will get no credit and no feedback. Attaching two actionable reasons is cheap and changes adoption more than accuracy does. *(floor Tier 1 — Serverless, In-Warehouse)*
- **They need a script. The conversation has to be written for them.** → Then the deliverable includes wording, not just ranking, and that is a content workflow with an owner. It is also where a language model earns its place: turning two drivers into a sentence. *(floor Tier 1 — Serverless, In-Warehouse)*
- **We have not designed the screen yet.** → Design it before the model, with the people who will use it. The screen decides which features are worth having, and doing it the other way round produces reasons nobody can use.

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
| Tier 0 — Out of the Box | Ruled out (Insufficient) | Measure it properly before modelling it. | Below the floor (Tier 2 — Distributed & Custom ML), set by Does the system keep dated history, Neither the past state nor the past experiment exists, and no rung recovers either. |
| Tier 1 — Serverless, In-Warehouse | **Adjacent Lower Tier (A/B Benchmark)** | A weekly list, ranked by what it is worth. Lower complexity and operational overhead. | Below the floor (Tier 2 — Distributed & Custom ML), set by Does the system keep dated history, Neither the past state nor the past experiment exists, and no rung recovers either. Viable as an A/B comparator to quantify the performance/accuracy lift of Tier 2 — Distributed & Custom ML. |
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

- Tier 0 — Out of the Box — Measure it properly before modelling it. Out: the floor is Tier 2 — Distributed & Custom ML — Does the system keep dated history, Neither the past state nor the past experiment exists, and no rung recovers either.
- Tier 1 — Serverless, In-Warehouse — A weekly list, ranked by what it is worth. Out: the floor is Tier 2 — Distributed & Custom ML — Does the system keep dated history, Neither the past state nor the past experiment exists, and no rung recovers either.

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

## 7. POC Data Discovery & Profiling Contract (Tier 2)

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
    "floor": 2,
    "ceiling": 2,
    "clash": false
  },
  "recommended_rung": 2,
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
      "status": "open",
      "options": [
        "Ninety days. It is written down and everyone uses it.",
        "Finance and the product team use different windows.",
        "It depends. Some customers only use us a few times a year.",
        "We have never had to put a number on it."
      ]
    },
    {
      "id": "dunning",
      "order": 10,
      "status": "open",
      "options": [
        "Smart retries, a card updater, and a proper email sequence.",
        "It retries a couple of times and then gives up.",
        "The subscription just cancels.",
        "Billing handles that. I have never seen it."
      ]
    },
    {
      "id": "rollup",
      "order": 11,
      "status": "open",
      "options": [
        "Yes. We watch the main users individually.",
        "No. We look at total usage on the account.",
        "The person who signed the deal left. That is our real signal.",
        "I am not sure we could tell."
      ]
    },
    {
      "id": "treated",
      "order": 12,
      "status": "open",
      "options": [
        "Yes, and we know who was contacted and when.",
        "Probably, but there is no record of who.",
        "No, this would be the first programme.",
        "Several teams send things. I could not tell you."
      ]
    },
    {
      "id": "reminder",
      "order": 13,
      "status": "open",
      "options": [
        "We have seen that. Certain segments react badly to contact.",
        "We have never looked at it that way.",
        "We could not check. We contact everyone at risk.",
        "I would not know where to start."
      ]
    },
    {
      "id": "spiky",
      "order": 14,
      "status": "open",
      "options": [
        "It spikes at renewal. Months eleven to thirteen, every time.",
        "Fairly steady. People drop off all year round.",
        "It follows our own price rises, mostly.",
        "Nobody has plotted it."
      ]
    },
    {
      "id": "channels",
      "order": 15,
      "status": "open",
      "options": [
        "They open things. Email still works for us.",
        "The ones we most want to reach ignore everything.",
        "Half of them have opted out of marketing entirely.",
        "Marketing owns the sending. I see the list go out."
      ]
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
      "status": "open",
      "options": [
        "A team leader can approve it while the call is live.",
        "No. It goes to a queue and somebody rings them back.",
        "Most cases fit within what the agent can already give.",
        "That is an operations question."
      ]
    },
    {
      "id": "reasons",
      "order": 18,
      "status": "open",
      "options": [
        "They see the specific thing that is wrong. Open tickets, usage drop.",
        "Just the score. They work out the rest themselves.",
        "They need a script. The conversation has to be written for them.",
        "We have not designed the screen yet."
      ]
    }
  ],
  "conflicts": [
    "Neither the past state nor the past experiment exists, and no rung recovers either. The first deliverable is change capture plus an experiment design; the first defensible number is quarters away. Say that in the first meeting, or somebody will believe a number nobody can trace.",
    "A third of the loss is a payment problem and nothing about the spend has ever been measured. Retry logic and a card updater will beat any model funded this year, and they belong to billing. Fix that first; it buys the credibility to ask for the experiment."
  ],
  "still_to_ask": [
    "lapse",
    "dunning",
    "rollup",
    "treated",
    "reminder",
    "spiky",
    "channels",
    "exception",
    "reasons"
  ],
  "counts": {
    "answered": 8,
    "stale": 0,
    "open": 9,
    "not_in_play": 1,
    "dropped": 0
  },
  "schema_version": "1.0",
  "problem_id": "churn",
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
