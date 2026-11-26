---
schema_version: "1.0"
problem_id: "marketing-measurement"
target_tier: 0
recommended_rung: 0
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

- **Floor: Tier 0 — Out of the Box** — set by Which number is the budget graded on, and who produces it, What does an advert actually land on here, How many channels to separate, over how many weeks, Can they say what was spent in one market in one week, Has any number here ever been scored against an experiment, What actually changes when the number arrives, Whose data is outside the company, and what may cross
- **Ceiling: Tier 1 — Serverless, In-Warehouse** — set by Will they switch spend off somewhere, and can they name it

## 3. What was asked, and what it steered

### 1. Which number is the budget graded on, and who produces it

**Asked:** When someone says the advertising worked, which number are they pointing at — and who produced that number?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Our own orders, in our own database, same day.
- **Which means:** The cleanest position. The thing you are trying to move is recorded by you, at whatever level of detail you like, with no lag and no revision. Everything downstream gets easier, and a switch-off test reads out in days, not a month.
- **Bounds:** not below Tier 0 — Out of the Box
- **For the brief:** Outcome: our own sales, same-day, no revision.
- **Why it was asked:** It decides whether there is anything to model at all. A number produced by the sellers cannot be used to grade the sellers, and a number bought from outside brings a lag and a correction history with it.
- **What it forecloses:** The common opening move of building against whatever the reporting deck already shows. Half the time that deck is the platforms’ own output, and modelling it just launders it.

### 2. What does an advert actually land on here

**Asked:** When one of these adverts lands, what does it land on — a home, a phone, a named doctor, a sales patch?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Homes and phones. Ordinary consumer advertising.
- **Which means:** The standard shape, and every channel can sit in one table. Randomisation happens over broadcast geography, the only boundary television respects.
- **Bounds:** not below Tier 0 — Out of the Box
- **For the brief:** Exposure unit: household. Randomise over markets.
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

- **Heard:** Nothing ever goes dark. Every region gets everything.
- **Which means:** There will never be an independent check, so the ceiling is a correlational fit whose beliefs do most of the work. Build it if the history supports it, price it honestly, and do not let anyone call the output causal.
- **Bounds:** Tier 1 — Serverless, In-Warehouse is the ceiling
- **For the brief:** No experiment possible. Correlational ceiling; label it as such.
- **Why it was asked:** Nothing else separates the rungs this cleanly. If spend never stops anywhere, every number you produce is a correlation in good clothing and no modelling choice repairs it.
- **What it forecloses:** The argument about which model to build. A signed plan to go dark is worth more than every specification decision on this page put together.

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

- **Heard:** Next year’s plan, agreed once, in a meeting.
- **Which means:** One decision a year, so the model runs a handful of times and everything above the first rung is decoration. Spend the budget on the switch-off test and the spend table instead.
- **Bounds:** not below Tier 0 — Out of the Box
- **For the brief:** Annual decision. No fast path. Invest in the switch-off test, not the pipeline.
- **Why it was asked:** It decides the cadence and the shape of the output, and whether any of the fast machinery on the upper rung is needed at all.
- **What it forecloses:** The build that answers faster than the organisation can act, which is most of the over-engineering on this problem.

### 10. Whose data is outside the company, and what may cross

**Asked:** Is there data you need that belongs to somebody else, and what are you actually allowed to see of it?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Everything we need is ours already.
- **Which means:** Then skip the whole subject. A large amount of architecture on this problem exists to solve a constraint plenty of customers do not have.
- **Bounds:** not below Tier 0 — Out of the Box
- **For the brief:** No partner data. No shared environment needed.
- **Why it was asked:** It decides whether a privacy-preserving join is architecture or theatre, and which product it is — the wrong one is the commonest naming error on this problem.
- **What it forecloses:** The expensive shared environment built for a row-level join that was never going to be permitted.

## 4. Still worth asking

**These are instructions, not blanks.** Ask each one. The possible answers below are authored, with what each would rule in or out, so a reply can be recognised rather than interpreted.

### 6. What each channel is assumed to return, and who signs it

**Ask:** Before any data is fitted, what does the business already assume each channel returns — and who would put their name to that assumption?

**Why it matters:** When spend has barely moved, those starting assumptions do most of the work in the answer. That makes them a governance item rather than a setting.

What the answers would mean:

- **Finance has planning assumptions and will stand behind them.** → The strongest position. Show finance the assumptions with no data attached and ask whether they would defend them; if yes, the model has a governance owner outside marketing before it has an answer. *(floor Tier 1 — Serverless, In-Warehouse)*
- **The agency has benchmarks from other clients.** → Benchmarks from the party being measured, which is exactly the circularity the whole exercise is meant to escape. Usable as a starting point only if they are written down, signed by your side, and frozen before the fit runs. *(floor Tier 1 — Serverless, In-Warehouse)*
- **None. We would want the model to tell us.** → With thin history that is not an option, and pretending otherwise means the software’s defaults become your unexamined assumptions. Elicit them from the business explicitly, even roughly, so at least they are visible. *(floor Tier 1 — Serverless, In-Warehouse)*
- **Different people would give you different numbers.** → Collect the spread and show it. The disagreement between channel owners about what their own channel returns is frequently a more useful finding than the model.

### 9. Who is measured on the answer this produces

**Ask:** Who is measured on the answer — and do they report to the person who reads it out?

**Why it matters:** It predicts whether the model gets used or litigated, and it is the question most likely to be skipped because it is uncomfortable.

What the answers would mean:

- **A separate analytics function reporting to finance.** → The structural condition for this working at all. It does not guarantee agreement, but it means disagreements are argued on the evidence rather than settled by reporting lines. *(floor Tier 1 — Serverless, In-Warehouse)*
- **The same team that plans and buys the media.** → The measured party owns the measurement. Expect the assumptions to be revisited whenever the answer is unwelcome, so the written-down-first record is not bureaucracy here, it is the only defence available. *(floor Tier 1 — Serverless, In-Warehouse)*
- **The agency produces it, and they also sell us the media.** → The strongest possible conflict, and it is normal in this industry. It does not mean the agency is dishonest; it means nobody can tell, which is the same thing for decision-making. Moving the readout in-house is the deliverable. *(floor Tier 1 — Serverless, In-Warehouse)*
- **It is a bit unclear who owns it, honestly.** → Then it will be owned by whoever is loudest after the first uncomfortable result. Settle it before the first result exists.

### 14. Which channels could be reported as one family without anyone losing a decision they actually make?

**Ask:** Which channels could be reported as one family without anyone losing a decision they actually make?

**Why it matters:** It decides whether the model becomes identifiable by design or stays unidentifiable and gets shipped anyway.

What the answers would mean:

- **Yes — nobody moves budget below the family level anyway.** → The best possible answer. If no decision is made at the individual channel level, reporting at that level was never doing anything except making the model worse. *(floor Tier 1 — Serverless, In-Warehouse)*
- **Each channel owner will insist on their own line.** → The demand for detail is organisational, not analytical, and it will produce numbers nobody should act on. Show the row count per line in the same deck as the numbers, so the precision and its cost are visible together. *(floor Tier 0 — Out of the Box)*
- **We have never asked what the smallest real decision is.** → Ask it before you fit anything. The answer sets the reporting level, and it is nearly always coarser than the reporting people say they need.

### 16. Who would re-cut three years of spend to market and week, and what would they charge?

**Ask:** Who would re-cut three years of spend to market and week, and what would they charge?

**Why it matters:** It decides whether the geographic cut is a data task or a procurement one, and it usually turns out to be the largest single line in the project.

What the answers would mean:

- **We hold the raw buys ourselves; it is a query.** → Then it is a week of work and the geographic cut is effectively free. Check that television is in there too, because it is normally bought and reported separately from everything else. *(floor Tier 1 — Serverless, In-Warehouse)*
- **The agency holds it. They will quote for the work.** → A paid project with a lead time, sitting on the critical path before any fit. Price it in the first proposal rather than discovering it in month three, and note that the agency may also be a party whose performance the model will judge. *(floor Tier 1 — Serverless, In-Warehouse)*
- **Older buys are not recoverable at that detail.** → The usable window for a geographic model starts from whenever the detail does. That may be shorter than the history you need, in which case the national model is the honest answer this year. *(floor Tier 0 — Out of the Box)*
- **Nobody has asked them for it.** → Ask in week one. The answer changes the shape of the engagement and the number in the proposal.

### 21. How long after someone sees one of these adverts might they still act on it?

**Ask:** How long after someone sees one of these adverts might they still act on it?

**Why it matters:** It sets the carryover window, one of the two shapes the whole fit rests on, and it bounds how short a switch-off test can usefully be.

What the answers would mean:

- **Search is same-day. Television might be two months.** → Awkward: the tool takes one maximum window for every channel at once, so you are choosing the longest plausible one and letting the shorter channels fade fast within it. Say so rather than presenting it as a per-channel setting. *(floor Tier 1 — Serverless, In-Warehouse)*
- **Everything we buy is direct response. Days, not weeks.** → A short window keeps the fit simple and lets a switch-off test read out in four weeks rather than twelve. It also means a shorter switch-off test is defensible, which materially lowers the cost of the second rung. *(floor Tier 1 — Serverless, In-Warehouse)*
- **The agency uses eight weeks for everything.** → An inherited default nobody has tested, and it will be defended as if it were measured. Refit at two or three windows and show how much the answer moves; that sensitivity is often the most persuasive slide in the pack. *(floor Tier 1 — Serverless, In-Warehouse)*
- **We have never thought about it in those terms.** → Ask how long after a campaign ends they still see an effect in the raw numbers. Non-technical people answer this well when it is put as a business question.

### 22. When a switch-off test reads out, should the model be forced to match it, or allowed to argue with it?

**Ask:** When a switch-off test reads out, should the model be forced to match it, or allowed to argue with it?

**Why it matters:** It changes the recommendation, sometimes materially, and it is a choice the customer should make knowingly rather than inherit from a default.

What the answers would mean:

- **If we paid for the experiment, the model should match it.** → Defensible and easy to explain, and it makes the switch-off test the anchor of the whole exercise. The risk is a switch-off test run in an unusual period being treated as permanent truth, so tie it to the window it was measured in. *(floor Tier 2 — Distributed & Custom ML)*
- **It should inform the model, not override the data.** → The usual default: the switch-off test pulls the answer without pinning it. Then say how hard it pulls, because a weak pull with a strong-sounding name lets everyone believe the model was validated when it was barely nudged. *(floor Tier 2 — Distributed & Custom ML)*
- **We did not know that was a choice.** → It is the choice that most changes the output, and it is the one most often left at a default. Show both fits side by side once; the difference makes the decision for them. *(floor Tier 2 — Distributed & Custom ML)*
- **We have not run one yet, so it has not come up.** → Decide it before the switch-off test launches, not after it reads out. Deciding afterwards means deciding while looking at the answer.

### 23. What else moved the sales last year that had nothing to do with advertising?

**Ask:** What else moved the sales last year that had nothing to do with advertising?

**Why it matters:** It decides which outside drivers must sit in the table. Leaving out the big one is the commonest cause of a channel whose return looks impossibly good.

What the answers would mean:

- **Price, availability, and one big competitor launch.** → Those go in as outside drivers and the model needs them at the same level of detail as everything else, which is often the hard part. A outside driver you can only get nationally cannot help a model built by market. *(floor Tier 1 — Serverless, In-Warehouse)*
- **Whether the insurer covers us, and how easily.** → Usually the single largest driver in the model and it is not advertising. It also moves in steps rather than smoothly, which makes it easy to confuse with a campaign, and it is often held in a spreadsheet rather than a system. *(floor Tier 1 — Serverless, In-Warehouse)*
- **Mostly seasonality, and we always advertise into it.** → The worst case for separating anything: if advertising and the season move together, the split between them comes from the assumptions rather than the data. Simplify the seasonal shape, and check what happens to the answer when you do. *(floor Tier 1 — Serverless, In-Warehouse)*
- **We would have to ask around the business.** → Do exactly that, and ask commercial and supply teams rather than marketing. Marketing rarely volunteers the outside driver that explains its own best quarter.

### 24. What result would make you stop believing the model?

**Ask:** What result would make you stop believing the model?

**Why it matters:** It separates a measurement programme from a reporting exercise, and it takes one sentence to ask.

What the answers would mean:

- **If a paid-off channel showed a strong return, we would stop.** → A real refutation condition, so build it in as a standing check: feed the model a channel that cannot have worked and confirm it returns roughly nothing. Run it every refit, not once. *(floor Tier 1 — Serverless, In-Warehouse)*
- **If the answers swung wildly between refits.** → A good instinct, and it needs a threshold before it is a rule. A channel whose return moves more than twofold between consecutive refits is telling you the fit is unidentified, not that the market changed. *(floor Tier 1 — Serverless, In-Warehouse)*
- **Nothing really. It is the best we have.** → Then it is reporting, and the honest move is to price and present it as reporting. A model that cannot fail will be used to justify decisions already made, and everyone in the room will eventually know it. *(ceiling Tier 1 — Serverless, In-Warehouse)*
- **That is a good question. Nobody has asked it.** → Agree one before the first refit. Agreed afterwards, it will be agreed by whoever is least happy with the number.

### 25. When the answer for a channel comes back as somewhere between minus a bit and plus a lot, what happens?

**Ask:** When the answer for a channel comes back as somewhere between minus a bit and plus a lot, what happens?

**Why it matters:** Every honest output here is a range rather than a number, so the rule for an uncertain one must be agreed before any of them exists.

What the answers would mean:

- **We would leave the budget where it is and go and test it.** → Exactly right, and it makes uncertainty productive rather than embarrassing: an unreadable channel becomes the next candidate for a switch-off test. The newer tooling will even nominate which channel would gain most from being tested. *(floor Tier 2 — Distributed & Custom ML)*
- **We would use the middle of the range and move on.** → This is how a range becomes a false certainty. It is not always wrong, but it must be a stated rule agreed in advance, with the band the model believes printed beside it. *(floor Tier 1 — Serverless, In-Warehouse)*
- **The channel owner would push back until it moved.** → The single most common failure on this problem, and it is organisational. Whoever reads the number out must not report to whoever is measured on it, and the rule for uncertain results has to exist in writing beforehand. *(floor Tier 1 — Serverless, In-Warehouse)*
- **It has not come up because we have never shown a range.** → Then start showing ranges immediately, before any budget depends on one. The first range presented after a reallocation looks like an excuse; the tenth looks like rigour.

### 27. How much of next year’s budget is already committed before anyone sees a number?

**Ask:** How much of next year’s budget is already committed before anyone sees a number?

**Why it matters:** It bounds what any recommendation can move, and therefore what the whole programme can be worth.

What the answers would mean:

- **Most of it can move with a few weeks’ notice.** → Unusual, and it raises the value of everything here. Recommendations can be acted on within the year rather than filed for the next planning round. *(floor Tier 1 — Serverless, In-Warehouse)*
- **Television and the big deals are locked a year ahead.** → The model informs next year’s commitments, not this year’s. That is fine, and it should reset expectations about cadence: an annual decision does not need a monthly refit or anything faster. *(floor Tier 1 — Serverless, In-Warehouse)*
- **Every channel has minimums nobody will breach.** → Those minimums are constraints the optimiser must carry, or it will recommend zero for a channel that contractually cannot go to zero and lose the room in one slide. *(floor Tier 1 — Serverless, In-Warehouse)*
- **Procurement would know what is committed.** → Get the list before the first recommendation. A recommendation that ignores the commitments is worse than no recommendation, because it costs you credibility you needed later.

### 29. Are the platform numbers you receive partly estimated for visitors who refused tracking?

**Ask:** Are the platform numbers you receive partly estimated for visitors who refused tracking?

**Why it matters:** It decides whether your inputs are counted or estimated on your behalf, and nothing downstream carries a label saying which.

What the answers would mean:

- **Yes, a good share of European numbers are estimated.** → You are fitting a model on top of somebody else’s model, and the two sets of assumptions compound invisibly. It is workable if stated, and it is another argument for grading against your own sales instead. *(floor Tier 1 — Serverless, In-Warehouse)*
- **We are outside Europe and it is all directly counted.** → Simpler, but check the assumption rather than accepting it, because consent requirements arrive by region and by platform and nobody sends a memo to the analytics team. *(floor Tier 0 — Out of the Box)*
- **We did not know that was happening.** → Very common. Check each platform’s settings before treating any reported figure as a count of real events.

## 5. Not worth asking yet

Each of these is gated behind a branch that is not open. They are listed so the absence is legible: they were not forgotten, they were ruled out.

- **How much does that bought number move after it is first published, and how would you know?** — closed by *Which number is the budget graded on, and who produces it* → “Our own orders, in our own database, same day”.
- **Do you already send your own sales back to those platforms?** — closed by *Which number is the budget graded on, and who produces it* → “Our own orders, in our own database, same day”.
- **What does one visit cost you, all in, and can you count visits per market per week?** — closed by *What does an advert actually land on here* → “Homes and phones. Ordinary consumer advertising”.
- **Do your big markets and small ones behave alike enough to borrow strength from each other?** — closed by *How many channels to separate, over how many weeks* → “Two years, and fifteen or more separate lines of spend”.
- **How large an effect would that design actually be able to see, given how much these markets normally bounce around?** — closed by *Will they switch spend off somewhere, and can they name it* → “Nothing ever goes dark. Every region gets everything”.
- **What could still reach a switched-off market that nobody in this room controls?** — closed by *Will they switch spend off somewhere, and can they name it* → “Nothing ever goes dark. Every region gets everything”.
- **Who would have to sign off deliberately forgoing sales in a named market, and have they ever met you?** — closed by *Will they switch spend off somewhere, and can they name it* → “Nothing ever goes dark. Every region gets everything”.
- **Has the field ever varied by market for any other reason — a vacancy, a reorganisation, a staggered rollout?** — closed by *Will they switch spend off somewhere, and can they name it* → “Nothing ever goes dark. Every region gets everything”.
- **How quickly does a sale actually have to reach the platform — seconds, an hour, overnight?** — closed by *What actually changes when the number arrives* → “Next year’s plan, agreed once, in a meeting”.
- **What is the smallest group the partner will report on, and how small are your markets?** — closed by *Whose data is outside the company, and what may cross* → “Everything we need is ours already”.

## 6. What is being suggested, and why the alternatives are out

### Tier 0 — Out of the Box

Run the experiments they have already paid for

- **What it is:** Data Transfer Service mart in BigQuery → Looker + Conversational Analytics; platform lift studies
- **Google Cloud & open-weight options at this rung:** BigQuery, BigQuery Data Transfer Service, AI.PREDICT, Looker, Conversational Analytics
- **Why here:** Zero build. The platforms sell randomised lift studies this customer has usually bought and never actioned. The transfer mart plus Conversational Analytics answers “what did we spend, where” in a day, and the row count says whether a fit is even possible.
- **Where it breaks:** Every seller grades its own work: reads are not comparable across platforms that cannot see each other, exist only where sold, and give no curve to reallocate against. Nothing for television, trade or field staff. Defends a line item; cannot allocate $200M.
- **What would move it up:** Lift studies reach only the channels that sell them — television, trade and personal promotion stay dark — and two years of stable week spend and sale history exist.

#### Architecture Decision Record (ADR) Matrix

A scenario-aware evaluation of the ladder against this customer's constraints. Where an adjacent tier serves as a viable A/B benchmark or a Phase 2 evolution, that role is explicitly called out:

| Rung | Role in this Engagement | Architecture & Stance | Deciding Constraint & Trade-off |
| --- | --- | --- | --- |
| Tier 0 — Out of the Box | **Primary Baseline (MVP)** | Run the experiments they have already paid for. Fits all bounded constraints. | Selected target. Fits floor (Tier 0 — Out of the Box) and ceiling (Tier 1 — Serverless, In-Warehouse). Wins: Zero build. The platforms sell randomised lift studies this customer has usually bought and never actioned. The transfer mart plus Conversational Analytics answers “what did we spend, where” in a day, and the row count says whether a fit is even possible. |
| Tier 1 — Serverless, In-Warehouse | **Adjacent Higher Tier (Phase 2 Evolution)** | One weekly table, and a model fitted on it. Higher freshness, lower latency, or specialised modeling. | Inside the range, but nothing heard requires it yet. Step-up trigger: Lift studies reach only the channels that sell them — television, trade and personal promotion stay dark — and two years of stable week spend and sale history exist. Propose as Phase 2 expansion once this condition is met. |
| Tier 2 — Distributed & Custom ML | Ruled out (Theatre) | A switch-off test the model has to answer to. | Past the ceiling (Tier 1 — Serverless, In-Warehouse), set by Will they switch spend off somewhere, and can they name it. Unjustified operational cost. |
| Tier 3 — Real-Time & Specialised | Ruled out (Theatre) | Always-on testing inside a closed budget loop. | Past the ceiling (Tier 1 — Serverless, In-Warehouse), set by Will they switch spend off somewhere, and can they name it. Unjustified operational cost. |

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

- Tier 1 — Serverless, In-Warehouse — One weekly table, and a model fitted on it. Out: not ruled out, but nothing heard in the room requires it.
- Tier 2 — Distributed & Custom ML — A switch-off test the model has to answer to. Out: past the ceiling at Tier 1 — Serverless, In-Warehouse — Will they switch spend off somewhere, and can they name it.
- Tier 3 — Real-Time & Specialised — Always-on testing inside a closed budget loop. Out: past the ceiling at Tier 1 — Serverless, In-Warehouse — Will they switch spend off somewhere, and can they name it.

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

## 7. POC Data Discovery & Profiling Contract (Tier 0)

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
    "floor": 0,
    "ceiling": 0,
    "clash": false
  },
  "recommended_rung": 0,
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
        "key": "own",
        "heard": "Our own orders, in our own database, same day.",
        "means": "The cleanest position. The thing you are trying to move is recorded by you, at whatever level of detail you like, with no lag and no revision. Everything downstream gets easier, and a switch-off test reads out in days, not a month.",
        "floor": 0,
        "ceiling": null
      }
    },
    {
      "id": "unit",
      "order": 2,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "home",
        "heard": "Homes and phones. Ordinary consumer advertising.",
        "means": "The standard shape, and every channel can sit in one table. Randomisation happens over broadcast geography, the only boundary television respects.",
        "floor": 0,
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
        "key": "never",
        "heard": "Nothing ever goes dark. Every region gets everything.",
        "means": "There will never be an independent check, so the ceiling is a correlational fit whose beliefs do most of the work. Build it if the history supports it, price it honestly, and do not let anyone call the output causal.",
        "floor": null,
        "ceiling": 1
      }
    },
    {
      "id": "beliefs",
      "order": 6,
      "status": "open",
      "keystone": true,
      "options": [
        "Finance has planning assumptions and will stand behind them.",
        "The agency has benchmarks from other clients.",
        "None. We would want the model to tell us.",
        "Different people would give you different numbers."
      ]
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
        "key": "annual",
        "heard": "Next year’s plan, agreed once, in a meeting.",
        "means": "One decision a year, so the model runs a handful of times and everything above the first rung is decoration. Spend the budget on the switch-off test and the spend table instead.",
        "floor": 0,
        "ceiling": null
      }
    },
    {
      "id": "arbiter",
      "order": 9,
      "status": "open",
      "keystone": true,
      "options": [
        "A separate analytics function reporting to finance.",
        "The same team that plans and buys the media.",
        "The agency produces it, and they also sell us the media.",
        "It is a bit unclear who owns it, honestly."
      ]
    },
    {
      "id": "partner",
      "order": 10,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "none",
        "heard": "Everything we need is ours already.",
        "means": "Then skip the whole subject. A large amount of architecture on this problem exists to solve a constraint plenty of customers do not have.",
        "floor": 0,
        "ceiling": null
      }
    },
    {
      "id": "revision",
      "order": 11,
      "status": "not_in_play",
      "gate": "The graded number is bought from a data provider",
      "closed_by": {
        "question": "graded",
        "answer": "own"
      }
    },
    {
      "id": "loop",
      "order": 12,
      "status": "not_in_play",
      "gate": "The graded number is what the ad platforms report",
      "closed_by": {
        "question": "graded",
        "answer": "own"
      }
    },
    {
      "id": "promotion",
      "order": 13,
      "status": "not_in_play",
      "gate": "Advertising lands on a named individual, not a household",
      "closed_by": {
        "question": "unit",
        "answer": "home"
      }
    },
    {
      "id": "combine",
      "order": 14,
      "status": "open",
      "options": [
        "Yes — nobody moves budget below the family level anyway.",
        "Each channel owner will insist on their own line.",
        "We have never asked what the smallest real decision is."
      ]
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
      "status": "open",
      "options": [
        "We hold the raw buys ourselves; it is a query.",
        "The agency holds it. They will quote for the work.",
        "Older buys are not recoverable at that detail.",
        "Nobody has asked them for it."
      ]
    },
    {
      "id": "power",
      "order": 17,
      "status": "not_in_play",
      "gate": "A plan to go dark in named markets is already signed",
      "closed_by": {
        "question": "switch",
        "answer": "never"
      }
    },
    {
      "id": "leak",
      "order": 18,
      "status": "not_in_play",
      "gate": "A plan to go dark in named markets is already signed",
      "closed_by": {
        "question": "switch",
        "answer": "never"
      }
    },
    {
      "id": "whosigns",
      "order": 19,
      "status": "not_in_play",
      "gate": "Going dark is acceptable in principle but has never been done",
      "closed_by": {
        "question": "switch",
        "answer": "never"
      }
    },
    {
      "id": "twotreat",
      "order": 20,
      "status": "not_in_play",
      "gate": "Advertising can go dark but the sales force cannot",
      "closed_by": {
        "question": "switch",
        "answer": "never"
      }
    },
    {
      "id": "carry",
      "order": 21,
      "status": "open",
      "options": [
        "Search is same-day. Television might be two months.",
        "Everything we buy is direct response. Days, not weeks.",
        "The agency uses eight weeks for everything.",
        "We have never thought about it in those terms."
      ]
    },
    {
      "id": "anchor",
      "order": 22,
      "status": "open",
      "options": [
        "If we paid for the experiment, the model should match it.",
        "It should inform the model, not override the data.",
        "We did not know that was a choice.",
        "We have not run one yet, so it has not come up."
      ]
    },
    {
      "id": "confound",
      "order": 23,
      "status": "open",
      "options": [
        "Price, availability, and one big competitor launch.",
        "Whether the insurer covers us, and how easily.",
        "Mostly seasonality, and we always advertise into it.",
        "We would have to ask around the business."
      ]
    },
    {
      "id": "refute",
      "order": 24,
      "status": "open",
      "options": [
        "If a paid-off channel showed a strong return, we would stop.",
        "If the answers swung wildly between refits.",
        "Nothing really. It is the best we have.",
        "That is a good question. Nobody has asked it."
      ]
    },
    {
      "id": "zero",
      "order": 25,
      "status": "open",
      "options": [
        "We would leave the budget where it is and go and test it.",
        "We would use the middle of the range and move on.",
        "The channel owner would push back until it moved.",
        "It has not come up because we have never shown a range."
      ]
    },
    {
      "id": "sla",
      "order": 26,
      "status": "not_in_play",
      "gate": "The output has to reach an automated bidder",
      "closed_by": {
        "question": "decision",
        "answer": "annual"
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
      "status": "not_in_play",
      "gate": "Partner data may only cross as aggregates",
      "closed_by": {
        "question": "partner",
        "answer": "none"
      }
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
    "beliefs",
    "arbiter",
    "combine",
    "restatecost",
    "carry",
    "anchor",
    "confound",
    "refute",
    "zero",
    "locked",
    "modelled"
  ],
  "counts": {
    "answered": 8,
    "stale": 0,
    "open": 11,
    "not_in_play": 10,
    "dropped": 0
  },
  "schema_version": "1.0",
  "problem_id": "marketing-measurement",
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
