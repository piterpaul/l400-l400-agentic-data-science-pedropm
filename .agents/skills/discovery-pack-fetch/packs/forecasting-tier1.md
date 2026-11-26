---
schema_version: "1.0"
problem_id: "forecasting"
target_tier: 1
recommended_rung: 1
source: "built-in-classroom-pack"
---

# Discovery pack — Demand Forecasting & Inventory Allocation

`forecasting` · recorded by **classroom-repo** · version 1 · served 2026-10-27T00:00:00Z

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

> **VP Supply Chain, national grocery chain — 1,200 stores, 40k SKUs** — We keep stocking out of high-demand items while our warehouses are full of dead inventory. We need AI to tell us what to stock.
>
> **Director of Demand Planning, CPG manufacturer — 300 product families, monthly S&OP** — Our S&OP consensus process runs in a spreadsheet and takes three weeks. I need a statistical baseline the sales team can argue against, and a number I can put in front of the board.
>
> **Head of Data Platform, quick-commerce grocer — 90 dark stores, 30-minute delivery** — We need to re-forecast every hour, per dark store per SKU, because availability drives cart abandonment and we are promising delivery windows in the app.

**Vocabulary is unbound.** The nouns below are the method's neutral words, not this customer's — treat them as placeholders and confirm the real terms early.

**The five specifics.**

- **How many, of the thing being predicted** — *not captured. Ask.*
- **How much history there is, and how much arrives** — *not captured. Ask.*
- **The deadline the run has to hit** — *not captured. Ask.*
- **What being wrong costs, per event or per year** — *not captured. Ask.*
- **Who owns the decision, and who would run this** — *not captured. Ask.*

## 2. Where discovery landed

- **Floor: Tier 1 — Serverless, In-Warehouse** — set by The level of detail the ordering system reads, How far ahead the decision needs, How many things, and how many are new, Is the total already committed?, Built-in methods vs custom Python packages, A range, or a single number?
- **Ceiling: Tier 1 — Serverless, In-Warehouse** — set by Drivers vs history-only baseline

> **Together, not apart.** Adding up and a range, together. Sold at no tier: the setting that produces a range will not combine with the one that makes the levels agree. Price a container, MinT and a scheduled pipeline.

## 3. What was asked, and what it steered

### 1. The level of detail the ordering system reads

**Asked:** When someone acts on this number, what exactly are they deciding about? One item, at one location, for one period? Or a whole group of them, across a whole area, for a much longer stretch? Ask what the ordering system actually reads — not what would score best in a bake-off.

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** One item, at one location, for the period our planners plan in.
- **Which means:** The common case. Thousands to hundreds of thousands of series, and every question below is now asked at this level — including how accuracy gets measured.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse, Tier 2 — Distributed & Custom ML is the ceiling
- **For the brief:** Level: one item, one location, one planning period.
- **Why it was asked:** The grain that everything else is counted at. Ask it first: it sets how many series there are, how accuracy gets measured, and whether the ordering system can consume the output at all.
- **What it forecloses:** Nothing yet — but every question below is asked at this level. Answering it late means asking most of them a second time.

### 2. How far back usable history goes

**Asked:** How far back does trustworthy history go for a typical item, and for a new one? Two clean years is a different project from four months. Then: what happened to 2020–2022 — is that period explained, deliberately cut out, or quietly still sitting in the data?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Months, not years, on a large share of them. The list turns over quickly.
- **Which means:** No yearly pattern to learn on those, but TimesFM at Tier 0 still forecasts from a few months. What fitting each alone cannot do is number an item with no history, and that is where cold start becomes the main event.
- **Bounds:** none
- **For the brief:** History: under two cycles on a large share — new items are core scope.
- **Why it was asked:** Whether a yearly pattern can be learned at all: that needs roughly two seasonal cycles. Separately, whether the pandemic years are a covariate, a deliberate hole, or silent contamination.
- **What it forecloses:** Under two cycles every seasonality question is moot, and cold start becomes the main event rather than a side quest.

### 3. How far ahead the decision needs

**Asked:** How far ahead does the number need to reach, and how did you get to that figure? Build it up out loud: how long the supplier takes, plus how long until the next chance to act, plus a margin. "Twelve weeks, because that is a quarter" is not a reason.

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** It varies hugely. Weeks for some items, days for others, depending on the supplier.
- **Which means:** Two models, not one model run twice. Accuracy then has to be measured at the distance each decision actually uses: excellent at one week and poor at eight is useless to a planner acting at eight.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Reach: varies by supplier — a separate model per lead-time band.
- **Why it was asked:** The horizon: supplier lead time, plus the review period, plus safety time. A reach that varies by supplier is not one model with a longer window — it is two models.
- **What it forecloses:** A short, uniform reach closes the long-lead branch and the distance-specific evaluation questions further down.

### 4. How many things, and how many are new

**Asked:** At that level of detail, how many separate things are you forecasting — hundreds, or tens of millions? And roughly what share of them are too new to have a year or two behind them? Multiply it out in the room: this gets under-estimated by a factor of a thousand routinely.

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Tens of thousands, into the millions. Most of them have history behind them.
- **Which means:** Still one statement at Tier 1 if nothing else forces you up: time_series_id_col fits thousands of series at once. Run time against the deadline the ordering system reads at becomes the thing to check.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse, Tier 2 — Distributed & Custom ML is the ceiling
- **For the brief:** Scale: millions of item-and-location lines, mostly established.
- **Why it was asked:** One SQL statement versus a registered fit. The share with under two seasonal cycles decides whether cold start is a footnote or the actual project — and that share, never the line count, is what argues for pooling.
- **What it forecloses:** A small, long-established set of series closes the new-item branch and most of the argument for Tier 2.

### 5. Is the total already committed?

**Asked:** Has anyone already committed to the total — a revenue figure finance has put in front of the board? Or is the total simply whatever the individual forecasts happen to add up to? Ask it exactly that way round. Asking whether the numbers "need to reconcile" gets a yes from everybody and tells you nothing.

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** The levels have to agree with each other. Nobody has fixed the top number.
- **Which means:** Adjust from the bottom up, which is a built-in option and costs nothing — as long as nothing else has to be true at the same time.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Levels must agree; adjust upward from the smallest parts.
- **Why it was asked:** Which direction reconciliation runs, and the direction picks the product. Bottom-up is a built-in option and costs nothing; top-down is sold nowhere managed, so you are writing it.
- **What it forecloses:** A total that is simply whatever the parts come to means no hierarchy requirement, which closes that whole branch — and with it the hardest trade-off on this problem.

### 6. Drivers vs history-only baseline

**Asked:** Besides past demand, what actually moves demand here — and do you need to prove the value added of those outside signals over a history-only fit? Separate what you know in advance for the periods being forecast — a promotion in the calendar, a published price, a holiday — from what you only find out afterwards, like weather or local traffic.

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Past demand, basically. It is fairly steady and nothing much moves it.
- **Which means:** Eight questions close at once. No contribution analysis, no forecasting the driver, no feed reliability, no pricing loop, no promotion lift. A history-only model is the honest answer.
- **Bounds:** Tier 1 — Serverless, In-Warehouse is the ceiling
- **For the brief:** No drivers: history-only modelling is appropriate.
- **Why it was asked:** The model class, outright. Anything besides past sales is a covariate, and the split that matters is known in advance versus only known afterwards: just the first kind can extend a forecast.
- **What it forecloses:** The biggest saving in the set. No drivers at all closes eight questions at once: contribution analysis, forecasting the driver, feed reliability, pricing, promotion lift. Ask it early, or spend the meeting on a branch that does not apply.

### 7. Built-in methods vs custom Python packages

**Asked:** Does the team want a managed baseline fast, or do they need to benchmark specific Python forecasting packages they already use against built-in methods across rewind folds — or combine them in a learned ensemble?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Compare built-in history-only fits against built-in driver models in SQL.
- **Which means:** Tier 1 in BigQuery: benchmark AI.FORECAST and univariate ARIMA_PLUS against ARIMA_PLUS_XREG to prove the value added of covariates over history alone.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse, Tier 2 — Distributed & Custom ML is the ceiling
- **For the brief:** Methods: in-BigQuery univariate vs covariate comparison.
- **Why it was asked:** Whether built-in BigQuery models (AI.FORECAST, ARIMA_PLUS_XREG) suffice, or whether Tier 2 must distribute series × Python methods on Managed Spark / UDFs or train a global TiDE/TFT fit.
- **What it forecloses:** If built-in methods meet the accuracy target on the rewind split, maintaining custom Python containers and Spark fan-out pipelines is unnecessary overhead.

### 8. A range, or a single number?

**Asked:** Can the ordering system take a range — "90% chance of 60 or fewer" — or does it want exactly one number? Ask whoever maintains that system rather than whoever asked for the forecast. They frequently give different answers.

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** It can take a range. The buffer policy already works off one.
- **Which means:** This is where the money is. How much buffer to hold depends on how bad a shortfall is, which is a question about the range and not about the average.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Output: a range is accepted downstream.
- **Why it was asked:** Whether anything above Tier 1 has somewhere to go. If the ordering system accepts one number, range forecasting buys nothing at all until that system changes — and changing it is somebody else’s roadmap.
- **What it forecloses:** A single-number answer closes the probabilistic branch at every tier, and makes a Tier 2 recommendation theatre.

## 4. Still worth asking

**These are instructions, not blanks.** Ask each one. The possible answers below are authored, with what each would rule in or out, so a reply can be recognised rather than interpreted.

### 9. Does everything need the same reach, or do some items need much longer?

**Ask:** Does everything need the same reach, or do some items need much longer? A distant supplier may need sixteen weeks while a local one needs three days — and that is two different models, not one model run twice.

What the answers would mean:

- **Yes. Two or three clear bands, depending on how far away the supplier is.** → Two or three models split by band, not one model with a longer window. Say it before anyone builds the first one, because retrofitting a second band means re-running every evaluation. *(floor Tier 1 — Serverless, In-Warehouse)*
- **No. Every supplier works to much the same timing.** → One model, one reach, and the distance-specific accuracy questions stay closed.
- **We go by what the agreement says. I do not think anyone has checked the real dates.** → Ten minutes with the real receipt dates settles it. The agreement states one number and the real spread is always wider — that spread is what the buffer is actually covering.

### 10. What has to add up to what?

**Ask:** What has to add up to what? Location into area into whole business, item into group into category — or both of those at the same time, which is a much harder problem than either alone.

What the answers would mean:

- **Just the one. Location into area, area into the whole business.** → One nesting, which is the tractable case and the one the built-in option handles. *(floor Tier 1 — Serverless, In-Warehouse)*
- **Both. Locations have to add up and so do the item groups.** → Substantially harder than either alone, and nothing managed does both axes. That is a hand-written MinT step inside a pipeline whatever else turns out to be true. *(floor Tier 2 — Distributed & Custom ML)*
- **Everything has to tie back to everything. I could not name the levels for you.** → Get the levels on a whiteboard. Two axes is a different project from one, and the difference is invisible in the way people describe it.

### 11. Do you need the numbers to add up and to account for promotions, at the same time?

**Ask:** Do you need the numbers to add up and to account for promotions, at the same time? Ask early. No single managed product does both, so needing the pair is on its own a sufficient reason to leave Tier 1 — and it is much cheaper to know that in week one.

What the answers would mean:

- **Yes, both. Promotions move the numbers and the numbers still have to add up.** → No single managed product does both. This alone is sufficient reason to leave Tier 1, and knowing it in week one rather than week nine is most of what this question is worth. *(floor Tier 2 — Distributed & Custom ML)*
- **Adding up matters. We hardly run promotions in this part of the business.** → Then Tier 1 does it for free with the built-in option, and the hardest trade-off in this problem never arises.
- **I have never thought about the two of them together. Separately, yes to each.** → Ask it as one sentence rather than two questions. Separately they both get a yes; together is the answer that picks the rung.

### 20. How does a brand-new item, or a location opening next month, get its first number?

**Ask:** How does a brand-new item, or a location opening next month, get its first number? Somebody is doing this today — find out whether it is a rule, a similar item picked by hand, or a planner typing in what feels right.

What the answers would mean:

- **A planner picks a similar item and copies its curve. It is all in their head.** → That is your baseline and your training signal at once. It is also the process being automated, so get the rule out of their head and written down while they are in the room.
- **Nothing. Somebody types in a flat guess and we correct it once it starts moving.** → Then the first-weeks number is a deliverable in its own right, and it needs a model that has learnt from other items — which is a rung, not a feature. *(floor Tier 2 — Distributed & Custom ML)*
- **Every planner does it differently. There is no rule I could write down.** → Sit with two of them for an hour. The variation between planners is itself the finding, and it is usually the strongest argument for the project.

### 21. How are items being retired handled?

**Ask:** How are items being retired handled? And can you tell the difference between "nobody wanted it" and "we had none available"? Both look like a run of zeros in the data and they mean opposite things.

What the answers would mean:

- **Every item carries a status flag, and we keep it current.** → Then a run of zeros can be read correctly. Without it, "nobody wanted it" and "we had none available" look identical and mean opposite things.
- **No. It just stops appearing one period, or it sits at zero forever.** → A retired item and a shortfall both read as zeros, so the model learns to forecast zero for items still on offer. A rule for this comes before any modelling. *(floor Tier 1 — Serverless, In-Warehouse)*
- **There is a flag. I would not trust it, and I do not know how stale it is.** → Same as not having one, and worth saying so plainly. Check it against the last hundred retirements before relying on it in training.

### 22. Is accuracy measured at the distance the decision actually uses?

**Ask:** Is accuracy measured at the distance the decision actually uses? A model that looks excellent one week out can be poor at eight weeks, and eight weeks is what the planner is acting on.

What the answers would mean:

- **Yes. We score it at the distance the planner actually acts at.** → Rare, and worth keeping. A model that looks excellent one week out can be poor at eight weeks, and eight is the number being acted on.
- **No. One number, averaged across the whole window, and that is what we report.** → That average hides the only part anyone acts on. Break it out per distance band before agreeing a target, or the target gets met while the orders stay wrong. *(floor Tier 1 — Serverless, In-Warehouse)*
- **Honestly, we do not measure it today. Nobody has ever scored what we do now.** → Then the first deliverable is a number for the current process, including manual adjustments. Without it there is nothing to beat and no way to show you did.

## 5. Not worth asking yet

Each of these is gated behind a branch that is not open. They are listed so the absence is legible: they were not forgotten, they were ruled out.

- **Sort every candidate driver into three boxes before designing anything** — closed by *Drivers vs history-only baseline* → “Past demand, basically. It is fairly steady and nothing much moves it”.
- **The drivers you only learn afterwards are still worth collecting: they cannot extend the forecast, but they explain why last month was odd and they support a same-day adjustment** — closed by *Drivers vs history-only baseline* → “Past demand, basically. It is fairly steady and nothing much moves it”.
- **The moment a driver enters the model, somebody will ask why the number moved** — closed by *Drivers vs history-only baseline* → “Past demand, basically. It is fairly steady and nothing much moves it”.
- **For anything you only learn afterwards: is somebody already forecasting that thing itself?** — closed by *Drivers vs history-only baseline* → “Past demand, basically. It is fairly steady and nothing much moves it”.
- **Is a promotion the single biggest reason demand moves?** — closed by *Drivers vs history-only baseline* → “Past demand, basically. It is fairly steady and nothing much moves it”.
- **When you push one item, what happens to the ones beside it?** — closed by *Drivers vs history-only baseline* → “Past demand, basically. It is fairly steady and nothing much moves it”.
- **Is price being set by another system or another model?** — closed by *Drivers vs history-only baseline* → “Past demand, basically. It is fairly steady and nothing much moves it”.
- **If a driver feed arrives late or not at all, does anyone find out?** — closed by *Drivers vs history-only baseline* → “Past demand, basically. It is fairly steady and nothing much moves it”.

## 6. What is being suggested, and why the alternatives are out

### Tier 1 — Serverless, In-Warehouse

Thousands of lines at once: promotions or levels that add up

- **What it is:** Iceberg managed tables → ARIMA_PLUS_XREG or hierarchical ARIMA_PLUS → Dataform on a schedule → forecast table
- **Google Cloud & open-weight options at this rung:** BigQuery ML, ARIMA_PLUS_XREG, HIERARCHICAL_TIME_SERIES_COLS, ML.EXPLAIN_FORECAST, AI.FORECAST (TimesFM 3.0), Iceberg managed tables, Dataform
- **What it carries:** Both axes carried from Tier 0; what changed is that you now train your own model, with covariates or a hierarchy, and Dataform sequences the run.
- **Why here:** time_series_id_col = ['location','item'] fits thousands of series in one line, and ML.EXPLAIN_FORECAST hands a planner a breakdown to argue with. One discovery answer picks which: XREG adds promotions, HIERARCHICAL_TIME_SERIES_COLS buys numbers that add up.
- **Where it breaks:** Never both: HIERARCHICAL_TIME_SERIES_COLS is ARIMA_PLUS-only, so needing promotions and a number that sums to plan ends this rung. It only works bottom-up, useless against a total finance has already committed. Nothing for slow movers. No export.
- **What would move it up:** Promotions and adding-up are needed together, most items are slow-moving, or the run crosses the deadline.

#### Architecture Decision Record (ADR) Matrix

A scenario-aware evaluation of the ladder against this customer's constraints. Where an adjacent tier serves as a viable A/B benchmark or a Phase 2 evolution, that role is explicitly called out:

| Rung | Role in this Engagement | Architecture & Stance | Deciding Constraint & Trade-off |
| --- | --- | --- | --- |
| Tier 0 — Out of the Box | **Adjacent Lower Tier (A/B Benchmark)** | A forecast from a model nobody here trained. Lower complexity and operational overhead. | Below the floor (Tier 1 — Serverless, In-Warehouse), set by The level of detail the ordering system reads, How far ahead the decision needs, How many things, and how many are new, Is the total already committed?, Built-in methods vs custom Python packages, A range, or a single number?. Viable as an A/B comparator to quantify the performance/accuracy lift of Tier 1 — Serverless, In-Warehouse. |
| Tier 1 — Serverless, In-Warehouse | **Primary Baseline (MVP)** | Thousands of lines at once: promotions or levels that add up. Fits all bounded constraints. | Selected target. Fits floor (Tier 1 — Serverless, In-Warehouse) and ceiling (Tier 1 — Serverless, In-Warehouse). Wins: time_series_id_col = ['location','item'] fits thousands of series in one line, and ML.EXPLAIN_FORECAST hands a planner a breakdown to argue with. One discovery answer picks which: XREG adds promotions, HIERARCHICAL_TIME_SERIES_COLS buys numbers that add up. |
| Tier 2 — Distributed & Custom ML | Ruled out (Theatre) | A registered fit: a range or adding up, not both. | Past the ceiling (Tier 1 — Serverless, In-Warehouse), set by Drivers vs history-only baseline. Unjustified operational cost. |
| Tier 3 — Real-Time & Specialised | Ruled out (Theatre) | A promise made while the customer waits, against reality. | Past the ceiling (Tier 1 — Serverless, In-Warehouse), set by Drivers vs history-only baseline. Unjustified operational cost. |

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

- Tier 0 — Out of the Box — A forecast from a model nobody here trained. Out: the floor is Tier 1 — Serverless, In-Warehouse — The level of detail the ordering system reads, How far ahead the decision needs, How many things, and how many are new, Is the total already committed?, Built-in methods vs custom Python packages, A range, or a single number?.

**Above it, and why that is theatre here.**

- Tier 2 — Distributed & Custom ML — A registered fit: a range or adding up, not both. Out: past the ceiling at Tier 1 — Serverless, In-Warehouse — Drivers vs history-only baseline.
- Tier 3 — Real-Time & Specialised — A promise made while the customer waits, against reality. Out: past the ceiling at Tier 1 — Serverless, In-Warehouse — Drivers vs history-only baseline.

**Below the rung sit the calls no rung makes for you.** The tier does not settle these, and a design that has not stated them has not been made. Nothing on the page asks for them, so they travel unanswered.

- **What one row is** — One item at one location for one period, because that is what the ordering system orders at. Anything coarser has to be split back down before it can be acted on, and splitting is where the accuracy goes.
  Options: The level the ordering system reads · A coarser level, then split down
- **What goes in beside the past** — Whether each line is fitted on its own past alone or with promotions, prices and calendar effects beside it — and this is a separate question from how many models there are.
  Options: Own past only · Drivers alongside
- **One fit, one each, or one per group** — Forty-eight million lines can be forty-eight million fits, one fit with line identity as a column, or a fit per category. All three are on Tier 2 and the rung does not choose between them.
  Options: One fit per line · One fit across everything · One fit per category
- **Which methods get a run** — A slow-mover method, a boosted tree on a stacked table, and a pretrained model that has never seen your data. All three are cheap enough here to run against each other.
  Options: Statistical · Boosted trees on a stacked table · Pretrained
- **How you would know** — A rewind from several starting points, each one hiding everything that had not arrived by that date, scored on a measure that survives a line which sold nothing.
  Options: Rewind from several origins · A single held-back tail
- **What tuning is worth** — Search order matters more than search budget. Getting the shortfall correction right and getting the stacked table right both pay more than any setting search, and they pay first.
  Options: Leave the defaults · Search the settings
- **One winner, or several combined** — Averaging a statistical fit, a boosted tree and a pretrained model is one line of code once all three exist. Whether it is worth keeping is a measurement, and it goes both ways on the same catalog.
  Options: Pick the winner · Average them
- **Making the numbers agree** — Line numbers do not sum to the category plan, and the category plan is what gets committed to. Something has to make them add up, in one direction or the other.
  Options: Add up from the bottom · Split a committed total down · Adjust every level at once

**Dataset for the build.** Every workshop build runs on public or shipped tables:

- **Source:** BigQuery public tables
- **Tables:** `bigquery-public-data.new_york_citibike.citibike_trips`, `bigquery-public-data.new_york_citibike.citibike_stations`, `bigquery-public-data.ml_datasets.holidays_and_events_for_forecasting`, `bigquery-public-data.noaa_gsod.gsod*`
- **Grain & size:** Daily station-level and rider-segment demand (`start_station_id`, `usertype`, `trip_date`) across all NYC Citi Bike stations on a birth-aware spine (`trip_date >= station_first_date`), joined with `citibike_stations` metadata (`capacity`, `latitude`, `longitude`), causal `station_customer_share` ratio (`ROWS BETWEEN 36 PRECEDING AND 30 PRECEDING`), horizon-safe 30-day lags (`lag_30d`, `lag_37d`), holiday indicators, and NOAA weather observations.
- **Target / label:** Daily trip starts (`total_trips`) per station (`start_station_id`) and rider segment (`usertype`) over a 30-day rebalance horizon, reconciling bottom-level `station_id × usertype` forecasts up to `usertype` (`Subscriber`, `Customer`) and system-wide totals.
- **Tier 1 / Tier 2 build:** Tier 0 runs `AI.FORECAST` (`TimesFM`) and a Conversational Analytics Data Agent over segment totals; Tier 1 fits `ARIMA_PLUS` (hierarchical) and `ARIMA_PLUS_XREG` (weather/holiday/`station_customer_share` covariates) in BigQuery ML; Tier 2 runs a multi-runtime challenger tournament across BigQuery ML (`ARIMA_PLUS` / `ARIMA_PLUS_XREG`), Serverless Spark (`groupBy.applyInPandas` for `Holt-Winters` & `ThetaModel`, and `SparkML` for distributed `SparkXGBRegressor` / `GBTRegressor`), and Vertex AI CustomJob (global `XGBoost` / `RandomForestRegressor` scoring established + cold-start stations & hierarchical reconciliation), aggregated into a BigQuery SQL ensemble.
- **Caveat:** Multi-day weather or operational shutdowns vanish from a naive `GROUP BY DATE(starttime)` unless left-joined to a continuous `GENERATE_DATE_ARRAY` calendar spine (`trip_date >= station_first_date`); autoregressive lags and rolling ratios over a 30-day holdout must look back at least 30 days (`LAG(..., 30)`, `ROWS BETWEEN 36 PRECEDING AND 30 PRECEDING`) to prevent target leakage; and raw NOAA `gsod*` weather fields contain out-of-range missing-value sentinel numbers (`9999.9`, `99.99`, `999.9`) that must be profiled and cleaned.
- **Setup / verify:** `bq head -n 5 bigquery-public-data:new_york_citibike.citibike_stations`
- **Agent skills (`bigquery-data-science` & Data Agent Kit):** `uvx bigquery-data-science lookup AI.FORECAST # BQDS: AI.DETECT_ANOMALIES, AI.EVALUATE, ARIMA_PLUS_XREG, BOOSTED_TREE_REGRESSOR, ML.EXPLAIN_FORECAST | Data Agent Kit: bigquery-ai-ml, dataform-bigquery, bigquery-bigframes, ml-best-practices, gcp-spark`

**The ladder, for reference.** No site is needed to read the tiers above.

- **Tier 0 — Out of the Box** — A model somebody else trained already answers the question. Nothing to fit, nothing to provision, and the bill starts on the first query. The most senior move in the room is often to say so.
- **Tier 1 — Serverless, In-Warehouse** — Bring the model to the data. No cluster, no container, no serving stack. SQL is the interface.
- **Tier 2 — Distributed & Custom ML** — The transformation or the model outgrew SQL. Bring distributed compute to the data, keep the storage where it is.
- **Tier 3 — Real-Time & Specialised** — A hard SLA or a custom objective justifies owning the stack. You are now engineering a system, not training a model.
- **Tier 4 — Hardening for High-Stakes Operation** — Not a rung you buy. It is what changes about a system already at Tier 1, 2 or 3 once being wrong is expensive, contested or unsafe — and what changes is different for every problem in Discovery.

## 7. POC Data Discovery & Challenger Contract (Pass 2 · Solo Tier 1)

Pass 2 builds directly on the data facts you discovered in Pass 1 and expands the investigation to station-level series across all NYC Citi Bike stations, `station_customer_share` ratio covariates, and exogenous weather/holiday covariates in BigQuery ML:

- **BigQuery Source Tables (`bigquery-region: "US"`):** `bigquery-public-data.new_york_citibike.citibike_trips`, `bigquery-public-data.new_york_citibike.citibike_stations`, `bigquery-public-data.ml_datasets.holidays_and_events_for_forecasting`, `bigquery-public-data.noaa_gsod.gsod*`
- **Pass 1 -> Pass 2 Data Discovery Continuity for `agy` in Step 3 (Checkpoint 08):**
  1. **Carry Forward Pass 1 Findings:** Reuse the contiguous historical window, continuous `GENERATE_DATE_ARRAY` calendar spine (zero-filling multi-day weather shutdowns), 30-day temporal holdout split, and Pass 1 `citibike_tier0.holdout_eval_summary` baseline error floor.
  2. **All-Station Hierarchy, Birth-Aware Spine & `station_customer_share` Ratio Covariate:** Profile `citibike_stations` and `citibike_trips` across all active stations × `usertype`, build a birth-aware calendar spine (`trip_date >= station_first_date`), and compute both horizon-safe 30-day lags (`lag_30d`, `lag_37d`) and the causal `station_customer_share` ratio (`ROWS BETWEEN 36 PRECEDING AND 30 PRECEDING`).
  3. **NOAA GSOD Weather Sentinel Discovery:** Profile `bigquery-public-data.noaa_gsod.gsod*` (filtering to NYC Central Park station `stn = '725053'` across your historical years) by inspecting `MIN`/`MAX` of `temp`, `prcp`, and `wdsp` to discover out-of-range missing-value sentinel numbers (`9999.9`, `99.99`, `999.9`) that must be cleaned with `NULLIF` before model fitting.
  4. **Holiday & Calendar Covariates:** Inspect `bigquery-public-data.ml_datasets.holidays_and_events_for_forecasting` (`region = 'US'`) and calendar indicators (`day_of_week`, `is_weekend`) to capture leisure demand spikes.
- **Pass 2 Target Deliverables (`l400_ds_work` at Tier 1):**
  - `DESIGN.md` with Mermaid architecture diagram and `## Architect's Design Audit & Steering Log` (Checkpoint 08)
  - Custom execution skill `.agents/skills/build-forecasting/SKILL.md` (Checkpoint 09)
  - Leak-free `l400_ds_work.feature_spine` joining birth-aware station × `usertype` calendar spine + `station_customer_share` ratio + cleaned NOAA weather + US holidays (Checkpoint 10)
  - In-warehouse BigQuery ML model training (`ARIMA_PLUS`, `ARIMA_PLUS_XREG`, `BOOSTED_TREE_REGRESSOR`, or `AI.FORECAST` `TimesFM 3.0` with covariates in `bigquery-region` — zero local VM compute) writing `l400_ds_work.eval_comparison` and `artifacts/eval_metrics.json` (Checkpoint 11)
  - Pass 1 (Tier 0) vs. Pass 2 holdout showdown & promotion decision in `EVALUATION.md` (Checkpoint 12)

---

### The same thing, for a program to read

```json
{
  "problem": "forecasting",
  "ldap": "classroom-repo",
  "version": 1,
  "served_at": "2026-10-27T00:00:00Z",
  "binding": {
    "item": "item",
    "location": "location",
    "period": "period",
    "consumer": "ordering system",
    "decider": "planner",
    "action": "order",
    "shortfall": "shortfall",
    "source": "supplier",
    "lever": "promotion"
  },
  "range": {
    "floor": 1,
    "ceiling": 1,
    "clash": false
  },
  "recommended_rung": 1,
  "data": {
    "source": "BigQuery public tables",
    "tables": [
      "bigquery-public-data.new_york_citibike.citibike_trips",
      "bigquery-public-data.new_york_citibike.citibike_stations",
      "bigquery-public-data.ml_datasets.holidays_and_events_for_forecasting",
      "bigquery-public-data.noaa_gsod.gsod*"
    ],
    "grain": "Daily station-level and rider-segment demand (start_station_id, usertype, trip_date) across all NYC Citi Bike stations on a birth-aware spine (trip_date >= station_first_date), joined with citibike_stations metadata (capacity, latitude, longitude), causal station_customer_share ratio (ROWS BETWEEN 36 PRECEDING AND 30 PRECEDING), horizon-safe 30-day lags (lag_30d, lag_37d), holiday indicators, and NOAA weather observations.",
    "label": "Daily trip starts (total_trips) per station (start_station_id) and rider segment (usertype) over a 30-day rebalance horizon, reconciling bottom-level station_id x usertype forecasts up to usertype (Subscriber, Customer) and system-wide totals.",
    "rungs": "Tier 0 runs AI.FORECAST (TimesFM) and a Conversational Analytics Data Agent over segment totals; Tier 1 fits ARIMA_PLUS (hierarchical) and ARIMA_PLUS_XREG (weather/holiday/station_customer_share covariates) in BigQuery ML; Tier 2 runs a multi-runtime challenger tournament across BigQuery ML (ARIMA_PLUS / ARIMA_PLUS_XREG), Serverless Spark (applyInPandas Holt-Winters & ThetaModel, and SparkML SparkXGBRegressor / GBTRegressor), and Vertex AI CustomJob (global XGBoost / RandomForestRegressor scoring established + cold-start stations & hierarchical reconciliation), aggregated into a BigQuery SQL ensemble.",
    "caveat": "Multi-day weather or operational shutdowns vanish from a naive GROUP BY DATE(starttime) unless left-joined to a continuous GENERATE_DATE_ARRAY calendar spine (trip_date >= station_first_date); autoregressive lags and rolling ratios over a 30-day holdout must look back at least 30 days (LAG(..., 30), ROWS BETWEEN 36 PRECEDING AND 30 PRECEDING) to prevent target leakage; and raw NOAA gsod* weather fields contain out-of-range missing-value sentinel numbers (9999.9, 99.99, 999.9) that must be profiled and cleaned.",
    "setup": "bq head -n 5 bigquery-public-data:new_york_citibike.citibike_stations",
    "skills": "uvx bigquery-data-science lookup AI.FORECAST # BQDS: AI.DETECT_ANOMALIES, AI.EVALUATE, ARIMA_PLUS_XREG, BOOSTED_TREE_REGRESSOR, ML.EXPLAIN_FORECAST | Data Agent Kit: bigquery-ai-ml, dataform-bigquery, bigquery-bigframes, ml-best-practices, gcp-spark"
  },
  "questions": [
    {
      "id": "grain",
      "order": 1,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "planning",
        "heard": "One item, at one location, for the period our planners plan in.",
        "means": "The common case. Thousands to hundreds of thousands of series, and every question below is now asked at this level — including how accuracy gets measured.",
        "floor": 1,
        "ceiling": 2
      }
    },
    {
      "id": "history",
      "order": 2,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "short",
        "heard": "Months, not years, on a large share of them. The list turns over quickly.",
        "means": "No yearly pattern to learn on those, but TimesFM at Tier 0 still forecasts from a few months. What fitting each alone cannot do is number an item with no history, and that is where cold start becomes the main event.",
        "floor": null,
        "ceiling": null
      }
    },
    {
      "id": "horizon",
      "order": 3,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "mixed",
        "heard": "It varies hugely. Weeks for some items, days for others, depending on the supplier.",
        "means": "Two models, not one model run twice. Accuracy then has to be measured at the distance each decision actually uses: excellent at one week and poor at eight is useless to a planner acting at eight.",
        "floor": 1,
        "ceiling": null
      }
    },
    {
      "id": "count",
      "order": 4,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "large",
        "heard": "Tens of thousands, into the millions. Most of them have history behind them.",
        "means": "Still one statement at Tier 1 if nothing else forces you up: time_series_id_col fits thousands of series at once. Run time against the deadline the ordering system reads at becomes the thing to check.",
        "floor": 1,
        "ceiling": 2
      }
    },
    {
      "id": "total",
      "order": 5,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "levels",
        "heard": "The levels have to agree with each other. Nobody has fixed the top number.",
        "means": "Adjust from the bottom up, which is a built-in option and costs nothing — as long as nothing else has to be true at the same time.",
        "floor": 1,
        "ceiling": null
      }
    },
    {
      "id": "drivers",
      "order": 6,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "none",
        "heard": "Past demand, basically. It is fairly steady and nothing much moves it.",
        "means": "Eight questions close at once. No contribution analysis, no forecasting the driver, no feed reliability, no pricing loop, no promotion lift. A history-only model is the honest answer.",
        "floor": null,
        "ceiling": 1
      }
    },
    {
      "id": "method-compare",
      "order": 7,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "sql-covar",
        "heard": "Compare built-in history-only fits against built-in driver models in SQL.",
        "means": "Tier 1 in BigQuery: benchmark AI.FORECAST and univariate ARIMA_PLUS against ARIMA_PLUS_XREG to prove the value added of covariates over history alone.",
        "floor": 1,
        "ceiling": 2
      }
    },
    {
      "id": "output",
      "order": 8,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "range",
        "heard": "It can take a range. The buffer policy already works off one.",
        "means": "This is where the money is. How much buffer to hold depends on how bad a shortfall is, which is a question about the range and not about the average.",
        "floor": 1,
        "ceiling": null
      }
    },
    {
      "id": "lead-bands",
      "order": 9,
      "status": "open",
      "options": [
        "Yes. Two or three clear bands, depending on how far away the supplier is.",
        "No. Every supplier works to much the same timing.",
        "We go by what the agreement says. I do not think anyone has checked the real dates."
      ]
    },
    {
      "id": "rollup-shape",
      "order": 10,
      "status": "open",
      "options": [
        "Just the one. Location into area, area into the whole business.",
        "Both. Locations have to add up and so do the item groups.",
        "Everything has to tie back to everything. I could not name the levels for you."
      ]
    },
    {
      "id": "addup-plus-promo",
      "order": 11,
      "status": "open",
      "options": [
        "Yes, both. Promotions move the numbers and the numbers still have to add up.",
        "Adding up matters. We hardly run promotions in this part of the business.",
        "I have never thought about the two of them together. Separately, yes to each."
      ]
    },
    {
      "id": "driver-boxes",
      "order": 12,
      "status": "not_in_play",
      "gate": "Anything other than past sales drives demand",
      "closed_by": {
        "question": "drivers",
        "answer": "none"
      }
    },
    {
      "id": "observed-value",
      "order": 13,
      "status": "not_in_play",
      "gate": "Some drivers are only known afterwards",
      "closed_by": {
        "question": "drivers",
        "answer": "none"
      }
    },
    {
      "id": "explain",
      "order": 14,
      "status": "not_in_play",
      "gate": "Anything other than past sales drives demand",
      "closed_by": {
        "question": "drivers",
        "answer": "none"
      }
    },
    {
      "id": "driver-forecast",
      "order": 15,
      "status": "not_in_play",
      "gate": "Some drivers are only known afterwards",
      "closed_by": {
        "question": "drivers",
        "answer": "none"
      }
    },
    {
      "id": "promo-dominant",
      "order": 16,
      "status": "not_in_play",
      "gate": "Anything other than past sales drives demand",
      "closed_by": {
        "question": "drivers",
        "answer": "none"
      }
    },
    {
      "id": "cross-effects",
      "order": 17,
      "status": "not_in_play",
      "gate": "Anything other than past sales drives demand",
      "closed_by": {
        "question": "drivers",
        "answer": "none"
      }
    },
    {
      "id": "price-loop",
      "order": 18,
      "status": "not_in_play",
      "gate": "Anything other than past sales drives demand",
      "closed_by": {
        "question": "drivers",
        "answer": "none"
      }
    },
    {
      "id": "feed-alarm",
      "order": 19,
      "status": "not_in_play",
      "gate": "Anything other than past sales drives demand",
      "closed_by": {
        "question": "drivers",
        "answer": "none"
      }
    },
    {
      "id": "new-item-today",
      "order": 20,
      "status": "open",
      "options": [
        "A planner picks a similar item and copies its curve. It is all in their head.",
        "Nothing. Somebody types in a flat guess and we correct it once it starts moving.",
        "Every planner does it differently. There is no rule I could write down."
      ]
    },
    {
      "id": "lifecycle-flag",
      "order": 21,
      "status": "open",
      "options": [
        "Every item carries a status flag, and we keep it current.",
        "No. It just stops appearing one period, or it sits at zero forever.",
        "There is a flag. I would not trust it, and I do not know how stale it is."
      ]
    },
    {
      "id": "horizon-eval",
      "order": 22,
      "status": "open",
      "options": [
        "Yes. We score it at the distance the planner actually acts at.",
        "No. One number, averaged across the whole window, and that is what we report.",
        "Honestly, we do not measure it today. Nobody has ever scored what we do now."
      ]
    }
  ],
  "conflicts": [
    "Adding up and a range, together. Sold at no tier: the setting that produces a range will not combine with the one that makes the levels agree. Price a container, MinT and a scheduled pipeline."
  ],
  "still_to_ask": [
    "lead-bands",
    "rollup-shape",
    "addup-plus-promo",
    "new-item-today",
    "lifecycle-flag",
    "horizon-eval"
  ],
  "counts": {
    "answered": 8,
    "stale": 0,
    "open": 6,
    "not_in_play": 8,
    "dropped": 0
  },
  "schema_version": "1.0",
  "problem_id": "forecasting",
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
