---
schema_version: "1.0"
problem_id: "recommender"
target_tier: 3
recommended_rung: 3
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

- **Floor: Tier 3 — Real-Time & Specialised** — set by How old the row is allowed to be
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

- **Heard:** The home page or the app feed. There is nothing on the page yet.
- **Which means:** The hard case, because the row has to be built out of the person rather than the page. It needs either a profile worth having or the last few minutes of the visit, which is a different rung entirely.
- **Bounds:** not below Tier 2 — Distributed & Custom ML
- **For the brief:** Anchorless placement. Needs a customer profile or in-visit behaviour; this is where cost lives.
- **Why it was asked:** Whether the system needs a thing to start from or has to invent one. A model built around a starting item cannot fill a page that has none, and that is usually where the traffic turns out to be.
- **What it forecloses:** Closes the personalization scope argument. With a starting item most of the value is reachable without knowing who the person is at all.

### 3. What counts as it having worked

**Asked:** Of the things you record — looked at it, added it, bought it, kept it, bought it again — which ones mean the row did its job?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** A purchase, obviously.
- **Which means:** The right instinct, and it hides a trap in categories where things come back. A purchase that is returned is not a success, and a model trained on raw purchases learns to push whatever photographs well.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Positive is purchase. Confirm whether returns are netted out before training.
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

- **Heard:** Constantly. Half of what we sell now was not there two months ago.
- **Which means:** Then history is the exception and descriptions and pictures are the substrate. A model that needs interactions will look excellent in testing and cover a fraction of what is live.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** High turnover. Content and image based space is the primary path, not the fallback.
- **Why it was asked:** Whether learning from behaviour is possible at all. If most of what you sell has been there a month, nothing has enough history, and the no-history path stops being an edge case and becomes the main path.
- **What it forecloses:** Closes what to do with things that have no history, most of the model-family question, and the argument about how often to retrain, all at once.

### 6. Whose number the row has to move

**Asked:** Whose number does this row have to move — revenue, profit after costs, engagement, or shifting things you are overstocked on — and who is allowed to overrule it?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Profit. Revenue is easy to move by pushing cheap things.
- **Which means:** A second objective on top of a model trained on behaviour, which is a re-sort rather than a different model. The number that matters is how much relevance you are willing to trade, and it belongs to a person, not a coefficient.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Objective is margin. Apply as a re-sort with an agreed relevance trade, not inside the loss.
- **Why it was asked:** The objective and the constraint layer together. These four order the same items differently, and the team that owns the pixels is bonused on exactly one of them.
- **What it forecloses:** Closes the objective question and the entire override conversation, which is otherwise discovered late and rewrites the serving path.

### 7. What must never be shown, and where

**Asked:** Is there anything that must never appear in this row for certain people or in certain places — and can that change during the day?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Whether we have it, in that particular place, right now.
- **Which means:** The expensive answer, and the one that quietly changes the project. An overnight row cannot know this, and trimming the shortlist as it is served is what leaves three tiles where six should be.
- **Bounds:** not below Tier 2 — Distributed & Custom ML
- **For the brief:** Eligibility varies by place and hour. Rule must run inside the lookup; precomputed rows fail.
- **Why it was asked:** Where the rule runs. A rule that is fixed can be applied when the row is built; a rule that moves during the day has to run at the moment somebody looks, which is a different architecture and a different bill.
- **What it forecloses:** Closes the serving-tier argument, and with it most of the freshness discussion. It is also half of the pair that decides whether this engagement is configuration or engineering.

### 8. How old the row is allowed to be

**Asked:** Can this row be worked out overnight, or does it have to react to something they did a few minutes ago?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** What they looked at a minute ago has to change it.
- **Which means:** This is a real rung up, and it is worth asking what evidence exists for it. A month of records will show whether the last few actions predict better than the overnight profile, and often the gap is smaller than the bill.
- **Bounds:** not below Tier 3 — Real-Time & Specialised
- **For the brief:** In-visit reaction required. Verify the gain against the overnight profile before committing.
- **Why it was asked:** Whether there is a model in the request path at all. An overnight answer read by key is the cheapest serving architecture there is, and most placements do not need anything else.
- **What it forecloses:** Closes latency, most of the infrastructure conversation, and the cost model. Make the customer justify leaving the cheap answer rather than assuming they have.

## 4. Still worth asking

**These are instructions, not blanks.** Ask each one. The possible answers below are authored, with what each would rule in or out, so a reply can be recognised rather than interpreted.

### 9. When the rules cut the list down, how often does the row end up with fewer things in it than there are spaces, and what does the page do then?

**Ask:** When the rules cut the list down, how often does the row end up with fewer things in it than there are spaces, and what does the page do then?

**Why it matters:** Whether the filtering has to move inside the lookup. It is the one failure here that no relevance measure can see, because a half-empty row scores perfectly on everything the model reports.

What the answers would mean:

- **We measure it. It happens on a few percent of pages.** → Then somebody is already looking, which is rarer than it sounds. Take the number as the budget: it decides whether the rule moves inside the lookup now or after the next peak. *(floor Tier 2 — Distributed & Custom ML)*
- **I do not think anyone has ever looked.** → One query over what was shown answers it, and the answer is routinely far worse than anybody expects in the thin places. This is the cheapest credibility you can buy in this problem. *(floor Tier 2 — Distributed & Custom ML)*
- **It falls back to a generic list, so nobody notices.** → Then the fallback is doing more work than the model and nobody is counting how often. Measure the share of impressions it serves, because it is often most of them in exactly the places that matter. *(floor Tier 2 — Distributed & Custom ML)*
- **I would not know where to see that.** → It needs what was shown to be recorded, not just what was clicked. If that does not exist, this becomes the first thing to fix, because nothing else here can be measured without it.

### 10. What share of what gets bought comes back, and are those taken back off before anybody counts a success?

**Ask:** What share of what gets bought comes back, and are those taken back off before anybody counts a success?

**Why it matters:** Whether the label is honest. In categories where a third of orders return, training on raw purchases teaches the system to push whatever photographs best, and the number goes up while the business gets worse.

What the answers would mean:

- **We take them off. Returns are joined back to the order.** → The right setup and unusual. The cost is patience: the label is not final until the return window closes, so training deliberately runs on an older period than feels natural. *(floor Tier 1 — Serverless, In-Warehouse)*
- **No. A sale is a sale as far as the reporting goes.** → Then the model will learn the wrong thing and the reporting will agree with it. Joining returns back is a query, not a project, and it is the highest-value hour available in this problem. *(floor Tier 1 — Serverless, In-Warehouse)*
- **Returns are negligible in what we sell.** → Fine, and worth confirming per category rather than overall, because one category with heavy returns will quietly dominate what the model learns to push.
- **I do not know if that join exists.** → Check whether returns can be tied back to the original order at all. In some systems they cannot, and that is a finding worth surfacing early rather than at model review.

### 11. What share of what gets shown in a normal week is stuff with almost nothing recorded against it — fewer than ten interactions, say?

**Ask:** What share of what gets shown in a normal week is stuff with almost nothing recorded against it — fewer than ten interactions, say?

**Why it matters:** Whether the content path is the main build or the fallback. It also decides whether a failure that nothing reports is already happening in production.

What the answers would mean:

- **Most of it. That is just what our catalog looks like.** → Then build the content and picture path first and treat behaviour as the enrichment. Doing it the other way round produces a system that tests beautifully and covers a third of what is live. *(floor Tier 1 — Serverless, In-Warehouse)*
- **A meaningful slice, mostly the newest things.** → A routing rule rather than a rebuild: under a threshold, answer from the content space. Make the switchover explicit and logged, because it is a rule somebody has to own rather than a model output. *(floor Tier 1 — Serverless, In-Warehouse)*
- **We have new things going up all the time and no idea how they do.** → Worth checking for a specific failure: some methods return a default score for something they have never seen, without any error, so every new item ranks identically for everybody. It shows up as a flat row, not as an alert. *(floor Tier 1 — Serverless, In-Warehouse)*
- **No idea what that share is.** → One query against what was shown, joined to interaction counts. It is usually larger than the room expects and it reframes which model family is the main one.

### 12. If the row came back with five versions of nearly the same thing, would anybody notice before a customer did?

**Ask:** If the row came back with five versions of nearly the same thing, would anybody notice before a customer did?

**Why it matters:** Whether a spread rule is a requirement or an afterthought. It is applied after scoring, so it changes what a good score is worth and has to be agreed before anybody tunes one.

What the answers would mean:

- **We already have a rule. One per brand, roughly.** → Good, and it needs writing into the build rather than living in somebody’s head. Ask what it costs: every spread rule trades measured relevance for a row that looks sensible.
- **No rule. It has just not come up.** → It will, on the first demo, and it is the failure that makes a room lose confidence fastest. Agree the rule before the demo rather than after it. *(floor Tier 1 — Serverless, In-Warehouse)*
- **I assume the platform handles that.** → Rarely true, and easy to check by looking at ten live pages. Do that before the next meeting; it takes five minutes and it is often the most persuasive thing you bring.

### 14. How much worse is the row allowed to get in exchange for making more money on it, and who signed off on that number?

**Ask:** How much worse is the row allowed to get in exchange for making more money on it, and who signed off on that number?

**Why it matters:** Whether the second objective is a decision or an accident. Somebody is going to set that balance; the only question is whether it is set in the open or inside a model nobody reads.

What the answers would mean:

- **There is a number and the commercial team owns it.** → Then it belongs in the ordering step as a visible weight with that person’s name on it, and in the monitoring as a number that can be shown to have moved. *(floor Tier 1 — Serverless, In-Warehouse)*
- **No number. We just want it to favour the better lines.** → That is the accident. Propose the smallest honest version: rank normally, then re-sort the shortlist by margin, and report what relevance it cost. A number nobody set is a number nobody can defend. *(floor Tier 1 — Serverless, In-Warehouse)*
- **That would be a conversation above me.** → Then have it before building, and bring the shape of the answer rather than the question. A worked example of two orderings side by side gets a decision faster than a request for a number.

### 15. How many times a day does this row get shown, and how small an improvement would still be worth having?

**Ask:** How many times a day does this row get shown, and how small an improvement would still be worth having?

**Why it matters:** Whether anything learned can ever be proven here. Plenty of placements cannot settle a small improvement inside a quarter, and that is worth knowing before the model is built rather than after.

What the answers would mean:

- **Hundreds of thousands of times a day.** → Then live comparison is available and should be the gate on every launch. It also means the smaller rungs can be settled quickly, so ship in short steps rather than one big one. *(floor Tier 2 — Distributed & Custom ML)*
- **A few thousand. It is not a big site.** → Then a small improvement cannot be proven inside a sensible time, and building something that needs proving is a poor trade. Stay low on the ladder and spend the money on coverage instead.
- **I could get that number.** → Get it, along with how often the row converts today. Those two numbers decide how long any test has to run, and that duration is usually the thing that kills the ambitious version.

## 5. Not worth asking yet

Each of these is gated behind a branch that is not open. They are listed so the absence is legible: they were not forgotten, they were ruled out.

- **Who decides that one thing is genuinely a better version of another, rather than just a more expensive one?** — closed by *More like this, goes with this, or a step up* → “Another one like it. People land on the wrong thing and we want to keep them”.

## 6. What is being suggested, and why the alternatives are out

### Tier 3 — Real-Time & Specialised

The last few minutes become the question you ask

- **What it is:** Item feed → Agent Retrieval data object writes; Cloud Run, Memorystore for Valkey → query tower → filters → the row
- **Google Cloud & open-weight options at this rung:** Cloud Run, Agent Platform endpoints, Agent Retrieval, Memorystore for Valkey, BigQuery
- **What it carries:** Both axes carried from Tier 2. Everything that changes is retrieval: a live collection, filters on availability and price band, and the visit sequence in Memorystore for Valkey.
- **Why here:** What somebody looked at thirty seconds ago is in the question, not in last night’s profile. Availability as a field and price band as a number are filters applied inside the lookup, so “only what we have” is a write, not a retrain.
- **Where it breaks:** Freshness moves the cost to the write path: every stock or price change is a data object update, so a busy feed is a busy write path to size. Filters only see fields the collection carries, so decide availability and price band before launch.
- **What would change the call:** A month of records shows the in-visit question beating the overnight one by less than the live collection and the Valkey session cache cost to run.

#### Architecture Decision Record (ADR) Matrix

A scenario-aware evaluation of the ladder against this customer's constraints. Where an adjacent tier serves as a viable A/B benchmark or a Phase 2 evolution, that role is explicitly called out:

| Rung | Role in this Engagement | Architecture & Stance | Deciding Constraint & Trade-off |
| --- | --- | --- | --- |
| Tier 0 — Out of the Box | Ruled out (Insufficient) | Measure what the row you already have is worth. | Below the floor (Tier 3 — Real-Time & Specialised), set by How old the row is allowed to be. |
| Tier 1 — Serverless, In-Warehouse | Ruled out (Insufficient) | Learn from behaviour and from descriptions, both in SQL. | Below the floor (Tier 3 — Real-Time & Specialised), set by How old the row is allowed to be. |
| Tier 2 — Distributed & Custom ML | **Adjacent Lower Tier (A/B Benchmark)** | A learned shortlist, with the ordering split out behind it. Lower complexity and operational overhead. | Below the floor (Tier 3 — Real-Time & Specialised), set by How old the row is allowed to be. Viable as an A/B comparator to quantify the performance/accuracy lift of Tier 3 — Real-Time & Specialised. |
| Tier 3 — Real-Time & Specialised | **Primary Baseline (MVP)** | The last few minutes become the question you ask. Fits all bounded constraints. | Selected target. Fits floor (Tier 3 — Real-Time & Specialised). Wins: What somebody looked at thirty seconds ago is in the question, not in last night’s profile. Availability as a field and price band as a number are filters applied inside the lookup, so “only what we have” is a write, not a retrain. |

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

- Tier 0 — Out of the Box — Measure what the row you already have is worth. Out: the floor is Tier 3 — Real-Time & Specialised — How old the row is allowed to be.
- Tier 1 — Serverless, In-Warehouse — Learn from behaviour and from descriptions, both in SQL. Out: the floor is Tier 3 — Real-Time & Specialised — How old the row is allowed to be.
- Tier 2 — Distributed & Custom ML — A learned shortlist, with the ordering split out behind it. Out: the floor is Tier 3 — Real-Time & Specialised — How old the row is allowed to be.

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

## 7. POC Data Discovery & Profiling Contract (Tier 3)

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
    "floor": 3,
    "ceiling": 3,
    "clash": false
  },
  "recommended_rung": 3,
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
        "key": "open",
        "heard": "The home page or the app feed. There is nothing on the page yet.",
        "means": "The hard case, because the row has to be built out of the person rather than the page. It needs either a profile worth having or the last few minutes of the visit, which is a different rung entirely.",
        "floor": 2,
        "ceiling": null
      }
    },
    {
      "id": "positives",
      "order": 3,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "purchase",
        "heard": "A purchase, obviously.",
        "means": "The right instinct, and it hides a trap in categories where things come back. A purchase that is returned is not a success, and a model trained on raw purchases learns to push whatever photographs well.",
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
        "key": "fast",
        "heard": "Constantly. Half of what we sell now was not there two months ago.",
        "means": "Then history is the exception and descriptions and pictures are the substrate. A model that needs interactions will look excellent in testing and cover a fraction of what is live.",
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
        "key": "margin",
        "heard": "Profit. Revenue is easy to move by pushing cheap things.",
        "means": "A second objective on top of a model trained on behaviour, which is a re-sort rather than a different model. The number that matters is how much relevance you are willing to trade, and it belongs to a person, not a coefficient.",
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
        "key": "local",
        "heard": "Whether we have it, in that particular place, right now.",
        "means": "The expensive answer, and the one that quietly changes the project. An overnight row cannot know this, and trimming the shortlist as it is served is what leaves three tiles where six should be.",
        "floor": 2,
        "ceiling": null
      }
    },
    {
      "id": "staleness",
      "order": 8,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "session",
        "heard": "What they looked at a minute ago has to change it.",
        "means": "This is a real rung up, and it is worth asking what evidence exists for it. A month of records will show whether the last few actions predict better than the overnight profile, and often the gap is smaller than the bill.",
        "floor": 3,
        "ceiling": null
      }
    },
    {
      "id": "shortfall",
      "order": 9,
      "status": "open",
      "options": [
        "We measure it. It happens on a few percent of pages.",
        "I do not think anyone has ever looked.",
        "It falls back to a generic list, so nobody notices.",
        "I would not know where to see that."
      ]
    },
    {
      "id": "returns",
      "order": 10,
      "status": "open",
      "options": [
        "We take them off. Returns are joined back to the order.",
        "No. A sale is a sale as far as the reporting goes.",
        "Returns are negligible in what we sell.",
        "I do not know if that join exists."
      ]
    },
    {
      "id": "thin",
      "order": 11,
      "status": "open",
      "options": [
        "Most of it. That is just what our catalog looks like.",
        "A meaningful slice, mostly the newest things.",
        "We have new things going up all the time and no idea how they do.",
        "No idea what that share is."
      ]
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
      "status": "open",
      "options": [
        "There is a number and the commercial team owns it.",
        "No number. We just want it to favour the better lines.",
        "That would be a conversation above me."
      ]
    },
    {
      "id": "traffic",
      "order": 15,
      "status": "open",
      "options": [
        "Hundreds of thousands of times a day.",
        "A few thousand. It is not a big site.",
        "I could get that number."
      ]
    }
  ],
  "conflicts": [],
  "still_to_ask": [
    "shortfall",
    "returns",
    "thin",
    "duplicates",
    "tradeoff",
    "traffic"
  ],
  "counts": {
    "answered": 8,
    "stale": 0,
    "open": 6,
    "not_in_play": 1,
    "dropped": 0
  },
  "schema_version": "1.0",
  "problem_id": "recommender",
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
