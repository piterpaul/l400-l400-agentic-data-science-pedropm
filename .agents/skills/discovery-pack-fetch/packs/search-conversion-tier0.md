---
schema_version: "1.0"
problem_id: "search-conversion"
target_tier: 0
recommended_rung: 0
source: "built-in-classroom-pack"
---

# Discovery pack — Search & Product Discovery Conversion

`search-conversion` · recorded by **classroom-repo** · version 1 · served 2026-10-27T00:00:00Z

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

> **VP Digital, mid-market home-improvement retailer, 400k SKUs** — People search on our site and do not find what they want. Search converts at half the rate of category browsing. We need AI search.
>
> **Head of Digital Commerce, industrial distributor, 2M SKUs, B2B only** — Our customers search by manufacturer part number and half the time get nothing back. Sales keeps telling us to just make it work like Google.
>
> **Director of Search Science, marketplace, 60M listings, existing ranker** — Our offline ranking score is up 6% over three quarters and sales per search have not moved. We want to go to real-time personalisation.

**Vocabulary is unbound.** The nouns below are the method's neutral words, not this customer's — treat them as placeholders and confirm the real terms early.

**The five specifics.**

- **How many, of the thing being predicted** — *not captured. Ask.*
- **How much history there is, and how much arrives** — *not captured. Ask.*
- **The deadline the run has to hit** — *not captured. Ask.*
- **What being wrong costs, per event or per year** — *not captured. Ask.*
- **Who owns the decision, and who would run this** — *not captured. Ask.*

## 2. Where discovery landed

- **Floor:** nothing heard yet requires anything above the cheapest rung
- **Ceiling: Tier 2 — Distributed & Custom ML** — set by How much traffic there is

## 3. What was asked, and what it steered

### 1. What kind of thing people type

**Asked:** When somebody uses the box, are they typing an exact code they already know, a brand and a category, or a description of what they want in their own words? Ask for the split of last month, not for the impression.

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Whole sentences. People describe the thing, and some of them paste a photo.
- **Which means:** Meaning matching earns its place, and if pictures are in play so does a shared space for images and words. Both are BigQuery functions now, so the build is a table and a schedule rather than a serving stack.
- **Bounds:** none
- **For the brief:** Query mix is descriptive, some visual. Meaning matching primary; check whether pictures need to be searchable too.
- **Why it was asked:** How the matching has to work, the largest architecture fork in this problem. Codes need literal matching. Descriptions need meaning matching. Most real catalogs need both at once, and picking one is how sites end up rebuilding twice.
- **What it forecloses:** Settles the retrieval engine before anyone argues about ranking. It also closes the "we need AI search" conversation, because a catalog of codes gets worse with meaning matching, not better.

### 2. What happens when nothing comes back

**Asked:** What share of searches come back with nothing at all, and what share come back with fewer than five things? Ask for both numbers as they stand today.

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** We track it. It sits around 2% and somebody works the list every week.
- **Which means:** Genuinely good, and rarer than the room thinks. It means the failures left are about ordering and about the things that come back but are wrong, which is a harder and more interesting problem.
- **Bounds:** none
- **For the brief:** Empty-result rate ~2% and actively worked. Failures are ordering, not retrieval.
- **Why it was asked:** Whether there is a retrieval problem or an ordering problem, and those get completely different budgets. Nothing coming back is the cheapest number in this whole problem and the one most sites cannot produce.
- **What it forecloses:** A high empty rate closes the ranking conversation for a quarter. There is no ordering of zero things, and every hour spent on a ranker while one search in ten finds nothing is an hour spent on the wrong end.

### 3. Is the catalog filled in

**Asked:** For each filter people actually use, what share of the catalog has that field filled in? Ask for it per category, because one number for the whole catalog hides the category that is empty.

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Over 90% on the filters we actually show, and we check it.
- **Which means:** Unusual and worth saying out loud in the room, because it means the money is better spent on how results are ordered. Ask who checks it and how, then keep that person close.
- **Bounds:** none
- **For the brief:** Attribute coverage above 90% on live filters. Move the budget to matching and ordering.
- **Why it was asked:** Whether anything above the first rung is worth costing. A filter nobody can use is a dead end, and an item with no fields cannot be found by anyone narrowing down. It is the least glamorous number here and explains more than any model.
- **What it forecloses:** Closes the argument about buying a retrieval engine before the catalog is filled in. Meaning matching over blank records returns confident nonsense, so coverage comes first whatever the query mix turns out to be.

### 4. Does everyone see the same catalog

**Asked:** Does everybody who searches see the same things at the same price, or does what they can see and what they pay depend on who they are signed in as?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Same catalog, same price, signed in or not.
- **Which means:** The simple case, and it keeps every retrieval option open. Personalisation, if it comes, is about ordering rather than about which things exist.
- **Bounds:** none
- **For the brief:** One catalog, one price for everyone. No account rule inside retrieval.
- **Why it was asked:** Where the account rule runs. Applying it after the search is the default in most stacks and it is wrong: ask for ten results, get two, because eight were cut afterwards. Applying it inside the lookup is a different product choice.
- **What it forecloses:** Closes the serving database question for anyone with contract pricing. It also closes the personalisation debate early, because relevance is a second-order concern next to showing somebody a price they are not entitled to.

### 5. What counts as the search working

**Asked:** Which single thing do you want more of, and would you accept fewer of the others to get it — clicks, sales, money kept after returns, or your cut of a sale somebody else fulfils?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Engagement. We want people clicking through and looking at things.
- **Which means:** The easiest to move and the easiest to move dishonestly. Clicks respond to anything eye-catching, so agree a second number that cannot be gamed the same way, or the first win will be lurid pictures.
- **Bounds:** none
- **For the brief:** Target is engagement. Pair it with a guardrail the same trick cannot move.
- **Why it was asked:** Which outcome every model above the first rung is trained to move, and so what the whole system optimises. These four order the same results differently, and everybody in the room already knows which one they are bonused on.
- **What it forecloses:** Names the target, which closes the evaluation argument before it starts. It also surfaces the fight between the commercial team and the search team early enough to be useful.

### 6. Who can override the results

**Asked:** Who can change what comes back without asking permission, and is what they can do written down anywhere?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** There is a documented set of pins, boosts and exclusions.
- **Which means:** Excellent, and rarer than it sounds. Take the list as the specification. If a rung cannot express all of it as configuration, that rung is wrong regardless of how good its ordering is.
- **Bounds:** none
- **For the brief:** Rules are written and finite. Treat the list as an architecture requirement.
- **Why it was asked:** The rule layer, which is not optional and not a nuisance. Every commerce site has one, and a model that cannot express the rules will be overridden by hand until somebody turns it off.
- **What it forecloses:** Getting the list in writing closes an entire category of late surprises. The rules are the constraint the architecture has to satisfy, and they are almost never in the brief.

### 8. How much traffic there is

**Asked:** How many searches a day, and how much of that is the same thousand phrases typed over and over?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Decent volume, but the top thousand phrases are most of it.
- **Which means:** Curating the common phrases will beat a model, probably for a year. The interesting question becomes what share of the money sits in the rarely typed searches, because that is where a model would have to earn its keep.
- **Bounds:** Tier 2 — Distributed & Custom ML is the ceiling
- **For the brief:** Volume concentrated in common searches. Curate the head; measure revenue sitting in the rare tail.
- **Why it was asked:** Whether behaviour can teach you anything, and whether any change you make can be proved. Both have hard floors, and below them the honest answer is curation and better matching rather than a model.
- **What it forecloses:** Closes the top rung outright for most catalogs. It also closes the promise-making, because the smallest win your traffic could prove is arithmetic, not opinion.

### 11. Do people already send you pictures to identify things, and are your manuals, spec sheets and photos stored somewhere a query could reach?

**Asked:** Do people already send you pictures to identify things, and are your manuals, spec sheets and photos stored somewhere a query could reach?

- **Heard:** Not photos, but the answers live in PDFs and manuals nobody can search.
- **Which means:** The catalog is not the only thing that needs indexing. Treat the documents as a second set of records with their own filters, because merging them into one list without a source label makes both look wrong.
- **Bounds:** none
- **For the brief:** Documents are a second searchable set. Index separately with a source label; do not merge blind.

## 4. Still worth asking

**These are instructions, not blanks.** Ask each one. The possible answers below are authored, with what each would rule in or out, so a reply can be recognised rather than interpreted.

### 7. Do you know what was shown

**Ask:** When somebody searches, do you record everything that was put in front of them and in what order, or only the things they clicked?

**Why it matters:** Whether learning the ordering from behaviour is possible at all. Clicks alone tell you what won and never what it beat, so there is nothing to learn from and no way to correct for people clicking the top result because it is the top result.

What the answers would mean:

- **Everything shown, with its position and an id tying the page together.** → You have a record of what was shown, which is the thing most sites lack. Check one more level down: was the scoring input logged with it, or is it rebuilt later from the analytics tables? Rebuilds cannot reproduce what the engine saw. *(floor Tier 1 — Serverless, In-Warehouse)*
- **Clicks only. We know what they picked, not what else was there.** → The single most common blocker in this problem. Sprint one is instrumentation and there is no way around it, because nothing rebuilt from the catalog afterwards can tell you what was on the page that day. *(floor Tier 1 — Serverless, In-Warehouse; ceiling Tier 2 — Distributed & Custom ML)*
- **We log impressions but only on a small sample of traffic.** → Fine for the phrases people type constantly and useless for the long list typed once, which is exactly the part you were hired to fix. Ask for the sampling rate and the retention window in the same breath. *(floor Tier 1 — Serverless, In-Warehouse)*
- **I would have to check what the front end sends.** → Ask for one raw event, not a schema diagram. The diagram will show fields the front end stopped populating two releases ago, and everybody will believe it.

## 5. Not worth asking yet

Each of these is gated behind a branch that is not open. They are listed so the absence is legible: they were not forgotten, they were ruled out.

- **When somebody searches, gets nothing useful and immediately types something different, does the log let you follow that chain?** — closed by *What happens when nothing comes back* → “We track it. It sits around 2% and somebody works the list every week”.
- **When a part is replaced by a newer one, does anything record that the old code now means the new thing?** — closed by *What kind of thing people type* → “Whole sentences. People describe the thing, and some of them paste a photo”.
- **Whoever writes the descriptions — do they gain anything by wording them a particular way?** — closed by *Is the catalog filled in* → “Over 90% on the filters we actually show, and we check it”.
- **When you narrow results down today, does the narrowing happen as part of finding them, or does the engine find a batch and then throw some away?** — closed by *Does everyone see the same catalog* → “Same catalog, same price, signed in or not”.
- **If something sells out or changes price at ten in the morning, when does search stop showing the old answer — seconds, minutes, or tomorrow?** — closed by *Does everyone see the same catalog* → “Same catalog, same price, signed in or not”.
- **Does a paid placement get dropped into a fixed slot on the page, or does paying make an item more likely to rank well?** — closed by *Who can override the results* → “There is a documented set of pins, boosts and exclusions”.
- **Has any part of your traffic ever been deliberately shown results in a shuffled order?** — needs “A slice of traffic could be shown a shuffled order”, which nothing answered has opened.
- **When you change the ordering, how do you decide it was better?** — closed by *How much traffic there is* → “Decent volume, but the top thousand phrases are most of it”.

## 6. What is being suggested, and why the alternatives are out

### Tier 0 — Out of the Box

Buy the engine and spend the time on its controls

- **What it is:** Catalog feed + behaviour events → AI Commerce Search → boost / bury / pin / filter controls
- **Google Cloud & open-weight options at this rung:** AI Commerce Search, BigQuery, Conversational Analytics
- **Why here:** Typo tolerance, synonyms, both kinds of matching and event-trained tuning, no model to own. Curators get boost, bury, pin and filter as configuration. Audit the searches returning nothing in BigQuery and let the commercial team query it in plain language.
- **Where it breaks:** Tuning on behaviour needs volume before it beats what is there, so 900 searches a day never reaches it. Visibility per account is a filter the caller passes, so every contract has to become attributes. Money kept after returns is engineering, not a control.
- **What would move it up:** Coverage on a live filter comes back below what the filter needs to work, or a curator rule will not express as boost, bury, pin or filter.

#### Architecture Decision Record (ADR) Matrix

A scenario-aware evaluation of the ladder against this customer's constraints. Where an adjacent tier serves as a viable A/B benchmark or a Phase 2 evolution, that role is explicitly called out:

| Rung | Role in this Engagement | Architecture & Stance | Deciding Constraint & Trade-off |
| --- | --- | --- | --- |
| Tier 0 — Out of the Box | **Primary Baseline (MVP)** | Buy the engine and spend the time on its controls. Fits all bounded constraints. | Selected target. Fits ceiling (Tier 2 — Distributed & Custom ML). Wins: Typo tolerance, synonyms, both kinds of matching and event-trained tuning, no model to own. Curators get boost, bury, pin and filter as configuration. Audit the searches returning nothing in BigQuery and let the commercial team query it in plain language. |
| Tier 1 — Serverless, In-Warehouse | **Adjacent Higher Tier (Phase 2 Evolution)** | Fill in the catalog and read the failed searches. Higher freshness, lower latency, or specialised modeling. | Inside the range, but nothing heard requires it yet. Step-up trigger: Coverage on a live filter comes back below what the filter needs to work, or a curator rule will not express as boost, bury, pin or filter. Propose as Phase 2 expansion once this condition is met. |
| Tier 2 — Distributed & Custom ML | In range, not required | Match on words and meaning, and filter before you match. | Not ruled out, but nothing heard in the room requires it. |
| Tier 3 — Real-Time & Specialised | Ruled out (Theatre) | Let behaviour set the order, once the log can be trusted. | Past the ceiling (Tier 2 — Distributed & Custom ML), set by How much traffic there is. Unjustified operational cost. |

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

- Tier 1 — Serverless, In-Warehouse — Fill in the catalog and read the failed searches. Out: not ruled out, but nothing heard in the room requires it.
- Tier 2 — Distributed & Custom ML — Match on words and meaning, and filter before you match. Out: not ruled out, but nothing heard in the room requires it.
- Tier 3 — Real-Time & Specialised — Let behaviour set the order, once the log can be trusted. Out: past the ceiling at Tier 2 — Distributed & Custom ML — How much traffic there is.

**Below the rung sit the calls no rung makes for you.** The tier does not settle these, and a design that has not stated them has not been made. Nothing on the page asks for them, so they travel unanswered.

- **What one row is** — One shown item inside one search, with the page as the group — not one search, and not one visit. Where the outcome attaches is a second decision hiding inside the first, and it is usually never made.
  Options: One shown item in one search · One search, page collapsed · One item in one visit
- **What goes in beside the past** — Beside the item’s own text: match quality, filter coverage, price, availability, click history. The split that matters is what fits the page budget — 200ms, of which retrieval and counting filters already spend 110.
  Options: Match and item inputs only · Add behaviour history per item · Add searcher state from this visit
- **One fit, one each, or one per group** — One order across the whole catalog, one per category, or one per kind of search. Exact codes and written descriptions fail in opposite directions, and a single fit averages the two failures rather than fixing either.
  Options: One fit across the catalog · One fit per category · One fit per kind of search
- **Which methods get a run** — The thing to beat is the Tier 2 order merged by position, not nothing. Against it: a pairwise boosted ranker grouped by page, and a weighted logistic fit carrying the position correction as a row weight.
  Options: The tuned merge, as the baseline · Pairwise boosted ranker · Weighted logistic fit
- **How you would know** — Offline and online disagree here by construction. Judgements taken from your own click log score a new order on how faithfully it copies the old one, which is exactly how 6% offline over three quarters arrives with sales flat.
  Options: A judged set graded by people · Two orderings on one page · A split test
- **What tuning is worth** — Three things compete for the same fortnight: filter coverage, what counts as an outcome, and the settings. A live filter filled in on 42% of a category ends the ordering argument before any setting is worth searching.
  Options: Fix coverage first · Fix the label next · Search the settings
- **One winner, or several combined** — The combining here sits under the model rather than over it: two retrieval arms merged into one list, then optionally a learned pass over the top few hundred. Averaging two rankers is the rarer and later question.
  Options: One arm · Both arms, merged by position · Both arms plus a learned reorder

**Dataset for the build.** Every workshop build runs on public or shipped tables:

- **Source:** BigQuery public tables
- **Tables:** `bigquery-public-data.thelook_ecommerce.products`, `bigquery-public-data.thelook_ecommerce.events`, `bigquery-public-data.thelook_ecommerce.order_items`
- **Grain & size:** One row per catalogue item in products (29,120 items with id, name, brand, category, department, retail_price) paired with 2.43M clickstream rows in events and 181,313 purchases in order_items.
- **Target / label:** Relevant product hit in top 10 (Recall@10) and click-to-purchase conversion on held-out queries.
- **Tier 1 / Tier 2 build:** Hard Tier 1 extracts attributes from sparse titles with AI.GENERATE_TABLE (2,500-item slice), encodes items and queries with AI.GENERATE_EMBEDDING (text-embedding-005), and retrieves with VECTOR_SEARCH; Tier 2 adds a boosted ranker.
- **Caveat:** Encoding raw product titles into vectors without structured attribute filtering returns items in the wrong department or price bracket on constraint-heavy queries.
- **Setup / verify:** `bq head -n 5 bigquery-public-data:thelook_ecommerce.products`
- **Agent skills (`bigquery-data-science` & Data Agent Kit):** `uvx bigquery-data-science lookup VECTOR_SEARCH # BQDS: AI.GENERATE_EMBEDDING, AI.GENERATE_TABLE, CREATE VECTOR INDEX, AI.SIMILARITY, AI.SCORE | Data Agent Kit: bigquery-ai-ml, bigquery-sql, dataform-bigquery, ml-best-practices, cloud-databases-onboarding`

**The ladder, for reference.** No site is needed to read the tiers above.

- **Tier 0 — Out of the Box** — A model somebody else trained already answers the question. Nothing to fit, nothing to provision, and the bill starts on the first query. The most senior move in the room is often to say so.
- **Tier 1 — Serverless, In-Warehouse** — Bring the model to the data. No cluster, no container, no serving stack. SQL is the interface.
- **Tier 2 — Distributed & Custom ML** — The transformation or the model outgrew SQL. Bring distributed compute to the data, keep the storage where it is.
- **Tier 3 — Real-Time & Specialised** — A hard SLA or a custom objective justifies owning the stack. You are now engineering a system, not training a model.
- **Tier 4 — Hardening for High-Stakes Operation** — Not a rung you buy. It is what changes about a system already at Tier 1, 2 or 3 once being wrong is expensive, contested or unsafe — and what changes is different for every problem in Discovery.

## 7. POC Data Discovery & Profiling Contract (Tier 0)

- **Source Tables (`bigquery-region: "US"`):** `bigquery-public-data.thelook_ecommerce.products`, `bigquery-public-data.thelook_ecommerce.events`, `bigquery-public-data.thelook_ecommerce.order_items`
- **Grain & Target:** One row per catalogue item in products (29,120 items with id, name, brand, category, department, retail_price) paired with 2.43M clickstream rows in events and 181,313 purchases in order_items. | Relevant product hit in top 10 (Recall@10) and click-to-purchase conversion on held-out queries.
- **Data Caveat to Profile & Guard Against:** Encoding raw product titles into vectors without structured attribute filtering returns items in the wrong department or price bracket on constraint-heavy queries.
- **Verification Command:** `bq head -n 5 bigquery-public-data:thelook_ecommerce.products`

---

### The same thing, for a program to read

```json
{
  "problem": "search-conversion",
  "ldap": "classroom-repo",
  "version": 1,
  "served_at": "2026-10-27T00:00:00Z",
  "binding": {
    "record": "item",
    "query": "search",
    "searcher": "searcher",
    "catalog": "catalog",
    "facet": "filter",
    "seller": "supplier",
    "curator": "curator",
    "outcome": "outcome",
    "visit": "visit"
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
      "bigquery-public-data.thelook_ecommerce.products",
      "bigquery-public-data.thelook_ecommerce.events",
      "bigquery-public-data.thelook_ecommerce.order_items"
    ],
    "grain": "One row per catalogue item in products (29,120 items with id, name, brand, category, department, retail_price) paired with 2.43M clickstream rows in events and 181,313 purchases in order_items.",
    "label": "Relevant product hit in top 10 (Recall@10) and click-to-purchase conversion on held-out queries.",
    "rungs": "Hard Tier 1 extracts attributes from sparse titles with AI.GENERATE_TABLE (2,500-item slice), encodes items and queries with AI.GENERATE_EMBEDDING (text-embedding-005), and retrieves with VECTOR_SEARCH; Tier 2 adds a boosted ranker.",
    "caveat": "Encoding raw product titles into vectors without structured attribute filtering returns items in the wrong department or price bracket on constraint-heavy queries.",
    "setup": "bq head -n 5 bigquery-public-data:thelook_ecommerce.products",
    "skills": "uvx bigquery-data-science lookup VECTOR_SEARCH # BQDS: AI.GENERATE_EMBEDDING, AI.GENERATE_TABLE, CREATE VECTOR INDEX, AI.SIMILARITY, AI.SCORE | Data Agent Kit: bigquery-ai-ml, bigquery-sql, dataform-bigquery, ml-best-practices, cloud-databases-onboarding"
  },
  "questions": [
    {
      "id": "mix",
      "order": 1,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "describe",
        "heard": "Whole sentences. People describe the thing, and some of them paste a photo.",
        "means": "Meaning matching earns its place, and if pictures are in play so does a shared space for images and words. Both are BigQuery functions now, so the build is a table and a schedule rather than a serving stack.",
        "floor": null,
        "ceiling": null
      }
    },
    {
      "id": "empty",
      "order": 2,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "low",
        "heard": "We track it. It sits around 2% and somebody works the list every week.",
        "means": "Genuinely good, and rarer than the room thinks. It means the failures left are about ordering and about the things that come back but are wrong, which is a harder and more interesting problem.",
        "floor": null,
        "ceiling": null
      }
    },
    {
      "id": "attributes",
      "order": 3,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "most",
        "heard": "Over 90% on the filters we actually show, and we check it.",
        "means": "Unusual and worth saying out loud in the room, because it means the money is better spent on how results are ordered. Ask who checks it and how, then keep that person close.",
        "floor": null,
        "ceiling": null
      }
    },
    {
      "id": "allowed",
      "order": 4,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "same",
        "heard": "Same catalog, same price, signed in or not.",
        "means": "The simple case, and it keeps every retrieval option open. Personalisation, if it comes, is about ordering rather than about which things exist.",
        "floor": null,
        "ceiling": null
      }
    },
    {
      "id": "paid",
      "order": 5,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "click",
        "heard": "Engagement. We want people clicking through and looking at things.",
        "means": "The easiest to move and the easiest to move dishonestly. Clicks respond to anything eye-catching, so agree a second number that cannot be gamed the same way, or the first win will be lurid pictures.",
        "floor": null,
        "ceiling": null
      }
    },
    {
      "id": "whocuts",
      "order": 6,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "written",
        "heard": "There is a documented set of pins, boosts and exclusions.",
        "means": "Excellent, and rarer than it sounds. Take the list as the specification. If a rung cannot express all of it as configuration, that rung is wrong regardless of how good its ordering is.",
        "floor": null,
        "ceiling": null
      }
    },
    {
      "id": "impressions",
      "order": 7,
      "status": "open",
      "keystone": true,
      "options": [
        "Everything shown, with its position and an id tying the page together.",
        "Clicks only. We know what they picked, not what else was there.",
        "We log impressions but only on a small sample of traffic.",
        "I would have to check what the front end sends."
      ]
    },
    {
      "id": "volume",
      "order": 8,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "concentrated",
        "heard": "Decent volume, but the top thousand phrases are most of it.",
        "means": "Curating the common phrases will beat a model, probably for a year. The interesting question becomes what share of the money sits in the rarely typed searches, because that is where a model would have to earn its keep.",
        "floor": null,
        "ceiling": 2
      }
    },
    {
      "id": "reformulate",
      "order": 9,
      "status": "not_in_play",
      "gate": "People retype and try again in the same sitting",
      "closed_by": {
        "question": "empty",
        "answer": "low"
      }
    },
    {
      "id": "supersede",
      "order": 10,
      "status": "not_in_play",
      "gate": "Codes change and old ones stay in circulation",
      "closed_by": {
        "question": "mix",
        "answer": "describe"
      }
    },
    {
      "id": "pictures",
      "order": 11,
      "status": "answered",
      "answer": {
        "key": "docs",
        "heard": "Not photos, but the answers live in PDFs and manuals nobody can search.",
        "means": "The catalog is not the only thing that needs indexing. Treat the documents as a second set of records with their own filters, because merging them into one list without a source label makes both look wrong.",
        "floor": null,
        "ceiling": null
      }
    },
    {
      "id": "authoring",
      "order": 12,
      "status": "not_in_play",
      "gate": "Somebody outside the company writes the descriptions",
      "closed_by": {
        "question": "attributes",
        "answer": "most"
      }
    },
    {
      "id": "wherefilter",
      "order": 13,
      "status": "not_in_play",
      "gate": "Filters have to be applied before the search, not after",
      "closed_by": {
        "question": "allowed",
        "answer": "same"
      }
    },
    {
      "id": "livestate",
      "order": 14,
      "status": "not_in_play",
      "gate": "Live stock or price has to be right at the moment of the search",
      "closed_by": {
        "question": "allowed",
        "answer": "same"
      }
    },
    {
      "id": "paidwhere",
      "order": 15,
      "status": "not_in_play",
      "gate": "Some placements are paid for",
      "closed_by": {
        "question": "whocuts",
        "answer": "written"
      }
    },
    {
      "id": "randomised",
      "order": 16,
      "status": "not_in_play",
      "gate": "A slice of traffic could be shown a shuffled order",
      "closed_by": null
    },
    {
      "id": "measure",
      "order": 17,
      "status": "not_in_play",
      "gate": "There is enough traffic to settle a test in a week",
      "closed_by": {
        "question": "volume",
        "answer": "concentrated"
      }
    }
  ],
  "conflicts": [],
  "still_to_ask": [
    "impressions"
  ],
  "counts": {
    "answered": 8,
    "stale": 0,
    "open": 1,
    "not_in_play": 8,
    "dropped": 0
  },
  "schema_version": "1.0",
  "problem_id": "search-conversion",
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
