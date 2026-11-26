---
schema_version: "1.0"
problem_id: "marketing-measurement"
target_tier: 3
recommended_rung: 3
source: "built-in-classroom-pack"
---

# Discovery pack — Marketing Measurement & Incrementality

`marketing-measurement` · recorded by **classroom-repo** · version 1 · served 2026-10-27T00:00:00Z

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

> **Director of Marketing Analytics, national mobile carrier — 15+ media platforms, in-house media team** — Device upgrades and new lines are bought across fifteen platforms. Our multi-touch model, the platforms’ own numbers and our media mix model disagree by a factor of two or three. Give us one number, and feed conversions back server-side so the bidders optimise on real upgrades.
>
> **Commercial Analytics Lead, pharmaceutical manufacturer — one brand, DTC media plus 900 field reps** — We split promotional spend between DTC television, radio and print and a field force that details prescribers. Tell us how to allocate next year to grow new prescriptions.
>
> **Head of Growth, DTC skincare brand — $18M annual spend, no analytics team** — Meta says it drove 40,000 conversions last month and Google says it drove 35,000. We only had 51,000 orders. We need one model that arbitrates between the platforms and tells us the truth.

**Vocabulary is unbound.** The nouns below are the method's neutral words, not this customer's — treat them as placeholders and confirm the real terms early.

**The five specifics.**

- **How many, of the thing being predicted** — *not captured. Ask.*
- **How much history there is, and how much arrives** — *not captured. Ask.*
- **The deadline the run has to hit** — *not captured. Ask.*
- **What being wrong costs, per event or per year** — *not captured. Ask.*
- **Who owns the decision, and who would run this** — *not captured. Ask.*

## 2. Where discovery landed

- **Floor: Tier 3 — Real-Time & Specialised** — set by How quickly does a sale actually have to reach the platform — seconds, an hour, overnight?
- **Ceiling:** nothing heard yet rules out the top of the ladder

## 3. What was asked, and what it steered

### 1. Which number is the budget graded on, and who produces it

**Asked:** When someone says the advertising worked, which number are they pointing at — and who produced that number?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** We buy it from a data provider. It lands a few weeks later.
- **Which means:** The outcome is a purchased feed with a lag and a correction history, and neither is under your control. It rules out any fast loop, and it means a quarterly refit silently changes last quarter’s answer when corrections land.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Outcome: purchased feed, lagged, corrected after publication.
- **Why it was asked:** It decides whether there is anything to model at all. A number produced by the sellers cannot be used to grade the sellers, and a number bought from outside brings a lag and a correction history with it.
- **What it forecloses:** The common opening move of building against whatever the reporting deck already shows. Half the time that deck is the platforms’ own output, and modelling it just launders it.

### 2. What does an advert actually land on here

**Asked:** When one of these adverts lands, what does it land on — a home, a phone, a named doctor, a sales patch?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** A named doctor, or a named account, visited by our own staff.
- **Which means:** Two exposure units in one budget. The personal half has a cost per visit, a reach curve and a point where more stops helping like any other channel, but is almost always left out of the media table. It also has a compliance owner.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Two exposure units: broadcast and personal. Model both or say why not.
- **Why it was asked:** It fixes the shape of every row in the table and the unit any switch-off test has to be randomised over. Get it wrong and the switch-off test and the model are measuring different things.
- **What it forecloses:** The assumption that this is a consumer advertising problem. In several industries the largest line of spend is people visiting other people, and that never appears in a media plan.

### 3. How many channels to separate, over how many weeks

**Asked:** How many channels do you want told apart, and how many weeks of history sit behind them at one stable definition?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Two years, and fifteen or more separate lines of spend.
- **Which means:** Roughly five rows behind each thing you want separated. Not enough. The fix is arithmetic, not software: combine channels into families, simplify the season, drop outside drivers that are not confounders, or go by market for more rows.
- **Bounds:** not below Tier 0 — Out of the Box
- **For the brief:** Too many channels for the history. Combine before fitting.
- **Why it was asked:** It is a division you can do on a napkin in the meeting, and it decides whether a fitted model is possible before any product is chosen.
- **What it forecloses:** The entire build conversation when the answer is small, which is more often than anyone expects and is the most valuable thing you can say that day.

### 4. Can they say what was spent in one market in one week

**Asked:** Can you tell me what was spent in one named market in one named week, or only the national total?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Sales, yes. Spend only comes as a national number.
- **Which means:** The common case, and it caps you at a national model until somebody pays to have the spend re-cut. That re-cut is a paid project at the agency, it takes weeks, and it lands before anything can be fitted.
- **Bounds:** not below Tier 0 — Out of the Box
- **For the brief:** Spend national only. Price the agency re-cut before scoping.
- **Why it was asked:** It caps the model. National-only spend means a national model however good the sale data is, and that is the single most common blocker on this problem.
- **What it forecloses:** The plan that assumes the geographic cut is available because the sales data has it. Sales are almost always finer than spend, and spend is the side that has to be bought back from the agency.

### 5. Will they switch spend off somewhere, and can they name it

**Asked:** Will you stop advertising in some places, on purpose, for a set number of weeks — and can you name the places?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Eight named markets, eight weeks, already agreed.
- **Which means:** A real experiment exists, so one channel stops being a belief and becomes a measurement, and that anchor drags every other channel toward honesty. This is the difference between a model that describes the past and one you can argue for.
- **Bounds:** not below Tier 2 — Distributed & Custom ML
- **For the brief:** Signed switch-off test: named markets, fixed duration, agreed in advance.
- **Why it was asked:** Nothing else separates the rungs this cleanly. If spend never stops anywhere, every number you produce is a correlation in good clothing and no modelling choice repairs it.
- **What it forecloses:** The argument about which model to build. A signed plan to go dark is worth more than every specification decision on this page put together.

### 6. What each channel is assumed to return, and who signs it

**Asked:** Before any data is fitted, what does the business already assume each channel returns — and who would put their name to that assumption?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Finance has planning assumptions and will stand behind them.
- **Which means:** The strongest position. Show finance the assumptions with no data attached and ask whether they would defend them; if yes, the model has a governance owner outside marketing before it has an answer.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Assumptions owned and signed by finance, before the fit.
- **Why it was asked:** When spend has barely moved, those starting assumptions do most of the work in the answer. That makes them a governance item rather than a setting.
- **What it forecloses:** The quiet edit: an assumption nudged after somebody saw the result it changes, with no record that it moved.

### 7. Has any number here ever been scored against an experiment

**Asked:** Of the numbers you already have, has any one of them ever been checked against a real experiment?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** No. They just disagree and we argue about it.
- **Which means:** The finding, and it is worth more than a fourth number would be. Three unscored estimates disagreeing by two or three times is not a modelling problem; it is the absence of any check, and that reframes the entire engagement.
- **Bounds:** not below Tier 0 — Out of the Box
- **For the brief:** No number ever scored. Reframe from arbitration to measurement.
- **Why it was asked:** It tells you whether this is a measurement programme or a reporting one, and the answer is usually the most valuable slide you will produce all engagement.
- **What it forecloses:** The request to arbitrate between existing numbers. None of them has been scored, so there is nothing to arbitrate with.

### 8. What actually changes when the number arrives

**Asked:** When the number arrives, what physically changes — a plan, a booking, a call schedule, a bidder?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** It has to reach the platforms so bidding can use it.
- **Which means:** Two different jobs wearing one name. Getting sales to the platforms quickly is an activation requirement with its own speed promise; the measurement stays slow. Conflating them is where this problem gets over-built.
- **Bounds:** not below Tier 2 — Distributed & Custom ML
- **For the brief:** Split activation from measurement. Separate speed promises.
- **Why it was asked:** It decides the cadence and the shape of the output, and whether any of the fast machinery on the upper rung is needed at all.
- **What it forecloses:** The build that answers faster than the organisation can act, which is most of the over-engineering on this problem.

### 9. Who is measured on the answer this produces

**Asked:** Who is measured on the answer — and do they report to the person who reads it out?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** A separate analytics function reporting to finance.
- **Which means:** The structural condition for this working at all. It does not guarantee agreement, but it means disagreements are argued on the evidence rather than settled by reporting lines.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Readout independent of spend ownership. Note it as a strength.
- **Why it was asked:** It predicts whether the model gets used or litigated, and it is the question most likely to be skipped because it is uncomfortable.
- **What it forecloses:** The technically excellent programme that dies in its second quarter because the number moved someone’s budget and they owned the analyst.

### 10. Whose data is outside the company, and what may cross

**Asked:** Is there data you need that belongs to somebody else, and what are you actually allowed to see of it?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** A distributor or publisher holds exposure data we need.
- **Which means:** This is where a shared analysis environment fits: neither side sees the other’s rows and only aggregates come out. Check the aggregate rules first, because they apply to shared views rather than tables and they will shape the design.
- **Bounds:** not below Tier 2 — Distributed & Custom ML
- **For the brief:** Partner sharing fits. Confirm aggregate rules before designing.
- **Why it was asked:** It decides whether a privacy-preserving join is architecture or theatre, and which product it is — the wrong one is the commonest naming error on this problem.
- **What it forecloses:** The expensive shared environment built for a row-level join that was never going to be permitted.

### 11. How much does that bought number move after it is first published, and how would you know?

**Asked:** How much does that bought number move after it is first published, and how would you know?

- **Heard:** We keep every version as it arrived, dated.
- **Which means:** Unusual and valuable. You can refit on what was known at the time, and you can show a channel owner whether their channel moved or the data underneath it did.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Keep dated snapshots; refit on data as it stood at the time.
- **Why it was asked:** It sets whether a refit can be compared with the last one at all. If two months of history quietly change under you, a channel that appears to have moved may only have been recut.
- **What it forecloses:** The argument that follows the first surprising refit, where nobody can tell a real change from a correction because neither version was kept.

### 13. What does one visit cost you, all in, and can you count visits per market per week?

**Asked:** What does one visit cost you, all in, and can you count visits per market per week?

- **Heard:** The call log is clean and we know the fully loaded cost.
- **Which means:** The personal half can enter as its own treatment with its own diminishing-returns shape, which is the whole point. Meridian carries non-advertising treatments natively, so this is a configuration decision rather than a custom model.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Personal promotion enters as a treatment with counted contacts.
- **Why it was asked:** It decides whether the personal half of the budget can enter the model as a treatment at all, or has to sit outside it as an apology.
- **What it forecloses:** The usual outcome, where the largest line of spend is left out because the call log lives in a different system and nobody costed it.

### 14. Which channels could be reported as one family without anyone losing a decision they actually make?

**Asked:** Which channels could be reported as one family without anyone losing a decision they actually make?

- **Heard:** Yes — nobody moves budget below the family level anyway.
- **Which means:** The best possible answer. If no decision is made at the individual channel level, reporting at that level was never doing anything except making the model worse.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Report at family level. Matches the smallest decision made.
- **Why it was asked:** It decides whether the model becomes identifiable by design or stays unidentifiable and gets shipped anyway.
- **What it forecloses:** The reflex to fix a thin table by tightening beliefs instead, which produces the same precise-looking numbers with none of the evidence.

### 16. Who would re-cut three years of spend to market and week, and what would they charge?

**Asked:** Who would re-cut three years of spend to market and week, and what would they charge?

- **Heard:** We hold the raw buys ourselves; it is a query.
- **Which means:** Then it is a week of work and the geographic cut is effectively free. Check that television is in there too, because it is normally bought and reported separately from everything else.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Re-cut in house. Confirm television is included.
- **Why it was asked:** It decides whether the geographic cut is a data task or a procurement one, and it usually turns out to be the largest single line in the project.
- **What it forecloses:** The estimate that priced compute and people and forgot the invoice that arrives before either of them is needed.

### 17. How large an effect would that design actually be able to see, given how much these markets normally bounce around?

**Asked:** How large an effect would that design actually be able to see, given how much these markets normally bounce around?

- **Heard:** We worked out the smallest effect we could detect first.
- **Which means:** The right order, and rarer than it should be. The design search that comes with the tooling will rank candidate splits of markets by exactly this and hand you the strongest one.
- **Bounds:** not below Tier 2 — Distributed & Custom ML
- **For the brief:** Design powered and chosen before launch. Record the target effect.
- **Why it was asked:** It decides whether the switch-off test is worth running. An underpowered design costs real suppressed revenue and returns a shrug.
- **What it forecloses:** The pattern where a switch-off test runs, reads out as no significant effect, and the channel is cut on the strength of a design that could never have detected it.

### 18. What could still reach a switched-off market that nobody in this room controls?

**Asked:** What could still reach a switched-off market that nobody in this room controls?

- **Heard:** We will alert on any spend showing up in a dark market.
- **Which means:** Treat that alert as the reliability promise of the whole programme. One unfiltered path invalidates the quarter, so the check belongs in the live path rather than in a report somebody reads on Fridays.
- **Bounds:** not below Tier 2 — Distributed & Custom ML
- **For the brief:** Leakage alert live in the path. Any instance voids that market.
- **Why it was asked:** It decides whether the readout will mean anything. Spend leaking into a dark market does not add noise, it removes the contrast the whole switch-off test depends on.
- **What it forecloses:** The quarterly audit that discovers the leak after the result has already been presented.

### 21. How long after someone sees one of these adverts might they still act on it?

**Asked:** How long after someone sees one of these adverts might they still act on it?

- **Heard:** Search is same-day. Television might be two months.
- **Which means:** Awkward: the tool takes one maximum window for every channel at once, so you are choosing the longest plausible one and letting the shorter channels fade fast within it. Say so rather than presenting it as a per-channel setting.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** One shared window at the longest plausible lag. Note the constraint.
- **Why it was asked:** It sets the carryover window, one of the two shapes the whole fit rests on, and it bounds how short a switch-off test can usefully be.
- **What it forecloses:** The four-week switch-off test on a channel whose effect takes eight, which measures the ramp and calls it the answer.

### 22. When a switch-off test reads out, should the model be forced to match it, or allowed to argue with it?

**Asked:** When a switch-off test reads out, should the model be forced to match it, or allowed to argue with it?

- **Heard:** If we paid for the experiment, the model should match it.
- **Which means:** Defensible and easy to explain, and it makes the switch-off test the anchor of the whole exercise. The risk is a switch-off test run in an unusual period being treated as permanent truth, so tie it to the window it was measured in.
- **Bounds:** not below Tier 2 — Distributed & Custom ML
- **For the brief:** Anchor binds, scoped to the switch-off test window. State the window.
- **Why it was asked:** It changes the recommendation, sometimes materially, and it is a choice the customer should make knowingly rather than inherit from a default.
- **What it forecloses:** The surprise where an expensive switch-off test runs, and the fitted number for that channel comes out somewhere else entirely.

### 23. What else moved the sales last year that had nothing to do with advertising?

**Asked:** What else moved the sales last year that had nothing to do with advertising?

- **Heard:** Price, availability, and one big competitor launch.
- **Which means:** Those go in as outside drivers and the model needs them at the same level of detail as everything else, which is often the hard part. A outside driver you can only get nationally cannot help a model built by market.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Outside drivers identified. Confirm each is available per market per week.
- **Why it was asked:** It decides which outside drivers must sit in the table. Leaving out the big one is the commonest cause of a channel whose return looks impossibly good.
- **What it forecloses:** The fit where a distribution win or a coverage decision lands in the same quarter as a campaign and the campaign gets the credit.

### 24. What result would make you stop believing the model?

**Asked:** What result would make you stop believing the model?

- **Heard:** If a paid-off channel showed a strong return, we would stop.
- **Which means:** A real refutation condition, so build it in as a standing check: feed the model a channel that cannot have worked and confirm it returns roughly nothing. Run it every refit, not once.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Standing refutation check every refit. Record the pass or fail.
- **Why it was asked:** It separates a measurement programme from a reporting exercise, and it takes one sentence to ask.
- **What it forecloses:** The model that can never be wrong, which is the model every organisation drifts toward once budgets depend on it.

### 25. When the answer for a channel comes back as somewhere between minus a bit and plus a lot, what happens?

**Asked:** When the answer for a channel comes back as somewhere between minus a bit and plus a lot, what happens?

- **Heard:** We would leave the budget where it is and go and test it.
- **Which means:** Exactly right, and it makes uncertainty productive rather than embarrassing: an unreadable channel becomes the next candidate for a switch-off test. The newer tooling will even nominate which channel would gain most from being tested.
- **Bounds:** not below Tier 2 — Distributed & Custom ML
- **For the brief:** Uncertain channels hold budget and enter the switch-off test queue.
- **Why it was asked:** Every honest output here is a range rather than a number, so the rule for an uncertain one must be agreed before any of them exists.
- **What it forecloses:** The collapse of a range to a single figure somewhere between the model and the slide, which is where most of the harm in this field is done.

### 26. How quickly does a sale actually have to reach the platform — seconds, an hour, overnight?

**Asked:** How quickly does a sale actually have to reach the platform — seconds, an hour, overnight?

- **Heard:** Minutes. Our bidding genuinely reacts within the day.
- **Which means:** This is the one case for a continuous path, and it carries a floor cost that never scales to zero. Price the standing capacity against the value of the freshness before agreeing to it.
- **Bounds:** not below Tier 3 — Real-Time & Specialised
- **For the brief:** Minutes required. Continuous path with standing capacity priced.
- **Why it was asked:** It decides whether this needs a streaming path at all, and the honest answer almost always removes one.
- **What it forecloses:** The streaming architecture bought to satisfy a requirement nobody ever wrote down.

## 4. Still worth asking

**These are instructions, not blanks.** Ask each one. The possible answers below are authored, with what each would rule in or out, so a reply can be recognised rather than interpreted.

### 27. How much of next year’s budget is already committed before anyone sees a number?

**Ask:** How much of next year’s budget is already committed before anyone sees a number?

**Why it matters:** It bounds what any recommendation can move, and therefore what the whole programme can be worth.

What the answers would mean:

- **Most of it can move with a few weeks’ notice.** → Unusual, and it raises the value of everything here. Recommendations can be acted on within the year rather than filed for the next planning round. *(floor Tier 1 — Serverless, In-Warehouse)*
- **Television and the big deals are locked a year ahead.** → The model informs next year’s commitments, not this year’s. That is fine, and it should reset expectations about cadence: an annual decision does not need a monthly refit or anything faster. *(floor Tier 1 — Serverless, In-Warehouse)*
- **Every channel has minimums nobody will breach.** → Those minimums are constraints the optimiser must carry, or it will recommend zero for a channel that contractually cannot go to zero and lose the room in one slide. *(floor Tier 1 — Serverless, In-Warehouse)*
- **Procurement would know what is committed.** → Get the list before the first recommendation. A recommendation that ignores the commitments is worse than no recommendation, because it costs you credibility you needed later.

### 28. What is the smallest group the partner will report on, and how small are your markets?

**Ask:** What is the smallest group the partner will report on, and how small are your markets?

**Why it matters:** It decides whether the aggregates you are allowed to receive are fine enough to be worth receiving.

What the answers would mean:

- **We checked; the threshold sits well below our smallest market.** → Then it is genuinely usable. Still assert on it in the pipeline, because a threshold that is comfortable today moves when the partner changes their policy and nothing will fail loudly when it does. *(floor Tier 2 — Distributed & Custom ML)*
- **The threshold would wipe out our smaller markets.** → Then model at a coarser geography for that partner rather than pretending you have the detail. And make the missing rows fail the build rather than quietly becoming zeros, which is what usually happens. *(floor Tier 2 — Distributed & Custom ML)*
- **It clears weekly but not daily.** → Fine, because the whole model is weekly anyway. Worth checking nobody downstream has built a daily view on top of it that has been quietly wrong for months. *(floor Tier 2 — Distributed & Custom ML)*
- **We have not seen the rules, only the sales pitch.** → Get the actual numbers and compute it against your own market sizes before any design work. This is an afternoon that regularly saves a quarter.

### 29. Are the platform numbers you receive partly estimated for visitors who refused tracking?

**Ask:** Are the platform numbers you receive partly estimated for visitors who refused tracking?

**Why it matters:** It decides whether your inputs are counted or estimated on your behalf, and nothing downstream carries a label saying which.

What the answers would mean:

- **Yes, a good share of European numbers are estimated.** → You are fitting a model on top of somebody else’s model, and the two sets of assumptions compound invisibly. It is workable if stated, and it is another argument for grading against your own sales instead. *(floor Tier 1 — Serverless, In-Warehouse)*
- **We are outside Europe and it is all directly counted.** → Simpler, but check the assumption rather than accepting it, because consent requirements arrive by region and by platform and nobody sends a memo to the analytics team. *(floor Tier 0 — Out of the Box)*
- **We did not know that was happening.** → Very common. Check each platform’s settings before treating any reported figure as a count of real events.

## 5. Not worth asking yet

Each of these is gated behind a branch that is not open. They are listed so the absence is legible: they were not forgotten, they were ruled out.

- **Do you already send your own sales back to those platforms?** — closed by *Which number is the budget graded on, and who produces it* → “We buy it from a data provider. It lands a few weeks later”.
- **Do your big markets and small ones behave alike enough to borrow strength from each other?** — closed by *How many channels to separate, over how many weeks* → “Two years, and fifteen or more separate lines of spend”.
- **Who would have to sign off deliberately forgoing sales in a named market, and have they ever met you?** — closed by *Will they switch spend off somewhere, and can they name it* → “Eight named markets, eight weeks, already agreed”.
- **Has the field ever varied by market for any other reason — a vacancy, a reorganisation, a staggered rollout?** — closed by *Will they switch spend off somewhere, and can they name it* → “Eight named markets, eight weeks, already agreed”.

## 6. What is being suggested, and why the alternatives are out

### Tier 3 — Real-Time & Specialised

Always-on testing inside a closed budget loop

- **What it is:** Managed Airflow rotates the switch-off test reserve → GeoX readout; continuous query → Pub/Sub → Cloud Run router
- **Google Cloud & open-weight options at this rung:** Managed Service for Apache Airflow, BigQuery, BigQuery continuous queries, Pub/Sub, Cloud Run, Meridian GeoX
- **What it carries:** Both axes carried from Tier 2. What changed is sequencing and activation: Airflow rotation, and a continuous query feeding the router.
- **Why here:** A standing reserve puts every channel under switch-off test during the year, and sequential stopping calls a promotion in days, not quarters. Activation is one SQL job: a continuous query over new rows into Pub/Sub, and a router that sends each sale once.
- **Where it breaks:** Closing the loop makes your own system part of the treatment: the bidder optimises on last week’s reallocation and confounds this one. There is no sub-second rung — this is experiment infrastructure, not latency. Continuous queries read standard tables only.
- **What would change the call:** Two quarters of continuous reallocation fail to beat a quarterly refit on realised lift, or spend leaks into dark markets faster than the reserve rotates — drop back a rung.

#### Architecture Decision Record (ADR) Matrix

A scenario-aware evaluation of the ladder against this customer's constraints. Where an adjacent tier serves as a viable A/B benchmark or a Phase 2 evolution, that role is explicitly called out:

| Rung | Role in this Engagement | Architecture & Stance | Deciding Constraint & Trade-off |
| --- | --- | --- | --- |
| Tier 0 — Out of the Box | Ruled out (Insufficient) | Run the experiments they have already paid for. | Below the floor (Tier 3 — Real-Time & Specialised), set by How quickly does a sale actually have to reach the platform — seconds, an hour, overnight?. |
| Tier 1 — Serverless, In-Warehouse | Ruled out (Insufficient) | One weekly table, and a model fitted on it. | Below the floor (Tier 3 — Real-Time & Specialised), set by How quickly does a sale actually have to reach the platform — seconds, an hour, overnight?. |
| Tier 2 — Distributed & Custom ML | **Adjacent Lower Tier (A/B Benchmark)** | A switch-off test the model has to answer to. Lower complexity and operational overhead. | Below the floor (Tier 3 — Real-Time & Specialised), set by How quickly does a sale actually have to reach the platform — seconds, an hour, overnight?. Viable as an A/B comparator to quantify the performance/accuracy lift of Tier 3 — Real-Time & Specialised. |
| Tier 3 — Real-Time & Specialised | **Primary Baseline (MVP)** | Always-on testing inside a closed budget loop. Fits all bounded constraints. | Selected target. Fits floor (Tier 3 — Real-Time & Specialised). Wins: A standing reserve puts every channel under switch-off test during the year, and sequential stopping calls a promotion in days, not quarters. Activation is one SQL job: a continuous query over new rows into Pub/Sub, and a router that sends each sale once. |

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

- Tier 0 — Out of the Box — Run the experiments they have already paid for. Out: the floor is Tier 3 — Real-Time & Specialised — How quickly does a sale actually have to reach the platform — seconds, an hour, overnight?.
- Tier 1 — Serverless, In-Warehouse — One weekly table, and a model fitted on it. Out: the floor is Tier 3 — Real-Time & Specialised — How quickly does a sale actually have to reach the platform — seconds, an hour, overnight?.
- Tier 2 — Distributed & Custom ML — A switch-off test the model has to answer to. Out: the floor is Tier 3 — Real-Time & Specialised — How quickly does a sale actually have to reach the platform — seconds, an hour, overnight?.

**Below the rung sit the calls no rung makes for you.** The tier does not settle these, and a design that has not stated them has not been made. Nothing on the page asks for them, so they travel unanswered.

- **What one row is** — One row is one national week, or one market in one week. The same answer fixes what a switch-off test can be randomised over, so this is the experiment design as much as the table, and spend is the side that decides it.
  Options: National, one row per week · One market, one week · The sales patch, not the broadcast market
- **What goes in beside the past** — The own past is only the baseline — what would have sold anyway. What tells channels apart sits beside it: spend lines, exposure, the outside drivers. Leaving out the big outside driver is what makes a return look impossibly good.
  Options: Spend lines only · Spend plus the outside drivers that confound · Exposure alongside spend
- **One fit, one each, or one per group** — Two hundred markets can be one national fit, a fit per market, or one fit with market levels inside it so the small ones borrow shape from the big ones. Meridian does the third, and how far the borrowing goes is yours.
  Options: One national fit · Borrow across all markets · Tiers of market, or the largest apart
- **Which methods get a run** — A Bayesian fit with carryover and diminishing returns, a plain regression on the same columns, and a switch-off readout that fits no media model at all. They answer different questions, and only the third one has a control.
  Options: Meridian, the Bayesian fit · A plain regression on the same columns · A readout with no media model
- **How you would know** — Nothing here has a held-back answer key, so fit statistics mislead: a model can reproduce history exactly and still be wrong about every channel. Proof is an experiment the fit never saw, or things that ought to return nothing.
  Options: Agreement with a switch-off test it never saw · A refutation battery on every refit · Reproducing history, plus sensitivity
- **What tuning is worth** — Tuning is not settings on this problem. It is the starting assumptions about what each channel returns, and when spend has barely moved they do most of the work in the answer. That makes them governance, not a knob.
  Options: Take the defaults · Elicit and sign them before the fit · Search the shapes and publish the spread
- **One winner, or several combined** — The ask is often to average three numbers that disagree, and averaging figures each seller produced about its own work fixes nothing. The real call is narrower: does one signed fit carry the recommendation, or the spread across a grid?
  Options: One signed fit, the grid beside it · The envelope across the grid
- **Making the numbers agree** — The fitted return for a channel, the switch-off test readout on that channel, and what the sellers report they drove will not add up. Which one moves is a choice, and it is usually inherited from a default.
  Options: The switch-off test binds the fit · The switch-off test pulls; record how hard · Publish both and let them differ

**Dataset for the build.** Every workshop build runs on public or shipped tables:

- **Source:** Shipped Apache-2.0 CSVs + loader
- **Tables:** `.mmm_workshop.geo_all_channels`, `.mmm_workshop.national_all_channels`, `.mmm_workshop.geo_holdout_experiment`
- **Grain & size:** One row per market-week (geo, time, five paid channel spend and impression columns, Organic_channel0_impression, Promo, controls, conversions, revenue_per_conversion, population); 40 markets across 156 weeks (6,240 rows) plus an 8-week 20-market switch-off test.
- **Target / label:** Weekly conversions and revenue per market, evaluated by incremental return per dollar against the 8-week market switch-off lift.
- **Tier 1 / Tier 2 build:** Hard Tier 1 builds geometric carryover and diminishing-returns transforms in BigQuery SQL with LINEAR_REG to diagnose channel co-movement (r = 0.27–0.70) and Promo confounding; Tier 2 fits a pooled market model (google-meridian or PyMC) anchored to the 8-week switch-off test.
- **Caveat:** Fitting a plain linear regression without carryover, diminishing returns, or the Promo control credits the promotional spike to paid media and misses diminishing returns on the largest channel.
- **Setup / verify:** `uv run python labs/data/marketing-measurement/load_to_bq.py --project $GOOGLE_CLOUD_PROJECT`
- **Agent skills (`bigquery-data-science` & Data Agent Kit):** `uvx bigquery-data-science lookup LINEAR_REG # BQDS: AI.FORECAST, ML.CORRELATION, ARIMA_PLUS_XREG, ML.WEIGHTS, ML.EVALUATE | Data Agent Kit: bigquery-data-transfer-service, dataform-bigquery, bigquery-ai-ml, ml-best-practices, gcp-managed-airflow-dag-authoring`

**The ladder, for reference.** No site is needed to read the tiers above.

- **Tier 0 — Out of the Box** — A model somebody else trained already answers the question. Nothing to fit, nothing to provision, and the bill starts on the first query. The most senior move in the room is often to say so.
- **Tier 1 — Serverless, In-Warehouse** — Bring the model to the data. No cluster, no container, no serving stack. SQL is the interface.
- **Tier 2 — Distributed & Custom ML** — The transformation or the model outgrew SQL. Bring distributed compute to the data, keep the storage where it is.
- **Tier 3 — Real-Time & Specialised** — A hard SLA or a custom objective justifies owning the stack. You are now engineering a system, not training a model.
- **Tier 4 — Hardening for High-Stakes Operation** — Not a rung you buy. It is what changes about a system already at Tier 1, 2 or 3 once being wrong is expensive, contested or unsafe — and what changes is different for every problem in Discovery.

## 7. POC Data Discovery & Profiling Contract (Tier 3)

- **Source Tables (`bigquery-region: "US"`):** `.mmm_workshop.geo_all_channels`, `.mmm_workshop.national_all_channels`, `.mmm_workshop.geo_holdout_experiment`
- **Grain & Target:** One row per market-week (geo, time, five paid channel spend and impression columns, Organic_channel0_impression, Promo, controls, conversions, revenue_per_conversion, population); 40 markets across 156 weeks (6,240 rows) plus an 8-week 20-market switch-off test. | Weekly conversions and revenue per market, evaluated by incremental return per dollar against the 8-week market switch-off lift.
- **Data Caveat to Profile & Guard Against:** Fitting a plain linear regression without carryover, diminishing returns, or the Promo control credits the promotional spike to paid media and misses diminishing returns on the largest channel.
- **Verification Command:** `uv run python labs/data/marketing-measurement/load_to_bq.py --project $GOOGLE_CLOUD_PROJECT`

---

### The same thing, for a program to read

```json
{
  "problem": "marketing-measurement",
  "ldap": "classroom-repo",
  "version": 1,
  "served_at": "2026-10-27T00:00:00Z",
  "binding": {
    "medium": "channel",
    "market": "market",
    "purchase": "sale",
    "interval": "week",
    "recipient": "household",
    "sponsor": "channel owner",
    "test": "switch-off test",
    "sway": "outside driver"
  },
  "range": {
    "floor": 3,
    "ceiling": 3,
    "clash": false
  },
  "recommended_rung": 3,
  "data": {
    "source": "Shipped Apache-2.0 CSVs + loader",
    "tables": [
      ".mmm_workshop.geo_all_channels",
      ".mmm_workshop.national_all_channels",
      ".mmm_workshop.geo_holdout_experiment"
    ],
    "grain": "One row per market-week (geo, time, five paid channel spend and impression columns, Organic_channel0_impression, Promo, controls, conversions, revenue_per_conversion, population); 40 markets across 156 weeks (6,240 rows) plus an 8-week 20-market switch-off test.",
    "label": "Weekly conversions and revenue per market, evaluated by incremental return per dollar against the 8-week market switch-off lift.",
    "rungs": "Hard Tier 1 builds geometric carryover and diminishing-returns transforms in BigQuery SQL with LINEAR_REG to diagnose channel co-movement (r = 0.27–0.70) and Promo confounding; Tier 2 fits a pooled market model (google-meridian or PyMC) anchored to the 8-week switch-off test.",
    "caveat": "Fitting a plain linear regression without carryover, diminishing returns, or the Promo control credits the promotional spike to paid media and misses diminishing returns on the largest channel.",
    "setup": "uv run python labs/data/marketing-measurement/load_to_bq.py --project $GOOGLE_CLOUD_PROJECT",
    "skills": "uvx bigquery-data-science lookup LINEAR_REG # BQDS: AI.FORECAST, ML.CORRELATION, ARIMA_PLUS_XREG, ML.WEIGHTS, ML.EVALUATE | Data Agent Kit: bigquery-data-transfer-service, dataform-bigquery, bigquery-ai-ml, ml-best-practices, gcp-managed-airflow-dag-authoring"
  },
  "questions": [
    {
      "id": "graded",
      "order": 1,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "bought",
        "heard": "We buy it from a data provider. It lands a few weeks later.",
        "means": "The outcome is a purchased feed with a lag and a correction history, and neither is under your control. It rules out any fast loop, and it means a quarterly refit silently changes last quarter’s answer when corrections land.",
        "floor": 1,
        "ceiling": null
      }
    },
    {
      "id": "unit",
      "order": 2,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "person",
        "heard": "A named doctor, or a named account, visited by our own staff.",
        "means": "Two exposure units in one budget. The personal half has a cost per visit, a reach curve and a point where more stops helping like any other channel, but is almost always left out of the media table. It also has a compliance owner.",
        "floor": 1,
        "ceiling": null
      }
    },
    {
      "id": "width",
      "order": 3,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "thin",
        "heard": "Two years, and fifteen or more separate lines of spend.",
        "means": "Roughly five rows behind each thing you want separated. Not enough. The fix is arithmetic, not software: combine channels into families, simplify the season, drop outside drivers that are not confounders, or go by market for more rows.",
        "floor": 0,
        "ceiling": null
      }
    },
    {
      "id": "spendgrain",
      "order": 4,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "salesonly",
        "heard": "Sales, yes. Spend only comes as a national number.",
        "means": "The common case, and it caps you at a national model until somebody pays to have the spend re-cut. That re-cut is a paid project at the agency, it takes weeks, and it lands before anything can be fitted.",
        "floor": 0,
        "ceiling": null
      }
    },
    {
      "id": "switch",
      "order": 5,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "signed",
        "heard": "Eight named markets, eight weeks, already agreed.",
        "means": "A real experiment exists, so one channel stops being a belief and becomes a measurement, and that anchor drags every other channel toward honesty. This is the difference between a model that describes the past and one you can argue for.",
        "floor": 2,
        "ceiling": null
      }
    },
    {
      "id": "beliefs",
      "order": 6,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "finance",
        "heard": "Finance has planning assumptions and will stand behind them.",
        "means": "The strongest position. Show finance the assumptions with no data attached and ask whether they would defend them; if yes, the model has a governance owner outside marketing before it has an answer.",
        "floor": 1,
        "ceiling": null
      }
    },
    {
      "id": "scored",
      "order": 7,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "never",
        "heard": "No. They just disagree and we argue about it.",
        "means": "The finding, and it is worth more than a fourth number would be. Three unscored estimates disagreeing by two or three times is not a modelling problem; it is the absence of any check, and that reframes the entire engagement.",
        "floor": 0,
        "ceiling": null
      }
    },
    {
      "id": "decision",
      "order": 8,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "bidder",
        "heard": "It has to reach the platforms so bidding can use it.",
        "means": "Two different jobs wearing one name. Getting sales to the platforms quickly is an activation requirement with its own speed promise; the measurement stays slow. Conflating them is where this problem gets over-built.",
        "floor": 2,
        "ceiling": null
      }
    },
    {
      "id": "arbiter",
      "order": 9,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "independent",
        "heard": "A separate analytics function reporting to finance.",
        "means": "The structural condition for this working at all. It does not guarantee agreement, but it means disagreements are argued on the evidence rather than settled by reporting lines.",
        "floor": 1,
        "ceiling": null
      }
    },
    {
      "id": "partner",
      "order": 10,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "thirdparty",
        "heard": "A distributor or publisher holds exposure data we need.",
        "means": "This is where a shared analysis environment fits: neither side sees the other’s rows and only aggregates come out. Check the aggregate rules first, because they apply to shared views rather than tables and they will shape the design.",
        "floor": 2,
        "ceiling": null
      }
    },
    {
      "id": "revision",
      "order": 11,
      "status": "answered",
      "answer": {
        "key": "archived",
        "heard": "We keep every version as it arrived, dated.",
        "means": "Unusual and valuable. You can refit on what was known at the time, and you can show a channel owner whether their channel moved or the data underneath it did.",
        "floor": 1,
        "ceiling": null
      }
    },
    {
      "id": "loop",
      "order": 12,
      "status": "not_in_play",
      "gate": "The graded number is what the ad platforms report",
      "closed_by": {
        "question": "graded",
        "answer": "bought"
      }
    },
    {
      "id": "promotion",
      "order": 13,
      "status": "answered",
      "answer": {
        "key": "counted",
        "heard": "The call log is clean and we know the fully loaded cost.",
        "means": "The personal half can enter as its own treatment with its own diminishing-returns shape, which is the whole point. Meridian carries non-advertising treatments natively, so this is a configuration decision rather than a custom model.",
        "floor": 1,
        "ceiling": null
      }
    },
    {
      "id": "combine",
      "order": 14,
      "status": "answered",
      "answer": {
        "key": "willing",
        "heard": "Yes — nobody moves budget below the family level anyway.",
        "means": "The best possible answer. If no decision is made at the individual channel level, reporting at that level was never doing anything except making the model worse.",
        "floor": 1,
        "ceiling": null
      }
    },
    {
      "id": "pool",
      "order": 15,
      "status": "not_in_play",
      "gate": "The history exists for many markets rather than one country",
      "closed_by": {
        "question": "width",
        "answer": "thin"
      }
    },
    {
      "id": "restatecost",
      "order": 16,
      "status": "answered",
      "answer": {
        "key": "inhouse",
        "heard": "We hold the raw buys ourselves; it is a query.",
        "means": "Then it is a week of work and the geographic cut is effectively free. Check that television is in there too, because it is normally bought and reported separately from everything else.",
        "floor": 1,
        "ceiling": null
      }
    },
    {
      "id": "power",
      "order": 17,
      "status": "answered",
      "answer": {
        "key": "computed",
        "heard": "We worked out the smallest effect we could detect first.",
        "means": "The right order, and rarer than it should be. The design search that comes with the tooling will rank candidate splits of markets by exactly this and hand you the strongest one.",
        "floor": 2,
        "ceiling": null
      }
    },
    {
      "id": "leak",
      "order": 18,
      "status": "answered",
      "answer": {
        "key": "monitored",
        "heard": "We will alert on any spend showing up in a dark market.",
        "means": "Treat that alert as the reliability promise of the whole programme. One unfiltered path invalidates the quarter, so the check belongs in the live path rather than in a report somebody reads on Fridays.",
        "floor": 2,
        "ceiling": null
      }
    },
    {
      "id": "whosigns",
      "order": 19,
      "status": "not_in_play",
      "gate": "Going dark is acceptable in principle but has never been done",
      "closed_by": {
        "question": "switch",
        "answer": "signed"
      }
    },
    {
      "id": "twotreat",
      "order": 20,
      "status": "not_in_play",
      "gate": "Advertising can go dark but the sales force cannot",
      "closed_by": {
        "question": "switch",
        "answer": "signed"
      }
    },
    {
      "id": "carry",
      "order": 21,
      "status": "answered",
      "answer": {
        "key": "varies",
        "heard": "Search is same-day. Television might be two months.",
        "means": "Awkward: the tool takes one maximum window for every channel at once, so you are choosing the longest plausible one and letting the shorter channels fade fast within it. Say so rather than presenting it as a per-channel setting.",
        "floor": 1,
        "ceiling": null
      }
    },
    {
      "id": "anchor",
      "order": 22,
      "status": "answered",
      "answer": {
        "key": "hard",
        "heard": "If we paid for the experiment, the model should match it.",
        "means": "Defensible and easy to explain, and it makes the switch-off test the anchor of the whole exercise. The risk is a switch-off test run in an unusual period being treated as permanent truth, so tie it to the window it was measured in.",
        "floor": 2,
        "ceiling": null
      }
    },
    {
      "id": "confound",
      "order": 23,
      "status": "answered",
      "answer": {
        "key": "named",
        "heard": "Price, availability, and one big competitor launch.",
        "means": "Those go in as outside drivers and the model needs them at the same level of detail as everything else, which is often the hard part. A outside driver you can only get nationally cannot help a model built by market.",
        "floor": 1,
        "ceiling": null
      }
    },
    {
      "id": "refute",
      "order": 24,
      "status": "answered",
      "answer": {
        "key": "stated",
        "heard": "If a paid-off channel showed a strong return, we would stop.",
        "means": "A real refutation condition, so build it in as a standing check: feed the model a channel that cannot have worked and confirm it returns roughly nothing. Run it every refit, not once.",
        "floor": 1,
        "ceiling": null
      }
    },
    {
      "id": "zero",
      "order": 25,
      "status": "answered",
      "answer": {
        "key": "rule",
        "heard": "We would leave the budget where it is and go and test it.",
        "means": "Exactly right, and it makes uncertainty productive rather than embarrassing: an unreadable channel becomes the next candidate for a switch-off test. The newer tooling will even nominate which channel would gain most from being tested.",
        "floor": 2,
        "ceiling": null
      }
    },
    {
      "id": "sla",
      "order": 26,
      "status": "answered",
      "answer": {
        "key": "minutes",
        "heard": "Minutes. Our bidding genuinely reacts within the day.",
        "means": "This is the one case for a continuous path, and it carries a floor cost that never scales to zero. Price the standing capacity against the value of the freshness before agreeing to it.",
        "floor": 3,
        "ceiling": null
      }
    },
    {
      "id": "locked",
      "order": 27,
      "status": "open",
      "options": [
        "Most of it can move with a few weeks’ notice.",
        "Television and the big deals are locked a year ahead.",
        "Every channel has minimums nobody will breach.",
        "Procurement would know what is committed."
      ]
    },
    {
      "id": "threshold",
      "order": 28,
      "status": "open",
      "options": [
        "We checked; the threshold sits well below our smallest market.",
        "The threshold would wipe out our smaller markets.",
        "It clears weekly but not daily.",
        "We have not seen the rules, only the sales pitch."
      ]
    },
    {
      "id": "modelled",
      "order": 29,
      "status": "open",
      "options": [
        "Yes, a good share of European numbers are estimated.",
        "We are outside Europe and it is all directly counted.",
        "We did not know that was happening."
      ]
    }
  ],
  "conflicts": [],
  "still_to_ask": [
    "locked",
    "threshold",
    "modelled"
  ],
  "counts": {
    "answered": 22,
    "stale": 0,
    "open": 3,
    "not_in_play": 4,
    "dropped": 0
  },
  "schema_version": "1.0",
  "problem_id": "marketing-measurement",
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
