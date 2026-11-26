---
schema_version: "1.0"
problem_id: "payment-fraud"
target_tier: 0
recommended_rung: 0
source: "built-in-classroom-pack"
---

# Discovery pack — Payment Fraud Detection

`payment-fraud` · recorded by **classroom-repo** · version 1 · served 2026-10-27T00:00:00Z

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

> **Head of Fraud Strategy, card issuer, ~8M active cards** — Our rules engine has about 400 rules. Analysts add ten a week and nobody has ever switched one off. We are declining good customers and still eating chargebacks. We need AI.
>
> **VP Engineering, payment service provider, card-present and online** — The network gives us 100 milliseconds. We need a machine learning score inside that — call it sub-50ms — and our current stack cannot get near it.
>
> **Head of Financial Crime, digital bank on instant-payment rails** — Our losses have moved from stolen cards to scams. The customer logs in normally, passes every check, and sends the money themselves. Device and authentication signals tell us nothing.

**Vocabulary is unbound.** The nouns below are the method's neutral words, not this customer's — treat them as placeholders and confirm the real terms early.

**The five specifics.**

- **How many, of the thing being predicted** — *not captured. Ask.*
- **How much history there is, and how much arrives** — *not captured. Ask.*
- **The deadline the run has to hit** — *not captured. Ask.*
- **What being wrong costs, per event or per year** — *not captured. Ask.*
- **Who owns the decision, and who would run this** — *not captured. Ask.*

## 2. Where discovery landed

- **Floor:** nothing heard yet requires anything above the cheapest rung
- **Ceiling: Tier 1 — Serverless, In-Warehouse** — set by Whether anything can still be stopped

> **Together, not apart.** You never learn a wrong block was wrong, and nobody has priced one. Both numbers the threshold depends on are missing, and no rung supplies either. The audit is one query over the decision log; the random slice is a signature. Get both before anyone draws an architecture.

## 3. What was asked, and what it steered

### 1. What a confirmed case actually is

**Asked:** What tells you, in the end, that an transaction really was fraud — a formal dispute coming back from the scheme, an analyst writing down what they found, or the account holder phoning to say it was not them?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** A formal dispute comes back to us with a coded reason. Finance trusts that one.
- **Which means:** The cleanest label available and the slowest. A scheme dispute is trusted by finance, arrives 30 to 120 days after the transaction, and sets the clock every later decision runs on.
- **Bounds:** none
- **For the brief:** Confirmed case: a coded scheme dispute, arriving months later.
- **Why it was asked:** The training table, how late every measure is, and whether this is a stolen-credentials problem or a scam problem at all. Those two share almost no features and take different actions.
- **What it forecloses:** A victim report closes everything about login and device signals and opens the whole counterparty branch. A coded dispute closes the scam branch and opens the question of how long you wait.

### 2. How late the confirmed case arrives

**Asked:** How long after the transaction does that answer actually arrive — the same day, a few weeks, or the far side of a quarter? And what share turns up after whatever cut-off you use today?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Three months before most of them land, and we still get a tail after that.
- **Which means:** The clock everything else obeys. Refitting weekly against a label that matures in ninety days fits noise, however good the scheduler looks. Something has to stand in meanwhile, and its honesty has to be measured.
- **Bounds:** none
- **For the brief:** Confirmed case matures at ~90 days — the refit cadence answers to this, not to a scheduler.
- **Why it was asked:** The gap in every rewind test, the training window, the refit cadence, and whether a stand-in label is needed at all.
- **What it forecloses:** Same-day answers close the whole stand-in branch. A quarter opens it, and makes the agreement between the stand-in and the real answer a number somebody has to watch.

### 3. Whether anything can still be stopped

**Asked:** At the moment the score exists, can anything still be stopped? Or has the money already moved and the work is a queue somebody picks up the next morning?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** The money has gone by then. We work a queue the next morning.
- **Which means:** Nothing here needs to be fast, and that is a finding worth saying out loud early. The whole value is ranking a queue well enough that the people working it start at the top.
- **Bounds:** Tier 1 — Serverless, In-Warehouse is the ceiling
- **For the brief:** Decision point: after the fact — the output is a ranked queue, not a verdict.
- **Why it was asked:** Everything. The rung, the serving path, whether a graph can be minutes behind, which of the five models get built, and what the cost of being late even is.
- **What it forecloses:** Working a queue closes the entire latency branch. A middle action closes refusal and opens the abandonment question. An inline refusal opens the deadline and the timeout, and those two together decide the rung.

### 4. What actually reads the score

**Asked:** What reads the score once it exists — a person picking cases off a list, the decision engine you already run, or a service your team owns end to end?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** An analyst picks it up off a ranked list. Nothing happens until they do.
- **Which means:** Then the threshold is set by how many cases the team can clear in a day, not by any curve. That number is fixed in the short term and it is the operating point whether anyone writes it down or not.
- **Bounds:** Tier 2 — Distributed & Custom ML is the ceiling
- **For the brief:** Consumer: a human queue — the operating point is the team’s daily capacity.
- **Why it was asked:** Whether the output is a rank or a probability, where the threshold lives, who can move it, and what the realistic ceiling on the whole project is.
- **What it forecloses:** A human queue closes everything about inline serving and makes daily capacity the only number that matters. The existing decision engine closes the question of who owns the threshold.

### 5. Whether a wrong block has ever been priced

**Asked:** What does it cost you to stop a good customer by mistake — the payment you lost, plus how likely they are never to come back? Has anyone actually worked that out?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** It has honestly never come up. We measure fraud losses and that is it.
- **Which means:** Then the organisation is optimising one side of a two-sided decision, and at most issuers the unmeasured side is the larger one. Do not build an inline refuser for a business that cannot say what refusing costs.
- **Bounds:** Tier 2 — Distributed & Custom ML is the ceiling
- **For the brief:** Wrong block cost: never considered. Price it before any inline refusal is designed.
- **Why it was asked:** The threshold, the objective, and whether the business is even able to judge the model it is asking for.
- **What it forecloses:** A signed price closes the whole threshold argument. Never having considered it opens the audit, which is usually the first deliverable whatever the customer came in asking for.

### 6. Whether refused transactions are ever followed up

**Asked:** When you stop an transaction, does anything ever tell you whether stopping it was right? A payment that never happened cannot come back as a confirmed case.

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** No. Once we stop it, that is the end of the record. Nothing comes back.
- **Which means:** The hole at the centre of this problem. Every model you train afterwards is fitted only to traffic you allowed, and the harder you stop things the better your numbers look and the less you can see.
- **Bounds:** none
- **For the brief:** Refused transactions produce no outcome at all — every later measure is on allowed traffic only.
- **Why it was asked:** Whether any measure quoted about this model can be believed, and whether the honest route is to buy labels with a random slice or to fill the gap by assumption and label it as such.
- **What it forecloses:** An existing slice closes the whole argument about whether the numbers are trustworthy. Never closes nothing — it opens the most expensive conversation on the problem.

### 7. How fast the other side adapts

**Asked:** When you ship a change, how long does it keep working before the volume routes around it — a quarter, a month, days? Ask for the measurement rather than the impression.

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** A change we ship holds up for a quarter or more. Sometimes a whole year.
- **Which means:** Then this behaves like an ordinary prediction problem and the usual cadences apply. Worth checking against evidence rather than impression — slow often means nobody is measuring how fast.
- **Bounds:** Tier 3 — Real-Time & Specialised is the ceiling
- **For the brief:** Adaptation: a quarter or more. Ordinary refit cadences apply.
- **Why it was asked:** The refit cadence, whether retraining fires on a trigger or a calendar, and whether the hardening overlay is a nice-to-have or the actual requirement.
- **What it forecloses:** A quarter closes the whole hardening branch. Days opens it and makes the red team and the combined switch part of the first release rather than a later phase.

### 10. How many cases a day the team can clear

**Asked:** How many cases can the team clear in a day, and is that number allowed to change? A team that clears 500 needs a threshold tuned to hand them exactly 500.

- **Heard:** They will give you the number, and it has not moved in a year.
- **Which means:** Then you have the operating point already and the modelling target is precision in the top N, not accuracy overall. Tune to hand them exactly that many and report on that slice.
- **Bounds:** none
- **For the brief:** Capacity: a known, stable daily figure — tune the threshold to fill it exactly.
- **Why it was asked:** The operating point, and therefore what the model is optimised for: precision in the top N rather than any overall score.
- **What it forecloses:** A small fixed capacity closes every argument for more volume and moves the whole conversation to ranking quality at the top of the list.

### 11. Whether a random slice could be signed off

**Asked:** Would the risk function sign off letting a thin random slice of the worst-scoring traffic through, knowing some of it is fraud you will pay for?

- **Heard:** Probably, if we could size the loss first. They will not sign a blank cheque.
- **Which means:** Then size it: a tenth of a percent of the worst traffic, times the average amount, times a year. It is usually a smaller number than the room fears and it buys back the ability to evaluate anything.
- **Bounds:** none
- **For the brief:** Random slice: fundable if sized. Cost it before the next conversation.
- **Why it was asked:** Whether the model can ever be honestly evaluated at the boundary, or whether every number will always be an argument.
- **What it forecloses:** A refusal closes the evaluation branch permanently and turns inferred outcomes from an interim into the method.

## 4. Still worth asking

*Every question in play has been answered.*

## 5. Not worth asking yet

Each of these is gated behind a branch that is not open. They are listed so the absence is legible: they were not forgotten, they were ruled out.

- **What is genuinely left of the deadline** — closed by *Whether anything can still be stopped* → “The money has gone by then. We work a queue the next morning”.
- **What happens when the score is late** — closed by *Whether anything can still be stopped* → “The money has gone by then. We work a queue the next morning”.
- **Whether a candidate can watch live traffic** — closed by *How fast the other side adapts* → “A change we ship holds up for a quarter or more. Sometimes a whole year”.

## 6. What is being suggested, and why the alternatives are out

### Tier 0 — Out of the Box

Tune the score you are already paying for

- **What it is:** Bought fraud score + Datastream change capture of the decision log → BigQuery → Conversational Analytics + Looker
- **Google Cloud & open-weight options at this rung:** Datastream, BigQuery, AI.PREDICT, Conversational Analytics, Looker
- **Why here:** The bought score rides on every transaction, usually consumed as one fixed threshold. Land the decision log in BigQuery, point Conversational Analytics at it, and fraud ops asks which card ranges drove the week’s wrong blocks. Re-tuning it beats a new model.
- **Where it breaks:** The bought score cannot see your own signals — tenure, device history, what happened in this session — and tuning per group means moving one number. It does nothing for scams or disputes the account holder raised themselves, and hands you no queue.
- **What would move it up:** A rewind test on the decision log shows one of your own signals — tenure, device history — separating fraud the bought score misses at the threshold you actually run.

#### Architecture Decision Record (ADR) Matrix

A scenario-aware evaluation of the ladder against this customer's constraints. Where an adjacent tier serves as a viable A/B benchmark or a Phase 2 evolution, that role is explicitly called out:

| Rung | Role in this Engagement | Architecture & Stance | Deciding Constraint & Trade-off |
| --- | --- | --- | --- |
| Tier 0 — Out of the Box | **Primary Baseline (MVP)** | Tune the score you are already paying for. Fits all bounded constraints. | Selected target. Fits ceiling (Tier 1 — Serverless, In-Warehouse). Wins: The bought score rides on every transaction, usually consumed as one fixed threshold. Land the decision log in BigQuery, point Conversational Analytics at it, and fraud ops asks which card ranges drove the week’s wrong blocks. Re-tuning it beats a new model. |
| Tier 1 — Serverless, In-Warehouse | **Adjacent Higher Tier (Phase 2 Evolution)** | Retrospective hunting and a ranked case queue. Higher freshness, lower latency, or specialised modeling. | Inside the range, but nothing heard requires it yet. Step-up trigger: A rewind test on the decision log shows one of your own signals — tenure, device history — separating fraud the bought score misses at the threshold you actually run. Propose as Phase 2 expansion once this condition is met. |
| Tier 2 — Distributed & Custom ML | Ruled out (Theatre) | Streaming scores and an entity graph, off the payment path. | Past the ceiling (Tier 1 — Serverless, In-Warehouse), set by Whether anything can still be stopped. Unjustified operational cost. |
| Tier 3 — Real-Time & Specialised | Ruled out (Theatre) | Inline refusal inside a defended millisecond budget. | Past the ceiling (Tier 1 — Serverless, In-Warehouse), set by Whether anything can still be stopped. Unjustified operational cost. |

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

- Tier 1 — Serverless, In-Warehouse — Retrospective hunting and a ranked case queue. Out: not ruled out, but nothing heard in the room requires it.
- Tier 2 — Distributed & Custom ML — Streaming scores and an entity graph, off the payment path. Out: past the ceiling at Tier 1 — Serverless, In-Warehouse — Whether anything can still be stopped.
- Tier 3 — Real-Time & Specialised — Inline refusal inside a defended millisecond budget. Out: past the ceiling at Tier 1 — Serverless, In-Warehouse — Whether anything can still be stopped.

**Below the rung sit the calls no rung makes for you.** The tier does not settle these, and a design that has not stated them has not been made. Nothing on the page asks for them, so they travel unanswered.

- **What one row is** — One transaction, as of the instant the decision engine asks — not the settled row it becomes an hour later. Those are different rows with different fields, and only one of them exists while anything can still be stopped.
  Options: One transaction, at the decision moment · One card or one account holder per day · A group of cards, devices and counterparties
- **What goes in beside the past** — Which fields exist when the decision engine asks, and which only turn up when the payment settles. The final amount and the address checks often differ, and the training table is almost always built from the settled version.
  Options: Daily aggregates only · Sub-minute counts as well · The group label off the entity graph
- **One fit, one each, or one per group** — One fit over all transactions, one per counterparty, or a handful cut by channel and market. A distributed rung will fan out to thousands of fits as happily as it runs four, so the rung is not deciding this.
  Options: One fit across everything · A handful, cut by channel or market · One fit per counterparty
- **Which methods get a run** — A boosted tree, a linear fit that can state a reason, and a pretrained classifier that repairs the label rather than making the decision. The baseline is not a null model: it is the rules the decision engine runs and nobody switches off.
  Options: Boosted trees · A linear fit with coefficients · A pretrained classifier on the free text
- **How you would know** — Rewind to a past date and go forward, leaving a gap as long as a confirmed case takes to arrive. And everything you rewind over is traffic you allowed: a refused transaction never comes back with an answer at all.
  Options: Rewind by time, with a maturity gap · Let a candidate watch live traffic · A stand-in label, and how badly it lies
- **What tuning is worth** — Three things compete for the same weeks: repairing a label three sources disagree about, choosing the operating point, and searching the settings. Label first, settings last, and the middle one usually moves the most money.
  Options: Leave the settings alone · Search the settings · Search the operating point instead
- **One winner, or several combined** — Three scores can be live at once: the tree, the group label off the graph, and the bought score the decision engine still reads. Combining them is one line offline and a second model call inside the budget.
  Options: Keep the single best model · Average two or more · Feed one in as a column of the other
- **Making the numbers agree** — Three numbers describe the same week and none of them match: what the analyst queue called fraud that day, what coded disputes confirm 90 days later, and the loss the business carries once recovery is netted off.
  Options: Restate once the labels mature · Freeze the first figure, monitor the gap · Judge it on the loss you actually carry

**Dataset for the build.** Every workshop build runs on public or shipped tables:

- **Source:** BigQuery public tables
- **Tables:** `bigquery-public-data.ml_datasets.ulb_fraud_detection`
- **Grain & size:** One row per card transaction (Time in seconds across two days, PCA components V1–V28, Amount, Class); 284,807 transactions with 492 confirmed frauds (0.173% positive rate).
- **Target / label:** Binary fraud indicator Class = 1 on a strict time split by Time.
- **Tier 1 / Tier 2 build:** Hard Tier 1 fits BOOSTED_TREE_CLASSIFIER with auto_class_weights=TRUE (checked against a TabFM AI.PREDICT slice) and sets the review cut-off in SQL by daily queue capacity and Amount loss; Tier 2 fits custom LightGBM or XGBoost with probability adjustment.
- **Caveat:** Predicting zero on every row scores 99.83% accuracy, a random split leaks fraud bursts across time, and anonymised PCA columns lack card or merchant keys for graph rings.
- **Setup / verify:** `bq head -n 5 bigquery-public-data:ml_datasets.ulb_fraud_detection`
- **Agent skills (`bigquery-data-science` & Data Agent Kit):** `uvx bigquery-data-science lookup BOOSTED_TREE_CLASSIFIER # BQDS: AI.KEY_DRIVERS, AI.PREDICT, AI.CLASSIFY, KMEANS, PCA, ML.ROC_CURVE | Data Agent Kit: bigquery-ai-ml, bigquery-graph-author, bigquery-graph-query, ml-best-practices, gcp-dataflow, bigtable-basics`

**The ladder, for reference.** No site is needed to read the tiers above.

- **Tier 0 — Out of the Box** — A model somebody else trained already answers the question. Nothing to fit, nothing to provision, and the bill starts on the first query. The most senior move in the room is often to say so.
- **Tier 1 — Serverless, In-Warehouse** — Bring the model to the data. No cluster, no container, no serving stack. SQL is the interface.
- **Tier 2 — Distributed & Custom ML** — The transformation or the model outgrew SQL. Bring distributed compute to the data, keep the storage where it is.
- **Tier 3 — Real-Time & Specialised** — A hard SLA or a custom objective justifies owning the stack. You are now engineering a system, not training a model.
- **Tier 4 — Hardening for High-Stakes Operation** — Not a rung you buy. It is what changes about a system already at Tier 1, 2 or 3 once being wrong is expensive, contested or unsafe — and what changes is different for every problem in Discovery.

## 7. POC Data Discovery & Profiling Contract (Tier 0)

- **Source Tables (`bigquery-region: "US"`):** `bigquery-public-data.ml_datasets.ulb_fraud_detection`
- **Grain & Target:** One row per card transaction (Time in seconds across two days, PCA components V1–V28, Amount, Class); 284,807 transactions with 492 confirmed frauds (0.173% positive rate). | Binary fraud indicator Class = 1 on a strict time split by Time.
- **Data Caveat to Profile & Guard Against:** Predicting zero on every row scores 99.83% accuracy, a random split leaks fraud bursts across time, and anonymised PCA columns lack card or merchant keys for graph rings.
- **Verification Command:** `bq head -n 5 bigquery-public-data:ml_datasets.ulb_fraud_detection`

---

### The same thing, for a program to read

```json
{
  "problem": "payment-fraud",
  "ldap": "classroom-repo",
  "version": 1,
  "served_at": "2026-10-27T00:00:00Z",
  "binding": {
    "event": "transaction",
    "holder": "account holder",
    "counterparty": "counterparty",
    "gate": "decision engine",
    "reviewer": "analyst",
    "confirmation": "confirmed case",
    "block": "wrong block",
    "friction": "step-up"
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
      "bigquery-public-data.ml_datasets.ulb_fraud_detection"
    ],
    "grain": "One row per card transaction (Time in seconds across two days, PCA components V1–V28, Amount, Class); 284,807 transactions with 492 confirmed frauds (0.173% positive rate).",
    "label": "Binary fraud indicator Class = 1 on a strict time split by Time.",
    "rungs": "Hard Tier 1 fits BOOSTED_TREE_CLASSIFIER with auto_class_weights=TRUE (checked against a TabFM AI.PREDICT slice) and sets the review cut-off in SQL by daily queue capacity and Amount loss; Tier 2 fits custom LightGBM or XGBoost with probability adjustment.",
    "caveat": "Predicting zero on every row scores 99.83% accuracy, a random split leaks fraud bursts across time, and anonymised PCA columns lack card or merchant keys for graph rings.",
    "setup": "bq head -n 5 bigquery-public-data:ml_datasets.ulb_fraud_detection",
    "skills": "uvx bigquery-data-science lookup BOOSTED_TREE_CLASSIFIER # BQDS: AI.KEY_DRIVERS, AI.PREDICT, AI.CLASSIFY, KMEANS, PCA, ML.ROC_CURVE | Data Agent Kit: bigquery-ai-ml, bigquery-graph-author, bigquery-graph-query, ml-best-practices, gcp-dataflow, bigtable-basics"
  },
  "questions": [
    {
      "id": "label",
      "order": 1,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "dispute",
        "heard": "A formal dispute comes back to us with a coded reason. Finance trusts that one.",
        "means": "The cleanest label available and the slowest. A scheme dispute is trusted by finance, arrives 30 to 120 days after the transaction, and sets the clock every later decision runs on.",
        "floor": null,
        "ceiling": null
      }
    },
    {
      "id": "delay",
      "order": 2,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "quarter",
        "heard": "Three months before most of them land, and we still get a tail after that.",
        "means": "The clock everything else obeys. Refitting weekly against a label that matures in ninety days fits noise, however good the scheduler looks. Something has to stand in meanwhile, and its honesty has to be measured.",
        "floor": null,
        "ceiling": null
      }
    },
    {
      "id": "inline",
      "order": 3,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "after",
        "heard": "The money has gone by then. We work a queue the next morning.",
        "means": "Nothing here needs to be fast, and that is a finding worth saying out loud early. The whole value is ranking a queue well enough that the people working it start at the top.",
        "floor": null,
        "ceiling": 1
      }
    },
    {
      "id": "reader",
      "order": 4,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "queue",
        "heard": "An analyst picks it up off a ranked list. Nothing happens until they do.",
        "means": "Then the threshold is set by how many cases the team can clear in a day, not by any curve. That number is fixed in the short term and it is the operating point whether anyone writes it down or not.",
        "floor": null,
        "ceiling": 2
      }
    },
    {
      "id": "insult",
      "order": 5,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "never",
        "heard": "It has honestly never come up. We measure fraud losses and that is it.",
        "means": "Then the organisation is optimising one side of a two-sided decision, and at most issuers the unmeasured side is the larger one. Do not build an inline refuser for a business that cannot say what refusing costs.",
        "floor": null,
        "ceiling": 2
      }
    },
    {
      "id": "reject",
      "order": 6,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "never",
        "heard": "No. Once we stop it, that is the end of the record. Nothing comes back.",
        "means": "The hole at the centre of this problem. Every model you train afterwards is fitted only to traffic you allowed, and the harder you stop things the better your numbers look and the less you can see.",
        "floor": null,
        "ceiling": null
      }
    },
    {
      "id": "adversary",
      "order": 7,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "slow",
        "heard": "A change we ship holds up for a quarter or more. Sometimes a whole year.",
        "means": "Then this behaves like an ordinary prediction problem and the usual cadences apply. Worth checking against evidence rather than impression — slow often means nobody is measuring how fast.",
        "floor": null,
        "ceiling": 3
      }
    },
    {
      "id": "deadline",
      "order": 8,
      "status": "not_in_play",
      "gate": "A decision must be made inside a deadline",
      "closed_by": {
        "question": "inline",
        "answer": "after"
      }
    },
    {
      "id": "timeout",
      "order": 9,
      "status": "not_in_play",
      "gate": "A decision must be made inside a deadline",
      "closed_by": {
        "question": "inline",
        "answer": "after"
      }
    },
    {
      "id": "capacity",
      "order": 10,
      "status": "answered",
      "answer": {
        "key": "known",
        "heard": "They will give you the number, and it has not moved in a year.",
        "means": "Then you have the operating point already and the modelling target is precision in the top N, not accuracy overall. Tune to hand them exactly that many and report on that slice.",
        "floor": null,
        "ceiling": null
      }
    },
    {
      "id": "slice",
      "order": 11,
      "status": "answered",
      "answer": {
        "key": "willing",
        "heard": "Probably, if we could size the loss first. They will not sign a blank cheque.",
        "means": "Then size it: a tenth of a percent of the worst traffic, times the average amount, times a year. It is usually a smaller number than the room fears and it buys back the ability to evaluate anything.",
        "floor": null,
        "ceiling": null
      }
    },
    {
      "id": "shadow",
      "order": 12,
      "status": "not_in_play",
      "gate": "The other side adapts within days",
      "closed_by": {
        "question": "adversary",
        "answer": "slow"
      }
    }
  ],
  "conflicts": [
    "You never learn a wrong block was wrong, and nobody has priced one. Both numbers the threshold depends on are missing, and no rung supplies either. The audit is one query over the decision log; the random slice is a signature. Get both before anyone draws an architecture."
  ],
  "still_to_ask": [],
  "counts": {
    "answered": 9,
    "stale": 0,
    "open": 0,
    "not_in_play": 3,
    "dropped": 0
  },
  "schema_version": "1.0",
  "problem_id": "payment-fraud",
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
