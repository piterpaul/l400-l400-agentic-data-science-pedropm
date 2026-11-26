---
schema_version: "1.0"
problem_id: "recommender"
target_tier: 0
recommended_rung: 0
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

- **Floor: Tier 0 — Out of the Box** — set by Has the existing row ever been switched off, Whose number the row has to move
- **Ceiling:** nothing heard yet rules out the top of the ladder

> **Together, not apart.** Nobody has measured what the existing row is worth and nobody agrees whose number it should move. Two teams will read the same result as a win and a loss. Neither is a modelling problem and no rung fixes either. The first deliverable is switching the row off and naming an objective.

## 3. What was asked, and what it steered

### 4. Has the existing row ever been switched off

**Asked:** Has anybody ever turned the row off for a slice of people, to see what happens without it?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Never. It has always just been there.
- **Which means:** The normal answer, and the first build is this measurement rather than a model. A recency-weighted popularity list is embarrassingly hard to beat, and finding that out costs one query and a fortnight.
- **Bounds:** not below Tier 0 — Out of the Box
- **For the brief:** Incumbent never switched off. First deliverable is that test plus the popularity baseline.
- **Why it was asked:** Whether there is any number to beat. Without it every later claim of improvement is measured against a thing whose own value has never been established.
- **What it forecloses:** Closes the whole evaluation argument. It also closes the funding argument, because the gap to a free list is the honest size of the prize.

### 6. Whose number the row has to move

**Asked:** Whose number does this row have to move — revenue, profit after costs, engagement, or shifting things you are overstocked on — and who is allowed to overrule it?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Depends who you ask. Merchandising and growth want different things.
- **Which means:** The honest answer and a genuine finding. Nothing above the first rung can be blessed while it is true, because two teams will read the same result as a win and a loss.
- **Bounds:** not below Tier 0 — Out of the Box
- **For the brief:** Objective contested between teams. Resolve ownership before anything learned is blessed.
- **Why it was asked:** The objective and the constraint layer together. These four order the same items differently, and the team that owns the pixels is bonused on exactly one of them.
- **What it forecloses:** Closes the objective question and the entire override conversation, which is otherwise discovered late and rewrites the serving path.

## 4. Still worth asking

**These are instructions, not blanks.** Ask each one. The possible answers below are authored, with what each would rule in or out, so a reply can be recognised rather than interpreted.

### 1. More like this, goes with this, or a step up

**Ask:** When this row works, what has it shown — another one like the thing they are looking at, something that goes with it, or something better than it?

**Why it matters:** The objective, the training pairs and whether a similarity model is the right shape at all. These three want opposite things, and one model told to serve all three serves none of them well.

What the answers would mean:

- **Another one like it. People land on the wrong thing and we want to keep them.** → The cheapest of the three and the one a content space answers directly. Watch the near-duplicate trap: without a spread rule the row fills with five colours of the same thing and reads as broken. *(floor Tier 1 — Serverless, In-Warehouse)*
- **Something that goes with it. We sell the tent, we want to sell the pegs.** → This is the one that pays, and it is learned from what people actually buy together rather than from descriptions. Two things that go together are rarely similar, so a meaning space alone will not find them. *(floor Tier 1 — Serverless, In-Warehouse)*
- **Something better. We want the more expensive one in front of them.** → Not a model, and saying so early buys credibility. It is a lookup filtered to a higher price than the anchor and sorted by margin, over a set somebody agreed is genuinely substitutable. The judgement is the scarce part, not the maths. *(floor Tier 1 — Serverless, In-Warehouse)*
- **Whatever performs. We have not thought about it that way.** → The most common answer and the reason these projects wander. Get one named before anything is built, because the three produce different training data and there is no metric that tells you afterwards which one you built.

### 2. Where the row sits, and what is on the page

**Ask:** Where exactly does this row appear, and is there already something on that page it should relate to?

**Why it matters:** Whether the system needs a thing to start from or has to invent one. A model built around a starting item cannot fill a page that has none, and that is usually where the traffic turns out to be.

What the answers would mean:

- **On the page for a specific thing, underneath it.** → The easy case, and the one where being signed in barely matters. One item space answers it, and you can ship value to people you cannot identify. *(floor Tier 1 — Serverless, In-Warehouse)*
- **The home page or the app feed. There is nothing on the page yet.** → The hard case, because the row has to be built out of the person rather than the page. It needs either a profile worth having or the last few minutes of the visit, which is a different rung entirely. *(floor Tier 2 — Distributed & Custom ML)*
- **Both, and honestly the feed is the one the business cares about.** → Then scope the two separately, because they are two builds. The anchored one funds itself quickly and the open one is where the argument about identification and freshness has to be had. *(floor Tier 2 — Distributed & Custom ML)*
- **Wherever the platform puts it, I think.** → Count impressions per placement before designing anything. The answer routinely turns out to be that the revenue sits in a slot nobody scoped, and it costs one query to find out.

### 3. What counts as it having worked

**Ask:** Of the things you record — looked at it, added it, bought it, kept it, bought it again — which ones mean the row did its job?

**Why it matters:** The label, and therefore what the whole system will optimise. Every rung above the first is trained to move whichever of these you name, and they order the same items differently.

What the answers would mean:

- **A click. That is what the platform reports and what we are judged on.** → Workable and the most common starting point, but it rewards a thumbnail rather than a good recommendation. Get purchase joined on before anyone is bonused on this number. *(floor Tier 1 — Serverless, In-Warehouse)*
- **A purchase, obviously.** → The right instinct, and it hides a trap in categories where things come back. A purchase that is returned is not a success, and a model trained on raw purchases learns to push whatever photographs well. *(floor Tier 1 — Serverless, In-Warehouse)*
- **A purchase that is not sent back, and ideally bought again.** → The strongest answer in this problem and unusual to hear. It arrives late, which is the cost: the label matures over the return window, so training always runs on a period old enough to be trustworthy. *(floor Tier 1 — Serverless, In-Warehouse)*
- **Nobody has written that down.** → Then write it down in the room. It takes ten minutes, it is a business decision rather than a technical one, and leaving it open means a data scientist will quietly make it alone.

### 5. How fast the catalog changes

**Ask:** How many new things appear in a normal week, and how long does a typical one stay before it is gone?

**Why it matters:** Whether learning from behaviour is possible at all. If most of what you sell has been there a month, nothing has enough history, and the no-history path stops being an edge case and becomes the main path.

What the answers would mean:

- **It barely changes. Same range, season after season.** → The comfortable case. Behaviour accumulates, and the items people interact with are the ones you have history for. Something with no history is a genuine edge case here and can be handled by a rule. *(floor Tier 1 — Serverless, In-Warehouse)*
- **Constantly. Half of what we sell now was not there two months ago.** → Then history is the exception and descriptions and pictures are the substrate. A model that needs interactions will look excellent in testing and cover a fraction of what is live. *(floor Tier 1 — Serverless, In-Warehouse)*
- **It comes back. Same things return each year under new codes.** → Worth catching, because it looks like a brand-new thing to the system and like the same old thing to the customer. Mapping returning codes to their predecessor recovers history nobody knew they had. *(floor Tier 1 — Serverless, In-Warehouse)*
- **I could not give you a number.** → One query over the catalog gives both numbers in an afternoon, and they decide more of the architecture than anything else in this section. Do not design before you have them.

### 7. What must never be shown, and where

**Ask:** Is there anything that must never appear in this row for certain people or in certain places — and can that change during the day?

**Why it matters:** Where the rule runs. A rule that is fixed can be applied when the row is built; a rule that moves during the day has to run at the moment somebody looks, which is a different architecture and a different bill.

What the answers would mean:

- **Nothing much. If it is in the catalog we can show it.** → Unusually clean, and it means a row worked out overnight and read by key is a complete answer. Say so plainly, because it removes the most expensive component people assume they need. *(floor Tier 1 — Serverless, In-Warehouse)*
- **Age ratings and where we can ship. It does not change hour to hour.** → Still precomputable, as long as the rule is applied while the row is being built rather than as it is served. Build it into the shortlist, not into the page template. *(floor Tier 1 — Serverless, In-Warehouse)*
- **Whether we have it, in that particular place, right now.** → The expensive answer, and the one that quietly changes the project. An overnight row cannot know this, and trimming the shortlist as it is served is what leaves three tiles where six should be. *(floor Tier 2 — Distributed & Custom ML)*
- **There are rules. I do not know where they are enforced.** → Find out where they run today, because the answer is usually the page template, and that is exactly the arrangement that empties rows without telling anybody.

### 8. How old the row is allowed to be

**Ask:** Can this row be worked out overnight, or does it have to react to something they did a few minutes ago?

**Why it matters:** Whether there is a model in the request path at all. An overnight answer read by key is the cheapest serving architecture there is, and most placements do not need anything else.

What the answers would mean:

- **Overnight is fine. Nobody would notice it was twelve hours old.** → Then the row is a lookup by key and there is no model in the request path. This is the answer that saves the most money in this problem and the one people are most reluctant to give. *(floor Tier 1 — Serverless, In-Warehouse)*
- **What they looked at a minute ago has to change it.** → This is a real rung up, and it is worth asking what evidence exists for it. A month of records will show whether the last few actions predict better than the overnight profile, and often the gap is smaller than the bill. *(floor Tier 3 — Real-Time & Specialised)*
- **The row can be old. New things appearing cannot wait three days.** → A useful split, because these are two different clocks and only one of them is expensive. Streaming new items into the index is far cheaper than making every row live. *(floor Tier 2 — Distributed & Custom ML)*
- **Real-time, I assume. Is that not the point?** → The default assumption and rarely tested. Ask which of the two clocks they mean — how fresh the person is, or how fast a new thing appears — because the second is cheap and the first is not.

## 5. Not worth asking yet

Each of these is gated behind a branch that is not open. They are listed so the absence is legible: they were not forgotten, they were ruled out.

- **When the rules cut the list down, how often does the row end up with fewer things in it than there are spaces, and what does the page do then?** — needs “The row can come back with fewer things than there are slots”, which nothing answered has opened.
- **What share of what gets bought comes back, and are those taken back off before anybody counts a success?** — needs “A meaningful share of what is bought comes back”, which nothing answered has opened.
- **What share of what gets shown in a normal week is stuff with almost nothing recorded against it — fewer than ten interactions, say?** — needs “Most of what is live has almost no history”, which nothing answered has opened.
- **If the row came back with five versions of nearly the same thing, would anybody notice before a customer did?** — needs “The row can fill with near-identical things”, which nothing answered has opened.
- **Who decides that one thing is genuinely a better version of another, rather than just a more expensive one?** — needs “Somebody has to agree what is genuinely a step up”, which nothing answered has opened.
- **How much worse is the row allowed to get in exchange for making more money on it, and who signed off on that number?** — closed by *Whose number the row has to move* → “Depends who you ask. Merchandising and growth want different things”.
- **How many times a day does this row get shown, and how small an improvement would still be worth having?** — needs “A learned model needs proving on live traffic”, which nothing answered has opened.

## 6. What is being suggested, and why the alternatives are out

### Tier 0 — Out of the Box

Measure what the row you already have is worth

- **What it is:** Impression and click records → holdout in BigQuery → popularity baseline → Conversational Analytics
- **Google Cloud & open-weight options at this rung:** BigQuery, AI.PREDICT, Conversational Analytics, AI Commerce Search
- **Why here:** Almost every placement already has something in it and almost nobody has switched it off. Run that first: a recency-weighted popular list beats plenty of them, and at a few thousand items a curated set of rules beats anything you could train.
- **Where it breaks:** Rules cover the familiar and leave everything else on one default row. No personalization and no path for new items beyond somebody pinning them by hand. The audit needs what was shown recorded, not just what was clicked, so sprint one is instrumentation.
- **What would move it up:** The test shows both the curated rules and the default row losing to simple popularity outside the best-known few hundred items, and that is where the catalog is growing.

Peers at the same price, with a different shape:

- **Buy the models rather than build them** — Catalog and event feeds → AI Commerce Search recommendation models → serving config per placement

#### Architecture Decision Record (ADR) Matrix

A scenario-aware evaluation of the ladder against this customer's constraints. Where an adjacent tier serves as a viable A/B benchmark or a Phase 2 evolution, that role is explicitly called out:

| Rung | Role in this Engagement | Architecture & Stance | Deciding Constraint & Trade-off |
| --- | --- | --- | --- |
| Tier 0 — Out of the Box | **Primary Baseline (MVP)** | Measure what the row you already have is worth. Fits all bounded constraints. | Selected target. Fits floor (Tier 0 — Out of the Box). Wins: Almost every placement already has something in it and almost nobody has switched it off. Run that first: a recency-weighted popular list beats plenty of them, and at a few thousand items a curated set of rules beats anything you could train. |
| Tier 1 — Serverless, In-Warehouse | **Adjacent Higher Tier (Phase 2 Evolution)** | Learn from behaviour and from descriptions, both in SQL. Higher freshness, lower latency, or specialised modeling. | Inside the range, but nothing heard requires it yet. Step-up trigger: The test shows both the curated rules and the default row losing to simple popularity outside the best-known few hundred items, and that is where the catalog is growing. Propose as Phase 2 expansion once this condition is met. |
| Tier 2 — Distributed & Custom ML | In range, not required | A learned shortlist, with the ordering split out behind it. | Not ruled out, but nothing heard in the room requires it. |
| Tier 3 — Real-Time & Specialised | In range, not required | The last few minutes become the question you ask. | Not ruled out, but nothing heard in the room requires it. |

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

- Tier 1 — Serverless, In-Warehouse — Learn from behaviour and from descriptions, both in SQL. Out: not ruled out, but nothing heard in the room requires it.
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

## 7. POC Data Discovery & Profiling Contract (Tier 0)

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
    "floor": 0,
    "ceiling": 0,
    "clash": false
  },
  "recommended_rung": 0,
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
      "status": "open",
      "keystone": true,
      "options": [
        "Another one like it. People land on the wrong thing and we want to keep them.",
        "Something that goes with it. We sell the tent, we want to sell the pegs.",
        "Something better. We want the more expensive one in front of them.",
        "Whatever performs. We have not thought about it that way."
      ]
    },
    {
      "id": "surface",
      "order": 2,
      "status": "open",
      "keystone": true,
      "options": [
        "On the page for a specific thing, underneath it.",
        "The home page or the app feed. There is nothing on the page yet.",
        "Both, and honestly the feed is the one the business cares about.",
        "Wherever the platform puts it, I think."
      ]
    },
    {
      "id": "positives",
      "order": 3,
      "status": "open",
      "keystone": true,
      "options": [
        "A click. That is what the platform reports and what we are judged on.",
        "A purchase, obviously.",
        "A purchase that is not sent back, and ideally bought again.",
        "Nobody has written that down."
      ]
    },
    {
      "id": "heldout",
      "order": 4,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "never",
        "heard": "Never. It has always just been there.",
        "means": "The normal answer, and the first build is this measurement rather than a model. A recency-weighted popularity list is embarrassingly hard to beat, and finding that out costs one query and a fortnight.",
        "floor": 0,
        "ceiling": null
      }
    },
    {
      "id": "turnover",
      "order": 5,
      "status": "open",
      "keystone": true,
      "options": [
        "It barely changes. Same range, season after season.",
        "Constantly. Half of what we sell now was not there two months ago.",
        "It comes back. Same things return each year under new codes.",
        "I could not give you a number."
      ]
    },
    {
      "id": "owner",
      "order": 6,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "contested",
        "heard": "Depends who you ask. Merchandising and growth want different things.",
        "means": "The honest answer and a genuine finding. Nothing above the first rung can be blessed while it is true, because two teams will read the same result as a win and a loss.",
        "floor": 0,
        "ceiling": null
      }
    },
    {
      "id": "eligibility",
      "order": 7,
      "status": "open",
      "keystone": true,
      "options": [
        "Nothing much. If it is in the catalog we can show it.",
        "Age ratings and where we can ship. It does not change hour to hour.",
        "Whether we have it, in that particular place, right now.",
        "There are rules. I do not know where they are enforced."
      ]
    },
    {
      "id": "staleness",
      "order": 8,
      "status": "open",
      "keystone": true,
      "options": [
        "Overnight is fine. Nobody would notice it was twelve hours old.",
        "What they looked at a minute ago has to change it.",
        "The row can be old. New things appearing cannot wait three days.",
        "Real-time, I assume. Is that not the point?"
      ]
    },
    {
      "id": "shortfall",
      "order": 9,
      "status": "not_in_play",
      "gate": "The row can come back with fewer things than there are slots",
      "closed_by": null
    },
    {
      "id": "returns",
      "order": 10,
      "status": "not_in_play",
      "gate": "A meaningful share of what is bought comes back",
      "closed_by": null
    },
    {
      "id": "thin",
      "order": 11,
      "status": "not_in_play",
      "gate": "Most of what is live has almost no history",
      "closed_by": null
    },
    {
      "id": "duplicates",
      "order": 12,
      "status": "not_in_play",
      "gate": "The row can fill with near-identical things",
      "closed_by": null
    },
    {
      "id": "substitutable",
      "order": 13,
      "status": "not_in_play",
      "gate": "Somebody has to agree what is genuinely a step up",
      "closed_by": null
    },
    {
      "id": "tradeoff",
      "order": 14,
      "status": "not_in_play",
      "gate": "Money is traded against relevance in the ordering",
      "closed_by": {
        "question": "owner",
        "answer": "contested"
      }
    },
    {
      "id": "traffic",
      "order": 15,
      "status": "not_in_play",
      "gate": "A learned model needs proving on live traffic",
      "closed_by": null
    }
  ],
  "conflicts": [
    "Nobody has measured what the existing row is worth and nobody agrees whose number it should move. Two teams will read the same result as a win and a loss. Neither is a modelling problem and no rung fixes either. The first deliverable is switching the row off and naming an objective."
  ],
  "still_to_ask": [
    "relation",
    "surface",
    "positives",
    "turnover",
    "eligibility",
    "staleness"
  ],
  "counts": {
    "answered": 2,
    "stale": 0,
    "open": 6,
    "not_in_play": 7,
    "dropped": 0
  },
  "schema_version": "1.0",
  "problem_id": "recommender",
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
