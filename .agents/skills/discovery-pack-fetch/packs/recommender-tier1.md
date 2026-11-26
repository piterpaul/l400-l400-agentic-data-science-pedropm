---
schema_version: "1.0"
problem_id: "recommender"
target_tier: 1
recommended_rung: 1
source: "built-in-classroom-pack"
---

# Discovery pack — Product Recommendation & Item Affinity

`recommender` · recorded by **classroom-repo** · version 1 · served 2026-10-27T00:00:00Z

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

> **Head of E-commerce, specialty outdoor retailer — 4,000 SKUs, platform-hosted storefront** — Our “you may also like” row is whatever the platform ships. We want a real AI recommender that pushes people to the better tent, not another of the same tent.
>
> **Director of Personalization, grocery & general merchandise — 60k SKUs, 8M loyalty members** — We want people-also-bought across the basket, it has to favour higher-margin lines, and it must never show anything that is out of stock in the customer’s store.
>
> **Principal ML Engineer, streaming marketplace — 2M titles, 40M monthly users, two-tower in production** — Recommendations are rebuilt nightly. The home feed has no idea what you watched twenty minutes ago, and new titles take three days to surface. We need real-time.

**Vocabulary is unbound.** The nouns below are the method's neutral words, not this customer's — treat them as placeholders and confirm the real terms early.

**The five specifics.**

- **How many, of the thing being predicted** — *not captured. Ask.*
- **How much history there is, and how much arrives** — *not captured. Ask.*
- **The deadline the run has to hit** — *not captured. Ask.*
- **What being wrong costs, per event or per year** — *not captured. Ask.*
- **Who owns the decision, and who would run this** — *not captured. Ask.*

## 2. Where discovery landed

- **Floor: Tier 1 — Serverless, In-Warehouse** — set by More like this, goes with this, or a step up, Where the row sits, and what is on the page, What counts as it having worked, Has the existing row ever been switched off, How fast the catalog changes, Whose number the row has to move, What must never be shown, and where, How old the row is allowed to be
- **Ceiling:** nothing heard yet rules out the top of the ladder

## 3. What was asked, and what it steered

### 1. More like this, goes with this, or a step up

**Asked:** When this row works, what has it shown — another one like the thing they are looking at, something that goes with it, or something better than it?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Another one like it. People land on the wrong thing and we want to keep them.
- **Which means:** The cheapest of the three and the one a content space answers directly. Watch the near-duplicate trap: without a spread rule the row fills with five colours of the same thing and reads as broken.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Relation is substitution. Content space plus a spread rule; near-duplicates are the failure mode.
- **Why it was asked:** The objective, the training pairs and whether a similarity model is the right shape at all. These three want opposite things, and one model told to serve all three serves none of them well.
- **What it forecloses:** Closes the model-family argument. “Something better” is not a learned relation, so naming it here removes every question about which algorithm ranks upsells.

### 2. Where the row sits, and what is on the page

**Asked:** Where exactly does this row appear, and is there already something on that page it should relate to?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** On the page for a specific thing, underneath it.
- **Which means:** The easy case, and the one where being signed in barely matters. One item space answers it, and you can ship value to people you cannot identify.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Anchored placement. Item-to-item lookup; identification is not on the critical path.
- **Why it was asked:** Whether the system needs a thing to start from or has to invent one. A model built around a starting item cannot fill a page that has none, and that is usually where the traffic turns out to be.
- **What it forecloses:** Closes the personalization scope argument. With a starting item most of the value is reachable without knowing who the person is at all.

### 3. What counts as it having worked

**Asked:** Of the things you record — looked at it, added it, bought it, kept it, bought it again — which ones mean the row did its job?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** A click. That is what the platform reports and what we are judged on.
- **Which means:** Workable and the most common starting point, but it rewards a thumbnail rather than a good recommendation. Get purchase joined on before anyone is bonused on this number.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Positive is click. Known bias toward thumbnails; join purchase before setting targets.
- **Why it was asked:** The label, and therefore what the whole system will optimise. Every rung above the first is trained to move whichever of these you name, and they order the same items differently.
- **What it forecloses:** Closes the loss-function debate and most of the metric debate with it. Once the positive is named, the question of what to measure online is nearly answered.

### 4. Has the existing row ever been switched off

**Asked:** Has anybody ever turned the row off for a slice of people, to see what happens without it?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Yes, and we know what it is worth.
- **Which means:** Rare, and it changes the conversation entirely: you are optimising a known quantity rather than guessing. Ask what the comparison was against, because a comparison against nothing is not the same as one against a simple list.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Incumbent value measured. Confirm the comparison used a popularity list, not an empty slot.
- **Why it was asked:** Whether there is any number to beat. Without it every later claim of improvement is measured against a thing whose own value has never been established.
- **What it forecloses:** Closes the whole evaluation argument. It also closes the funding argument, because the gap to a free list is the honest size of the prize.

### 5. How fast the catalog changes

**Asked:** How many new things appear in a normal week, and how long does a typical one stay before it is gone?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** It barely changes. Same range, season after season.
- **Which means:** The comfortable case. Behaviour accumulates, and the items people interact with are the ones you have history for. Something with no history is a genuine edge case here and can be handled by a rule.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Stable catalog. Behaviour-based methods viable; things with no history handled by a routing rule.
- **Why it was asked:** Whether learning from behaviour is possible at all. If most of what you sell has been there a month, nothing has enough history, and the no-history path stops being an edge case and becomes the main path.
- **What it forecloses:** Closes what to do with things that have no history, most of the model-family question, and the argument about how often to retrain, all at once.

### 6. Whose number the row has to move

**Asked:** Whose number does this row have to move — revenue, profit after costs, engagement, or shifting things you are overstocked on — and who is allowed to overrule it?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Revenue. More of what we sell, that is it.
- **Which means:** The simplest to build and the easiest to game with things people were going to buy anyway. Pair it early with a measurement of what would have happened without the row.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Objective is revenue. Guard against crediting purchases that needed no prompting.
- **Why it was asked:** The objective and the constraint layer together. These four order the same items differently, and the team that owns the pixels is bonused on exactly one of them.
- **What it forecloses:** Closes the objective question and the entire override conversation, which is otherwise discovered late and rewrites the serving path.

### 7. What must never be shown, and where

**Asked:** Is there anything that must never appear in this row for certain people or in certain places — and can that change during the day?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Nothing much. If it is in the catalog we can show it.
- **Which means:** Unusually clean, and it means a row worked out overnight and read by key is a complete answer. Say so plainly, because it removes the most expensive component people assume they need.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** No live eligibility constraint. Precomputed rows are a complete serving answer.
- **Why it was asked:** Where the rule runs. A rule that is fixed can be applied when the row is built; a rule that moves during the day has to run at the moment somebody looks, which is a different architecture and a different bill.
- **What it forecloses:** Closes the serving-tier argument, and with it most of the freshness discussion. It is also half of the pair that decides whether this engagement is configuration or engineering.

### 8. How old the row is allowed to be

**Asked:** Can this row be worked out overnight, or does it have to react to something they did a few minutes ago?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Overnight is fine. Nobody would notice it was twelve hours old.
- **Which means:** Then the row is a lookup by key and there is no model in the request path. This is the answer that saves the most money in this problem and the one people are most reluctant to give.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Overnight refresh acceptable. Precompute and serve by key; no request-path inference.
- **Why it was asked:** Whether there is a model in the request path at all. An overnight answer read by key is the cheapest serving architecture there is, and most placements do not need anything else.
- **What it forecloses:** Closes latency, most of the infrastructure conversation, and the cost model. Make the customer justify leaving the cheap answer rather than assuming they have.

## 4. Still worth asking

**These are instructions, not blanks.** Ask each one. The possible answers below are authored, with what each would rule in or out, so a reply can be recognised rather than interpreted.

### 12. If the row came back with five versions of nearly the same thing, would anybody notice before a customer did?

**Ask:** If the row came back with five versions of nearly the same thing, would anybody notice before a customer did?

**Why it matters:** Whether a spread rule is a requirement or an afterthought. It is applied after scoring, so it changes what a good score is worth and has to be agreed before anybody tunes one.

What the answers would mean:

- **We already have a rule. One per brand, roughly.** → Good, and it needs writing into the build rather than living in somebody’s head. Ask what it costs: every spread rule trades measured relevance for a row that looks sensible.
- **No rule. It has just not come up.** → It will, on the first demo, and it is the failure that makes a room lose confidence fastest. Agree the rule before the demo rather than after it. *(floor Tier 1 — Serverless, In-Warehouse)*
- **I assume the platform handles that.** → Rarely true, and easy to check by looking at ten live pages. Do that before the next meeting; it takes five minutes and it is often the most persuasive thing you bring.

## 5. Not worth asking yet

Each of these is gated behind a branch that is not open. They are listed so the absence is legible: they were not forgotten, they were ruled out.

- **When the rules cut the list down, how often does the row end up with fewer things in it than there are spaces, and what does the page do then?** — closed by *What must never be shown, and where* → “Nothing much. If it is in the catalog we can show it”.
- **What share of what gets bought comes back, and are those taken back off before anybody counts a success?** — closed by *What counts as it having worked* → “A click. That is what the platform reports and what we are judged on”.
- **What share of what gets shown in a normal week is stuff with almost nothing recorded against it — fewer than ten interactions, say?** — closed by *How fast the catalog changes* → “It barely changes. Same range, season after season”.
- **Who decides that one thing is genuinely a better version of another, rather than just a more expensive one?** — closed by *More like this, goes with this, or a step up* → “Another one like it. People land on the wrong thing and we want to keep them”.
- **How much worse is the row allowed to get in exchange for making more money on it, and who signed off on that number?** — closed by *Whose number the row has to move* → “Revenue. More of what we sell, that is it”.
- **How many times a day does this row get shown, and how small an improvement would still be worth having?** — closed by *Where the row sits, and what is on the page* → “On the page for a specific thing, underneath it”.

## 6. What is being suggested, and why the alternatives are out

### Tier 1 — Serverless, In-Warehouse

Learn from behaviour and from descriptions, both in SQL

- **What it is:** MATRIX_FACTORIZATION on a reservation → ML.RECOMMEND into a scored table; AI.GENERATE_EMBEDDING + VECTOR_SEARCH
- **Google Cloud & open-weight options at this rung:** MATRIX_FACTORIZATION, ML.RECOMMEND, ML.WEIGHTS, AI.GENERATE_EMBEDDING, VECTOR_SEARCH, AI.EMBED, Data Science Agent
- **What it carries:** Build carried from Tier 0. What changed is the surface: a trained factorization now gets scored into a BigQuery table.
- **Why here:** Factorization over what people did, not what they said learns pairings no description holds, and the factors from ML.WEIGHTS serve item-to-item through VECTOR_SEARCH. The upsell is that lookup with a price floor. The Data Science Agent builds the time split.
- **Where it breaks:** CREATE MODEL needs an Enterprise reservation; on-demand can serve but not train it. An unseen item does not error; it scores at the intercept, so every new one ranks the same for everybody. NO_SPLIT is the default, so reported numbers are training numbers.
- **What would move it up:** Price, availability and time of day change what should be shown and the model cannot see any of them: its input is three columns and there is no preprocessing step to add a fourth.

#### Architecture Decision Record (ADR) Matrix

A scenario-aware evaluation of the ladder against this customer's constraints. Where an adjacent tier serves as a viable A/B benchmark or a Phase 2 evolution, that role is explicitly called out:

| Rung | Role in this Engagement | Architecture & Stance | Deciding Constraint & Trade-off |
| --- | --- | --- | --- |
| Tier 0 — Out of the Box | **Adjacent Lower Tier (A/B Benchmark)** | Measure what the row you already have is worth. Lower complexity and operational overhead. | Below the floor (Tier 1 — Serverless, In-Warehouse), set by More like this, goes with this, or a step up, Where the row sits, and what is on the page, What counts as it having worked, Has the existing row ever been switched off, How fast the catalog changes, Whose number the row has to move, What must never be shown, and where, How old the row is allowed to be. Viable as an A/B comparator to quantify the performance/accuracy lift of Tier 1 — Serverless, In-Warehouse. |
| Tier 1 — Serverless, In-Warehouse | **Primary Baseline (MVP)** | Learn from behaviour and from descriptions, both in SQL. Fits all bounded constraints. | Selected target. Fits floor (Tier 1 — Serverless, In-Warehouse). Wins: Factorization over what people did, not what they said learns pairings no description holds, and the factors from ML.WEIGHTS serve item-to-item through VECTOR_SEARCH. The upsell is that lookup with a price floor. The Data Science Agent builds the time split. |
| Tier 2 — Distributed & Custom ML | **Adjacent Higher Tier (Phase 2 Evolution)** | A learned shortlist, with the ordering split out behind it. Higher freshness, lower latency, or specialised modeling. | Inside the range, but nothing heard requires it yet. Step-up trigger: Price, availability and time of day change what should be shown and the model cannot see any of them: its input is three columns and there is no preprocessing step to add a fourth. Propose as Phase 2 expansion once this condition is met. |
| Tier 3 — Real-Time & Specialised | In range, not required | The last few minutes become the question you ask. | Not ruled out, but nothing heard in the room requires it. |

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

- Tier 0 — Out of the Box — Measure what the row you already have is worth. Out: the floor is Tier 1 — Serverless, In-Warehouse — More like this, goes with this, or a step up, Where the row sits, and what is on the page, What counts as it having worked, Has the existing row ever been switched off, How fast the catalog changes, Whose number the row has to move, What must never be shown, and where, How old the row is allowed to be.

**Above it, and why that is theatre here.**

- Tier 2 — Distributed & Custom ML — A learned shortlist, with the ordering split out behind it. Out: not ruled out, but nothing heard in the room requires it.
- Tier 3 — Real-Time & Specialised — The last few minutes become the question you ask. Out: not ruled out, but nothing heard in the room requires it.

**Below the rung sit the calls no rung makes for you.** The tier does not settle these, and a design that has not stated them has not been made. Nothing on the page asks for them, so they travel unanswered.

- **What one row is** — A row is a pair, and which pair is the choice: one customer with one item, or one anchor with one item. The second needs nobody identified, which decides the build where most visits are people you cannot name.
  Options: customer and item · anchor and item · One impression, with what else was shown
- **What goes in beside the past** — Whether the fit sees interactions alone, descriptions and pictures beside them, or live things like price and availability. The Tier 1 statement takes three columns and has no step where a fourth could be added.
  Options: Behaviour alone · Descriptions and pictures beside it · Live signals read at request time
- **One fit, one each, or one per group** — One fit over everybody, one small fit per item fanned out, or one per relation — more like this, goes with this and a step up want opposite things from the same records.
  Options: One fit over everything · One small fit per item · One fit per relation
- **Which methods get a run** — Three things that all produce a row: an unlearned list — popularity, or rules somebody already maintains — factorization on interactions, and a two-sided model. The first is nearly free and is the honest bar for the other two.
  Options: A popular list, or the rules you have · Factorization on behaviour · A two-sided model
- **How you would know** — Two proofs, not one. Offline, a cut by time rather than at random, because a later interaction by the same customer sitting on the training side flatters everything. Online, the existing row switched off for a slice.
  Options: Replay against a future window · Switch the existing row off for a slice · A second row beside the existing row
- **What tuning is worth** — The label outranks the settings here by a distance. Which interaction counts as success, and whether things sent back are taken off it, moves the ordering further than any search over a factorization will.
  Options: Fix the label, keep the defaults · Search the settings · Correct for the slot a thing sat in
- **One winner, or several combined** — Combining here is not averaging models. It is one shortlist drawn from several sources — behaviour, descriptions, the anchor lookup — and the step that merges them fits nothing and is owned by a person.
  Options: One source · Union with a quota per source · Merge by position across sources
- **Making the numbers agree** — Six slots, and several separate claims on them: a quota per source, the spread rule, eligibility rules, a coverage floor, and anything promised a fixed count of impressions. Set by different people, they do not add to six.
  Options: Let the ordering win, cut afterwards · Make the claims add up to the slots · Hold the promise over the week, not the row

**Dataset for the build.** Every workshop build runs on public or shipped tables:

- **Source:** BigQuery public tables + temporary Enterprise reservation
- **Tables:** `bigquery-public-data.thelook_ecommerce.order_items`, `bigquery-public-data.thelook_ecommerce.products`, `bigquery-public-data.thelook_ecommerce.events`
- **Grain & size:** One row per user-item interaction (user_id, product_id, created_at); 181,313 purchases across 80,000 buyers (average 2.27 items per buyer) and 29,120 catalogue products.
- **Target / label:** Held-out next-purchase hit rate in top 10 recommendations on a temporal split.
- **Tier 1 / Tier 2 build:** Hard Tier 1 compares MATRIX_FACTORIZATION + ML.RECOMMEND (temporary 100-slot Enterprise reservation) against a 2,500-item vector slice via AI.GENERATE_EMBEDDING + VECTOR_SEARCH and a top-seller floor; Tier 2 fits a two-tower pipeline in Python.
- **Caveat:** MATRIX_FACTORIZATION requires an Enterprise slot reservation (created for the run and deleted in teardown), and with 2.27 purchases per buyer matrix factorisation alone underperforms catalogue vector similarity on sparse users.
- **Setup / verify:** `bq mk --reservation --project_id=$GOOGLE_CLOUD_PROJECT --location=US --slots=0 --autoscale_max_slots=100 --edition=ENTERPRISE rec-workshop-res`
- **Agent skills (`bigquery-data-science` & Data Agent Kit):** `uvx bigquery-data-science lookup MATRIX_FACTORIZATION # BQDS: ML.RECOMMEND, AI.GENERATE_EMBEDDING, AI.SIMILARITY, VECTOR_SEARCH, BOOSTED_TREE_CLASSIFIER | Data Agent Kit: bigquery-ai-ml, dataform-bigquery, ml-best-practices, gcp-dataflow, bigtable-basics`

**The ladder, for reference.** No site is needed to read the tiers above.

- **Tier 0 — Out of the Box** — A model somebody else trained already answers the question. Nothing to fit, nothing to provision, and the bill starts on the first query. The most senior move in the room is often to say so.
- **Tier 1 — Serverless, In-Warehouse** — Bring the model to the data. No cluster, no container, no serving stack. SQL is the interface.
- **Tier 2 — Distributed & Custom ML** — The transformation or the model outgrew SQL. Bring distributed compute to the data, keep the storage where it is.
- **Tier 3 — Real-Time & Specialised** — A hard SLA or a custom objective justifies owning the stack. You are now engineering a system, not training a model.
- **Tier 4 — Hardening for High-Stakes Operation** — Not a rung you buy. It is what changes about a system already at Tier 1, 2 or 3 once being wrong is expensive, contested or unsafe — and what changes is different for every problem in Discovery.

## 7. POC Data Discovery & Profiling Contract (Tier 1)

- **Source Tables (`bigquery-region: "US"`):** `bigquery-public-data.thelook_ecommerce.order_items`, `bigquery-public-data.thelook_ecommerce.products`, `bigquery-public-data.thelook_ecommerce.events`
- **Grain & Target:** One row per user-item interaction (user_id, product_id, created_at); 181,313 purchases across 80,000 buyers (average 2.27 items per buyer) and 29,120 catalogue products. | Held-out next-purchase hit rate in top 10 recommendations on a temporal split.
- **Data Caveat to Profile & Guard Against:** MATRIX_FACTORIZATION requires an Enterprise slot reservation (created for the run and deleted in teardown), and with 2.27 purchases per buyer matrix factorisation alone underperforms catalogue vector similarity on sparse users.
- **Verification Command:** `bq mk --reservation --project_id=$GOOGLE_CLOUD_PROJECT --location=US --slots=0 --autoscale_max_slots=100 --edition=ENTERPRISE rec-workshop-res`

---

### The same thing, for a program to read

```json
{
  "problem": "recommender",
  "ldap": "classroom-repo",
  "version": 1,
  "served_at": "2026-10-27T00:00:00Z",
  "binding": {
    "candidate": "item",
    "audience": "customer",
    "surface": "placement",
    "anchor": "anchor",
    "relation": "relation",
    "interaction": "interaction",
    "incumbent": "existing row",
    "eligibility": "eligibility rule",
    "owner": "slot owner"
  },
  "range": {
    "floor": 1,
    "ceiling": 1,
    "clash": false
  },
  "recommended_rung": 1,
  "data": {
    "source": "BigQuery public tables + temporary Enterprise reservation",
    "tables": [
      "bigquery-public-data.thelook_ecommerce.order_items",
      "bigquery-public-data.thelook_ecommerce.products",
      "bigquery-public-data.thelook_ecommerce.events"
    ],
    "grain": "One row per user-item interaction (user_id, product_id, created_at); 181,313 purchases across 80,000 buyers (average 2.27 items per buyer) and 29,120 catalogue products.",
    "label": "Held-out next-purchase hit rate in top 10 recommendations on a temporal split.",
    "rungs": "Hard Tier 1 compares MATRIX_FACTORIZATION + ML.RECOMMEND (temporary 100-slot Enterprise reservation) against a 2,500-item vector slice via AI.GENERATE_EMBEDDING + VECTOR_SEARCH and a top-seller floor; Tier 2 fits a two-tower pipeline in Python.",
    "caveat": "MATRIX_FACTORIZATION requires an Enterprise slot reservation (created for the run and deleted in teardown), and with 2.27 purchases per buyer matrix factorisation alone underperforms catalogue vector similarity on sparse users.",
    "setup": "bq mk --reservation --project_id=$GOOGLE_CLOUD_PROJECT --location=US --slots=0 --autoscale_max_slots=100 --edition=ENTERPRISE rec-workshop-res",
    "skills": "uvx bigquery-data-science lookup MATRIX_FACTORIZATION # BQDS: ML.RECOMMEND, AI.GENERATE_EMBEDDING, AI.SIMILARITY, VECTOR_SEARCH, BOOSTED_TREE_CLASSIFIER | Data Agent Kit: bigquery-ai-ml, dataform-bigquery, ml-best-practices, gcp-dataflow, bigtable-basics"
  },
  "questions": [
    {
      "id": "relation",
      "order": 1,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "similar",
        "heard": "Another one like it. People land on the wrong thing and we want to keep them.",
        "means": "The cheapest of the three and the one a content space answers directly. Watch the near-duplicate trap: without a spread rule the row fills with five colours of the same thing and reads as broken.",
        "floor": 1,
        "ceiling": null
      }
    },
    {
      "id": "surface",
      "order": 2,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "anchored",
        "heard": "On the page for a specific thing, underneath it.",
        "means": "The easy case, and the one where being signed in barely matters. One item space answers it, and you can ship value to people you cannot identify.",
        "floor": 1,
        "ceiling": null
      }
    },
    {
      "id": "positives",
      "order": 3,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "clicks",
        "heard": "A click. That is what the platform reports and what we are judged on.",
        "means": "Workable and the most common starting point, but it rewards a thumbnail rather than a good recommendation. Get purchase joined on before anyone is bonused on this number.",
        "floor": 1,
        "ceiling": null
      }
    },
    {
      "id": "heldout",
      "order": 4,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "yes",
        "heard": "Yes, and we know what it is worth.",
        "means": "Rare, and it changes the conversation entirely: you are optimising a known quantity rather than guessing. Ask what the comparison was against, because a comparison against nothing is not the same as one against a simple list.",
        "floor": 1,
        "ceiling": null
      }
    },
    {
      "id": "turnover",
      "order": 5,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "stable",
        "heard": "It barely changes. Same range, season after season.",
        "means": "The comfortable case. Behaviour accumulates, and the items people interact with are the ones you have history for. Something with no history is a genuine edge case here and can be handled by a rule.",
        "floor": 1,
        "ceiling": null
      }
    },
    {
      "id": "owner",
      "order": 6,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "revenue",
        "heard": "Revenue. More of what we sell, that is it.",
        "means": "The simplest to build and the easiest to game with things people were going to buy anyway. Pair it early with a measurement of what would have happened without the row.",
        "floor": 1,
        "ceiling": null
      }
    },
    {
      "id": "eligibility",
      "order": 7,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "none",
        "heard": "Nothing much. If it is in the catalog we can show it.",
        "means": "Unusually clean, and it means a row worked out overnight and read by key is a complete answer. Say so plainly, because it removes the most expensive component people assume they need.",
        "floor": 1,
        "ceiling": null
      }
    },
    {
      "id": "staleness",
      "order": 8,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "overnight",
        "heard": "Overnight is fine. Nobody would notice it was twelve hours old.",
        "means": "Then the row is a lookup by key and there is no model in the request path. This is the answer that saves the most money in this problem and the one people are most reluctant to give.",
        "floor": 1,
        "ceiling": null
      }
    },
    {
      "id": "shortfall",
      "order": 9,
      "status": "not_in_play",
      "gate": "The row can come back with fewer things than there are slots",
      "closed_by": {
        "question": "eligibility",
        "answer": "none"
      }
    },
    {
      "id": "returns",
      "order": 10,
      "status": "not_in_play",
      "gate": "A meaningful share of what is bought comes back",
      "closed_by": {
        "question": "positives",
        "answer": "clicks"
      }
    },
    {
      "id": "thin",
      "order": 11,
      "status": "not_in_play",
      "gate": "Most of what is live has almost no history",
      "closed_by": {
        "question": "turnover",
        "answer": "stable"
      }
    },
    {
      "id": "duplicates",
      "order": 12,
      "status": "open",
      "options": [
        "We already have a rule. One per brand, roughly.",
        "No rule. It has just not come up.",
        "I assume the platform handles that."
      ]
    },
    {
      "id": "substitutable",
      "order": 13,
      "status": "not_in_play",
      "gate": "Somebody has to agree what is genuinely a step up",
      "closed_by": {
        "question": "relation",
        "answer": "similar"
      }
    },
    {
      "id": "tradeoff",
      "order": 14,
      "status": "not_in_play",
      "gate": "Money is traded against relevance in the ordering",
      "closed_by": {
        "question": "owner",
        "answer": "revenue"
      }
    },
    {
      "id": "traffic",
      "order": 15,
      "status": "not_in_play",
      "gate": "A learned model needs proving on live traffic",
      "closed_by": {
        "question": "surface",
        "answer": "anchored"
      }
    }
  ],
  "conflicts": [],
  "still_to_ask": [
    "duplicates"
  ],
  "counts": {
    "answered": 8,
    "stale": 0,
    "open": 1,
    "not_in_play": 6,
    "dropped": 0
  },
  "schema_version": "1.0",
  "problem_id": "recommender",
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
