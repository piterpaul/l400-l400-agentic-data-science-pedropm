---
schema_version: "1.0"
problem_id: "next-best-offer"
target_tier: 3
recommended_rung: 3
source: "built-in-classroom-pack"
---

# Discovery pack — Next-Best-Offer & Cross-Sell Across Silos

`next-best-offer` · recorded by **classroom-repo** · version 1 · served 2026-10-27T00:00:00Z

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

> **CMO, regional retail bank — 2.4M customers, no data science function** — Every customer should have a next best product. Marketing has twelve offers, the ad platform knows what people clicked, Salesforce knows what they already hold. Join it, rank it, and put the score on the customer record so the branch team can see it.
>
> **Head of Data Platform, telco — 30M subscribers, mature Spark shop** — The models are fine, the plumbing is the problem. Ad logs are 4TB a day of nested JSON, the identity graph is maintained by two people in a spreadsheet, and finance wants to know which part of the retention budget actually moved anything.
>
> **Director of Digital Product, marketplace — 200ms page budget** — The homepage hero and the basket upsell should change based on what the user just looked at. We have 200 milliseconds for the whole page. And merchandising gets final say on what can be shown.

**Vocabulary is unbound.** The nouns below are the method's neutral words, not this customer's — treat them as placeholders and confirm the real terms early.

**The five specifics.**

- **How many, of the thing being predicted** — *not captured. Ask.*
- **How much history there is, and how much arrives** — *not captured. Ask.*
- **The deadline the run has to hit** — *not captured. Ask.*
- **What being wrong costs, per event or per year** — *not captured. Ask.*
- **Who owns the decision, and who would run this** — *not captured. Ask.*

## 2. Where discovery landed

- **Floor: Tier 3 — Real-Time & Specialised** — set by Where the offer appears, and when it is picked, One plan that shares out limited offers and a decision taken while the person waits
- **Ceiling:** nothing heard yet rules out the top of the ladder

> **Together, not apart.** One plan that shares out limited offers and a decision taken while the person waits. The plan is a snapshot; spent live it needs a ledger every channel writes to. Take that on at Tier 3, or push the plan down as a price per offer and let the live ranker read prices.

## 3. What was asked, and what it steered

### 1. How many offers, and how many at once

**Asked:** How many different offers are on the table, and how many could one person qualify for at the same time? Twelve overlapping offers is a ranking job. Three that rule each other out is a yes-or-no.

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Thousands. It is the whole catalogue, and most of it is open to anyone.
- **Which means:** At this size the first step is no longer ranking, it is narrowing. That is a different problem and the catalog has one for it; this method picks up again once something has cut the field to a shortlist.
- **Bounds:** not below Tier 2 — Distributed & Custom ML
- **For the brief:** Offers: catalogue-sized — narrowing comes before ranking.
- **Why it was asked:** Whether this is a ranking problem at all. A handful of mutually exclusive offers is a rule set; a dozen overlapping ones is an ordering; a catalogue is a narrowing problem before it is an ordering.
- **What it forecloses:** A handful closes everything about putting scores on one scale, about running out, and about how a brand-new offer gets ranked with nothing behind it.

### 2. What the ranking is meant to maximise

**Asked:** What is the ranking meant to maximise: how many people say yes, the money each yes brings in, or the yeses that would not have happened without the offer? Those three disagree, and only the third one costs revenue to measure.

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Only the yeses we actually caused. Plenty of them would have bought anyway.
- **Which means:** A question about cause, not about prediction. It needs a group left out at random while the campaign ran — ask next whether one exists, because without it this is not buildable at any rung.
- **Bounds:** not below Tier 2 — Distributed & Custom ML
- **For the brief:** Objective: yeses the offer caused, not yeses observed.
- **Why it was asked:** Everything downstream: what a yes means, which measure is quoted, whether a held-back group is needed, and which of the five models get built at all.
- **What it forecloses:** Take-up or value closes the whole branch about proving cause. Caused yeses opens it, and makes whether anybody was ever randomly held back the only question that matters.

### 3. What counts as a yes

**Asked:** What counts as the person saying yes: a click, an application started, an approval, the money actually moving, or still being there in ninety days? Each one moves how often it happens by a factor of ten.

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Still there after ninety days. A yes that cancels in month two was never one.
- **Which means:** What the business actually cares about, and the hardest thing to train on, because a quarter of waiting sits between the send and the truth. Expect a stand-in, and be explicit about what it stands for.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Yes = still there at ninety days — truth lands a quarter late.
- **Why it was asked:** How often it happens, the training table, and how long after a send the truth arrives. It is also the number the business will judge the project by, so it is agreed rather than chosen.
- **What it forecloses:** A settled definition closes the questions about credit windows and fixes the retraining cadence, because the truth cannot arrive faster than the acceptance does.

### 4. What share of people match across the source systems

**Asked:** What share of people actually match between the ad-side records and the customer records today, which way has that share moved over six months, and who worked the number out?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Roughly half, and it has been slipping. It was better six months ago.
- **Which means:** Half the base is invisible to every model downstream, and a falling share looks exactly like the offers getting worse. Which half is missing matters more than the number does.
- **Bounds:** not below Tier 2 — Distributed & Custom ML
- **For the brief:** Matching: about half and slipping — who is missing is core scope.
- **Why it was asked:** How much of the base the ranking can even see, and whether building a matcher is the project. It also sets an honest ceiling on every accuracy claim made later.
- **What it forecloses:** One shared key closes the whole matching branch and the largest single piece of Tier 2. A prohibited join closes everything above Tier 0.

### 5. What runs out, and who sets the limit

**Asked:** Do any offers run out — a fixed number of units, a monthly budget, a quota — and how many times a month may one person be contacted at all? Who sets each of those numbers?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Yes. We have a fixed number of units on some and a monthly quota on others.
- **Which means:** This stops being scoring and becomes sharing a limited thing out. Ranking each person alone oversells the best offer by day three, and no amount of model quality repairs that.
- **Bounds:** not below Tier 2 — Distributed & Custom ML
- **For the brief:** Limits: hard caps per offer — a sharing-out step is required.
- **Why it was asked:** Whether this is scoring or sharing out. Independent per-person ranking and one solve over a shared pool are different systems, and the second cannot be retrofitted by sorting harder.
- **What it forecloses:** No binding limits closes the sharing-out branch, the questions about running out, and most of the argument for Tier 2.

### 6. Whether anyone was ever randomly held back

**Asked:** Has any offer ever been held back from a randomly chosen group, and is that recorded person by person rather than campaign by campaign?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Yes. The flag sits on the person, not just on the campaign.
- **Which means:** Rare and valuable. This is the one input that makes an answer about cause possible, and having it person by person means it can be joined to features rather than read off a campaign report.
- **Bounds:** not below Tier 2 — Distributed & Custom ML
- **For the brief:** Held back: exists in history, recorded per person.
- **Why it was asked:** Whether an answer about cause is buildable at all, now or only in six months. Nothing else here has a longer lead time, which is why it is asked early rather than in an experiment section.
- **What it forecloses:** A no closes the whole would-they-have-bought-anyway branch for this quarter, and turns Tier 2 into a sequencing conversation rather than an architecture one.

### 7. Where the offer appears, and when it is picked

**Asked:** Where does the chosen offer actually appear, and when is it chosen? Written onto a record overnight for somebody to read tomorrow, or picked while the person is waiting for a page?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** One slot on the page, and it has to be filled while the person waits.
- **Which means:** A deadline, not a workload. Forty milliseconds inside a page budget means the ranking runs over a shortlist the rules already cut, and the interesting engineering is the shortlist rather than the model.
- **Bounds:** not below Tier 3 — Real-Time & Specialised
- **For the brief:** Surface: one live slot, decided inside the page budget.
- **Why it was asked:** The clock, which is the strongest single constraint here. What reads the output decides the rung far more than how many people there are.
- **What it forecloses:** A nightly write to a record closes every live question, the whole streaming tier, and the argument about a shared ledger with it.

## 4. Still worth asking

**These are instructions, not blanks.** Ask each one. The possible answers below are authored, with what each would rule in or out, so a reply can be recognised rather than interpreted.

### 8. How long after a send does the truth arrive, and is that longer than the gap between retrains?

**Ask:** How long after a send does the truth arrive, and is that longer than the gap between retrains? If it is, what stand-in is the business willing to defend in the meantime?

What the answers would mean:

- **Days. We know inside a week whether it stuck.** → Comfortable. Retrain weekly on settled outcomes and skip the stand-in entirely; this is the case where the training table is simply true.
- **Six to eight weeks before it is final. The recent rows are always half-counted.** → Longer than most retrain cadences, so the most recent rows are always incomplete. Train on the settled window and count the unsettled rows rather than reading them as noes. *(floor Tier 1 — Serverless, In-Warehouse)*
- **A full quarter before it is final, and some of them never settle at all.** → Now a stand-in is unavoidable, and the risk is that the stand-in quietly becomes the objective. Name it, name what it stands for, and check the two still agree once a quarter. *(floor Tier 2 — Distributed & Custom ML)*
- **I could not tell you. Nobody here has measured the gap from send to outcome.** → One query against the send log and the outcome table. Until it is run, the retraining cadence in any design document is a guess wearing a number.

### 9. Who are the people the join loses?

**Ask:** Who are the people the join loses? If the ones that match skew older and better off, dropping the rest bakes that into every model built on top of it.

What the answers would mean:

- **We checked, and there is nothing systematic in who drops out.** → Unusual, and worth seeing the check. If it holds, the missing share is a capacity problem rather than a fairness one, and it can be priced instead of argued about.
- **They skew younger and lower value. The least engaged are the ones we lose.** → The model never sees the people it most needs to learn from, and every accuracy number is quoted on the easy half of the base. Report the measure on both halves from day one. *(floor Tier 2 — Distributed & Custom ML)*
- **Nobody has ever looked. I could not tell you which way it goes.** → A half-hour query. Comparing age, tenure and value between the matched and the unmatched is the cheapest credibility available on this problem, and it is almost never been run.
- **I am not sure we even count the ones that drop out. They just vanish.** → Worse than a skew. If rows disappear inside a join nobody logs, the number is invisible and so is the trend. Count them at the join before profiling them.

## 5. Not worth asking yet

Each of these is gated behind a branch that is not open. They are listed so the absence is legible: they were not forgotten, they were ruled out.

- **Is who-gets-what worked out on a schedule, or claimed at the moment of sending?** — closed by *Where the offer appears, and when it is picked* → “One slot on the page, and it has to be filled while the person waits”.
- **Can five to ten in every hundred people be held back from every offer from now on, and who has the authority to give up that revenue?** — closed by *Whether anyone was ever randomly held back* → “Yes. The flag sits on the person, not just on the campaign”.
- **Until a held-back group exists, will they accept a matched comparison — people nobody contacted, picked to look like the ones who were?** — closed by *Whether anyone was ever randomly held back* → “Yes. The flag sits on the person, not just on the campaign”.

## 6. What is being suggested, and why the alternatives are out

### Tier 3 — Real-Time & Specialised

A slot that has to be filled before the page paints

- **What it is:** Pub/Sub → Dataflow session state → Memorystore for Valkey → Cloud Run rules-then-rank service → the slot
- **Google Cloud & open-weight options at this rung:** Pub/Sub, Dataflow, Memorystore for Valkey, Bigtable, Cloud Run, Agent Platform endpoints
- **What it carries:** Nothing carries from Tier 2. Build moves off Spark, scoring moves off the nightly table; the overnight cold path still runs underneath.
- **Why here:** The rules fire before the model, so the ranker only ever sees a shortlist of under ten. A small tree model fits inside forty milliseconds of a two-hundred millisecond page, and what the person did sixty seconds ago is a Memorystore for Valkey read, not a join.
- **Where it breaks:** The rules layer is the system, and usually nobody owns it. Anonymous sessions carry no history, so the slot needs a fallback that is not the model. And the log only records what the rules allowed, so tomorrow’s training data is shaped by today’s rules.
- **What would change the call:** A month of slot logs shows scoring at request time beating last night’s plan by less than the warm Cloud Run instances cost — drop back to the plan.

Peers at the same price, with a different shape:

- **A ranker that spends traffic to learn** — Cloud Run policy service → Bigtable arm state → Pub/Sub outcomes → nightly replay in BigQuery

#### Architecture Decision Record (ADR) Matrix

A scenario-aware evaluation of the ladder against this customer's constraints. Where an adjacent tier serves as a viable A/B benchmark or a Phase 2 evolution, that role is explicitly called out:

| Rung | Role in this Engagement | Architecture & Stance | Deciding Constraint & Trade-off |
| --- | --- | --- | --- |
| Tier 0 — Out of the Box | Ruled out (Insufficient) | Build the audience in SQL, activate it this week. | Below the floor (Tier 3 — Real-Time & Specialised), set by Where the offer appears, and when it is picked, One plan that shares out limited offers and a decision taken while the person waits. |
| Tier 1 — Serverless, In-Warehouse | Ruled out (Insufficient) | One query scores everyone, ranked on what it is worth. | Below the floor (Tier 3 — Real-Time & Specialised), set by Where the offer appears, and when it is picked, One plan that shares out limited offers and a decision taken while the person waits. |
| Tier 2 — Distributed & Custom ML | **Adjacent Lower Tier (A/B Benchmark)** | Match at scale, then share the offers out under limits. Lower complexity and operational overhead. | Below the floor (Tier 3 — Real-Time & Specialised), set by Where the offer appears, and when it is picked, One plan that shares out limited offers and a decision taken while the person waits. Viable as an A/B comparator to quantify the performance/accuracy lift of Tier 3 — Real-Time & Specialised. |
| Tier 3 — Real-Time & Specialised | **Primary Baseline (MVP)** | A slot that has to be filled before the page paints. Fits all bounded constraints. | Selected target. Fits floor (Tier 3 — Real-Time & Specialised). Wins: The rules fire before the model, so the ranker only ever sees a shortlist of under ten. A small tree model fits inside forty milliseconds of a two-hundred millisecond page, and what the person did sixty seconds ago is a Memorystore for Valkey read, not a join. |

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

- Tier 0 — Out of the Box — Build the audience in SQL, activate it this week. Out: the floor is Tier 3 — Real-Time & Specialised — Where the offer appears, and when it is picked, One plan that shares out limited offers and a decision taken while the person waits.
- Tier 1 — Serverless, In-Warehouse — One query scores everyone, ranked on what it is worth. Out: the floor is Tier 3 — Real-Time & Specialised — Where the offer appears, and when it is picked, One plan that shares out limited offers and a decision taken while the person waits.
- Tier 2 — Distributed & Custom ML — Match at scale, then share the offers out under limits. Out: the floor is Tier 3 — Real-Time & Specialised — Where the offer appears, and when it is picked, One plan that shares out limited offers and a decision taken while the person waits.

**Below the rung sit the calls no rung makes for you.** The tier does not settle these, and a design that has not stated them has not been made. Nothing on the page asks for them, so they travel unanswered.

- **What one row is** — One person against one offer, as at the date somebody would be contacted. Not one row per person with the winner already chosen — the times a person was shown an offer and said nothing are half the training table.
  Options: One person, one offer, one send date · Person times offer times channel · The account or the household
- **What goes in beside the past** — What the person looked like as at the send date, what the ad-side join adds, and whether the offer carries attributes of its own. This is where it leaks: a holdings field updated on acceptance predicts acceptance perfectly.
  Options: The person’s own record, as at that date · Add the joined ad-side behaviour · Add attributes of the offer itself
- **One fit, one each, or one per group** — Twelve offers can be twelve fits, one fit with offer identity as an input column, or one fit per family. All three are one query at Tier 1, and the rung does not choose between them.
  Options: One fit per offer · One pooled fit, offer as a column · One fit per family of offers
- **Which methods get a run** — Only the chance of yes is fitted; the ranking over it is arithmetic. So the shortlist is a plain regression, a boosted tree, and — only where somebody was randomly left out — two fits differenced into the yeses the offer caused.
  Options: Logistic regression per offer · Boosted trees · A caused-yes pair
- **How you would know** — Hold back by send date, not by row: the same person is contacted more than once in a week, and a random split trains on the earlier contact and tests on the later. Then a measure that survives three takers in a hundred.
  Options: The last weeks of sends, held back · A random split of the rows · A live group left out at random
- **What tuning is worth** — Three things want the same week: features rebuilt as at the send date, a value per offer finance will defend, and a settings search. The first two pay more and both need a signature, which is why the third gets done.
  Options: Leave the defaults · Search the settings · Spend it on levelling instead
- **One winner, or several combined** — The multiplying happens before any averaging: chance times value times eligibility is already a stack of parts. Where averaging does come up it comes up twelve times, so an average per offer is twenty-four artefacts to level.
  Options: One model per offer, picked on the split · Average a regression and a tree · A difference of two fits, not an average
- **Making the numbers agree** — Add up what twelve independent rankings would send and it exceeds the units on hand, the monthly quota and what fulfilment can service. Score each person alone and the best offer is oversold by day three.
  Options: Let the ranking run, cut it off at the limit · One solve over the shared pool · Take the solve’s price per offer back down

**Dataset for the build.** Every workshop build runs on public or shipped tables:

- **Source:** BigQuery public tables
- **Tables:** `bigquery-public-data.thelook_ecommerce.orders`, `bigquery-public-data.thelook_ecommerce.order_items`, `bigquery-public-data.thelook_ecommerce.products`, `bigquery-public-data.thelook_ecommerce.events`, `bigquery-public-data.thelook_ecommerce.users`
- **Grain & size:** One row per line item (user_id, order_id, product_id, created_at, sale_price); 181,313 items across 125,000 orders and 80,000 buyers linked to 29,120 products and 2.43M browser events.
- **Target / label:** Next-30-day category purchase indicator weighted by unit gross margin (sale_price - cost).
- **Tier 1 / Tier 2 build:** Hard Tier 1 scores per-category purchase likelihood with BOOSTED_TREE_CLASSIFIER (checked against a TabFM AI.PREDICT floor) times retail_price - cost under a contact limit; Tier 2 adds a Python linear-programme allocator.
- **Caveat:** Synthetic data with no logged control group; ranking by raw purchase likelihood without retail_price - cost fills every slot with low-margin basics.
- **Setup / verify:** `bq head -n 5 bigquery-public-data:thelook_ecommerce.order_items`
- **Agent skills (`bigquery-data-science` & Data Agent Kit):** `uvx bigquery-data-science lookup AI.PREDICT # BQDS: AI.KEY_DRIVERS, BOOSTED_TREE_CLASSIFIER, LOGISTIC_REG, TRANSFORM, ML.EXPLAIN_PREDICT | Data Agent Kit: bigquery-ai-ml, dataform-bigquery, bigquery-graph-query, ml-best-practices, gcp-spark`

**The ladder, for reference.** No site is needed to read the tiers above.

- **Tier 0 — Out of the Box** — A model somebody else trained already answers the question. Nothing to fit, nothing to provision, and the bill starts on the first query. The most senior move in the room is often to say so.
- **Tier 1 — Serverless, In-Warehouse** — Bring the model to the data. No cluster, no container, no serving stack. SQL is the interface.
- **Tier 2 — Distributed & Custom ML** — The transformation or the model outgrew SQL. Bring distributed compute to the data, keep the storage where it is.
- **Tier 3 — Real-Time & Specialised** — A hard SLA or a custom objective justifies owning the stack. You are now engineering a system, not training a model.
- **Tier 4 — Hardening for High-Stakes Operation** — Not a rung you buy. It is what changes about a system already at Tier 1, 2 or 3 once being wrong is expensive, contested or unsafe — and what changes is different for every problem in Discovery.

## 7. POC Data Discovery & Profiling Contract (Tier 3)

- **Source Tables (`bigquery-region: "US"`):** `bigquery-public-data.thelook_ecommerce.orders`, `bigquery-public-data.thelook_ecommerce.order_items`, `bigquery-public-data.thelook_ecommerce.products`, `bigquery-public-data.thelook_ecommerce.events`, `bigquery-public-data.thelook_ecommerce.users`
- **Grain & Target:** One row per line item (user_id, order_id, product_id, created_at, sale_price); 181,313 items across 125,000 orders and 80,000 buyers linked to 29,120 products and 2.43M browser events. | Next-30-day category purchase indicator weighted by unit gross margin (sale_price - cost).
- **Data Caveat to Profile & Guard Against:** Synthetic data with no logged control group; ranking by raw purchase likelihood without retail_price - cost fills every slot with low-margin basics.
- **Verification Command:** `bq head -n 5 bigquery-public-data:thelook_ecommerce.order_items`

---

### The same thing, for a program to read

```json
{
  "problem": "next-best-offer",
  "ldap": "classroom-repo",
  "version": 1,
  "served_at": "2026-10-27T00:00:00Z",
  "binding": {
    "offer": "offer",
    "person": "person",
    "slot": "slot",
    "channel": "channel",
    "consumer": "activation system",
    "response": "acceptance",
    "gatekeeper": "rule owner",
    "system": "source system"
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
      "bigquery-public-data.thelook_ecommerce.orders",
      "bigquery-public-data.thelook_ecommerce.order_items",
      "bigquery-public-data.thelook_ecommerce.products",
      "bigquery-public-data.thelook_ecommerce.events",
      "bigquery-public-data.thelook_ecommerce.users"
    ],
    "grain": "One row per line item (user_id, order_id, product_id, created_at, sale_price); 181,313 items across 125,000 orders and 80,000 buyers linked to 29,120 products and 2.43M browser events.",
    "label": "Next-30-day category purchase indicator weighted by unit gross margin (sale_price - cost).",
    "rungs": "Hard Tier 1 scores per-category purchase likelihood with BOOSTED_TREE_CLASSIFIER (checked against a TabFM AI.PREDICT floor) times retail_price - cost under a contact limit; Tier 2 adds a Python linear-programme allocator.",
    "caveat": "Synthetic data with no logged control group; ranking by raw purchase likelihood without retail_price - cost fills every slot with low-margin basics.",
    "setup": "bq head -n 5 bigquery-public-data:thelook_ecommerce.order_items",
    "skills": "uvx bigquery-data-science lookup AI.PREDICT # BQDS: AI.KEY_DRIVERS, BOOSTED_TREE_CLASSIFIER, LOGISTIC_REG, TRANSFORM, ML.EXPLAIN_PREDICT | Data Agent Kit: bigquery-ai-ml, dataform-bigquery, bigquery-graph-query, ml-best-practices, gcp-spark"
  },
  "questions": [
    {
      "id": "offers",
      "order": 1,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "catalogue",
        "heard": "Thousands. It is the whole catalogue, and most of it is open to anyone.",
        "means": "At this size the first step is no longer ranking, it is narrowing. That is a different problem and the catalog has one for it; this method picks up again once something has cut the field to a shortlist.",
        "floor": 2,
        "ceiling": null
      }
    },
    {
      "id": "objective",
      "order": 2,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "incremental",
        "heard": "Only the yeses we actually caused. Plenty of them would have bought anyway.",
        "means": "A question about cause, not about prediction. It needs a group left out at random while the campaign ran — ask next whether one exists, because without it this is not buildable at any rung.",
        "floor": 2,
        "ceiling": null
      }
    },
    {
      "id": "label",
      "order": 3,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "retained",
        "heard": "Still there after ninety days. A yes that cancels in month two was never one.",
        "means": "What the business actually cares about, and the hardest thing to train on, because a quarter of waiting sits between the send and the truth. Expect a stand-in, and be explicit about what it stands for.",
        "floor": 1,
        "ceiling": null
      }
    },
    {
      "id": "match",
      "order": 4,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "partial",
        "heard": "Roughly half, and it has been slipping. It was better six months ago.",
        "means": "Half the base is invisible to every model downstream, and a falling share looks exactly like the offers getting worse. Which half is missing matters more than the number does.",
        "floor": 2,
        "ceiling": null
      }
    },
    {
      "id": "caps",
      "order": 5,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "hard",
        "heard": "Yes. We have a fixed number of units on some and a monthly quota on others.",
        "means": "This stops being scoring and becomes sharing a limited thing out. Ranking each person alone oversells the best offer by day three, and no amount of model quality repairs that.",
        "floor": 2,
        "ceiling": null
      }
    },
    {
      "id": "holdout",
      "order": 6,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "per-person",
        "heard": "Yes. The flag sits on the person, not just on the campaign.",
        "means": "Rare and valuable. This is the one input that makes an answer about cause possible, and having it person by person means it can be joined to features rather than read off a campaign report.",
        "floor": 2,
        "ceiling": null
      }
    },
    {
      "id": "surface",
      "order": 7,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "live",
        "heard": "One slot on the page, and it has to be filled while the person waits.",
        "means": "A deadline, not a workload. Forty milliseconds inside a page budget means the ranking runs over a shortlist the rules already cut, and the interesting engineering is the shortlist rather than the model.",
        "floor": 3,
        "ceiling": null
      }
    },
    {
      "id": "delay",
      "order": 8,
      "status": "open",
      "options": [
        "Days. We know inside a week whether it stuck.",
        "Six to eight weeks before it is final. The recent rows are always half-counted.",
        "A full quarter before it is final, and some of them never settle at all.",
        "I could not tell you. Nobody here has measured the gap from send to outcome."
      ]
    },
    {
      "id": "unmatched",
      "order": 9,
      "status": "open",
      "options": [
        "We checked, and there is nothing systematic in who drops out.",
        "They skew younger and lower value. The least engaged are the ones we lose.",
        "Nobody has ever looked. I could not tell you which way it goes.",
        "I am not sure we even count the ones that drop out. They just vanish."
      ]
    },
    {
      "id": "enforce",
      "order": 10,
      "status": "not_in_play",
      "gate": "More than one channel can reach the same person at once",
      "closed_by": {
        "question": "surface",
        "answer": "live"
      }
    },
    {
      "id": "start",
      "order": 11,
      "status": "not_in_play",
      "gate": "No randomised history exists, so a group must be held back now",
      "closed_by": {
        "question": "holdout",
        "answer": "per-person"
      }
    },
    {
      "id": "matched",
      "order": 12,
      "status": "not_in_play",
      "gate": "No randomised history exists, so a group must be held back now",
      "closed_by": {
        "question": "holdout",
        "answer": "per-person"
      }
    }
  ],
  "conflicts": [
    "One plan that shares out limited offers and a decision taken while the person waits. The plan is a snapshot; spent live it needs a ledger every channel writes to. Take that on at Tier 3, or push the plan down as a price per offer and let the live ranker read prices."
  ],
  "still_to_ask": [
    "delay",
    "unmatched"
  ],
  "counts": {
    "answered": 7,
    "stale": 0,
    "open": 2,
    "not_in_play": 3,
    "dropped": 0
  },
  "schema_version": "1.0",
  "problem_id": "next-best-offer",
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
