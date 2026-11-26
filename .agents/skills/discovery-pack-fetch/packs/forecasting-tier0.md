---
schema_version: "1.0"
problem_id: "forecasting"
target_tier: 0
recommended_rung: 0
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

- **Floor: Tier 0 — Out of the Box** — set by The level of detail the ordering system reads, Built-in methods vs custom Python packages
- **Ceiling: Tier 1 — Serverless, In-Warehouse** — set by The level of detail the ordering system reads, How many things, and how many are new, Drivers vs history-only baseline, Built-in methods vs custom Python packages, A range, or a single number?

## 3. What was asked, and what it steered

### 1. The level of detail the ordering system reads

**Asked:** When someone acts on this number, what exactly are they deciding about? One item, at one location, for one period? Or a whole group of them, across a whole area, for a much longer stretch? Ask what the ordering system actually reads — not what would score best in a bake-off.

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** A group of items across a whole area, for a long stretch. We meet about it.
- **Which means:** Few series, a slow clock, and a decision made by people in a room. Tier 0 gives a defensible number this week, and machinery above Tier 1 is being bought for a spreadsheet-sized problem.
- **Bounds:** not below Tier 0 — Out of the Box, Tier 1 — Serverless, In-Warehouse is the ceiling
- **For the brief:** Level: grouped items, wide area, long period.
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

- **Heard:** Days. We act today and it lands this week.
- **Which means:** A short reach closes the long-lead branch and the distance-specific accuracy questions. The horizon is set by the ordering rhythm rather than by the model.
- **Bounds:** none
- **For the brief:** Reach: days, the same for everything.
- **Why it was asked:** The horizon: supplier lead time, plus the review period, plus safety time. A reach that varies by supplier is not one model with a longer window — it is two models.
- **What it forecloses:** A short, uniform reach closes the long-lead branch and the distance-specific evaluation questions further down.

### 4. How many things, and how many are new

**Asked:** At that level of detail, how many separate things are you forecasting — hundreds, or tens of millions? And roughly what share of them are too new to have a year or two behind them? Multiply it out in the room: this gets under-estimated by a factor of a thousand routinely.

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** A few hundred, maybe a couple of thousand. They have all been around for years.
- **Which means:** Laptop-sized. One SQL statement fits the lot, and saying that plainly is worth more to this customer than an architecture. Anything above Tier 1 here is theatre.
- **Bounds:** Tier 1 — Serverless, In-Warehouse is the ceiling
- **For the brief:** Scale: low thousands, established.
- **Why it was asked:** One SQL statement versus a registered fit. The share with under two seasonal cycles decides whether cold start is a footnote or the actual project — and that share, never the line count, is what argues for pooling.
- **What it forecloses:** A small, long-established set of series closes the new-item branch and most of the argument for Tier 2.

### 5. Is the total already committed?

**Asked:** Has anyone already committed to the total — a revenue figure finance has put in front of the board? Or is the total simply whatever the individual forecasts happen to add up to? Ask it exactly that way round. Asking whether the numbers "need to reconcile" gets a yes from everybody and tells you nothing.

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Nobody has fixed a total. It is whatever the parts come to.
- **Which means:** The biggest close on this problem. No committed total means no adding-up requirement, which removes that branch entirely — and with it the hardest trade-off in Discovery.
- **Bounds:** none
- **For the brief:** No committed total: a plain roll-up is sufficient.
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

- **Heard:** Start with a zero-setup baseline and plain-English answers over past demand.
- **Which means:** Tier 0 fits the brief: run AI.FORECAST (TimesFM), AI.DETECT_ANOMALIES, and AI.EVALUATE on the demand history table with a Conversational Analytics Data Agent answering forward-facing questions.
- **Bounds:** not below Tier 0 — Out of the Box, Tier 1 — Serverless, In-Warehouse is the ceiling
- **For the brief:** Methods: zero-setup built-in baseline with conversational self-service.
- **Why it was asked:** Whether built-in BigQuery models (AI.FORECAST, ARIMA_PLUS_XREG) suffice, or whether Tier 2 must distribute series × Python methods on Managed Spark / UDFs or train a global TiDE/TFT fit.
- **What it forecloses:** If built-in methods meet the accuracy target on the rewind split, maintaining custom Python containers and Spark fan-out pipelines is unnecessary overhead.

### 8. A range, or a single number?

**Asked:** Can the ordering system take a range — "90% chance of 60 or fewer" — or does it want exactly one number? Ask whoever maintains that system rather than whoever asked for the forecast. They frequently give different answers.

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** One number. There is one field in the ordering system and it takes one number.
- **Which means:** Then a range buys nothing until that system changes, and changing it is somebody else’s roadmap. Recommending Tier 2 for probabilistic forecasting here is theatre.
- **Bounds:** Tier 1 — Serverless, In-Warehouse is the ceiling
- **For the brief:** Output: a single number — downstream takes no range.
- **Why it was asked:** Whether anything above Tier 1 has somewhere to go. If the ordering system accepts one number, range forecasting buys nothing at all until that system changes — and changing it is somebody else’s roadmap.
- **What it forecloses:** A single-number answer closes the probabilistic branch at every tier, and makes a Tier 2 recommendation theatre.

## 4. Still worth asking

**These are instructions, not blanks.** Ask each one. The possible answers below are authored, with what each would rule in or out, so a reply can be recognised rather than interpreted.

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

## 5. Not worth asking yet

Each of these is gated behind a branch that is not open. They are listed so the absence is legible: they were not forgotten, they were ruled out.

- **Does everything need the same reach, or do some items need much longer?** — closed by *How far ahead the decision needs* → “Days. We act today and it lands this week”.
- **What has to add up to what?** — closed by *Is the total already committed?* → “Nobody has fixed a total. It is whatever the parts come to”.
- **Do you need the numbers to add up and to account for promotions, at the same time?** — closed by *Is the total already committed?* → “Nobody has fixed a total. It is whatever the parts come to”.
- **Sort every candidate driver into three boxes before designing anything** — closed by *Drivers vs history-only baseline* → “Past demand, basically. It is fairly steady and nothing much moves it”.
- **The drivers you only learn afterwards are still worth collecting: they cannot extend the forecast, but they explain why last month was odd and they support a same-day adjustment** — closed by *Drivers vs history-only baseline* → “Past demand, basically. It is fairly steady and nothing much moves it”.
- **The moment a driver enters the model, somebody will ask why the number moved** — closed by *Drivers vs history-only baseline* → “Past demand, basically. It is fairly steady and nothing much moves it”.
- **For anything you only learn afterwards: is somebody already forecasting that thing itself?** — closed by *Drivers vs history-only baseline* → “Past demand, basically. It is fairly steady and nothing much moves it”.
- **Is a promotion the single biggest reason demand moves?** — closed by *Drivers vs history-only baseline* → “Past demand, basically. It is fairly steady and nothing much moves it”.
- **When you push one item, what happens to the ones beside it?** — closed by *Drivers vs history-only baseline* → “Past demand, basically. It is fairly steady and nothing much moves it”.
- **Is price being set by another system or another model?** — closed by *Drivers vs history-only baseline* → “Past demand, basically. It is fairly steady and nothing much moves it”.
- **If a driver feed arrives late or not at all, does anyone find out?** — closed by *Drivers vs history-only baseline* → “Past demand, basically. It is fairly steady and nothing much moves it”.
- **Is accuracy measured at the distance the decision actually uses?** — closed by *How far ahead the decision needs* → “Days. We act today and it lands this week”.

## 6. What is being suggested, and why the alternatives are out

### Tier 0 — Out of the Box

A forecast from a model nobody here trained

- **What it is:** BigQuery AI.FORECAST with the built-in TimesFM model → Conversational Analytics for planner self-service
- **Google Cloud & open-weight options at this rung:** BigQuery, AI.FORECAST, AI.DETECT_ANOMALIES, AI.PREDICT, Conversational Analytics
- **Why here:** One statement, no model artefact, no training job, no schedule. Produces a defensible accuracy floor in an afternoon and a number every later tier must beat. AI.DETECT_ANOMALIES over the same history surfaces the data faults that were the real problem.
- **Where it breaks:** Univariate: no promotion, no price effect, no breakdown to show a planner, and no way to make the numbers add up. And context_window truncates from the oldest end, so an hourly history quietly loses its annual season and nothing warns you.
- **What would move it up:** Someone must defend the number to a planner, or promotions explain more of the movement than the time of year — either forces covariates and a breakdown.

#### Architecture Decision Record (ADR) Matrix

A scenario-aware evaluation of the ladder against this customer's constraints. Where an adjacent tier serves as a viable A/B benchmark or a Phase 2 evolution, that role is explicitly called out:

| Rung | Role in this Engagement | Architecture & Stance | Deciding Constraint & Trade-off |
| --- | --- | --- | --- |
| Tier 0 — Out of the Box | **Primary Baseline (MVP)** | A forecast from a model nobody here trained. Fits all bounded constraints. | Selected target. Fits floor (Tier 0 — Out of the Box) and ceiling (Tier 1 — Serverless, In-Warehouse). Wins: One statement, no model artefact, no training job, no schedule. Produces a defensible accuracy floor in an afternoon and a number every later tier must beat. AI.DETECT_ANOMALIES over the same history surfaces the data faults that were the real problem. |
| Tier 1 — Serverless, In-Warehouse | **Adjacent Higher Tier (Phase 2 Evolution)** | Thousands of lines at once: promotions or levels that add up. Higher freshness, lower latency, or specialised modeling. | Inside the range, but nothing heard requires it yet. Step-up trigger: Someone must defend the number to a planner, or promotions explain more of the movement than the time of year — either forces covariates and a breakdown. Propose as Phase 2 expansion once this condition is met. |
| Tier 2 — Distributed & Custom ML | Ruled out (Theatre) | A registered fit: a range or adding up, not both. | Past the ceiling (Tier 1 — Serverless, In-Warehouse), set by The level of detail the ordering system reads, How many things, and how many are new, Drivers vs history-only baseline, Built-in methods vs custom Python packages, A range, or a single number?. Unjustified operational cost. |
| Tier 3 — Real-Time & Specialised | Ruled out (Theatre) | A promise made while the customer waits, against reality. | Past the ceiling (Tier 1 — Serverless, In-Warehouse), set by The level of detail the ordering system reads, How many things, and how many are new, Drivers vs history-only baseline, Built-in methods vs custom Python packages, A range, or a single number?. Unjustified operational cost. |

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

- Tier 1 — Serverless, In-Warehouse — Thousands of lines at once: promotions or levels that add up. Out: not ruled out, but nothing heard in the room requires it.
- Tier 2 — Distributed & Custom ML — A registered fit: a range or adding up, not both. Out: past the ceiling at Tier 1 — Serverless, In-Warehouse — The level of detail the ordering system reads, How many things, and how many are new, Drivers vs history-only baseline, Built-in methods vs custom Python packages, A range, or a single number?.
- Tier 3 — Real-Time & Specialised — A promise made while the customer waits, against reality. Out: past the ceiling at Tier 1 — Serverless, In-Warehouse — The level of detail the ordering system reads, How many things, and how many are new, Drivers vs history-only baseline, Built-in methods vs custom Python packages, A range, or a single number?.

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

## 7. POC Data Discovery & Profiling Contract (Pass 1 · Guided Tier 0)

In a real Customer PoC, you are not handed pre-derived data facts — you direct `agy` to profile the raw BigQuery tables and discover them before finalizing your design:

- **BigQuery Source Tables (`bigquery-region: "US"`):** `bigquery-public-data.new_york_citibike.citibike_trips`, `bigquery-public-data.new_york_citibike.citibike_stations`, `bigquery-public-data.ml_datasets.holidays_and_events_for_forecasting`, `bigquery-public-data.noaa_gsod.gsod*`
- **Data Discovery Questions for `agy` in Step 3 (Checkpoint 03):**
  1. **Temporal Coverage & Contiguous Historical Window:** Profile `bigquery-public-data.new_york_citibike.citibike_trips` by year and month (`MIN(DATE(starttime))`, `MAX(DATE(starttime))`, monthly trip counts) to identify the primary contiguous multi-year historical window before any feed gap, and define the last-30-day temporal holdout window at the end of that contiguous window.
  2. **Calendar Spine Completeness & Missing Contiguous Outages:** Compare `COUNT(DISTINCT DATE(starttime))` against `DATE_DIFF(MAX(DATE(starttime)), MIN(DATE(starttime)), DAY) + 1` inside that contiguous window, and left-join `GENERATE_DATE_ARRAY` to discover which specific calendar dates (especially multi-day weather/blizzard shutdowns) have zero trips and would silently vanish from a naive `GROUP BY`.
  3. **Rider Segment (`usertype`) Behavior:** Profile daily demand across `Subscriber` (annual commuter members) vs. `Customer` (short-term leisure/tourist passes) so both overall and segment-level series are zero-filled and evaluated on the holdout window.
- **Pass 1 Target Deliverables (`citibike_tier0`):**
  - `labs/guided/citibike/DESIGN-tier0.md` (Checkpoint 03)
  - `citibike_tier0.daily_trips` & `citibike_tier0.daily_trips_by_usertype` on a continuous `GENERATE_DATE_ARRAY` calendar spine with `COALESCE(COUNT(*), 0)` (Checkpoint 04)
  - `citibike_tier0.forecast_30d` (`AI.FORECAST` `TimesFM 2.5` / `3.0`), `citibike_tier0.anomalies_30d` (`AI.DETECT_ANOMALIES`), `citibike_tier0.holdout_eval_summary` (`AI.EVALUATE` 30-day rewind holdout), and optional `citibike_tier0.tabfm_trip_type_preds` (`AI.PREDICT` `TabFM`) (Checkpoint 05)
  - Stateful Conversational Analytics Data Agent (`citibike_tier0_agent` / `citibike_demand_agent`) + `labs/guided/citibike/tier1_trigger.md` recording the discovered holdout error gap between `Subscriber` and `Customer` that motivates Pass 2 (Checkpoint 06)

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
    "floor": 0,
    "ceiling": 0,
    "clash": false
  },
  "recommended_rung": 0,
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
        "key": "coarse",
        "heard": "A group of items across a whole area, for a long stretch. We meet about it.",
        "means": "Few series, a slow clock, and a decision made by people in a room. Tier 0 gives a defensible number this week, and machinery above Tier 1 is being bought for a spreadsheet-sized problem.",
        "floor": 0,
        "ceiling": 1
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
        "key": "short",
        "heard": "Days. We act today and it lands this week.",
        "means": "A short reach closes the long-lead branch and the distance-specific accuracy questions. The horizon is set by the ordering rhythm rather than by the model.",
        "floor": null,
        "ceiling": null
      }
    },
    {
      "id": "count",
      "order": 4,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "small",
        "heard": "A few hundred, maybe a couple of thousand. They have all been around for years.",
        "means": "Laptop-sized. One SQL statement fits the lot, and saying that plainly is worth more to this customer than an architecture. Anything above Tier 1 here is theatre.",
        "floor": null,
        "ceiling": 1
      }
    },
    {
      "id": "total",
      "order": 5,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "none",
        "heard": "Nobody has fixed a total. It is whatever the parts come to.",
        "means": "The biggest close on this problem. No committed total means no adding-up requirement, which removes that branch entirely — and with it the hardest trade-off in Discovery.",
        "floor": null,
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
        "key": "builtin-floor",
        "heard": "Start with a zero-setup baseline and plain-English answers over past demand.",
        "means": "Tier 0 fits the brief: run AI.FORECAST (TimesFM), AI.DETECT_ANOMALIES, and AI.EVALUATE on the demand history table with a Conversational Analytics Data Agent answering forward-facing questions.",
        "floor": 0,
        "ceiling": 1
      }
    },
    {
      "id": "output",
      "order": 8,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "point",
        "heard": "One number. There is one field in the ordering system and it takes one number.",
        "means": "Then a range buys nothing until that system changes, and changing it is somebody else’s roadmap. Recommending Tier 2 for probabilistic forecasting here is theatre.",
        "floor": null,
        "ceiling": 1
      }
    },
    {
      "id": "lead-bands",
      "order": 9,
      "status": "not_in_play",
      "gate": "Different items need different lead times",
      "closed_by": {
        "question": "horizon",
        "answer": "short"
      }
    },
    {
      "id": "rollup-shape",
      "order": 10,
      "status": "not_in_play",
      "gate": "The numbers have to add up",
      "closed_by": {
        "question": "total",
        "answer": "none"
      }
    },
    {
      "id": "addup-plus-promo",
      "order": 11,
      "status": "not_in_play",
      "gate": "The numbers have to add up",
      "closed_by": {
        "question": "total",
        "answer": "none"
      }
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
      "status": "not_in_play",
      "gate": "Different items need different lead times",
      "closed_by": {
        "question": "horizon",
        "answer": "short"
      }
    }
  ],
  "conflicts": [],
  "still_to_ask": [
    "new-item-today",
    "lifecycle-flag"
  ],
  "counts": {
    "answered": 8,
    "stale": 0,
    "open": 2,
    "not_in_play": 12,
    "dropped": 0
  },
  "schema_version": "1.0",
  "problem_id": "forecasting",
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
