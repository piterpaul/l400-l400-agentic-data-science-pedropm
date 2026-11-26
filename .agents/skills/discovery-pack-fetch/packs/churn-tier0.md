---
schema_version: "1.0"
problem_id: "churn"
target_tier: 0
recommended_rung: 0
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

- **Floor: Tier 0 — Out of the Box** — set by Does the money leave with the customer, How much of the loss is failed payments, How many customers the team can reach in a week
- **Ceiling:** nothing heard yet rules out the top of the ladder

> **Together, not apart.** The board is asking about revenue and the plan is a cancellation model worked by a handful of people. Those do not meet. Count reductions as events, which also multiplies a thin label set, and be honest that at this capacity what gets offered matters more than the ranking.

## 3. What was asked, and what it steered

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

### 6. How many customers the team can reach in a week

**Asked:** How many customers can the people who act on this list actually get to in a week?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** A handful of people, maybe fifty conversations a week.
- **Which means:** Then the whole game is the top fifty and a model is competing with an experienced person’s own list. Say the number out loud: it is often small enough that ranking adds less than the retention offer budget does.
- **Bounds:** not below Tier 0 — Out of the Box
- **For the brief:** Very tight capacity. Judge on the top fifty only; question whether ranking pays.
- **Why it was asked:** The operating point, and therefore the metric. Everything is judged in the top slice of the list; how the model orders the rest of the base is a number nobody will ever act on.
- **What it forecloses:** Closes the threshold debate, the metric debate, and most arguments about whether a better model is worth funding.

## 4. Still worth asking

**These are instructions, not blanks.** Ask each one. The possible answers below are authored, with what each would rule in or out, so a reply can be recognised rather than interpreted.

### 1. Is there a cancellation date, or is it a guess

**Ask:** When somebody leaves, is there a record of it happening on a particular day — or do you work it out from them going quiet?

**Why it matters:** Whether the label exists or has to be invented. An invented one carries an arbitrary threshold that no amount of modelling recovers from, and it is the largest single assumption most of these projects make.

What the answers would mean:

- **There is a cancellation record with a date on it.** → The comfortable case, and it means the rest of the discovery is about timing rather than definition. Still ask about notice periods: somebody who gave notice a fortnight ago is not a prediction. *(floor Tier 1 — Serverless, In-Warehouse)*
- **They just stop using it. There is no cancel button.** → Then churn does not exist here, only quiet, and any cut-off you pick invents the label. Say so early: it moves the work from prediction to estimating whether somebody is dormant or gone, which is a different family entirely. *(floor Tier 1 — Serverless, In-Warehouse)*
- **Some products you cancel, some you just stop using.** → Two definitions and usually two owners who have not spoken. Scope them separately rather than averaging them, because one is a date and the other is a judgement, and mixing them produces a label nobody can defend. *(floor Tier 1 — Serverless, In-Warehouse)*
- **I would have to check how the reporting counts it.** → Worth checking before anything else, because the finance number and the operational number are usually two different definitions and the meeting will eventually discover this the hard way.

### 4. What actually leaves

**Ask:** What is the thing that leaves — the whole account, one line on it, or one person inside a company that stays?

**Why it matters:** The row you train on, the identity you have to resolve, and whether the usage you can see is even at the same level as the thing you are predicting.

What the answers would mean:

- **The account. Usage and billing are both at that level.** → The easy case and it is worth confirming rather than assuming. When the two levels match, most of the feature engineering is a group-by and the project is genuinely as simple as it looks. *(floor Tier 1 — Serverless, In-Warehouse)*
- **The account leaves, but usage is per seat, or per SIM.** → The usual case and the usual trap. Averaging lines up to the account hides the thing you want: the one person who mattered stopped logging in while automated traffic kept the total flat. *(floor Tier 1 — Serverless, In-Warehouse)*
- **They usually keep something. It is rarely all or nothing.** → Then partial loss is the real event and full departure is the rare tail. This points at the same place as counting reductions: the target is how much is left, not whether anything is. *(floor Tier 1 — Serverless, In-Warehouse)*
- **It depends which system you ask.** → That answer is itself the finding. Two systems disagreeing about what an account is will produce two churn rates, and the project will spend its first month on that rather than on modelling.

### 5. Does the system keep dated history

**Ask:** Can you tell what a customer’s record looked like on a given day last March, or does the system only hold what is true now?

**Why it matters:** Whether an honest test against the past is possible at all, and therefore Tier 1 against Tier 2. Nothing sells you history you did not keep, so this answer sets the calendar for the whole engagement.

What the answers would mean:

- **We keep dated snapshots. We can rebuild any day.** → The strong answer, and it means features can be rebuilt as they were on the scoring date. Check the snapshots actually go back far enough for the lookback you want, which is a different question. *(floor Tier 1 — Serverless, In-Warehouse)*
- **The CRM shows the current state. It just gets updated.** → The common answer and the one that quietly decides the architecture. Change capture buys history from today forward and none for the past, so the honest number is quarters away rather than weeks. *(floor Tier 2 — Distributed & Custom ML)*
- **It is a vendor product. We get an export, not a log.** → Worse than overwrite, because there may be no reachable change log to capture at all. Dated daily exports are the fallback and they start from the day somebody sets them up. *(floor Tier 2 — Distributed & Custom ML)*
- **I assume we could get at it somehow.** → Find out in week one rather than week ten. It is the single answer most likely to change the delivery date, and it is usually a five-minute conversation with whoever owns the source.

### 7. Who may give money away

**Ask:** Who is allowed to give a customer something to keep them, and how much, before somebody else has to approve it?

**Why it matters:** What the system may actually recommend. A recommendation above the authority line gets overridden by hand every time, and the programme gets blamed on the model rather than the ceiling.

What the answers would mean:

- **There is a standard offer. Everyone gets the same one.** → Simplest to build and it makes measurement clean, because one treatment means one effect to estimate. Ask what it costs, since a fixed retention offer given to the wrong half of the list is the most expensive kind of waste. *(floor Tier 1 — Serverless, In-Warehouse)*
- **They pick from a menu, within a cap.** → Then this is an allocation problem under a budget, not a scoring problem. It also raises the bar on the history: to choose between offers you need past randomisation across offers, not just contact against no contact. *(floor Tier 1 — Serverless, In-Warehouse)*
- **Anything meaningful goes to an underwriter or a manager.** → Then the constraint is approval, not latency, and no amount of speed helps. Design the system to recommend inside the authority line and to flag the exception separately, rather than proposing things that get refused. *(floor Tier 1 — Serverless, In-Warehouse)*
- **In practice people just do what they think is right.** → A common and honest answer, and it means the historical data has no consistent treatment in it. Getting the policy written down is a prerequisite for measuring anything, and it is not your job but it is your dependency.

### 8. Was anyone ever left alone on purpose

**Ask:** Has any past campaign ever held the offer back from a randomly chosen group, so you could see what happened to them?

**Why it matters:** Whether the effect of the offer can be estimated at all, and therefore whether Tier 2 is a build or a research project. It is the single most load-bearing answer on this problem.

What the answers would mean:

- **Yes, a couple of campaigns kept a control group back.** → Then the effect is estimable and the project can rank on it. Check how the group was chosen: a control picked by excluding the hard cases is not a control, and that is the usual way this answer turns out to be optimistic. *(floor Tier 1 — Serverless, In-Warehouse)*
- **No. If we thought they were at risk, we called them.** → The normal answer, and it means the effect of every past campaign is unknown. Nothing recovers it after the fact. The deliverable becomes an experiment design, and saying so in week one is worth more than fitting the model anyway. *(floor Tier 1 — Serverless, In-Warehouse)*
- **Not on purpose, but some regions were never in scope.** → Worth exploring and worth being honest about: a group excluded for a reason is different in that reason. It can support an estimate with caveats, and the caveats belong in the board pack rather than in a footnote. *(floor Tier 1 — Serverless, In-Warehouse)*
- **Marketing would know. I have never asked.** → Ask before the next meeting, because the answer reroutes the entire engagement and it is one email. It is also the question that most reliably tells you how mature the retention programme really is.

### 10. When a card is declined, what happens next — and how many times?

**Ask:** When a card is declined, what happens next — and how many times?

**Why it matters:** Whether the cheapest fix in this whole problem has already been taken. Retry schedules and a card updater routinely recover a large share of failures, and nobody needs a model or a discount to do it.

What the answers would mean:

- **Smart retries, a card updater, and a proper email sequence.** → Then the easy money is gone and the remaining involuntary loss is genuinely hard. Ask for the recovery rate so it can be excluded honestly rather than blamed on the model later. *(floor Tier 1 — Serverless, In-Warehouse)*
- **It retries a couple of times and then gives up.** → Then retry timing alone is worth more this quarter than any ranking you could build. It is somebody else’s system, which is exactly why it never gets fixed, and naming it is worth the meeting. *(floor Tier 0 — Out of the Box)*
- **The subscription just cancels.** → Then a measurable share of reported churn is a billing configuration. Put a number on it before the retention programme is scoped, because it will change what the programme is for. *(floor Tier 0 — Out of the Box)*
- **Billing handles that. I have never seen it.** → Get whoever owns billing into the room once. The conversation is short, it is the highest-return hour of the engagement, and it usually reframes the size of the prize.

### 14. Do people leave steadily through the year, or does it cluster around renewal and price-change dates?

**Ask:** Do people leave steadily through the year, or does it cluster around renewal and price-change dates?

**Why it matters:** Whether a fixed-window classifier is the right shape at all. When risk spikes at an anniversary, a flat sixty-day question asked every week is answering the wrong question fifty times.

What the answers would mean:

- **It spikes at renewal. Months eleven to thirteen, every time.** → Then the shape is how long until it happens rather than yes-or-no, and the useful output is a curve per account rather than a probability. Note the cost: BigQuery has no built-in model for this, so it leaves SQL. *(floor Tier 2 — Distributed & Custom ML)*
- **Fairly steady. People drop off all year round.** → Then the ordinary fixed-window classifier is the right shape and the simplest tier holds. Worth confirming against a curve rather than an opinion, because renewal spikes are easy to miss in a monthly average. *(floor Tier 1 — Serverless, In-Warehouse)*
- **It follows our own price rises, mostly.** → Then the strongest predictor is a calendar the business controls, which is good news and awkward news at once. It makes the model useful and it makes the honest recommendation partly a pricing conversation. *(floor Tier 1 — Serverless, In-Warehouse)*
- **Nobody has plotted it.** → A retention curve by cohort answers it in one query and no model. It is also the most persuasive single chart available in an early meeting, because everybody in the room can read it.

## 5. Not worth asking yet

Each of these is gated behind a branch that is not open. They are listed so the absence is legible: they were not forgotten, they were ruled out.

- **How long does somebody have to go quiet before you would say they have gone?** — needs “Leaving is inferred from silence rather than observed”, which nothing answered has opened.
- **If the busiest person on an account stopped logging in but everything else carried on, would anybody notice?** — needs “Usage is measured below the level that leaves”, which nothing answered has opened.
- **Has the group you would train on already been called or emailed by previous retention campaigns?** — needs “The people in the training data have already been targeted”, which nothing answered has opened.
- **Is there any sign that people you contacted left more often than similar people you left alone?** — closed by *How many customers the team can reach in a week* → “A handful of people, maybe fifty conversations a week”.
- **For the people most at risk, do email and phone still reach them — or have they stopped opening anything you send?** — closed by *How many customers the team can reach in a week* → “A handful of people, maybe fifty conversations a week”.
- **When you hand a list of customers to an ad platform, who turns your records into their users?** — needs “Retention spend leaves the building for an ad platform”, which nothing answered has opened.
- **When an offer needs approving, how long does that take, and does the customer wait on the line for it?** — needs “Some offers need somebody else to approve them”, which nothing answered has opened.
- **When somebody is flagged, what does the retention rep see next to the name — and could they act on it?** — needs “The past cannot be reconstructed from the system of record”, which nothing answered has opened.

## 6. What is being suggested, and why the alternatives are out

### Tier 0 — Out of the Box

Measure it properly before modelling it

- **What it is:** Conversational Analytics in BigQuery over billing and subscription tables → cohort retention curves → Looker board
- **Google Cloud & open-weight options at this rung:** Conversational Analytics in BigQuery, BigQuery, AI.PREDICT, Looker
- **Why here:** Two splits in an afternoon, both reframing the project. Payment failure is a fifth to two fifths of gross loss, and retries fix it. Contraction is the other: money leaves while the customer stays. A retention curve per cohort is a windowed query.
- **Where it breaks:** Cannot rank individuals, cannot attach a reason to a named account, cannot see behaviour or ticket signal. It answers which segments leak, never which account, why, and what to offer.
- **What would move it up:** Voluntary departures reach the low hundreds a month and there are enough retention reps with a weekly budget to make a ranking worth having.

#### Architecture Decision Record (ADR) Matrix

A scenario-aware evaluation of the ladder against this customer's constraints. Where an adjacent tier serves as a viable A/B benchmark or a Phase 2 evolution, that role is explicitly called out:

| Rung | Role in this Engagement | Architecture & Stance | Deciding Constraint & Trade-off |
| --- | --- | --- | --- |
| Tier 0 — Out of the Box | **Primary Baseline (MVP)** | Measure it properly before modelling it. Fits all bounded constraints. | Selected target. Fits floor (Tier 0 — Out of the Box). Wins: Two splits in an afternoon, both reframing the project. Payment failure is a fifth to two fifths of gross loss, and retries fix it. Contraction is the other: money leaves while the customer stays. A retention curve per cohort is a windowed query. |
| Tier 1 — Serverless, In-Warehouse | **Adjacent Higher Tier (Phase 2 Evolution)** | A weekly list, ranked by what it is worth. Higher freshness, lower latency, or specialised modeling. | Inside the range, but nothing heard requires it yet. Step-up trigger: Voluntary departures reach the low hundreds a month and there are enough retention reps with a weekly budget to make a ranking worth having. Propose as Phase 2 expansion once this condition is met. |
| Tier 2 — Distributed & Custom ML | In range, not required | Replay the past, rank on the change you cause. | Not ruled out, but nothing heard in the room requires it. |
| Tier 3 — Real-Time & Specialised | In range, not required | The offer is on screen before they say hello. | Not ruled out, but nothing heard in the room requires it. |

**What a build at this rung is made of.** Products they mostly already run do the landing, the answer and the delivery, and only sometimes is a trained model one of them. Your work is connecting them, writing the query over the result, and being honest in the room about where the ceiling is.

The menu at this rung, not this design. Each line says what that component is doing *here* -- several of them appear at other rungs doing something else.

- **Where the data sits still** — Whether one copy can serve every reader, or whether you have just signed up to keep two copies honest.
    - **BigQuery standard tables** — Where the product you configured drops its export.
- **How the data gets there** — Whether anything genuinely has to stream, or whether the customer said real time and meant this morning.
    - **Data Transfer Service** — How the data got there before you arrived.
- **Where the logic runs** — Whether the work fits in SQL. Nearly everything else about the build follows from that one answer.
    - **BigQuery SQL and BigQuery ML** — A hosted model called by name from one statement, with no training data.
- **What makes it run in order** — Whether this is a timetable or a graph. A graph with a gate in it is a different product from a cron line.
    - **Scheduled queries** — Scoring somebody else’s export on your clock instead of theirs.
- **How the answer reaches whoever acts** — Who or what acts on the answer, and whether they can read the place you were going to put it.
    - **A scored table plus Looker** — One governed number with an owner who signs it off.
- **The database the business already runs on** — The read shape at the moment of decision. A key lookup, a real query and a nearest-match are three stores.
    - **Cloud SQL** — The source the connector reads from.

**Who operates it.** Whoever already owns the tool. No new pager, and the ceiling moves on the vendor’s roadmap rather than on your backlog.

**Above it, and why that is theatre here.**

- Tier 1 — Serverless, In-Warehouse — A weekly list, ranked by what it is worth. Out: not ruled out, but nothing heard in the room requires it.
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

## 7. POC Data Discovery & Profiling Contract (Tier 0)

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
    "floor": 0,
    "ceiling": 0,
    "clash": false
  },
  "recommended_rung": 0,
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
      "status": "open",
      "keystone": true,
      "options": [
        "There is a cancellation record with a date on it.",
        "They just stop using it. There is no cancel button.",
        "Some products you cancel, some you just stop using.",
        "I would have to check how the reporting counts it."
      ]
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
      "status": "open",
      "keystone": true,
      "options": [
        "The account. Usage and billing are both at that level.",
        "The account leaves, but usage is per seat, or per SIM.",
        "They usually keep something. It is rarely all or nothing.",
        "It depends which system you ask."
      ]
    },
    {
      "id": "history",
      "order": 5,
      "status": "open",
      "keystone": true,
      "options": [
        "We keep dated snapshots. We can rebuild any day.",
        "The CRM shows the current state. It just gets updated.",
        "It is a vendor product. We get an export, not a log.",
        "I assume we could get at it somehow."
      ]
    },
    {
      "id": "contacts",
      "order": 6,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "small",
        "heard": "A handful of people, maybe fifty conversations a week.",
        "means": "Then the whole game is the top fifty and a model is competing with an experienced person’s own list. Say the number out loud: it is often small enough that ranking adds less than the retention offer budget does.",
        "floor": 0,
        "ceiling": null
      }
    },
    {
      "id": "authority",
      "order": 7,
      "status": "open",
      "keystone": true,
      "options": [
        "There is a standard offer. Everyone gets the same one.",
        "They pick from a menu, within a cap.",
        "Anything meaningful goes to an underwriter or a manager.",
        "In practice people just do what they think is right."
      ]
    },
    {
      "id": "randomised",
      "order": 8,
      "status": "open",
      "keystone": true,
      "options": [
        "Yes, a couple of campaigns kept a control group back.",
        "No. If we thought they were at risk, we called them.",
        "Not on purpose, but some regions were never in scope.",
        "Marketing would know. I have never asked."
      ]
    },
    {
      "id": "lapse",
      "order": 9,
      "status": "not_in_play",
      "gate": "Leaving is inferred from silence rather than observed",
      "closed_by": null
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
      "status": "not_in_play",
      "gate": "Usage is measured below the level that leaves",
      "closed_by": null
    },
    {
      "id": "treated",
      "order": 12,
      "status": "not_in_play",
      "gate": "The people in the training data have already been targeted",
      "closed_by": null
    },
    {
      "id": "reminder",
      "order": 13,
      "status": "not_in_play",
      "gate": "Contacting people might remind them to leave",
      "closed_by": {
        "question": "contacts",
        "answer": "small"
      }
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
      "status": "not_in_play",
      "gate": "Contacting people might remind them to leave",
      "closed_by": {
        "question": "contacts",
        "answer": "small"
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
      "closed_by": null
    },
    {
      "id": "reasons",
      "order": 18,
      "status": "not_in_play",
      "gate": "The past cannot be reconstructed from the system of record",
      "closed_by": null
    }
  ],
  "conflicts": [
    "The board is asking about revenue and the plan is a cancellation model worked by a handful of people. Those do not meet. Count reductions as events, which also multiplies a thin label set, and be honest that at this capacity what gets offered matters more than the ranking."
  ],
  "still_to_ask": [
    "leaving",
    "unit",
    "history",
    "authority",
    "randomised",
    "dunning",
    "spiky"
  ],
  "counts": {
    "answered": 3,
    "stale": 0,
    "open": 7,
    "not_in_play": 8,
    "dropped": 0
  },
  "schema_version": "1.0",
  "problem_id": "churn",
  "target_tier": 0,
  "derivation": {
    "floor": 0,
    "ceiling": 0,
    "recommended_tier": 0,
    "recommended_rung": 0,
    "clash": false
  }
}
```
