---
schema_version: "1.0"
problem_id: "search-conversion"
target_tier: 1
recommended_rung: 1
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

- **Floor: Tier 1 — Serverless, In-Warehouse** — set by What kind of thing people type, What happens when nothing comes back, Is the catalog filled in, Does everyone see the same catalog, What counts as the search working, Who can override the results, Do you know what was shown, How much traffic there is
- **Ceiling: Tier 2 — Distributed & Custom ML** — set by What happens when nothing comes back

> **Together, not apart.** A record of what was shown and the traffic to learn from it. This is the minority case where learning the ordering from behaviour is genuinely available rather than aspirational. Spend the conversation on the shuffled slice and the launch gate, because those are what decide whether it works.

## 3. What was asked, and what it steered

### 1. What kind of thing people type

**Asked:** When somebody uses the box, are they typing an exact code they already know, a brand and a category, or a description of what they want in their own words? Ask for the split of last month, not for the impression.

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Mostly exact codes. Part numbers, our own item numbers, book numbers.
- **Which means:** Literal matching is the primary path and meaning matching is a hazard, not an upgrade. The wins here are punctuation and spacing normalisation, a replaced-by chain and a competitor cross-reference table. That table beats any model here.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Query mix is majority exact code. Literal matching primary; normalise and build the replaced-by table first.
- **Why it was asked:** How the matching has to work, the largest architecture fork in this problem. Codes need literal matching. Descriptions need meaning matching. Most real catalogs need both at once, and picking one is how sites end up rebuilding twice.
- **What it forecloses:** Settles the retrieval engine before anyone argues about ranking. It also closes the "we need AI search" conversation, because a catalog of codes gets worse with meaning matching, not better.

### 2. What happens when nothing comes back

**Asked:** What share of searches come back with nothing at all, and what share come back with fewer than five things? Ask for both numbers as they stand today.

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** We track it and it is over one in ten searches.
- **Which means:** The finding is the deliverable. At that level the cause is almost always blank fields or a filter combination nothing satisfies, and it is fixable with SQL and a backfill inside a quarter.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse, Tier 2 — Distributed & Custom ML is the ceiling
- **For the brief:** Empty-result rate above 10%. Fix retrieval and coverage before any ranking work is scoped.
- **Why it was asked:** Whether there is a retrieval problem or an ordering problem, and those get completely different budgets. Nothing coming back is the cheapest number in this whole problem and the one most sites cannot produce.
- **What it forecloses:** A high empty rate closes the ranking conversation for a quarter. There is no ordering of zero things, and every hour spent on a ranker while one search in ten finds nothing is an hour spent on the wrong end.

### 3. Is the catalog filled in

**Asked:** For each filter people actually use, what share of the catalog has that field filled in? Ask for it per category, because one number for the whole catalog hides the category that is empty.

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Good in the categories we care about, close to empty in the rest.
- **Which means:** The normal answer, and the backfill is a scoped job rather than an open one. Generate the missing fields from titles and pictures, grade a sample per category by hand, and suppress anything the generator was unsure about.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Coverage is patchy by category. Backfill the weak categories; hand-grade a sample before scheduling.
- **Why it was asked:** Whether anything above the first rung is worth costing. A filter nobody can use is a dead end, and an item with no fields cannot be found by anyone narrowing down. It is the least glamorous number here and explains more than any model.
- **What it forecloses:** Closes the argument about buying a retrieval engine before the catalog is filled in. Meaning matching over blank records returns confident nonsense, so coverage comes first whatever the query mix turns out to be.

### 4. Does everyone see the same catalog

**Asked:** Does everybody who searches see the same things at the same price, or does what they can see and what they pay depend on who they are signed in as?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Everyone sees the same things, but the price is per contract.
- **Which means:** Lighter than a visibility rule and still consequential. Price is a live value, so it belongs in the response rather than in the search copy, and putting it into the ordering makes it a pricing decision wearing a relevance costume.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Prices are per contract. Resolve price at response time; keep it out of the ordering unless the business signs that off.
- **Why it was asked:** Where the account rule runs. Applying it after the search is the default in most stacks and it is wrong: ask for ten results, get two, because eight were cut afterwards. Applying it inside the lookup is a different product choice.
- **What it forecloses:** Closes the serving database question for anyone with contract pricing. It also closes the personalisation debate early, because relevance is a second-order concern next to showing somebody a price they are not entitled to.

### 5. What counts as the search working

**Asked:** Which single thing do you want more of, and would you accept fewer of the others to get it — clicks, sales, money kept after returns, or your cut of a sale somebody else fulfils?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Money kept. A sale we lose money on is not a win.
- **Which means:** Honest and harder. It needs a cost per item that search can read, which is often the real blocker, and it will rank differently enough that the commercial team must see the change before it ships.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Target is contribution after returns. Confirm search can read a per-item cost.
- **Why it was asked:** Which outcome every model above the first rung is trained to move, and so what the whole system optimises. These four order the same results differently, and everybody in the room already knows which one they are bonused on.
- **What it forecloses:** Names the target, which closes the evaluation argument before it starts. It also surfaces the fight between the commercial team and the search team early enough to be useful.

### 6. Who can override the results

**Asked:** Who can change what comes back without asking permission, and is what they can do written down anywhere?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** A few people just go in and change things when they need to.
- **Which means:** The rules exist, they are just not written down, and they will reappear as hand edits over whatever you build. Spend a session reconstructing them from the last quarter of changes and get the list signed.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Override rules are informal. Reconstruct from recent changes and get the list agreed before building.
- **Why it was asked:** The rule layer, which is not optional and not a nuisance. Every commerce site has one, and a model that cannot express the rules will be overridden by hand until somebody turns it off.
- **What it forecloses:** Getting the list in writing closes an entire category of late surprises. The rules are the constraint the architecture has to satisfy, and they are almost never in the brief.

### 7. Do you know what was shown

**Asked:** When somebody searches, do you record everything that was put in front of them and in what order, or only the things they clicked?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Everything shown, with its position and an id tying the page together.
- **Which means:** You have a record of what was shown, which is the thing most sites lack. Check one more level down: was the scoring input logged with it, or is it rebuilt later from the analytics tables? Rebuilds cannot reproduce what the engine saw.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Impressions logged with position and page id. Verify the scoring inputs are logged alongside, not rebuilt later.
- **Why it was asked:** Whether learning the ordering from behaviour is possible at all. Clicks alone tell you what won and never what it beat, so there is nothing to learn from and no way to correct for people clicking the top result because it is the top result.
- **What it forecloses:** A no here closes the top two rungs for at least a quarter and turns the first sprint into a logging change. Better to say that in the first meeting than in the third.

### 8. How much traffic there is

**Asked:** How many searches a day, and how much of that is the same thousand phrases typed over and over?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Hundreds of thousands a day, spread across a very long list of phrases.
- **Which means:** Learning from behaviour is genuinely available and so is a test that settles in a week. This is the minority case, and it is the only one where the top of the ladder is honest work.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Traffic supports learned ordering and weekly tests. Top rungs are in play.
- **Why it was asked:** Whether behaviour can teach you anything, and whether any change you make can be proved. Both have hard floors, and below them the honest answer is curation and better matching rather than a model.
- **What it forecloses:** Closes the top rung outright for most catalogs. It also closes the promise-making, because the smallest win your traffic could prove is arithmetic, not opinion.

## 4. Still worth asking

**These are instructions, not blanks.** Ask each one. The possible answers below are authored, with what each would rule in or out, so a reply can be recognised rather than interpreted.

### 10. When a part is replaced by a newer one, does anything record that the old code now means the new thing?

**Ask:** When a part is replaced by a newer one, does anything record that the old code now means the new thing? And do you hold the table of what your competitors call the same part?

What the answers would mean:

- **Yes, both. The replaced-by chain and the cross-reference table are kept current.** → Then most of the answer already exists and nobody has plugged it into search. Expanding a search through the chain before matching usually removes a large share of the searches that return nothing, in a fortnight. *(floor Tier 1 — Serverless, In-Warehouse)*
- **There is a table. Nobody is sure how far behind it is.** → Worth measuring rather than assuming. Sample fifty codes that returned nothing last month and check by hand how many were superseded; that number decides whether this is a data job or a matching job.
- **It lives in people. The counter staff know which part replaced which.** → That knowledge is the asset and it is walking out of the building. Building the table is unglamorous and it will beat every model on the roadmap, so put it in the plan as the deliverable it is. *(floor Tier 1 — Serverless, In-Warehouse; ceiling Tier 2 — Distributed & Custom ML)*
- **I would have to ask the product data team.** → Ask, and ask specifically who updates it and when. A table that exists and is two years old fails in a way that is harder to spot than no table at all.

### 14. If something sells out or changes price at ten in the morning, when does search stop showing the old answer — seconds, minutes, or tomorrow?

**Ask:** If something sells out or changes price at ten in the morning, when does search stop showing the old answer — seconds, minutes, or tomorrow?

What the answers would mean:

- **It has to be right immediately. We sell single items that cannot be sold twice.** → Availability is not a property of the search copy, it is a live lookup at response time. Building it into the copy is the most-complained-about bug in this whole problem area, and rebuilding hourly does not fix it. *(floor Tier 2 — Distributed & Custom ML)*
- **A few minutes is fine. Nobody notices under about five.** → A streaming update into the search copy covers this and it is much cheaper than a live lookup on every result. Name the window as a number and monitor it, because it slips.
- **Overnight is genuinely fine. Prices move once a quarter.** → Then the whole freshness argument disappears and a scheduled rebuild is correct. Say so explicitly, because engineering teams default to streaming and it costs money nobody needed to spend.
- **Nobody has ever put a number on it.** → Get the number from whoever fields the complaints, not from engineering. The tolerance the business actually has is usually looser than the one the team assumed.

### 16. Has any part of your traffic ever been deliberately shown results in a shuffled order?

**Ask:** Has any part of your traffic ever been deliberately shown results in a shuffled order? And if not, who could approve doing it?

What the answers would mean:

- **Yes, a small slice runs shuffled and we keep the logs.** → Rare, and it is what makes correcting for position honest rather than assumed. Everything above this rung rests on it, so find out how large the slice is and how long the logs go back. *(floor Tier 2 — Distributed & Custom ML)*
- **Not today, but somebody could sign that off if it were argued.** → Then name them and name the number in the same conversation. Deliberately showing worse results costs real sales, and an unsigned assumption that it will be allowed is how projects stall at the last gate. *(floor Tier 1 — Serverless, In-Warehouse)*
- **Nobody here would ever approve deliberately serving worse results.** → Then say plainly that every offline improvement is the new ordering reproducing the old one, and that you cannot put a number on the gain. That is a more useful sentence than a model, and it is the truth. *(ceiling Tier 2 — Distributed & Custom ML)*
- **I do not know if we have ever done that.** → Ask whether any test ever randomised the ordering rather than the layout. Sometimes an old experiment left exactly the log you need and nobody remembers it.

### 17. When you change the ordering, how do you decide it was better?

**Ask:** When you change the ordering, how do you decide it was better? And can you show two different orderings on the same page rather than to two different groups of people?

What the answers would mean:

- **We mix the two orderings into one page and see which items get clicked.** → The sensitive option, and it lets a team iterate weekly instead of quarterly. It also costs real work in the request path, because the page has to merge two orderings and credit each click back to whichever produced it. *(floor Tier 2 — Distributed & Custom ML)*
- **A split test. Two groups of people, one ordering each.** → Fine and slow. Work out the smallest win it could prove in a quarter before promising anything, because most catalogs cannot prove a 1% relative improvement in that time and the whole project gets judged on it.
- **We score it against a judgement set and ship if the number goes up.** → If those judgements came from your own click log, the number rewards copying the current ordering. That is the exact failure that produces a rising score and flat sales, and it will keep producing it. *(floor Tier 1 — Serverless, In-Warehouse; ceiling Tier 3 — Real-Time & Specialised)*
- **It goes out and we watch the dashboards.** → Then nothing is attributable and every change is defended by argument. Agree the gate and the blocking numbers before the first change, not after a bad one.

## 5. Not worth asking yet

Each of these is gated behind a branch that is not open. They are listed so the absence is legible: they were not forgotten, they were ruled out.

- **When somebody searches, gets nothing useful and immediately types something different, does the log let you follow that chain?** — closed by *What happens when nothing comes back* → “We track it and it is over one in ten searches”.
- **Do people already send you pictures to identify things, and are your manuals, spec sheets and photos stored somewhere a query could reach?** — closed by *What kind of thing people type* → “Mostly exact codes. Part numbers, our own item numbers, book numbers”.
- **Whoever writes the descriptions — do they gain anything by wording them a particular way?** — closed by *Is the catalog filled in* → “Good in the categories we care about, close to empty in the rest”.
- **When you narrow results down today, does the narrowing happen as part of finding them, or does the engine find a batch and then throw some away?** — closed by *Does everyone see the same catalog* → “Everyone sees the same things, but the price is per contract”.
- **Does a paid placement get dropped into a fixed slot on the page, or does paying make an item more likely to rank well?** — closed by *Who can override the results* → “A few people just go in and change things when they need to”.

## 6. What is being suggested, and why the alternatives are out

### Tier 1 — Serverless, In-Warehouse

Fill in the catalog and read the failed searches

- **What it is:** Failed search mining + AI.GENERATE_TABLE backfill → AI.EMBED generated column → BigQuery pipelines refresh
- **Google Cloud & open-weight options at this rung:** AI.GENERATE_TABLE, AI.EMBED, AI.SEARCH, AI.PREDICT, VECTOR_SEARCH, BigQuery pipelines, Data Engineering Agent
- **Why here:** AI.GENERATE_TABLE fills missing filters from titles and pictures at catalog scale, and AI.EMBED as a generated column puts images and words in one space, kept in step by BigQuery: change one description and only that item is redone.
- **Where it breaks:** BigQuery is not in the request path: everything here is precomputed and pushed to whatever serves. VECTOR_SEARCH is a query, not a page-budget lookup, and SEARCH is built for point lookups, not ranked word matching. Generated filters need a graded sample.
- **What would move it up:** Coverage is fixed, and the remaining failures are about which of the returned items come first, or about searchers seeing things they cannot buy.

#### Architecture Decision Record (ADR) Matrix

A scenario-aware evaluation of the ladder against this customer's constraints. Where an adjacent tier serves as a viable A/B benchmark or a Phase 2 evolution, that role is explicitly called out:

| Rung | Role in this Engagement | Architecture & Stance | Deciding Constraint & Trade-off |
| --- | --- | --- | --- |
| Tier 0 — Out of the Box | **Adjacent Lower Tier (A/B Benchmark)** | Buy the engine and spend the time on its controls. Lower complexity and operational overhead. | Below the floor (Tier 1 — Serverless, In-Warehouse), set by What kind of thing people type, What happens when nothing comes back, Is the catalog filled in, Does everyone see the same catalog, What counts as the search working, Who can override the results, Do you know what was shown, How much traffic there is. Viable as an A/B comparator to quantify the performance/accuracy lift of Tier 1 — Serverless, In-Warehouse. |
| Tier 1 — Serverless, In-Warehouse | **Primary Baseline (MVP)** | Fill in the catalog and read the failed searches. Fits all bounded constraints. | Selected target. Fits floor (Tier 1 — Serverless, In-Warehouse) and ceiling (Tier 2 — Distributed & Custom ML). Wins: AI.GENERATE_TABLE fills missing filters from titles and pictures at catalog scale, and AI.EMBED as a generated column puts images and words in one space, kept in step by BigQuery: change one description and only that item is redone. |
| Tier 2 — Distributed & Custom ML | **Adjacent Higher Tier (Phase 2 Evolution)** | Match on words and meaning, and filter before you match. Higher freshness, lower latency, or specialised modeling. | Inside the range, but nothing heard requires it yet. Step-up trigger: Coverage is fixed, and the remaining failures are about which of the returned items come first, or about searchers seeing things they cannot buy. Propose as Phase 2 expansion once this condition is met. |
| Tier 3 — Real-Time & Specialised | Ruled out (Theatre) | Let behaviour set the order, once the log can be trusted. | Past the ceiling (Tier 2 — Distributed & Custom ML), set by What happens when nothing comes back. Unjustified operational cost. |

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

- Tier 0 — Out of the Box — Buy the engine and spend the time on its controls. Out: the floor is Tier 1 — Serverless, In-Warehouse — What kind of thing people type, What happens when nothing comes back, Is the catalog filled in, Does everyone see the same catalog, What counts as the search working, Who can override the results, Do you know what was shown, How much traffic there is.

**Above it, and why that is theatre here.**

- Tier 2 — Distributed & Custom ML — Match on words and meaning, and filter before you match. Out: not ruled out, but nothing heard in the room requires it.
- Tier 3 — Real-Time & Specialised — Let behaviour set the order, once the log can be trusted. Out: past the ceiling at Tier 2 — Distributed & Custom ML — What happens when nothing comes back.

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

## 7. POC Data Discovery & Profiling Contract (Tier 1)

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
    "floor": 1,
    "ceiling": 2,
    "clash": false
  },
  "recommended_rung": 1,
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
        "key": "identifier",
        "heard": "Mostly exact codes. Part numbers, our own item numbers, book numbers.",
        "means": "Literal matching is the primary path and meaning matching is a hazard, not an upgrade. The wins here are punctuation and spacing normalisation, a replaced-by chain and a competitor cross-reference table. That table beats any model here.",
        "floor": 1,
        "ceiling": null
      }
    },
    {
      "id": "empty",
      "order": 2,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "high",
        "heard": "We track it and it is over one in ten searches.",
        "means": "The finding is the deliverable. At that level the cause is almost always blank fields or a filter combination nothing satisfies, and it is fixable with SQL and a backfill inside a quarter.",
        "floor": 1,
        "ceiling": 2
      }
    },
    {
      "id": "attributes",
      "order": 3,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "patchy",
        "heard": "Good in the categories we care about, close to empty in the rest.",
        "means": "The normal answer, and the backfill is a scoped job rather than an open one. Generate the missing fields from titles and pictures, grade a sample per category by hand, and suppress anything the generator was unsure about.",
        "floor": 1,
        "ceiling": null
      }
    },
    {
      "id": "allowed",
      "order": 4,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "price",
        "heard": "Everyone sees the same things, but the price is per contract.",
        "means": "Lighter than a visibility rule and still consequential. Price is a live value, so it belongs in the response rather than in the search copy, and putting it into the ordering makes it a pricing decision wearing a relevance costume.",
        "floor": 1,
        "ceiling": null
      }
    },
    {
      "id": "paid",
      "order": 5,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "margin",
        "heard": "Money kept. A sale we lose money on is not a win.",
        "means": "Honest and harder. It needs a cost per item that search can read, which is often the real blocker, and it will rank differently enough that the commercial team must see the change before it ships.",
        "floor": 1,
        "ceiling": null
      }
    },
    {
      "id": "whocuts",
      "order": 6,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "informal",
        "heard": "A few people just go in and change things when they need to.",
        "means": "The rules exist, they are just not written down, and they will reappear as hand edits over whatever you build. Spend a session reconstructing them from the last quarter of changes and get the list signed.",
        "floor": 1,
        "ceiling": null
      }
    },
    {
      "id": "impressions",
      "order": 7,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "full",
        "heard": "Everything shown, with its position and an id tying the page together.",
        "means": "You have a record of what was shown, which is the thing most sites lack. Check one more level down: was the scoring input logged with it, or is it rebuilt later from the analytics tables? Rebuilds cannot reproduce what the engine saw.",
        "floor": 1,
        "ceiling": null
      }
    },
    {
      "id": "volume",
      "order": 8,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "high",
        "heard": "Hundreds of thousands a day, spread across a very long list of phrases.",
        "means": "Learning from behaviour is genuinely available and so is a test that settles in a week. This is the minority case, and it is the only one where the top of the ladder is honest work.",
        "floor": 1,
        "ceiling": null
      }
    },
    {
      "id": "reformulate",
      "order": 9,
      "status": "not_in_play",
      "gate": "People retype and try again in the same sitting",
      "closed_by": {
        "question": "empty",
        "answer": "high"
      }
    },
    {
      "id": "supersede",
      "order": 10,
      "status": "open",
      "options": [
        "Yes, both. The replaced-by chain and the cross-reference table are kept current.",
        "There is a table. Nobody is sure how far behind it is.",
        "It lives in people. The counter staff know which part replaced which.",
        "I would have to ask the product data team."
      ]
    },
    {
      "id": "pictures",
      "order": 11,
      "status": "not_in_play",
      "gate": "People search with a picture or a document",
      "closed_by": {
        "question": "mix",
        "answer": "identifier"
      }
    },
    {
      "id": "authoring",
      "order": 12,
      "status": "not_in_play",
      "gate": "Somebody outside the company writes the descriptions",
      "closed_by": {
        "question": "attributes",
        "answer": "patchy"
      }
    },
    {
      "id": "wherefilter",
      "order": 13,
      "status": "not_in_play",
      "gate": "Filters have to be applied before the search, not after",
      "closed_by": {
        "question": "allowed",
        "answer": "price"
      }
    },
    {
      "id": "livestate",
      "order": 14,
      "status": "open",
      "options": [
        "It has to be right immediately. We sell single items that cannot be sold twice.",
        "A few minutes is fine. Nobody notices under about five.",
        "Overnight is genuinely fine. Prices move once a quarter.",
        "Nobody has ever put a number on it."
      ]
    },
    {
      "id": "paidwhere",
      "order": 15,
      "status": "not_in_play",
      "gate": "Some placements are paid for",
      "closed_by": {
        "question": "whocuts",
        "answer": "informal"
      }
    },
    {
      "id": "randomised",
      "order": 16,
      "status": "open",
      "options": [
        "Yes, a small slice runs shuffled and we keep the logs.",
        "Not today, but somebody could sign that off if it were argued.",
        "Nobody here would ever approve deliberately serving worse results.",
        "I do not know if we have ever done that."
      ]
    },
    {
      "id": "measure",
      "order": 17,
      "status": "open",
      "options": [
        "We mix the two orderings into one page and see which items get clicked.",
        "A split test. Two groups of people, one ordering each.",
        "We score it against a judgement set and ship if the number goes up.",
        "It goes out and we watch the dashboards."
      ]
    }
  ],
  "conflicts": [
    "A record of what was shown and the traffic to learn from it. This is the minority case where learning the ordering from behaviour is genuinely available rather than aspirational. Spend the conversation on the shuffled slice and the launch gate, because those are what decide whether it works."
  ],
  "still_to_ask": [
    "supersede",
    "livestate",
    "randomised",
    "measure"
  ],
  "counts": {
    "answered": 8,
    "stale": 0,
    "open": 4,
    "not_in_play": 5,
    "dropped": 0
  },
  "schema_version": "1.0",
  "problem_id": "search-conversion",
  "target_tier": 1,
  "derivation": {
    "floor": 1,
    "ceiling": 2,
    "recommended_tier": 1,
    "recommended_rung": 1,
    "clash": false
  }
}
```
