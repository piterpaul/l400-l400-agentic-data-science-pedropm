---
schema_version: "1.0"
problem_id: "payment-fraud"
target_tier: 3
recommended_rung: 3
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

- **Floor: Tier 3 — Real-Time & Specialised** — set by Whether anything can still be stopped
- **Ceiling: Tier 3 — Real-Time & Specialised** — set by How fast the other side adapts

## 3. What was asked, and what it steered

### 1. What a confirmed case actually is

**Asked:** What tells you, in the end, that an transaction really was fraud — a formal dispute coming back from the scheme, an analyst writing down what they found, or the account holder phoning to say it was not them?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** The account holder phones to say they were tricked into sending it. Every check passed.
- **Which means:** A different problem wearing the same words. The account holder authorised it, so login and device signals are dead weight; the signal is in how new the counterparty is. The action is a warning, not a refusal, which sets the rung.
- **Bounds:** not below Tier 2 — Distributed & Custom ML
- **For the brief:** Confirmed case: victim report on an authorised payment — scams, not stolen credentials.
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

- **Heard:** We have to approve or refuse inside a deadline somebody else set.
- **Which means:** The only answer that justifies an inline path, and it is worth two more questions before believing it: what is genuinely left of that deadline, and what happens when the score is late.
- **Bounds:** not below Tier 3 — Real-Time & Specialised
- **For the brief:** Decision point: inline, approve or refuse, against an external deadline.
- **Why it was asked:** Everything. The rung, the serving path, whether a graph can be minutes behind, which of the five models get built, and what the cost of being late even is.
- **What it forecloses:** Working a queue closes the entire latency branch. A middle action closes refusal and opens the abandonment question. An inline refusal opens the deadline and the timeout, and those two together decide the rung.

### 4. What actually reads the score

**Asked:** What reads the score once it exists — a person picking cases off a list, the decision engine you already run, or a service your team owns end to end?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** It goes into the decision engine we already run, as one more input among the rules.
- **Which means:** The score becomes rule 401, and the decision engine caps everything the model can do. Say this out loud in week one: the ceiling on the project is the decision engine, not the model, and the room already suspects it.
- **Bounds:** none
- **For the brief:** Consumer: the existing decision engine. The score is one input; the decision engine sets the ceiling.
- **Why it was asked:** Whether the output is a rank or a probability, where the threshold lives, who can move it, and what the realistic ceiling on the whole project is.
- **What it forecloses:** A human queue closes everything about inline serving and makes daily capacity the only number that matters. The existing decision engine closes the question of who owns the threshold.

### 5. Whether a wrong block has ever been priced

**Asked:** What does it cost you to stop a good customer by mistake — the payment you lost, plus how likely they are never to come back? Has anyone actually worked that out?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Finance has a number for a wrong block, and they will defend it in a meeting.
- **Which means:** Rare and enormously valuable. With a price on both sides the threshold becomes arithmetic instead of an argument, and every later design choice can be justified in currency rather than in opinion.
- **Bounds:** none
- **For the brief:** Wrong block cost: a finance-signed figure exists — the threshold is arithmetic.
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

## 4. Still worth asking

**These are instructions, not blanks.** Ask each one. The possible answers below are authored, with what each would rule in or out, so a reply can be recognised rather than interpreted.

### 8. What is genuinely left of the deadline

**Ask:** After everything else on the path has taken its slice — routing, the outside device vendor, your own decision engine — how many milliseconds are genuinely left for a score? Ask for the measurement, not the number in the contract.

**Why it matters:** Whether the model can live behind a network hop or has to be compiled into the service, and how much of the budget the feature read is allowed to take.

What the answers would mean:

- **We have measured it. There is more than 50ms spare.** → Comfortable, and worth confirming it was measured at peak rather than on a quiet Tuesday. With that much room an endpoint hop is affordable and the design argument moves to correctness.
- **We measured it. About 20 to 30ms is left once the outside vendor has taken its share.** → The real number at most payment providers, and it is a design constraint before it is a workload. At this size the hop to a separate endpoint is a measurable share of the budget, so compiling the model into the service becomes an option. *(floor Tier 3 — Real-Time & Specialised)*
- **All I could give you is the deadline the network sets. We have never traced ours.** → You cannot design an inline path against a budget nobody has measured, and you should say so. One traced week of the existing path settles it, and it regularly halves what the room believed. *(ceiling Tier 2 — Distributed & Custom ML)*
- **The team that owns that path is not in this meeting. I would have to ask them.** → Get them in it. The budget is owned by whoever runs the path, and a number agreed without them is a number that will be withdrawn in month three.

### 9. What happens when the score is late

**Ask:** What happens when the score does not arrive in time — does the payment go through anyway, or get refused? And has anyone ever actually tested which one the system does?

**Why it matters:** What a millisecond is worth, and therefore whether the inline tier is a requirement or an expensive preference.

What the answers would mean:

- **It goes through. We would rather approve it than fail the transaction.** → This quietly demolishes the case for the top rung. If lateness is survivable, a slightly slow model is survivable, and a cached score read by key buys most of the same outcome for a fraction of the build. *(ceiling Tier 2 — Distributed & Custom ML)*
- **It gets refused. We do not let anything through unscored.** → Now every millisecond is revenue and the availability target is the real requirement, not the model. Price ten minutes of this against a year of fraud losses; the comparison usually surprises the room. *(floor Tier 3 — Real-Time & Specialised)*
- **On paper it approves. Nobody here has ever actually tried it.** → Then the answer is unknown, and it is the cheapest unknown here to close. Fail one instance in a load test and watch what the decision engine does; the documented behaviour and the real behaviour differ often enough to be worth the hour.
- **I could not tell you what the decision engine does in that case. Nobody here could.** → This is the question that most often changes the recommended rung, and it is answerable in an afternoon by whoever owns the decision engine. Do not design past it.

### 11. Whether a random slice could be signed off

**Ask:** Would the risk function sign off letting a thin random slice of the worst-scoring traffic through, knowing some of it is fraud you will pay for?

**Why it matters:** Whether the model can ever be honestly evaluated at the boundary, or whether every number will always be an argument.

What the answers would mean:

- **Probably, if we could size the loss first. They will not sign a blank cheque.** → Then size it: a tenth of a percent of the worst traffic, times the average amount, times a year. It is usually a smaller number than the room fears and it buys back the ability to evaluate anything.
- **No. Risk will not put their name to approving something we think is fraud.** → A defensible position, and it fixes the method. You are committed to filling the gap by assumption for good, so it has to be written into the design and re-stated in every result rather than mentioned once. *(ceiling Tier 3 — Real-Time & Specialised)*
- **It has never been put to them. I do not think anyone has dared ask.** → Put it to them with a number attached. Asked as an abstraction it is always refused; asked as a costed line against the value of being able to evaluate at all, it is sometimes approved.
- **I am not even sure whose decision that would be. Risk, maybe finance.** → Find the owner early. This is a spend approval, not an engineering choice, and it has the longest lead time of anything on the list.

## 5. Not worth asking yet

Each of these is gated behind a branch that is not open. They are listed so the absence is legible: they were not forgotten, they were ruled out.

- **How many cases a day the team can clear** — closed by *What actually reads the score* → “It goes into the decision engine we already run, as one more input among the rules”.
- **Whether a candidate can watch live traffic** — closed by *How fast the other side adapts* → “A change we ship holds up for a quarter or more. Sometimes a whole year”.

## 6. What is being suggested, and why the alternatives are out

### Tier 3 — Real-Time & Specialised

Inline refusal inside a defended millisecond budget

- **What it is:** Pub/Sub → Dataflow velocity → Bigtable features; Cloud Run decision service → Agent Platform endpoint, JAX model
- **Google Cloud & open-weight options at this rung:** Pub/Sub, Dataflow, Bigtable, Cloud Run, Agent Platform endpoints
- **What it carries:** Nothing carries from Tier 2. The build moves off Spark to a packaged artefact, and the surface moves off the streaming job onto the request path.
- **Why here:** Meets a deadline somebody else set. Bigtable is defensible here and rarely elsewhere: single-digit-ms point reads at sustained rate. The decision service owns the whole budget — feature read, endpoint call, timeout — so the slow tail is measured in one place.
- **Where it breaks:** Feature Store online serving adds a hop before the model runs, and no published figure says its share of a 50ms budget — measure it on your own traffic first. Direct Bigtable reads are faster, but then as-of correctness is yours, and the nodes bill while idle.
- **What would change the call:** Back down to Tier 2 when the path is measured to approve on timeout, or the sub-minute counts add no lift over the daily ones: a cached score then buys the same outcome.

Peers at the same price, with a different shape:

- **Scored inside the authorisation transaction** — Continuous query → ledger-side features; request → locked Spanner row → endpoint SAFE.ML.PREDICT → commit or refuse

#### Architecture Decision Record (ADR) Matrix

A scenario-aware evaluation of the ladder against this customer's constraints. Where an adjacent tier serves as a viable A/B benchmark or a Phase 2 evolution, that role is explicitly called out:

| Rung | Role in this Engagement | Architecture & Stance | Deciding Constraint & Trade-off |
| --- | --- | --- | --- |
| Tier 0 — Out of the Box | Ruled out (Insufficient) | Tune the score you are already paying for. | Below the floor (Tier 3 — Real-Time & Specialised), set by Whether anything can still be stopped. |
| Tier 1 — Serverless, In-Warehouse | Ruled out (Insufficient) | Retrospective hunting and a ranked case queue. | Below the floor (Tier 3 — Real-Time & Specialised), set by Whether anything can still be stopped. |
| Tier 2 — Distributed & Custom ML | **Adjacent Lower Tier (A/B Benchmark)** | Streaming scores and an entity graph, off the payment path. Lower complexity and operational overhead. | Below the floor (Tier 3 — Real-Time & Specialised), set by Whether anything can still be stopped. Viable as an A/B comparator to quantify the performance/accuracy lift of Tier 3 — Real-Time & Specialised. |
| Tier 3 — Real-Time & Specialised | **Primary Baseline (MVP)** | Inline refusal inside a defended millisecond budget. Fits all bounded constraints. | Selected target. Fits floor (Tier 3 — Real-Time & Specialised) and ceiling (Tier 3 — Real-Time & Specialised). Wins: Meets a deadline somebody else set. Bigtable is defensible here and rarely elsewhere: single-digit-ms point reads at sustained rate. The decision service owns the whole budget — feature read, endpoint call, timeout — so the slow tail is measured in one place. |

**What a build at this rung is made of.** A thin slice of the whole stack now runs inside the request: an event carrier, state computed over a window, and a deadline measured at the tail rather than the average.

The menu at this rung, not this design. Each line says what that component is doing *here* -- several of them appear at other rungs doing something else.

- **Where the data sits still** — Whether one copy can serve every reader, or whether you have just signed up to keep two copies honest.
    - **BigQuery standard tables** — The log every decision is written back to.
    - **Apache Iceberg managed tables** — Where a streaming write lands when the reader is not a continuous query.
    - **Cloud Storage and object tables** — Large payloads the request path fetches by reference.
- **How the data gets there** — Whether anything genuinely has to stream, or whether the customer said real time and meant this morning.
    - **Datastream** — The event you care about is a row changing, not a message being sent.
    - **Pub/Sub** — The carrier the streaming job and the request path both read.
    - **Managed Service for Apache Kafka** — The carrier in a shop that will not move off it.
    - **Dataflow** — State over a window, feeding the path that answers the request.
- **Where the logic runs** — Whether the work fits in SQL. Nearly everything else about the build follows from that one answer.
    - **BigQuery SQL and BigQuery ML** — A cheap standing baseline the expensive model has to keep beating.
    - **Managed Service for Apache Spark** — Streaming logic already written for it, where rewriting buys nothing.
    - **Dataflow** — The decision belongs to the stream, not to a caller waiting on a reply.
    - **Cloud Run** — The model inside the service, when a hop is a big slice of the budget.
    - **Agent Platform training** — Unchanged from the rung below. If training changed, something is wrong.
- **What makes it run in order** — Whether this is a timetable or a graph. A graph with a gate in it is a different product from a cron line.
    - **Managed Service for Apache Airflow** — The same graph, now with a gate before anything reaches the request path.
    - **Agent Platform Pipelines** — The same run, gated on evidence before a version is promoted.
- **How the answer reaches whoever acts** — Who or what acts on the answer, and whether they can read the place you were going to put it.
    - **Agent Platform endpoints and batch inference** — An online endpoint answers inside the budget, every time and not on average.
    - **A Cloud Run service** — The model in the request path with one less hop in it.
    - **Feature Store online serving** — The same definition, read inside the request.
    - **Agent Retrieval** — Match by resemblance inside the request path.
- **The database the business already runs on** — The read shape at the moment of decision. A key lookup, a real query and a nearest-match are three stores.
    - **Bigtable** — The read in the request path.
    - **AlloyDB** — A query, not a lookup, inside the decision path.
    - **Spanner** — The consistent store a continuous query can write into directly.
    - **Firestore** — Where the streaming decision is left for the application to pick up.
    - **Memorystore for Valkey** — The fastest read in the request path.

**Who operates it.** A platform team that can carry a pager. Latency and decision quality go on one board, because one of them is usually being traded for the other.

**Below it, and why that is not enough.**

- Tier 0 — Out of the Box — Tune the score you are already paying for. Out: the floor is Tier 3 — Real-Time & Specialised — Whether anything can still be stopped.
- Tier 1 — Serverless, In-Warehouse — Retrospective hunting and a ranked case queue. Out: the floor is Tier 3 — Real-Time & Specialised — Whether anything can still be stopped.
- Tier 2 — Distributed & Custom ML — Streaming scores and an entity graph, off the payment path. Out: the floor is Tier 3 — Real-Time & Specialised — Whether anything can still be stopped.

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

## 7. POC Data Discovery & Profiling Contract (Tier 3)

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
    "floor": 3,
    "ceiling": 3,
    "clash": false
  },
  "recommended_rung": 3,
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
        "key": "victim",
        "heard": "The account holder phones to say they were tricked into sending it. Every check passed.",
        "means": "A different problem wearing the same words. The account holder authorised it, so login and device signals are dead weight; the signal is in how new the counterparty is. The action is a warning, not a refusal, which sets the rung.",
        "floor": 2,
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
        "key": "blocking",
        "heard": "We have to approve or refuse inside a deadline somebody else set.",
        "means": "The only answer that justifies an inline path, and it is worth two more questions before believing it: what is genuinely left of that deadline, and what happens when the score is late.",
        "floor": 3,
        "ceiling": null
      }
    },
    {
      "id": "reader",
      "order": 4,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "gate",
        "heard": "It goes into the decision engine we already run, as one more input among the rules.",
        "means": "The score becomes rule 401, and the decision engine caps everything the model can do. Say this out loud in week one: the ceiling on the project is the decision engine, not the model, and the room already suspects it.",
        "floor": null,
        "ceiling": null
      }
    },
    {
      "id": "insult",
      "order": 5,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "priced",
        "heard": "Finance has a number for a wrong block, and they will defend it in a meeting.",
        "means": "Rare and enormously valuable. With a price on both sides the threshold becomes arithmetic instead of an argument, and every later design choice can be justified in currency rather than in opinion.",
        "floor": null,
        "ceiling": null
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
      "status": "open",
      "options": [
        "We have measured it. There is more than 50ms spare.",
        "We measured it. About 20 to 30ms is left once the outside vendor has taken its share.",
        "All I could give you is the deadline the network sets. We have never traced ours.",
        "The team that owns that path is not in this meeting. I would have to ask them."
      ]
    },
    {
      "id": "timeout",
      "order": 9,
      "status": "open",
      "options": [
        "It goes through. We would rather approve it than fail the transaction.",
        "It gets refused. We do not let anything through unscored.",
        "On paper it approves. Nobody here has ever actually tried it.",
        "I could not tell you what the decision engine does in that case. Nobody here could."
      ]
    },
    {
      "id": "capacity",
      "order": 10,
      "status": "not_in_play",
      "gate": "The score is worked by people",
      "closed_by": {
        "question": "reader",
        "answer": "gate"
      }
    },
    {
      "id": "slice",
      "order": 11,
      "status": "open",
      "options": [
        "Probably, if we could size the loss first. They will not sign a blank cheque.",
        "No. Risk will not put their name to approving something we think is fraud.",
        "It has never been put to them. I do not think anyone has dared ask.",
        "I am not even sure whose decision that would be. Risk, maybe finance."
      ]
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
  "conflicts": [],
  "still_to_ask": [
    "deadline",
    "timeout",
    "slice"
  ],
  "counts": {
    "answered": 7,
    "stale": 0,
    "open": 3,
    "not_in_play": 2,
    "dropped": 0
  },
  "schema_version": "1.0",
  "problem_id": "payment-fraud",
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
