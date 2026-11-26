---
schema_version: "1.0"
problem_id: "next-best-offer"
target_tier: 0
recommended_rung: 0
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

- **Floor: Tier 0 — Out of the Box** — set by How many offers, and how many at once
- **Ceiling: Tier 0 — Out of the Box** — set by What share of people match across the source systems

## 3. What was asked, and what it steered

### 1. How many offers, and how many at once

**Asked:** How many different offers are on the table, and how many could one person qualify for at the same time? Twelve overlapping offers is a ranking job. Three that rule each other out is a yes-or-no.

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Three or four, and they rule each other out. Nobody gets two of them.
- **Which means:** Rules can do this. A handful of mutually exclusive offers is a set of segments, not a ranking, and a model buys nothing a query cannot already say.
- **Bounds:** not below Tier 0 — Out of the Box, Tier 1 — Serverless, In-Warehouse is the ceiling
- **For the brief:** Offers: a handful, mutually exclusive — a rule set, not a ranking.
- **Why it was asked:** Whether this is a ranking problem at all. A handful of mutually exclusive offers is a rule set; a dozen overlapping ones is an ordering; a catalogue is a narrowing problem before it is an ordering.
- **What it forecloses:** A handful closes everything about putting scores on one scale, about running out, and about how a brand-new offer gets ranked with nothing behind it.

### 2. What the ranking is meant to maximise

**Asked:** What is the ranking meant to maximise: how many people say yes, the money each yes brings in, or the yeses that would not have happened without the offer? Those three disagree, and only the third one costs revenue to measure.

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Just get the take-up rate up. More yeses than last year is the whole target.
- **Which means:** Honest and cheap, and it will push the cheapest offer at everyone. Say that out loud in week one, because the first review of the results is where somebody else notices.
- **Bounds:** Tier 1 — Serverless, In-Warehouse is the ceiling
- **For the brief:** Objective: take-up rate — expect the cheapest offer to win.
- **Why it was asked:** Everything downstream: what a yes means, which measure is quoted, whether a held-back group is needed, and which of the five models get built at all.
- **What it forecloses:** Take-up or value closes the whole branch about proving cause. Caused yeses opens it, and makes whether anybody was ever randomly held back the only question that matters.

### 3. What counts as a yes

**Asked:** What counts as the person saying yes: a click, an application started, an approval, the money actually moving, or still being there in ninety days? Each one moves how often it happens by a factor of ten.

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** A click on the offer. That is what we can actually see today.
- **Which means:** Cheap, plentiful and only loosely related to money. Fine for a first ranking, and it will be quoted back as a business result — agree in writing that it is not one.
- **Bounds:** Tier 1 — Serverless, In-Warehouse is the ceiling
- **For the brief:** Yes = a click — a stand-in, not a business outcome.
- **Why it was asked:** How often it happens, the training table, and how long after a send the truth arrives. It is also the number the business will judge the project by, so it is agreed rather than chosen.
- **What it forecloses:** A settled definition closes the questions about credit windows and fixes the retraining cadence, because the truth cannot arrive faster than the acceptance does.

### 4. What share of people match across the source systems

**Asked:** What share of people actually match between the ad-side records and the customer records today, which way has that share moved over six months, and who worked the number out?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** The contract will not let us join the raw records at all. Legal was clear.
- **Which means:** Then there is no training table, and nothing above Tier 0 has anything to train on. What is left is counting overlaps inside an agreed safe space, which answers sizing questions and not ranking ones.
- **Bounds:** Tier 0 — Out of the Box is the ceiling
- **For the brief:** Matching: raw join prohibited — overlaps only, no training table.
- **Why it was asked:** How much of the base the ranking can even see, and whether building a matcher is the project. It also sets an honest ceiling on every accuracy claim made later.
- **What it forecloses:** One shared key closes the whole matching branch and the largest single piece of Tier 2. A prohibited join closes everything above Tier 0.

### 5. What runs out, and who sets the limit

**Asked:** Do any offers run out — a fixed number of units, a monthly budget, a quota — and how many times a month may one person be contacted at all? Who sets each of those numbers?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Some of them come from compliance, not from us. Those we do not argue with.
- **Which means:** A different kind of number. A commercial limit can be exceeded and apologised for; this one cannot, so it belongs in the eligibility filter that runs before ranking rather than in the sharing-out step.
- **Bounds:** none
- **For the brief:** Limits: some are regulatory — filter before ranking, not during.
- **Why it was asked:** Whether this is scoring or sharing out. Independent per-person ranking and one solve over a shared pool are different systems, and the second cannot be retrofitted by sorting harder.
- **What it forecloses:** No binding limits closes the sharing-out branch, the questions about running out, and most of the argument for Tier 2.

### 6. Whether anyone was ever randomly held back

**Asked:** Has any offer ever been held back from a randomly chosen group, and is that recorded person by person rather than campaign by campaign?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** No. In two years we have never left anyone out on purpose.
- **Which means:** There is no number to beat and no way to prove anything beat it. The recommendation is to start holding a group back this week and ship the ranking meanwhile — not to promise an answer about cause this quarter.
- **Bounds:** Tier 1 — Serverless, In-Warehouse is the ceiling
- **For the brief:** Held back: none in two years — start one in release one.
- **Why it was asked:** Whether an answer about cause is buildable at all, now or only in six months. Nothing else here has a longer lead time, which is why it is asked early rather than in an experiment section.
- **What it forecloses:** A no closes the whole would-they-have-bought-anyway branch for this quarter, and turns Tier 2 into a sequencing conversation rather than an architecture one.

### 7. Where the offer appears, and when it is picked

**Asked:** Where does the chosen offer actually appear, and when is it chosen? Written onto a record overnight for somebody to read tomorrow, or picked while the person is waiting for a page?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** We push it into the activation system once a night. That is the only run there is.
- **Which means:** Nightly is the whole answer, and it quietly removes every live architecture before anyone draws a box. Say it back to them: writing the score into the activation system fixes the clock at one run a night.
- **Bounds:** Tier 1 — Serverless, In-Warehouse is the ceiling
- **For the brief:** Surface: nightly write to the activation system — no live tier needed.
- **Why it was asked:** The clock, which is the strongest single constraint here. What reads the output decides the rung far more than how many people there are.
- **What it forecloses:** A nightly write to a record closes every live question, the whole streaming tier, and the argument about a shared ledger with it.

## 4. Still worth asking

**These are instructions, not blanks.** Ask each one. The possible answers below are authored, with what each would rule in or out, so a reply can be recognised rather than interpreted.

### 11. Can five to ten in every hundred people be held back from every offer from now on, and who has the authority to give up that revenue?

**Ask:** Can five to ten in every hundred people be held back from every offer from now on, and who has the authority to give up that revenue?

What the answers would mean:

- **Yes, at that size. And I can name the person who would sign it.** → An answer about cause is six months away rather than never. Start the hold-back in the same release as the ranking, so the clock is already running when somebody asks for the number. *(floor Tier 1 — Serverless, In-Warehouse)*
- **Only a token group, and only on the small offers. Maybe one in a hundred.** → Enough to look like an experiment and not enough to read one. Work the size out from how often it happens and the lift they expect before agreeing, or the result will be unreadable in either direction.
- **No. Every quarter is under revenue pressure. I could not give that up.** → Then say in week one that claims about cause are out of scope, and rank on value instead. This is the business’s decision to make, and pretending otherwise is what gets a project cancelled in month nine. *(ceiling Tier 1 — Serverless, In-Warehouse)*
- **I do not know who would sign that off. It is above me, certainly.** → Find the signature before designing anything that depends on it. The hold-back has the longest lead time on this problem and the shortest conversation.

### 12. Until a held-back group exists, will they accept a matched comparison — people nobody contacted, picked to look like the ones who were?

**Ask:** Until a held-back group exists, will they accept a matched comparison — people nobody contacted, picked to look like the ones who were? It argues, it does not prove, and what it misses is usually why somebody was targeted at all.

What the answers would mean:

- **Yes, as an interim. Put the caveat in writing and we can work with it.** → The pragmatic answer. It costs no revenue and gives a direction to work with while the real hold-back accrues, as long as every quote of the number carries the words “matched, not randomised”.
- **Only if it matches on what we knew on the day, not on what we know now.** → The right instinct, and it costs a rebuild rather than a rung. Matching on what a person looks like today rather than on the day they were contacted is the same leak as the holdings feature, so match on as-at history. *(floor Tier 1 — Serverless, In-Warehouse)*
- **No. Our finance team will only look at a randomised result.** → The cleanest answer to work with. It puts the claim about cause six months out, fixes the ranking on value in the meantime, and makes the hold-back a funded line rather than a favour.
- **I have never put that to finance. I do not know what they would say.** → Worth asking before the hold-back conversation, not after. A finance team that will read a matched number is a very different negotiation from one that will not.

## 5. Not worth asking yet

Each of these is gated behind a branch that is not open. They are listed so the absence is legible: they were not forgotten, they were ruled out.

- **How long after a send does the truth arrive, and is that longer than the gap between retrains?** — closed by *What counts as a yes* → “A click on the offer. That is what we can actually see today”.
- **Who are the people the join loses?** — closed by *What share of people match across the source systems* → “The contract will not let us join the raw records at all. Legal was clear”.
- **Is who-gets-what worked out on a schedule, or claimed at the moment of sending?** — closed by *Where the offer appears, and when it is picked* → “We push it into the activation system once a night. That is the only run there is”.

## 6. What is being suggested, and why the alternatives are out

### Tier 0 — Out of the Box

Build the audience in SQL, activate it this week

- **What it is:** BigQuery audience build → Conversational Analytics sizing → Customer Match or Display & Video 360 upload
- **Google Cloud & open-weight options at this rung:** BigQuery, AI.PREDICT, Conversational Analytics, Customer Match
- **Why here:** A SQL audience, sized in Conversational Analytics and pushed to a channel, returns a number in a day and buys the credibility to ask for the held-back group every rung above needs. The customer data platform they already licence does this too.
- **Where it breaks:** Rules rank nothing. With a dozen overlapping offers a segment says who qualifies, not which offer is worth the one contact allowed. No ordering per person, no way to compare scores across offers — and uploaded audiences match half to two-thirds.
- **What would move it up:** The audiences overlap: the same person falls into more than one, the contact limit allows a single send, and somebody now has to rank offers rather than pick a segment.

#### Architecture Decision Record (ADR) Matrix

A scenario-aware evaluation of the ladder against this customer's constraints. Where an adjacent tier serves as a viable A/B benchmark or a Phase 2 evolution, that role is explicitly called out:

| Rung | Role in this Engagement | Architecture & Stance | Deciding Constraint & Trade-off |
| --- | --- | --- | --- |
| Tier 0 — Out of the Box | **Primary Baseline (MVP)** | Build the audience in SQL, activate it this week. Fits all bounded constraints. | Selected target. Fits floor (Tier 0 — Out of the Box) and ceiling (Tier 0 — Out of the Box). Wins: A SQL audience, sized in Conversational Analytics and pushed to a channel, returns a number in a day and buys the credibility to ask for the held-back group every rung above needs. The customer data platform they already licence does this too. |
| Tier 1 — Serverless, In-Warehouse | Ruled out (Theatre) | One query scores everyone, ranked on what it is worth. | Past the ceiling (Tier 0 — Out of the Box), set by What share of people match across the source systems. Unjustified operational cost. |
| Tier 2 — Distributed & Custom ML | Ruled out (Theatre) | Match at scale, then share the offers out under limits. | Past the ceiling (Tier 0 — Out of the Box), set by What share of people match across the source systems. Unjustified operational cost. |
| Tier 3 — Real-Time & Specialised | Ruled out (Theatre) | A slot that has to be filled before the page paints. | Past the ceiling (Tier 0 — Out of the Box), set by What share of people match across the source systems. Unjustified operational cost. |

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

- Tier 1 — Serverless, In-Warehouse — One query scores everyone, ranked on what it is worth. Out: past the ceiling at Tier 0 — Out of the Box — What share of people match across the source systems.
- Tier 2 — Distributed & Custom ML — Match at scale, then share the offers out under limits. Out: past the ceiling at Tier 0 — Out of the Box — What share of people match across the source systems.
- Tier 3 — Real-Time & Specialised — A slot that has to be filled before the page paints. Out: past the ceiling at Tier 0 — Out of the Box — What share of people match across the source systems.

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

## 7. POC Data Discovery & Profiling Contract (Tier 0)

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
    "floor": 0,
    "ceiling": 0,
    "clash": false
  },
  "recommended_rung": 0,
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
        "key": "few",
        "heard": "Three or four, and they rule each other out. Nobody gets two of them.",
        "means": "Rules can do this. A handful of mutually exclusive offers is a set of segments, not a ranking, and a model buys nothing a query cannot already say.",
        "floor": 0,
        "ceiling": 1
      }
    },
    {
      "id": "objective",
      "order": 2,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "accept",
        "heard": "Just get the take-up rate up. More yeses than last year is the whole target.",
        "means": "Honest and cheap, and it will push the cheapest offer at everyone. Say that out loud in week one, because the first review of the results is where somebody else notices.",
        "floor": null,
        "ceiling": 1
      }
    },
    {
      "id": "label",
      "order": 3,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "click",
        "heard": "A click on the offer. That is what we can actually see today.",
        "means": "Cheap, plentiful and only loosely related to money. Fine for a first ranking, and it will be quoted back as a business result — agree in writing that it is not one.",
        "floor": null,
        "ceiling": 1
      }
    },
    {
      "id": "match",
      "order": 4,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "blocked",
        "heard": "The contract will not let us join the raw records at all. Legal was clear.",
        "means": "Then there is no training table, and nothing above Tier 0 has anything to train on. What is left is counting overlaps inside an agreed safe space, which answers sizing questions and not ranking ones.",
        "floor": null,
        "ceiling": 0
      }
    },
    {
      "id": "caps",
      "order": 5,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "regulated",
        "heard": "Some of them come from compliance, not from us. Those we do not argue with.",
        "means": "A different kind of number. A commercial limit can be exceeded and apologised for; this one cannot, so it belongs in the eligibility filter that runs before ranking rather than in the sharing-out step.",
        "floor": null,
        "ceiling": null
      }
    },
    {
      "id": "holdout",
      "order": 6,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "never",
        "heard": "No. In two years we have never left anyone out on purpose.",
        "means": "There is no number to beat and no way to prove anything beat it. The recommendation is to start holding a group back this week and ship the ranking meanwhile — not to promise an answer about cause this quarter.",
        "floor": null,
        "ceiling": 1
      }
    },
    {
      "id": "surface",
      "order": 7,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "record",
        "heard": "We push it into the activation system once a night. That is the only run there is.",
        "means": "Nightly is the whole answer, and it quietly removes every live architecture before anyone draws a box. Say it back to them: writing the score into the activation system fixes the clock at one run a night.",
        "floor": null,
        "ceiling": 1
      }
    },
    {
      "id": "delay",
      "order": 8,
      "status": "not_in_play",
      "gate": "The outcome takes weeks to settle",
      "closed_by": {
        "question": "label",
        "answer": "click"
      }
    },
    {
      "id": "unmatched",
      "order": 9,
      "status": "not_in_play",
      "gate": "The join drops a large share of people",
      "closed_by": {
        "question": "match",
        "answer": "blocked"
      }
    },
    {
      "id": "enforce",
      "order": 10,
      "status": "not_in_play",
      "gate": "More than one channel can reach the same person at once",
      "closed_by": {
        "question": "surface",
        "answer": "record"
      }
    },
    {
      "id": "start",
      "order": 11,
      "status": "open",
      "options": [
        "Yes, at that size. And I can name the person who would sign it.",
        "Only a token group, and only on the small offers. Maybe one in a hundred.",
        "No. Every quarter is under revenue pressure. I could not give that up.",
        "I do not know who would sign that off. It is above me, certainly."
      ]
    },
    {
      "id": "matched",
      "order": 12,
      "status": "open",
      "options": [
        "Yes, as an interim. Put the caveat in writing and we can work with it.",
        "Only if it matches on what we knew on the day, not on what we know now.",
        "No. Our finance team will only look at a randomised result.",
        "I have never put that to finance. I do not know what they would say."
      ]
    }
  ],
  "conflicts": [],
  "still_to_ask": [
    "start",
    "matched"
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
