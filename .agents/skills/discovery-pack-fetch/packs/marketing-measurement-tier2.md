---
schema_version: "1.0"
problem_id: "marketing-measurement"
target_tier: 2
recommended_rung: 2
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

- **Floor: Tier 2 — Distributed & Custom ML** — set by Will they switch spend off somewhere, and can they name it, Has any number here ever been scored against an experiment, What actually changes when the number arrives, Whose data is outside the company, and what may cross
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

- **Heard:** We ran our own geographic test two years ago.
- **Which means:** Then you have an anchor already, and the first question is whether the model reproduces it out of sample. If it does not, that gap is the deliverable rather than something to tune away.
- **Bounds:** not below Tier 2 — Distributed & Custom ML
- **For the brief:** Prior switch-off test exists. Score the current model against it first.
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

- **Heard:** We want deduplicated reach across Google and YouTube.
- **Which means:** A specific product answers this, not the general one: exposure joined to your own data stays inside Google’s privacy boundary, and newer options keep the matching inside your own perimeter. Naming the wrong one costs a CE the room.
- **Bounds:** not below Tier 2 — Distributed & Custom ML
- **For the brief:** Google exposure join needs the dedicated boundary, not a shared dataset.
- **Why it was asked:** It decides whether a privacy-preserving join is architecture or theatre, and which product it is — the wrong one is the commonest naming error on this problem.
- **What it forecloses:** The expensive shared environment built for a row-level join that was never going to be permitted.

## 4. Still worth asking

**These are instructions, not blanks.** Ask each one. The possible answers below are authored, with what each would rule in or out, so a reply can be recognised rather than interpreted.

### 11. How much does that bought number move after it is first published, and how would you know?

**Ask:** How much does that bought number move after it is first published, and how would you know?

**Why it matters:** It sets whether a refit can be compared with the last one at all. If two months of history quietly change under you, a channel that appears to have moved may only have been recut.

What the answers would mean:

- **We keep every version as it arrived, dated.** → Unusual and valuable. You can refit on what was known at the time, and you can show a channel owner whether their channel moved or the data underneath it did. *(floor Tier 1 — Serverless, In-Warehouse)*
- **The provider resends and we overwrite the table.** → History is being rewritten every load, and nobody can reconstruct what the model saw last quarter. This is a one-sprint fix and it must happen before the first refit, not after the first argument. *(floor Tier 1 — Serverless, In-Warehouse)*
- **Nobody has checked whether it changes.** → Diff two loads a month apart before you promise anything. It takes an hour and it occasionally kills the whole approach.

### 13. What does one visit cost you, all in, and can you count visits per market per week?

**Ask:** What does one visit cost you, all in, and can you count visits per market per week?

**Why it matters:** It decides whether the personal half of the budget can enter the model as a treatment at all, or has to sit outside it as an apology.

What the answers would mean:

- **The call log is clean and we know the fully loaded cost.** → The personal half can enter as its own treatment with its own diminishing-returns shape, which is the whole point. Meridian carries non-advertising treatments natively, so this is a configuration decision rather than a custom model. *(floor Tier 1 — Serverless, In-Warehouse)*
- **We have call counts, but samples and events are elsewhere.** → Half a treatment is worse than none, because the model will attribute the missing half to whatever moved alongside it. Either assemble the whole contact picture or model contacts and say plainly that samples and events are excluded. *(floor Tier 1 — Serverless, In-Warehouse)*
- **We know how many staff there are, not what they did.** → Headcount divided by territory is not a treatment; it barely varies, so the model cannot separate it from the territory itself. This line of spend is unmeasurable until the contact log exists, and that is a data project, not a model. *(floor Tier 0 — Out of the Box)*
- **The field system belongs to sales; we have never seen it.** → That access negotiation is the critical path and it is organisational. Start it in week one, because it will outlast every technical task on the plan.

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

### 17. How large an effect would that design actually be able to see, given how much these markets normally bounce around?

**Ask:** How large an effect would that design actually be able to see, given how much these markets normally bounce around?

**Why it matters:** It decides whether the switch-off test is worth running. An underpowered design costs real suppressed revenue and returns a shrug.

What the answers would mean:

- **We worked out the smallest effect we could detect first.** → The right order, and rarer than it should be. The design search that comes with the tooling will rank candidate splits of markets by exactly this and hand you the strongest one. *(floor Tier 2 — Distributed & Custom ML)*
- **We picked markets that felt representative.** → Feels-representative is the classic way to spend eight weeks of suppressed revenue on a result nobody can read. Re-run the selection properly before launch; it is a few hours of compute against a real revenue cost. *(floor Tier 1 — Serverless, In-Warehouse)*
- **We only have a handful of markets to work with.** → A handful means a built-up comparison market rather than a straight split, and it means being honest that only a large effect will show. Sometimes the right call is a longer switch-off test on fewer channels. *(floor Tier 2 — Distributed & Custom ML)*
- **We have not looked at how much they vary.** → Three years of history per market is all it takes and the calculation is standard. Do it before anyone commits to going dark, because the commitment is the expensive part.

### 18. What could still reach a switched-off market that nobody in this room controls?

**Ask:** What could still reach a switched-off market that nobody in this room controls?

**Why it matters:** It decides whether the readout will mean anything. Spend leaking into a dark market does not add noise, it removes the contrast the whole switch-off test depends on.

What the answers would mean:

- **We will alert on any spend showing up in a dark market.** → Treat that alert as the reliability promise of the whole programme. One unfiltered path invalidates the quarter, so the check belongs in the live path rather than in a report somebody reads on Fridays. *(floor Tier 2 — Distributed & Custom ML)*
- **National television and neighbouring areas will bleed in.** → Physical spillover cannot be prevented, only accounted for. Choose markets with buffers around them, or accept that the measured effect understates the truth and say by roughly how much. *(floor Tier 2 — Distributed & Custom ML)*
- **Local teams will keep spending if we do not stop them.** → The most common leak and the hardest, because the people leaking are being paid on the number you are suppressing. This is a compensation conversation before it is a monitoring one. *(floor Tier 2 — Distributed & Custom ML)*
- **We assumed switching the campaigns off would be enough.** → It is not. List every path spend can take into a market, including things bought centrally and things bought locally, and confirm each one can actually be stopped.

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

### 26. How quickly does a sale actually have to reach the platform — seconds, an hour, overnight?

**Ask:** How quickly does a sale actually have to reach the platform — seconds, an hour, overnight?

**Why it matters:** It decides whether this needs a streaming path at all, and the honest answer almost always removes one.

What the answers would mean:

- **Within the hour is fine. The platforms batch anyway.** → A scheduled export every few minutes does this, costs nothing when idle, and removes a standing reservation from the bill. Take the simpler thing. *(floor Tier 2 — Distributed & Custom ML)*
- **Minutes. Our bidding genuinely reacts within the day.** → This is the one case for a continuous path, and it carries a floor cost that never scales to zero. Price the standing capacity against the value of the freshness before agreeing to it. *(floor Tier 3 — Real-Time & Specialised)*
- **Nobody has ever specified it.** → Then it is overnight until somebody proves otherwise. Ship the cheap version, measure whether anything suffers, and let the evidence justify the upgrade. *(floor Tier 1 — Serverless, In-Warehouse)*
- **The media team would have a view.** → Get it in writing with a number in it. Fast is not a requirement; a number of minutes is.

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

- **Do you already send your own sales back to those platforms?** — closed by *Which number is the budget graded on, and who produces it* → “We buy it from a data provider. It lands a few weeks later”.
- **Do your big markets and small ones behave alike enough to borrow strength from each other?** — closed by *How many channels to separate, over how many weeks* → “Two years, and fifteen or more separate lines of spend”.
- **Who would have to sign off deliberately forgoing sales in a named market, and have they ever met you?** — closed by *Will they switch spend off somewhere, and can they name it* → “Eight named markets, eight weeks, already agreed”.
- **Has the field ever varied by market for any other reason — a vacancy, a reorganisation, a staggered rollout?** — closed by *Will they switch spend off somewhere, and can they name it* → “Eight named markets, eight weeks, already agreed”.
- **What is the smallest group the partner will report on, and how small are your markets?** — closed by *Whose data is outside the company, and what may cross* → “We want deduplicated reach across Google and YouTube”.

## 6. What is being suggested, and why the alternatives are out

### Tier 2 — Distributed & Custom ML

A switch-off test the model has to answer to

- **What it is:** GeoX design → run the switch-off test → readout as a Meridian anchor; Ads Data Hub for Google exposure
- **Google Cloud & open-weight options at this rung:** Meridian GeoX, Meridian, Ads Data Hub, BigQuery data clean rooms, Agent Platform custom training jobs
- **What it carries:** Place unchanged at none from Tier 1. What moved is the build: the notebook becomes a training job with lineage, and GeoX anchors the fit.
- **Why here:** GeoX does design and readout in one library: go dark, hold markets back or spend more, chosen against what the business will disturb, and read out by time-based regression. That becomes the anchor Meridian fits under, and it flags which channel to test next.
- **Where it breaks:** It needs somebody to deliberately not spend in named markets for eight to twelve weeks, a political negotiation before a technical one. Aggregate rules wipe out small markets. And a outside driver the size of an insurer coverage change swamps every channel.
- **What would move it up:** The decision cadence moves to continuous reallocation and a permanent switch-off test reserve is signed off with a stopping rule agreed in advance.

Peers at the same price, with a different shape:

- **Placebo and sensitivity grid on Spark** — Spark batch → applyInPandas, one task per run → placebo readouts and refits → BigQuery results

#### Architecture Decision Record (ADR) Matrix

A scenario-aware evaluation of the ladder against this customer's constraints. Where an adjacent tier serves as a viable A/B benchmark or a Phase 2 evolution, that role is explicitly called out:

| Rung | Role in this Engagement | Architecture & Stance | Deciding Constraint & Trade-off |
| --- | --- | --- | --- |
| Tier 0 — Out of the Box | Ruled out (Insufficient) | Run the experiments they have already paid for. | Below the floor (Tier 2 — Distributed & Custom ML), set by Will they switch spend off somewhere, and can they name it, Has any number here ever been scored against an experiment, What actually changes when the number arrives, Whose data is outside the company, and what may cross. |
| Tier 1 — Serverless, In-Warehouse | **Adjacent Lower Tier (A/B Benchmark)** | One weekly table, and a model fitted on it. Lower complexity and operational overhead. | Below the floor (Tier 2 — Distributed & Custom ML), set by Will they switch spend off somewhere, and can they name it, Has any number here ever been scored against an experiment, What actually changes when the number arrives, Whose data is outside the company, and what may cross. Viable as an A/B comparator to quantify the performance/accuracy lift of Tier 2 — Distributed & Custom ML. |
| Tier 2 — Distributed & Custom ML | **Primary Baseline (MVP)** | A switch-off test the model has to answer to. Fits all bounded constraints. | Selected target. Fits floor (Tier 2 — Distributed & Custom ML). Wins: GeoX does design and readout in one library: go dark, hold markets back or spend more, chosen against what the business will disturb, and read out by time-based regression. That becomes the anchor Meridian fits under, and it flags which channel to test next. |
| Tier 3 — Real-Time & Specialised | **Adjacent Higher Tier (Phase 2 Evolution)** | Always-on testing inside a closed budget loop. Higher freshness, lower latency, or specialised modeling. | Inside the range, but nothing heard requires it yet. Step-up trigger: The decision cadence moves to continuous reallocation and a permanent switch-off test reserve is signed off with a stopping rule agreed in advance. Propose as Phase 2 expansion once this condition is met. |

**What a build at this rung is made of.** Storage stays where it is and a second engine arrives beside it, with an artefact you can name, a registry to hold it, and a graph to sequence the steps.

The menu at this rung, not this design. Each line says what that component is doing *here* -- several of them appear at other rungs doing something else.

- **Where the data sits still** — Whether one copy can serve every reader, or whether you have just signed up to keep two copies honest.
    - **BigQuery standard tables** — The offline store the feature code reads and writes.
    - **Apache Iceberg managed tables** — What the distributed engine reads directly, with no export step.
    - **Cloud Storage and object tables** — The raw zone the distributed engine parses before anything is a table.
    - **External tables and BigQuery Omni** — A source in another cloud the transform reads without a migration.
- **How the data gets there** — Whether anything genuinely has to stream, or whether the customer said real time and meant this morning.
    - **Datastream** — Keeps a large mirror current under a transform that runs beside it.
    - **Pub/Sub** — A pipeline drains the topic into windowed features the nightly build reads, with nothing scored on the stream.
    - **Managed Service for Apache Kafka** — Batch consumers read topics the business already publishes.
    - **Dataflow** — Batch movement, written once so the stream can reuse it.
- **Where the logic runs** — Whether the work fits in SQL. Nearly everything else about the build follows from that one answer.
    - **BigQuery DataFrames** — Feature code in Python without standing up a second engine.
    - **Managed Service for Apache Spark** — The transform, and training inside it where that is simpler.
    - **Dataflow** — Batch scoring over a large population, written once.
    - **Cloud Run** — A scoring job that starts, finishes and costs nothing in between.
    - **Agent Platform training** — Where the custom model is produced.
- **What makes it run in order** — Whether this is a timetable or a graph. A graph with a gate in it is a different product from a cron line.
    - **Dataform** — The warehouse half of a graph whose other half runs elsewhere.
    - **BigQuery pipelines** — The warehouse-side steps of a larger build.
    - **Managed Service for Apache Airflow** — The retrain graph and everything that has to happen in order around it.
    - **Agent Platform Pipelines** — Train, evaluate and register as one repeatable run.
    - **Cloud Scheduler, Workflows and Eventarc** — Glue between products where a full graph engine would be too much.
- **How the answer reaches whoever acts** — Who or what acts on the answer, and whether they can read the place you were going to put it.
    - **BigQuery sharing** — The same, once there is a version on the table to keep straight.
    - **A push into the operational system** — A write from the scoring job straight into the operational store.
    - **Agent Platform endpoints and batch inference** — Batch inference fans the artefact out over the population.
    - **A Cloud Run service** — A container that scores and stops.
    - **Feature Store online serving** — One definition, written once and read by the training set.
    - **Agent Retrieval** — The item vectors a training run wrote, indexed in batch so a shortlist is looked up rather than computed.
- **The database the business already runs on** — The read shape at the moment of decision. A key lookup, a real query and a nearest-match are three stores.
    - **Bigtable** — Where the offline job writes what the request path will later read.
    - **AlloyDB** — The operational store the batch job pushes into.
    - **Cloud SQL** — The operational side of a build whose analytics live elsewhere.

**Who operates it.** A real data engineering function. Managed Airflow environments run continuously, so this rung carries a floor cost even in a week when nothing happens.

**Below it, and why that is not enough.**

- Tier 0 — Out of the Box — Run the experiments they have already paid for. Out: the floor is Tier 2 — Distributed & Custom ML — Will they switch spend off somewhere, and can they name it, Has any number here ever been scored against an experiment, What actually changes when the number arrives, Whose data is outside the company, and what may cross.
- Tier 1 — Serverless, In-Warehouse — One weekly table, and a model fitted on it. Out: the floor is Tier 2 — Distributed & Custom ML — Will they switch spend off somewhere, and can they name it, Has any number here ever been scored against an experiment, What actually changes when the number arrives, Whose data is outside the company, and what may cross.

**Above it, and why that is theatre here.**

- Tier 3 — Real-Time & Specialised — Always-on testing inside a closed budget loop. Out: not ruled out, but nothing heard in the room requires it.

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

## 7. POC Data Discovery & Profiling Contract (Tier 2)

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
    "floor": 2,
    "ceiling": 2,
    "clash": false
  },
  "recommended_rung": 2,
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
        "key": "own",
        "heard": "We ran our own geographic test two years ago.",
        "means": "Then you have an anchor already, and the first question is whether the model reproduces it out of sample. If it does not, that gap is the deliverable rather than something to tune away.",
        "floor": 2,
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
        "key": "google",
        "heard": "We want deduplicated reach across Google and YouTube.",
        "means": "A specific product answers this, not the general one: exposure joined to your own data stays inside Google’s privacy boundary, and newer options keep the matching inside your own perimeter. Naming the wrong one costs a CE the room.",
        "floor": 2,
        "ceiling": null
      }
    },
    {
      "id": "revision",
      "order": 11,
      "status": "open",
      "options": [
        "We keep every version as it arrived, dated.",
        "The provider resends and we overwrite the table.",
        "Nobody has checked whether it changes."
      ]
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
      "status": "open",
      "options": [
        "The call log is clean and we know the fully loaded cost.",
        "We have call counts, but samples and events are elsewhere.",
        "We know how many staff there are, not what they did.",
        "The field system belongs to sales; we have never seen it."
      ]
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
      "status": "open",
      "options": [
        "We worked out the smallest effect we could detect first.",
        "We picked markets that felt representative.",
        "We only have a handful of markets to work with.",
        "We have not looked at how much they vary."
      ]
    },
    {
      "id": "leak",
      "order": 18,
      "status": "open",
      "options": [
        "We will alert on any spend showing up in a dark market.",
        "National television and neighbouring areas will bleed in.",
        "Local teams will keep spending if we do not stop them.",
        "We assumed switching the campaigns off would be enough."
      ]
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
      "status": "open",
      "options": [
        "Within the hour is fine. The platforms batch anyway.",
        "Minutes. Our bidding genuinely reacts within the day.",
        "Nobody has ever specified it.",
        "The media team would have a view."
      ]
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
        "answer": "google"
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
    "revision",
    "promotion",
    "combine",
    "restatecost",
    "power",
    "leak",
    "carry",
    "anchor",
    "confound",
    "refute",
    "zero",
    "sla",
    "locked",
    "modelled"
  ],
  "counts": {
    "answered": 10,
    "stale": 0,
    "open": 14,
    "not_in_play": 5,
    "dropped": 0
  },
  "schema_version": "1.0",
  "problem_id": "marketing-measurement",
  "target_tier": 2,
  "derivation": {
    "floor": 2,
    "ceiling": 2,
    "recommended_tier": 2,
    "recommended_rung": 2,
    "clash": false
  }
}
```
