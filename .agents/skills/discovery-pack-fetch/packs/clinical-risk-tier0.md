---
schema_version: "1.0"
problem_id: "clinical-risk"
target_tier: 0
recommended_rung: 0
source: "built-in-classroom-pack"
---

# Discovery pack — Clinical Risk Stratification & Readmission

`clinical-risk` · recorded by **classroom-repo** · version 1 · served 2026-10-27T00:00:00Z

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

> **VP Finance, four-hospital nonprofit system, Epic shop** — CMS clawed back $1.8 million of our Medicare payments this year for readmissions. We already run Epic. I want a model that tells us who is going to bounce back before they walk out the door.
>
> **CMIO, 900-bed academic medical centre** — Our vendor score sits at 0.68 and the nurses have stopped looking at it. We think the real signal is in the notes. Our health equity committee will also want to see how it behaves across our patient populations before anything goes live.
>
> **VP Clinical Analytics, Medicare Advantage plan, 300k lives across 40 delivery systems** — We are at full risk for total cost of care. We want to know which members will be readmitted so care management can intervene, but our claims land 45 to 90 days after the event.

**Vocabulary is unbound.** The nouns below are the method's neutral words, not this customer's — treat them as placeholders and confirm the real terms early.

**The five specifics.**

- **How many, of the thing being predicted** — *not captured. Ask.*
- **How much history there is, and how much arrives** — *not captured. Ask.*
- **The deadline the run has to hit** — *not captured. Ask.*
- **What being wrong costs, per event or per year** — *not captured. Ask.*
- **Who owns the decision, and who would run this** — *not captured. Ask.*

## 2. Where discovery landed

- **Floor: Tier 0 — Out of the Box** — set by Which number are you graded on, and who works it out, How many a week the team can actually take on, What actually happens to someone the list flags, Where the number lands in someone else’s day, Do you find out when they go somewhere else
- **Ceiling:** nothing heard yet rules out the top of the ladder

## 3. What was asked, and what it steered

### 1. Which number are you graded on, and who works it out

**Asked:** Which number are you judged on at the end of the year, and who works that number out — you, or somebody outside?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** A federal programme claws back part of our payments when too many come back.
- **Which means:** The penalty ratio is a risk-standardised ratio, adjusted using conditions coded after the patient left, and since 2019 compared against a median of similar hospitals rather than against a fixed target.
- **Bounds:** not below Tier 0 — Out of the Box
- **For the brief:** Graded on an outside ratio. The model target and the graded number are different things.
- **Why it was asked:** Whether the target belongs to this customer or to a third party. A penalty ratio computed elsewhere fixes the label definition, the comparison group and how long you wait to see any effect, and none of the three are yours to change.
- **What it forecloses:** The contract question, the penalty arithmetic, and every argument about what the model should optimise. If somebody outside computes the number, no model metric is the business case.

### 2. How many a week the team can actually take on

**Asked:** How many people a week can the team that does the following up actually take on — not the target, what they managed last week?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Realistically about a dozen a week, and that is when nobody is on leave.
- **Which means:** At a dozen, ranking barely matters — almost any sensible order fills the list with people who qualify. What matters is that the twelve are ones a follow-up can still change.
- **Bounds:** not below Tier 0 — Out of the Box
- **For the brief:** Twelve a week. Rank for reachability, not for accuracy; a plain query is enough to start.
- **Why it was asked:** The operating point. The list gets cut at what the care coordinators can work, so the model is graded on how many of the top few dozen were right rather than on how well it separates everybody.
- **What it forecloses:** Every argument about a score cut-off, and most of the argument about accuracy. A team of twelve does not need a better model. It needs a shorter list.

### 3. What actually happens to someone the list flags

**Asked:** When a name comes up on the list, what actually happens to that person, and who does it?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Depends who picks it up. Sometimes a call, sometimes nothing.
- **Which means:** Then no effect will be measurable, because half the flagged people got nothing and nobody recorded which half. Logging what was actually done is the first build, ahead of any model.
- **Bounds:** not below Tier 0 — Out of the Box
- **For the brief:** Inconsistent follow-up. Log delivery per patient before promising any measurable effect.
- **Why it was asked:** Whether there is a follow-up at all. This is the single fact the build brief cannot be written without, and the one most often still open when a hospital commissions the score.
- **What it forecloses:** The whole argument about how good the model needs to be, and the ranking question underneath it. Nobody can rank by what they can change until somebody names what they can change.

### 4. Where the number lands in someone else’s day

**Asked:** Where does the number show up, and what is that person in the middle of doing when it appears?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** There is a column in the chart already. Nobody looks at it.
- **Which means:** The honest read: the score is not the problem, the delivery is. Before rebuilding the number, find out who was supposed to act on that column and what stopped them.
- **Bounds:** not below Tier 0 — Out of the Box
- **For the brief:** Existing column ignored. Diagnose the delivery failure before rebuilding the score.
- **Why it was asked:** The worklist. A number on a list somebody works through is a different build from a number that interrupts a clinician signing an order, and the second has a measured dismissal rate before you write a line.
- **What it forecloses:** The alert design questions and most of the integration scope. A list is a table. An interruption is a service inside the record system with a response budget and a change-control process.

### 6. Do you find out when they go somewhere else

**Asked:** If the same person turns up somewhere else instead of coming back to you, do you ever find out?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Only if they come back through our own doors.
- **Which means:** A known and quantified blind spot. It does not stop the build, but every reported figure is optimistic by the size of it, and that has to be stated before anybody sets a target.
- **Bounds:** not below Tier 0 — Out of the Box
- **For the brief:** Own-doors only. Label is incomplete by roughly a fifth; state it on every reported figure.
- **Why it was asked:** Whether the label is complete. A single provider misses roughly a fifth to a quarter of returns because the person went down the road, and every one of those is trained on as though nothing happened.
- **What it forecloses:** The out-of-network questions, the identity-matching scope, and the argument about whether the unit is a visit or a person-month.

## 4. Still worth asking

**These are instructions, not blanks.** Ask each one. The possible answers below are authored, with what each would rule in or out, so a reply can be recognised rather than interpreted.

### 5. Can you rebuild the record as it stood that morning

**Ask:** Can you rebuild what was written about someone exactly as it looked the morning they went home, or do you only have how it looks now?

**Why it matters:** Whether point-in-time reconstruction is the project. Much of a record is finished by coders three to ten days later, and a model trained on those fields but run at the bedside is the standard failure in this field.

What the answers would mean:

- **Every change is kept with a timestamp. We can rewind it.** → Rare and valuable. Say so — it means the hardest and least visible part of this build is already paid for, and the first honest model can be fitted this quarter. *(floor Tier 1 — Serverless, In-Warehouse)*
- **We archive a copy of the whole extract every night and keep them.** → Workable. Nightly granularity is enough when the decision happens once, on the morning of discharge, and it costs nothing to start from. It will not support a live cut later. *(floor Tier 1 — Serverless, In-Warehouse)*
- **The extract shows how things look today. There is no history in it.** → Then there is no defensible training set yet, only a leaky one. Capture starts the clock the day it is turned on, so the first credible model is quarters away and should be said so now. *(floor Tier 2 — Distributed & Custom ML)*
- **I think the reporting copy just overwrites. I would have to check.** → Check before anything else. This single answer decides whether the engagement opens with a model or with a data-capture build, and the two look nothing alike.

### 7. Where the worry is written down: a box, or the notes

**Ask:** The things that make your staff worry about someone going home — are those written in a box somewhere, or only in what people typed?

**Why it matters:** Whether free text is in scope, which is the largest single fork in this build. Text brings the housing, transport and caregiver context that the coded record simply does not carry, and it brings a governance review with it.

What the answers would mean:

- **It is mostly in the numbers. Results, observations, how long they stayed.** → Then the coded build is the whole build, which is good news for cost and for the review. Set expectations at the documented plateau and spend the effort on delivery instead. *(floor Tier 1 — Serverless, In-Warehouse)*
- **The real signal is in the notes. Housing, whether anyone is at home for them.** → The healthcare text service that used to map concepts to standard codes was switched off in May 2026 and the healthcare-tuned model the year before. A general model is the remaining path, and validating what it emits is yours. *(floor Tier 2 — Distributed & Custom ML)*
- **There are screening boxes for exactly that. They are mostly empty.** → Worse than absent, because the emptiness is rarely random. If it tracks language or payer, filling it in by assumption is a fairness decision dressed as data cleaning. *(floor Tier 2 — Distributed & Custom ML)*
- **I would guess the notes, but I have not looked at them in years.** → Read fifty of them with a clinician in the room. An afternoon of that settles the question better than any survey of the schema, and it is a good meeting to be in.

### 8. Who signs it off, and what have they turned down

**Ask:** Who has to approve this before anyone sees it, how often do they meet, and can they show you something they turned down?

**Why it matters:** The release process and the artefacts. It also sets the schedule: a committee that meets quarterly puts a hard floor under how fast anything ships, and no ladder rung shortens it.

What the answers would mean:

- **There is a standing committee. They meet monthly and they have said no before.** → Real governance, which is good news and a schedule constraint. Get a rejected submission: it tells you what they check, in their words, better than any policy document will. *(floor Tier 2 — Distributed & Custom ML)*
- **Our informatics team reviews it and then it goes live.** → Faster and lighter, and the review will be technical rather than about who the model serves worse. Somebody should still ask the second question, and it may have to be you. *(floor Tier 1 — Serverless, In-Warehouse)*
- **Nobody here has ever reviewed one of these. You would be the first.** → Then part of the deliverable is the review itself. That is a genuine gift to the customer and it is also the thing that will delay go-live, so it belongs in the plan on day one. *(floor Tier 1 — Serverless, In-Warehouse)*
- **There is a committee somewhere. I do not know what they cover.** → Find out early. Discovering a quarterly approval gate in month five is the most common way a healthcare build misses a date that was never actually achievable.

### 9. How you will know a year from now that it worked

**Ask:** A year from now, how will you know this worked — and what would convince somebody who thinks it did not?

**Why it matters:** Whether an effect will be measurable at all. The graded number is the worst available answer: its window is three years wide and closes fifteen months before the payment year it lands in.

What the answers would mean:

- **We could switch it on one unit at a time and compare as we go.** → The best answer anyone gives to this question. A staged rollout is free, it is normal practice for a change of this kind, and it turns an argument about what caused what into a comparison. *(floor Tier 2 — Distributed & Custom ML)*
- **The rate on the monthly board should come down.** → It will move for reasons that have nothing to do with you. Worth tracking, worthless as proof, and the honest version needs a comparison group of some sort even a weak one. *(floor Tier 1 — Serverless, In-Warehouse)*
- **The clawback should be smaller next year.** → It will not be, and not because the work failed. The window is three years wide and the comparison group moves underneath you, so the ratio cannot resolve anything you did this year. *(floor Tier 0 — Out of the Box)*
- **We have not talked about how we would prove it, no.** → The best moment to raise it is now, while the answer is still cheap. After go-live, every design that would have produced evidence has already been foreclosed.

### 10. How complete is the coding the adjustment runs on

**Ask:** When your coders finish a record, how often does a condition somebody clearly had never make it into the codes?

**Why it matters:** Whether part of the gap is documentation rather than care. The adjustment computes how many returns were expected from the conditions on file, so an under-coded stay raises the ratio without anybody treating anyone worse.

What the answers would mean:

- **We have a documentation team and they audit it. We think it is tight.** → Ask to see the audit. If it is genuinely tight the ratio gap is clinical, which is the case for building something — and now you can say so with evidence rather than hope. *(floor Tier 1 — Serverless, In-Warehouse)*
- **We know we under-document. It comes up every year and nothing changes.** → Then the cheapest point of the whole engagement is a gap report, not a model: which conditions appear in results and notes but never in codes. It moves the number the customer is actually graded on. *(floor Tier 0 — Out of the Box)*
- **That sits with the coding team. I could not tell you.** → Worth a meeting with them before the next one with you. This question decides whether the customer is buying a model or an audit, and they are very different quarters.

### 11. Do you know who you are actually being compared against

**Ask:** Do you know which other organisations you are compared with, and where you sit among them right now?

**Why it matters:** What "good" is. The comparison is against the middle of a group of similar providers, so the target moves every year and a small improvement can still be a penalty. It also decides which service lines are even in scope.

What the answers would mean:

- **Yes, we get the report and we know which group we are sorted into.** → Good sign. Ask for it. The report names which of the six condition groups actually contributed and how many cases each had, which is the scoping conversation in one page. *(floor Tier 1 — Serverless, In-Warehouse)*
- **We just look at whether the ratio is over one. Nobody mentioned a group.** → Then the goal has been wrong. A ratio slightly over 1.0 can carry no penalty at all if the comparison group sits higher, and a ratio under it can still cost money. Read the report first. *(floor Tier 0 — Out of the Box)*
- **A couple of the categories barely have any patients in them for us.** → Then those categories may not count against you at all, and building a cohort model for them is spend on a measure with no weight. Confirm the counts before scoping. *(floor Tier 0 — Out of the Box)*
- **I would have to dig that out of whatever finance filed.** → It exists and it is short. Getting it is the highest value-per-minute task in the first two weeks of this engagement.

### 14. How far do people travel for their care here

**Ask:** When people who live near you need care, how often do they go to a different organisation instead?

**Why it matters:** The size of the hole. In a rural single-provider area the blind spot is small and can be reasoned about; in a dense city with four systems on the same road it can dominate everything you report.

What the answers would mean:

- **We are the only one for fifty miles. They come to us or they go nowhere.** → Then the blind spot is genuinely small and the label is close to complete. Note the exception — the tertiary centre in the city that takes the sickest — and move on. *(floor Tier 1 — Serverless, In-Warehouse)*
- **There are three other systems within twenty minutes. People shop around.** → Then a meaningful share of your negatives are actually positives, and the model learns to like the people who leave. An external feed stops being a nice-to-have. *(floor Tier 2 — Distributed & Custom ML)*
- **No idea. We only ever see our own side of it.** → Approximable without buying anything: state hospital discharge files or the exchange’s own coverage report will size it well enough to decide.

## 5. Not worth asking yet

Each of these is gated behind a branch that is not open. They are listed so the absence is legible: they were not forgotten, they were ruled out.

- **What share of the current pop-ups get dismissed** — closed by *Where the number lands in someone else’s day* → “There is a column in the chart already. Nobody looks at it”.
- **Which fields settle after the person goes home** — needs “The record cannot be rebuilt as it stood when the call was made”, which nothing answered has opened.
- **How many sources send, and how would you notice a gap** — closed by *Do you find out when they go somewhere else* → “Only if they come back through our own doors”.
- **How long until the record for a month is stable** — closed by *Do you find out when they go somewhere else* → “Only if they come back through our own doors”.
- **How much of a note is copied from the last one** — needs “The signal everyone points to is in free text, not a coded field”, which nothing answered has opened.
- **Does the blankness track any group you must report on** — needs “The fields carrying social context are mostly blank”, which nothing answered has opened.
- **Which groups, and do they want ranking or meaning** — needs “A standing committee must approve the model before go-live”, which nothing answered has opened.
- **Is there enough volume to see the size of effect you expect** — needs “The rollout can be staged rather than switched on everywhere”, which nothing answered has opened.

## 6. What is being suggested, and why the alternatives are out

### Tier 0 — Out of the Box

Test the score they already own

- **What it is:** Vendor score + a four-field index as a BigQuery view → twelve-month replay → Conversational Analytics
- **Google Cloud & open-weight options at this rung:** BigQuery, AI.PREDICT, Conversational Analytics
- **Why here:** The four-field index — length of stay, how acute, other conditions, prior emergency visits — matched the Epic model in the one published external test: 0.703 ranking accuracy against 0.692 over 23,116 discharges. It costs a view.
- **Where it breaks:** Neither number is fitted to these patients or this coding, neither reads what was typed, and neither can be cut at what the care coordinators can take. In one cancer group the vendor score fell to 0.52, which is a coin toss.
- **What would move it up:** A year of your own discharges shows the score you already own ranking no better than the free view, or collapsing on one service line.

#### Architecture Decision Record (ADR) Matrix

A scenario-aware evaluation of the ladder against this customer's constraints. Where an adjacent tier serves as a viable A/B benchmark or a Phase 2 evolution, that role is explicitly called out:

| Rung | Role in this Engagement | Architecture & Stance | Deciding Constraint & Trade-off |
| --- | --- | --- | --- |
| Tier 0 — Out of the Box | **Primary Baseline (MVP)** | Test the score they already own. Fits all bounded constraints. | Selected target. Fits floor (Tier 0 — Out of the Box). Wins: The four-field index — length of stay, how acute, other conditions, prior emergency visits — matched the Epic model in the one published external test: 0.703 ranking accuracy against 0.692 over 23,116 discharges. It costs a view. |
| Tier 1 — Serverless, In-Warehouse | **Adjacent Higher Tier (Phase 2 Evolution)** | Fit it to your own people, and say why it fired. Higher freshness, lower latency, or specialised modeling. | Inside the range, but nothing heard requires it yet. Step-up trigger: A year of your own discharges shows the score you already own ranking no better than the free view, or collapsing on one service line. Propose as Phase 2 expansion once this condition is met. |
| Tier 2 — Distributed & Custom ML | In range, not required | Read the notes, freeze the clock, check every group. | Not ruled out, but nothing heard in the room requires it. |
| Tier 3 — Real-Time & Specialised | In range, not required | Act on the discharge message, not on the bill. | Not ruled out, but nothing heard in the room requires it. |

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

- Tier 1 — Serverless, In-Warehouse — Fit it to your own people, and say why it fired. Out: not ruled out, but nothing heard in the room requires it.
- Tier 2 — Distributed & Custom ML — Read the notes, freeze the clock, check every group. Out: not ruled out, but nothing heard in the room requires it.
- Tier 3 — Real-Time & Specialised — Act on the discharge message, not on the bill. Out: not ruled out, but nothing heard in the room requires it.

**Below the rung sit the calls no rung makes for you.** The tier does not settle these, and a design that has not stated them has not been made. Nothing on the page asks for them, so they travel unanswered.

- **What one row is** — One stay cut at discharge morning, labelled by a return inside 30 days. Or one patient-month, which is all a plan can build when it never sees the admission and the bill lands 45 to 90 days later.
  Options: One stay, cut at discharge morning · One patient-month of membership · One row per period still out
- **What goes in beside the past** — Whether the fit sees only coded fields that existed by discharge morning, or the housing and caregiver context a clinician typed into the notes — and, separately, which coded fields quietly settle after the patient has gone.
  Options: Coded fields, cut at the decision moment · Named concepts pulled from the notes · Late-settling codes, retrospective only
- **One fit, one each, or one per group** — Six graded measures across several facilities with different case mixes, plus the strata a committee wants seen separately. Which of those are fit groups and which are only evaluation groups is the entire question.
  Options: One pooled fit, group as an input column · One fit per measure and facility · One fit per protected population
- **Which methods get a run** — Three answers that differ in kind: a four-field index that is a view, a fitted classifier over your own mart, and a timing fit that treats death as its own ending. Only the last needs something SQL cannot write.
  Options: The four-field index, and the score you own · A fitted classifier over the mart · A timing fit, death competing
- **How you would know** — What is held back is time, not rows: fit on settled months, score the ones after. And no single measure covers it — hit rate at the cut the care coordinators work, and whether the number means the same per group, are different tests.
  Options: Hit rate at weekly capacity · Observed against expected, within each group · Group error-rate gaps, wired to block
- **What tuning is worth** — Three candidates for the time: the label, the as-of cut, and the settings. Here the label is the worst of the three — planned returns to exclude, deaths to separate, and the fifth to a quarter of returns that happen down the road.
  Options: Fix the label first · Fix the cut · Search the settings
- **One winner, or several combined** — Two combinings, and only one is a choice. The timing fit already sums a return hazard and a death hazard into one curve. Averaging the tree with the regression is the optional one, and it is judged differently.
  Options: One model, one card · Average the shortlist · Combine the causes, not the models

**Dataset for the build.** Every workshop build runs on public or shipped tables:

- **Source:** BigQuery public tables (synthetic)
- **Tables:** `bigquery-public-data.fhir_synthea.patient`, `bigquery-public-data.fhir_synthea.encounter`, `bigquery-public-data.fhir_synthea.condition`, `bigquery-public-data.fhir_synthea.medication_request`, `bigquery-public-data.cms_synthetic_patient_data_omop.person`, `bigquery-public-data.cms_synthetic_patient_data_omop.condition_occurrence`, `bigquery-public-data.cms_synthetic_patient_data_omop.death`
- **Grain & size:** One row per inpatient stay in fhir_synthea.encounter (class.code = “IMP”; 1.39M inpatient stays across 272,678 synthetic patients out of 40.3M encounters), plus 2.33M synthetic beneficiaries and 107,644 death dates in cms_synthetic_patient_data_omop.
- **Target / label:** Unplanned inpatient readmission within 30 days of discharge (Tier 1) or weeks from index inpatient stay to death (Tier 2).
- **Tier 1 / Tier 2 build:** Hard Tier 1 flattens FHIR arrays into a 50,000-stay cohort and fits BOOSTED_TREE_CLASSIFIER with ML.EXPLAIN_PREDICT explanations at a nurse-outreach cap; Tier 2 audits subgroup sensitivity and positive predictive value and fits a time-to-death model on OMOP.
- **Caveat:** cms_synthetic_patient_data_omop has no visit_occurrence table (inpatient stays sit on condition_occurrence.visit_occurrence_id with condition_type_concept_id = 38000200, or natively in fhir_synthea.encounter), and train/test splits must group by patient ID.
- **Setup / verify:** `bq head -n 5 bigquery-public-data:fhir_synthea.encounter`
- **Agent skills (`bigquery-data-science` & Data Agent Kit):** `uvx bigquery-data-science lookup ML.EXPLAIN_PREDICT # BQDS: CONTRIBUTION_ANALYSIS, ML.GET_INSIGHTS, BOOSTED_TREE_CLASSIFIER, LOGISTIC_REG, TRANSFORM | Data Agent Kit: bigquery-ai-ml, data-autocleaning, bigquery-sql, bigquery-bigframes, ml-best-practices`

**The ladder, for reference.** No site is needed to read the tiers above.

- **Tier 0 — Out of the Box** — A model somebody else trained already answers the question. Nothing to fit, nothing to provision, and the bill starts on the first query. The most senior move in the room is often to say so.
- **Tier 1 — Serverless, In-Warehouse** — Bring the model to the data. No cluster, no container, no serving stack. SQL is the interface.
- **Tier 2 — Distributed & Custom ML** — The transformation or the model outgrew SQL. Bring distributed compute to the data, keep the storage where it is.
- **Tier 3 — Real-Time & Specialised** — A hard SLA or a custom objective justifies owning the stack. You are now engineering a system, not training a model.
- **Tier 4 — Hardening for High-Stakes Operation** — Not a rung you buy. It is what changes about a system already at Tier 1, 2 or 3 once being wrong is expensive, contested or unsafe — and what changes is different for every problem in Discovery.

## 7. POC Data Discovery & Profiling Contract (Tier 0)

- **Source Tables (`bigquery-region: "US"`):** `bigquery-public-data.fhir_synthea.patient`, `bigquery-public-data.fhir_synthea.encounter`, `bigquery-public-data.fhir_synthea.condition`, `bigquery-public-data.fhir_synthea.medication_request`, `bigquery-public-data.cms_synthetic_patient_data_omop.person`, `bigquery-public-data.cms_synthetic_patient_data_omop.condition_occurrence`, `bigquery-public-data.cms_synthetic_patient_data_omop.death`
- **Grain & Target:** One row per inpatient stay in fhir_synthea.encounter (class.code = “IMP”; 1.39M inpatient stays across 272,678 synthetic patients out of 40.3M encounters), plus 2.33M synthetic beneficiaries and 107,644 death dates in cms_synthetic_patient_data_omop. | Unplanned inpatient readmission within 30 days of discharge (Tier 1) or weeks from index inpatient stay to death (Tier 2).
- **Data Caveat to Profile & Guard Against:** cms_synthetic_patient_data_omop has no visit_occurrence table (inpatient stays sit on condition_occurrence.visit_occurrence_id with condition_type_concept_id = 38000200, or natively in fhir_synthea.encounter), and train/test splits must group by patient ID.
- **Verification Command:** `bq head -n 5 bigquery-public-data:fhir_synthea.encounter`

---

### The same thing, for a program to read

```json
{
  "problem": "clinical-risk",
  "ldap": "classroom-repo",
  "version": 1,
  "served_at": "2026-10-27T00:00:00Z",
  "binding": {
    "subject": "patient",
    "episode": "stay",
    "relapse": "return",
    "reader": "clinician",
    "coordinator": "care coordinator",
    "followup": "follow-up",
    "grade": "penalty ratio",
    "notice": "discharge message",
    "placement": "worklist"
  },
  "range": {
    "floor": 0,
    "ceiling": 0,
    "clash": false
  },
  "recommended_rung": 0,
  "data": {
    "source": "BigQuery public tables (synthetic)",
    "tables": [
      "bigquery-public-data.fhir_synthea.patient",
      "bigquery-public-data.fhir_synthea.encounter",
      "bigquery-public-data.fhir_synthea.condition",
      "bigquery-public-data.fhir_synthea.medication_request",
      "bigquery-public-data.cms_synthetic_patient_data_omop.person",
      "bigquery-public-data.cms_synthetic_patient_data_omop.condition_occurrence",
      "bigquery-public-data.cms_synthetic_patient_data_omop.death"
    ],
    "grain": "One row per inpatient stay in fhir_synthea.encounter (class.code = “IMP”; 1.39M inpatient stays across 272,678 synthetic patients out of 40.3M encounters), plus 2.33M synthetic beneficiaries and 107,644 death dates in cms_synthetic_patient_data_omop.",
    "label": "Unplanned inpatient readmission within 30 days of discharge (Tier 1) or weeks from index inpatient stay to death (Tier 2).",
    "rungs": "Hard Tier 1 flattens FHIR arrays into a 50,000-stay cohort and fits BOOSTED_TREE_CLASSIFIER with ML.EXPLAIN_PREDICT explanations at a nurse-outreach cap; Tier 2 audits subgroup sensitivity and positive predictive value and fits a time-to-death model on OMOP.",
    "caveat": "cms_synthetic_patient_data_omop has no visit_occurrence table (inpatient stays sit on condition_occurrence.visit_occurrence_id with condition_type_concept_id = 38000200, or natively in fhir_synthea.encounter), and train/test splits must group by patient ID.",
    "setup": "bq head -n 5 bigquery-public-data:fhir_synthea.encounter",
    "skills": "uvx bigquery-data-science lookup ML.EXPLAIN_PREDICT # BQDS: CONTRIBUTION_ANALYSIS, ML.GET_INSIGHTS, BOOSTED_TREE_CLASSIFIER, LOGISTIC_REG, TRANSFORM | Data Agent Kit: bigquery-ai-ml, data-autocleaning, bigquery-sql, bigquery-bigframes, ml-best-practices"
  },
  "questions": [
    {
      "id": "scored",
      "order": 1,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "err",
        "heard": "A federal programme claws back part of our payments when too many come back.",
        "means": "The penalty ratio is a risk-standardised ratio, adjusted using conditions coded after the patient left, and since 2019 compared against a median of similar hospitals rather than against a fixed target.",
        "floor": 0,
        "ceiling": null
      }
    },
    {
      "id": "capacity",
      "order": 2,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "small",
        "heard": "Realistically about a dozen a week, and that is when nobody is on leave.",
        "means": "At a dozen, ranking barely matters — almost any sensible order fills the list with people who qualify. What matters is that the twelve are ones a follow-up can still change.",
        "floor": 0,
        "ceiling": null
      }
    },
    {
      "id": "acts",
      "order": 3,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "mixed",
        "heard": "Depends who picks it up. Sometimes a call, sometimes nothing.",
        "means": "Then no effect will be measurable, because half the flagged people got nothing and nobody recorded which half. Logging what was actually done is the first build, ahead of any model.",
        "floor": 0,
        "ceiling": null
      }
    },
    {
      "id": "where",
      "order": 4,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "column",
        "heard": "There is a column in the chart already. Nobody looks at it.",
        "means": "The honest read: the score is not the problem, the delivery is. Before rebuilding the number, find out who was supposed to act on that column and what stopped them.",
        "floor": 0,
        "ceiling": null
      }
    },
    {
      "id": "cutoff",
      "order": 5,
      "status": "open",
      "keystone": true,
      "options": [
        "Every change is kept with a timestamp. We can rewind it.",
        "We archive a copy of the whole extract every night and keep them.",
        "The extract shows how things look today. There is no history in it.",
        "I think the reporting copy just overwrites. I would have to check."
      ]
    },
    {
      "id": "coverage",
      "order": 6,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "own",
        "heard": "Only if they come back through our own doors.",
        "means": "A known and quantified blind spot. It does not stop the build, but every reported figure is optimistic by the size of it, and that has to be stated before anybody sets a target.",
        "floor": 0,
        "ceiling": null
      }
    },
    {
      "id": "signal",
      "order": 7,
      "status": "open",
      "keystone": true,
      "options": [
        "It is mostly in the numbers. Results, observations, how long they stayed.",
        "The real signal is in the notes. Housing, whether anyone is at home for them.",
        "There are screening boxes for exactly that. They are mostly empty.",
        "I would guess the notes, but I have not looked at them in years."
      ]
    },
    {
      "id": "equity",
      "order": 8,
      "status": "open",
      "keystone": true,
      "options": [
        "There is a standing committee. They meet monthly and they have said no before.",
        "Our informatics team reviews it and then it goes live.",
        "Nobody here has ever reviewed one of these. You would be the first.",
        "There is a committee somewhere. I do not know what they cover."
      ]
    },
    {
      "id": "proof",
      "order": 9,
      "status": "open",
      "keystone": true,
      "options": [
        "We could switch it on one unit at a time and compare as we go.",
        "The rate on the monthly board should come down.",
        "The clawback should be smaller next year.",
        "We have not talked about how we would prove it, no."
      ]
    },
    {
      "id": "coding",
      "order": 10,
      "status": "open",
      "options": [
        "We have a documentation team and they audit it. We think it is tight.",
        "We know we under-document. It comes up every year and nothing changes.",
        "That sits with the coding team. I could not tell you."
      ]
    },
    {
      "id": "peer",
      "order": 11,
      "status": "open",
      "options": [
        "Yes, we get the report and we know which group we are sorted into.",
        "We just look at whether the ratio is over one. Nobody mentioned a group.",
        "A couple of the categories barely have any patients in them for us.",
        "I would have to dig that out of whatever finance filed."
      ]
    },
    {
      "id": "fatigue",
      "order": 12,
      "status": "not_in_play",
      "gate": "The number will interrupt someone in the middle of a task",
      "closed_by": {
        "question": "where",
        "answer": "column"
      }
    },
    {
      "id": "history",
      "order": 13,
      "status": "not_in_play",
      "gate": "The record cannot be rebuilt as it stood when the call was made",
      "closed_by": null
    },
    {
      "id": "blind",
      "order": 14,
      "status": "open",
      "options": [
        "We are the only one for fifty miles. They come to us or they go nowhere.",
        "There are three other systems within twenty minutes. People shop around.",
        "No idea. We only ever see our own side of it."
      ]
    },
    {
      "id": "feed",
      "order": 15,
      "status": "not_in_play",
      "gate": "An outside notification feed is the only near-real-time signal",
      "closed_by": {
        "question": "coverage",
        "answer": "own"
      }
    },
    {
      "id": "lag",
      "order": 16,
      "status": "not_in_play",
      "gate": "The outcome only shows up on a bill that lands months later",
      "closed_by": {
        "question": "coverage",
        "answer": "own"
      }
    },
    {
      "id": "notes",
      "order": 17,
      "status": "not_in_play",
      "gate": "The signal everyone points to is in free text, not a coded field",
      "closed_by": null
    },
    {
      "id": "missing",
      "order": 18,
      "status": "not_in_play",
      "gate": "The fields carrying social context are mostly blank",
      "closed_by": null
    },
    {
      "id": "strata",
      "order": 19,
      "status": "not_in_play",
      "gate": "A standing committee must approve the model before go-live",
      "closed_by": null
    },
    {
      "id": "stepped",
      "order": 20,
      "status": "not_in_play",
      "gate": "The rollout can be staged rather than switched on everywhere",
      "closed_by": null
    }
  ],
  "conflicts": [],
  "still_to_ask": [
    "cutoff",
    "signal",
    "equity",
    "proof",
    "coding",
    "peer",
    "blind"
  ],
  "counts": {
    "answered": 5,
    "stale": 0,
    "open": 7,
    "not_in_play": 8,
    "dropped": 0
  },
  "schema_version": "1.0",
  "problem_id": "clinical-risk",
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
