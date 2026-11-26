---
schema_version: "1.0"
problem_id: "clinical-risk"
target_tier: 2
recommended_rung: 2
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

- **Floor: Tier 2 — Distributed & Custom ML** — set by How many a week the team can actually take on, Where the number lands in someone else’s day, Can you rebuild the record as it stood that morning, Do you find out when they go somewhere else, Where the worry is written down: a box, or the notes, Who signs it off, and what have they turned down, How you will know a year from now that it worked, Graded on an outside ratio, from a source with no history
- **Ceiling:** nothing heard yet rules out the top of the ladder

> **Together, not apart.** Graded on an outside ratio, from a source with no history. You can neither train without leaking nor reproduce the number you are judged on. The first deliverable is change capture, and the ratio cannot be the success measure — its window shuts long before the payment year.

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

- **Heard:** The outreach is a text message and a call centre, so thousands.
- **Which means:** Capacity stops being the constraint and cost of contact takes over. This is the only shape where a wide, always-on list is defensible, and it is also where irritation becomes the harm.
- **Bounds:** not below Tier 2 — Distributed & Custom ML
- **For the brief:** Automated outreach at scale. Constraint moves from capacity to contact cost and nuisance.
- **Why it was asked:** The operating point. The list gets cut at what the care coordinators can work, so the model is graded on how many of the top few dozen were right rather than on how well it separates everybody.
- **What it forecloses:** Every argument about a score cut-off, and most of the argument about accuracy. A team of twelve does not need a better model. It needs a shorter list.

### 3. What actually happens to someone the list flags

**Asked:** When a name comes up on the list, what actually happens to that person, and who does it?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** A nurse calls within two days and books the appointment before they leave.
- **Which means:** A real follow-up with an owner and a deadline. Now the ranking can be built against it: who is reachable, who has nothing booked, who is on medicines that need reviewing.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Named intervention with an owner. Rank on what that intervention can plausibly change.
- **Why it was asked:** Whether there is a follow-up at all. This is the single fact the build brief cannot be written without, and the one most often still open when a hospital commissions the score.
- **What it forecloses:** The whole argument about how good the model needs to be, and the ranking question underneath it. Nobody can rank by what they can change until somebody names what they can change.

### 4. Where the number lands in someone else’s day

**Asked:** Where does the number show up, and what is that person in the middle of doing when it appears?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** It has to appear in front of the doctor at the moment they discharge.
- **Which means:** That is a live callout from the record system to a service you host and keep inside the response budget. Real, and supported by the major vendors — but you are now inside somebody’s hands-on-keyboard moment.
- **Bounds:** not below Tier 2 — Distributed & Custom ML
- **For the brief:** In-record interruption required. Needs a hosted callout service and change control.
- **Why it was asked:** The worklist. A number on a list somebody works through is a different build from a number that interrupts a clinician signing an order, and the second has a measured dismissal rate before you write a line.
- **What it forecloses:** The alert design questions and most of the integration scope. A list is a table. An interruption is a service inside the record system with a response budget and a change-control process.

### 5. Can you rebuild the record as it stood that morning

**Asked:** Can you rebuild what was written about someone exactly as it looked the morning they went home, or do you only have how it looks now?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** The extract shows how things look today. There is no history in it.
- **Which means:** Then there is no defensible training set yet, only a leaky one. Capture starts the clock the day it is turned on, so the first credible model is quarters away and should be said so now.
- **Bounds:** not below Tier 2 — Distributed & Custom ML
- **For the brief:** Current-state only. Change capture is the first deliverable; no trustworthy fit before it.
- **Why it was asked:** Whether point-in-time reconstruction is the project. Much of a record is finished by coders three to ten days later, and a model trained on those fields but run at the bedside is the standard failure in this field.
- **What it forecloses:** The entire leakage group and the feature-storage argument. If the extract is current-state only, nothing downstream is trustworthy and building the history comes first.

### 6. Do you find out when they go somewhere else

**Asked:** If the same person turns up somewhere else instead of coming back to you, do you ever find out?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** A regional exchange messages us whenever one of ours is admitted anywhere.
- **Which means:** The only signal that arrives before the bill. It also drags in matching people across sources that never agreed on an identifier, which is usually the larger half of the work.
- **Bounds:** not below Tier 2 — Distributed & Custom ML
- **For the brief:** Exchange feed available. Matching people across sources is in scope from the start.
- **Why it was asked:** Whether the label is complete. A single provider misses roughly a fifth to a quarter of returns because the person went down the road, and every one of those is trained on as though nothing happened.
- **What it forecloses:** The out-of-network questions, the identity-matching scope, and the argument about whether the unit is a visit or a person-month.

### 7. Where the worry is written down: a box, or the notes

**Asked:** The things that make your staff worry about someone going home — are those written in a box somewhere, or only in what people typed?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** The real signal is in the notes. Housing, whether anyone is at home for them.
- **Which means:** The healthcare text service that used to map concepts to standard codes was switched off in May 2026 and the healthcare-tuned model the year before. A general model is the remaining path, and validating what it emits is yours.
- **Bounds:** not below Tier 2 — Distributed & Custom ML
- **For the brief:** Signal in free text. Extraction is a general model under agreement; validation is in scope.
- **Why it was asked:** Whether free text is in scope, which is the largest single fork in this build. Text brings the housing, transport and caregiver context that the coded record simply does not carry, and it brings a governance review with it.
- **What it forecloses:** The whole modelling-approach argument. Coded fields alone plateau in a narrow band that is well documented, and no amount of tuning moves it.

### 8. Who signs it off, and what have they turned down

**Asked:** Who has to approve this before anyone sees it, how often do they meet, and can they show you something they turned down?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** There is a standing committee. They meet monthly and they have said no before.
- **Which means:** Real governance, which is good news and a schedule constraint. Get a rejected submission: it tells you what they check, in their words, better than any policy document will.
- **Bounds:** not below Tier 2 — Distributed & Custom ML
- **For the brief:** Standing committee, monthly. Release cadence is set by them; obtain a prior submission.
- **Why it was asked:** The release process and the artefacts. It also sets the schedule: a committee that meets quarterly puts a hard floor under how fast anything ships, and no ladder rung shortens it.
- **What it forecloses:** Most of the governance group and the whole timeline argument. A previously accepted submission is worth more than any template, and asking for one is how you find out whether the process is real.

### 9. How you will know a year from now that it worked

**Asked:** A year from now, how will you know this worked — and what would convince somebody who thinks it did not?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** We could switch it on one unit at a time and compare as we go.
- **Which means:** The best answer anyone gives to this question. A staged rollout is free, it is normal practice for a change of this kind, and it turns an argument about what caused what into a comparison.
- **Bounds:** not below Tier 2 — Distributed & Custom ML
- **For the brief:** Staged rollout possible. Design the order as the comparison before the first unit goes live.
- **Why it was asked:** Whether an effect will be measurable at all. The graded number is the worst available answer: its window is three years wide and closes fifteen months before the payment year it lands in.
- **What it forecloses:** The success-criteria conversation, which otherwise reappears at the end of the engagement when nothing can be done about it.

## 4. Still worth asking

**These are instructions, not blanks.** Ask each one. The possible answers below are authored, with what each would rule in or out, so a reply can be recognised rather than interpreted.

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

### 12. What share of the current pop-ups get dismissed

**Ask:** Of the warnings that already pop up in front of your staff, roughly what share get clicked away without anything happening?

**Why it matters:** Whether an interruption is a viable delivery route here at all, and what threshold it would have to clear. The existing dismissal rate is the best available prediction of what yours will be.

What the answers would mean:

- **We measure it. It is somewhere north of ninety percent on most of them.** → They already know. That number is your argument for the list rather than the pop-up, and it is theirs, not yours — which is why it lands. *(floor Tier 0 — Out of the Box)*
- **We are strict about what fires. Only a handful, and people do read them.** → Rare and worth protecting. An organisation that rations interruptions has spent political capital doing it, and adding one is a governance conversation, not a configuration change. *(floor Tier 2 — Distributed & Custom ML)*
- **Nobody has ever put a number on that as far as I know.** → It is measurable from the record system’s own logs in an afternoon. Ask for it before designing anything that interrupts, because it decides the design.

### 13. Which fields settle after the person goes home

**Ask:** Which parts of a record get filled in or corrected after the person has already left, and how long does that usually take?

**Why it matters:** The banned list. Every field that settles after the decision has to be named and excluded, and the naming has to come from the customer because it varies by organisation and by service line.

What the answers would mean:

- **The final billing code and the discharge summary. Three days to a fortnight.** → A precise answer and the right one. Turn it directly into an assertion the build fails on, rather than a note in a document nobody reads at refit time. *(floor Tier 1 — Serverless, In-Warehouse)*
- **Almost everything gets touched at some point. Nobody has mapped it.** → Then the map is the work: for each field, the gap between when it first appears and when it stops changing. It is a week of profiling and it protects every model that follows. *(floor Tier 2 — Distributed & Custom ML)*
- **The coding team would know that better than I would.** → They will know it exactly, and they will enjoy being asked. This is also the meeting where the documentation gap conversation opens itself.

### 15. How many sources send, and how would you notice a gap

**Ask:** How many of the places your people actually go send you these messages, and how would anybody notice if one quietly stopped?

**Why it matters:** Whether the upper rung is buildable. Coverage is negotiated source by source, and the rule that made these messages mandatory points them at the person’s own practitioners — not at their health plan.

What the answers would mean:

- **Nearly all of them. The exchange has been at this for years.** → Then the feed is a real foundation. Spend the engineering on per-source volume alarms rather than on latency, because a dead source and a quiet week look identical on any total. *(floor Tier 3 — Real-Time & Specialised)*
- **Maybe half. The big ones send, the smaller places are a mixture.** → Workable but it has to be stated. Half the population is unreachable by this route, and reporting a programme result across everybody will silently blend two very different groups. *(floor Tier 2 — Distributed & Custom ML)*
- **We keep being told it is coming. Nothing arrives today.** → Then the upper rung is a roadmap item, not an architecture. Build the batch version against the bills, and make feed arrival the trigger that unlocks the next phase. *(floor Tier 1 — Serverless, In-Warehouse)*
- **Interfaces owns that. I could not tell you the coverage.** → The number exists and the interface team knows it. Ask for messages per source per day over the last month, which also hands you the alarm baseline for free.

### 17. How much of a note is copied from the last one

**Ask:** If you opened two notes about the same person a day apart, how much of the second one would be word for word the first?

**Why it matters:** Whether text will help or just teach the model which service line wrote it. Heavily copied documentation encodes the template and the author, and both look like signal in an offline test.

What the answers would mean:

- **Most of it. People pull the last note forward and edit a line.** → Then pull out a short list of named concepts a clinician can read back, and hold the line against a dense representation. It will win a point offline and lose the review that decides go-live. *(floor Tier 2 — Distributed & Custom ML)*
- **The nursing notes are genuinely written fresh each shift.** → Then the text is worth more than usual, and the nursing notes are the ones to read — they exist by discharge morning, and the signed summary generally does not. *(floor Tier 2 — Distributed & Custom ML)*
- **I could not say. It probably varies by service.** → Measurable in an hour by comparing consecutive notes for the same person. Do it before scoping text work, because it changes what you can promise.

### 19. Which groups, and do they want ranking or meaning

**Ask:** Which groups do they want to see separately, and do they want the order to be fair or the number itself to mean the same thing for everyone?

**Why it matters:** Which check you build. Fair ordering and a number that means the same thing are different properties, they can disagree, and only one of them is covered by the fairness measures the platform ships.

What the answers would mean:

- **Just make sure the list is not systematically missing certain patients.** → Error-rate comparisons across groups, which the platform does ship: differences in accuracy, in how many are correctly caught, and in the mix of mistakes. Wire them as a gate, not a report. *(floor Tier 2 — Distributed & Custom ML)*
- **A score of forty percent has to mean forty percent for every one of them.** → That is the harder one and it is not among the shipped measures — observed against expected, within each group, is a query you write. It also needs enough events per group to be worth reading. *(floor Tier 2 — Distributed & Custom ML)*
- **Some of the groups they care about have very few patients a year.** → Then say what cannot be reported and why, rather than reporting a number built on forty people. A committee will accept a stated limit far more readily than a fragile figure. *(floor Tier 2 — Distributed & Custom ML)*
- **They will tell us when they see it, I expect.** → Do not wait. The two properties need different evidence and different code, and finding out at the review is a rebuild rather than a revision.

### 20. Is there enough volume to see the size of effect you expect

**Ask:** How many people go home in a month, and how big a change would you actually be pleased with?

**Why it matters:** Whether the staged comparison can detect anything. At the usual rates a two-point improvement needs thousands of discharges per arm, and most single hospitals cannot supply them in a year.

What the answers would mean:

- **Several thousand a month across the system.** → Then a staged rollout across sites can resolve a realistic effect inside a year. Fix the order and the analysis before the first site, not after the third. *(floor Tier 2 — Distributed & Custom ML)*
- **A few hundred a month, and we would be happy with a couple of points.** → That comparison will not resolve in any reasonable time. Measure whether the follow-up was delivered and whether it reached the right people instead, and say plainly that the outcome will not settle. *(floor Tier 1 — Serverless, In-Warehouse)*
- **I know the annual figure. I have not thought about it that way.** → Two numbers and five minutes of arithmetic, and it is the most useful thing you can bring to the second meeting. Bring the duration it implies, not the formula.

## 5. Not worth asking yet

Each of these is gated behind a branch that is not open. They are listed so the absence is legible: they were not forgotten, they were ruled out.

- **How far do people travel for their care here** — closed by *Do you find out when they go somewhere else* → “A regional exchange messages us whenever one of ours is admitted anywhere”.
- **How long until the record for a month is stable** — closed by *Do you find out when they go somewhere else* → “A regional exchange messages us whenever one of ours is admitted anywhere”.
- **Does the blankness track any group you must report on** — closed by *Where the worry is written down: a box, or the notes* → “The real signal is in the notes. Housing, whether anyone is at home for them”.

## 6. What is being suggested, and why the alternatives are out

### Tier 2 — Distributed & Custom ML

Read the notes, freeze the clock, check every group

- **What it is:** FHIR change stream → BigQuery history → AI.GENERATE_TABLE notes → BigQuery DataFrames cohort → registered fit
- **Google Cloud & open-weight options at this rung:** Cloud Healthcare API, BigQuery, AI.GENERATE_TABLE, BigQuery DataFrames, Agent Platform training, Managed Service for Apache Airflow
- **What it carries:** Place carried from Tier 1, still a table read later. What changed is the build: a registered artefact and a gated weekly Managed Airflow graph.
- **Why here:** Streaming resource changes keeps every version of every resource, plus a current-version view, so the morning of discharge is rebuildable. A nightly extract never could. What lets any of it meet patient data is the covered-products list, not a launch stage.
- **Where it breaks:** The healthcare text service that mapped concepts to standard codes shut down on 27 May 2026, and the healthcare-tuned model a year before it. A general model is the remaining path, so the vocabulary mapping and its validation are now yours to build and defend.
- **What would move it up:** The outcome only reaches you as a claim from outside: the bill lands 45 to 90 days late, so a nightly list arrives after the window has shut.

Peers at the same price, with a different shape:

- **Managed Spark over the note plane** — FHIR bundles in Cloud Storage → Managed Spark de-identify + extract → BigQuery concepts → MLlib fit

#### Architecture Decision Record (ADR) Matrix

A scenario-aware evaluation of the ladder against this customer's constraints. Where an adjacent tier serves as a viable A/B benchmark or a Phase 2 evolution, that role is explicitly called out:

| Rung | Role in this Engagement | Architecture & Stance | Deciding Constraint & Trade-off |
| --- | --- | --- | --- |
| Tier 0 — Out of the Box | Ruled out (Insufficient) | Test the score they already own. | Below the floor (Tier 2 — Distributed & Custom ML), set by How many a week the team can actually take on, Where the number lands in someone else’s day, Can you rebuild the record as it stood that morning, Do you find out when they go somewhere else, Where the worry is written down: a box, or the notes, Who signs it off, and what have they turned down, How you will know a year from now that it worked, Graded on an outside ratio, from a source with no history. |
| Tier 1 — Serverless, In-Warehouse | **Adjacent Lower Tier (A/B Benchmark)** | Fit it to your own people, and say why it fired. Lower complexity and operational overhead. | Below the floor (Tier 2 — Distributed & Custom ML), set by How many a week the team can actually take on, Where the number lands in someone else’s day, Can you rebuild the record as it stood that morning, Do you find out when they go somewhere else, Where the worry is written down: a box, or the notes, Who signs it off, and what have they turned down, How you will know a year from now that it worked, Graded on an outside ratio, from a source with no history. Viable as an A/B comparator to quantify the performance/accuracy lift of Tier 2 — Distributed & Custom ML. |
| Tier 2 — Distributed & Custom ML | **Primary Baseline (MVP)** | Read the notes, freeze the clock, check every group. Fits all bounded constraints. | Selected target. Fits floor (Tier 2 — Distributed & Custom ML). Wins: Streaming resource changes keeps every version of every resource, plus a current-version view, so the morning of discharge is rebuildable. A nightly extract never could. What lets any of it meet patient data is the covered-products list, not a launch stage. |
| Tier 3 — Real-Time & Specialised | **Adjacent Higher Tier (Phase 2 Evolution)** | Act on the discharge message, not on the bill. Higher freshness, lower latency, or specialised modeling. | Inside the range, but nothing heard requires it yet. Step-up trigger: The outcome only reaches you as a claim from outside: the bill lands 45 to 90 days late, so a nightly list arrives after the window has shut. Propose as Phase 2 expansion once this condition is met. |

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

- Tier 0 — Out of the Box — Test the score they already own. Out: the floor is Tier 2 — Distributed & Custom ML — How many a week the team can actually take on, Where the number lands in someone else’s day, Can you rebuild the record as it stood that morning, Do you find out when they go somewhere else, Where the worry is written down: a box, or the notes, Who signs it off, and what have they turned down, How you will know a year from now that it worked, Graded on an outside ratio, from a source with no history.
- Tier 1 — Serverless, In-Warehouse — Fit it to your own people, and say why it fired. Out: the floor is Tier 2 — Distributed & Custom ML — How many a week the team can actually take on, Where the number lands in someone else’s day, Can you rebuild the record as it stood that morning, Do you find out when they go somewhere else, Where the worry is written down: a box, or the notes, Who signs it off, and what have they turned down, How you will know a year from now that it worked, Graded on an outside ratio, from a source with no history.

**Above it, and why that is theatre here.**

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

## 7. POC Data Discovery & Profiling Contract (Tier 2)

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
    "floor": 2,
    "ceiling": 2,
    "clash": false
  },
  "recommended_rung": 2,
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
        "key": "auto",
        "heard": "The outreach is a text message and a call centre, so thousands.",
        "means": "Capacity stops being the constraint and cost of contact takes over. This is the only shape where a wide, always-on list is defensible, and it is also where irritation becomes the harm.",
        "floor": 2,
        "ceiling": null
      }
    },
    {
      "id": "acts",
      "order": 3,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "named",
        "heard": "A nurse calls within two days and books the appointment before they leave.",
        "means": "A real follow-up with an owner and a deadline. Now the ranking can be built against it: who is reachable, who has nothing booked, who is on medicines that need reviewing.",
        "floor": 1,
        "ceiling": null
      }
    },
    {
      "id": "where",
      "order": 4,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "popup",
        "heard": "It has to appear in front of the doctor at the moment they discharge.",
        "means": "That is a live callout from the record system to a service you host and keep inside the response budget. Real, and supported by the major vendors — but you are now inside somebody’s hands-on-keyboard moment.",
        "floor": 2,
        "ceiling": null
      }
    },
    {
      "id": "cutoff",
      "order": 5,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "current",
        "heard": "The extract shows how things look today. There is no history in it.",
        "means": "Then there is no defensible training set yet, only a leaky one. Capture starts the clock the day it is turned on, so the first credible model is quarters away and should be said so now.",
        "floor": 2,
        "ceiling": null
      }
    },
    {
      "id": "coverage",
      "order": 6,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "exchange",
        "heard": "A regional exchange messages us whenever one of ours is admitted anywhere.",
        "means": "The only signal that arrives before the bill. It also drags in matching people across sources that never agreed on an identifier, which is usually the larger half of the work.",
        "floor": 2,
        "ceiling": null
      }
    },
    {
      "id": "signal",
      "order": 7,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "text",
        "heard": "The real signal is in the notes. Housing, whether anyone is at home for them.",
        "means": "The healthcare text service that used to map concepts to standard codes was switched off in May 2026 and the healthcare-tuned model the year before. A general model is the remaining path, and validating what it emits is yours.",
        "floor": 2,
        "ceiling": null
      }
    },
    {
      "id": "equity",
      "order": 8,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "committee",
        "heard": "There is a standing committee. They meet monthly and they have said no before.",
        "means": "Real governance, which is good news and a schedule constraint. Get a rejected submission: it tells you what they check, in their words, better than any policy document will.",
        "floor": 2,
        "ceiling": null
      }
    },
    {
      "id": "proof",
      "order": 9,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "staged",
        "heard": "We could switch it on one unit at a time and compare as we go.",
        "means": "The best answer anyone gives to this question. A staged rollout is free, it is normal practice for a change of this kind, and it turns an argument about what caused what into a comparison.",
        "floor": 2,
        "ceiling": null
      }
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
      "status": "open",
      "options": [
        "We measure it. It is somewhere north of ninety percent on most of them.",
        "We are strict about what fires. Only a handful, and people do read them.",
        "Nobody has ever put a number on that as far as I know."
      ]
    },
    {
      "id": "history",
      "order": 13,
      "status": "open",
      "options": [
        "The final billing code and the discharge summary. Three days to a fortnight.",
        "Almost everything gets touched at some point. Nobody has mapped it.",
        "The coding team would know that better than I would."
      ]
    },
    {
      "id": "blind",
      "order": 14,
      "status": "not_in_play",
      "gate": "Returns to other providers are invisible in your own data",
      "closed_by": {
        "question": "coverage",
        "answer": "exchange"
      }
    },
    {
      "id": "feed",
      "order": 15,
      "status": "open",
      "options": [
        "Nearly all of them. The exchange has been at this for years.",
        "Maybe half. The big ones send, the smaller places are a mixture.",
        "We keep being told it is coming. Nothing arrives today.",
        "Interfaces owns that. I could not tell you the coverage."
      ]
    },
    {
      "id": "lag",
      "order": 16,
      "status": "not_in_play",
      "gate": "The outcome only shows up on a bill that lands months later",
      "closed_by": {
        "question": "coverage",
        "answer": "exchange"
      }
    },
    {
      "id": "notes",
      "order": 17,
      "status": "open",
      "options": [
        "Most of it. People pull the last note forward and edit a line.",
        "The nursing notes are genuinely written fresh each shift.",
        "I could not say. It probably varies by service."
      ]
    },
    {
      "id": "missing",
      "order": 18,
      "status": "not_in_play",
      "gate": "The fields carrying social context are mostly blank",
      "closed_by": {
        "question": "signal",
        "answer": "text"
      }
    },
    {
      "id": "strata",
      "order": 19,
      "status": "open",
      "options": [
        "Just make sure the list is not systematically missing certain patients.",
        "A score of forty percent has to mean forty percent for every one of them.",
        "Some of the groups they care about have very few patients a year.",
        "They will tell us when they see it, I expect."
      ]
    },
    {
      "id": "stepped",
      "order": 20,
      "status": "open",
      "options": [
        "Several thousand a month across the system.",
        "A few hundred a month, and we would be happy with a couple of points.",
        "I know the annual figure. I have not thought about it that way."
      ]
    }
  ],
  "conflicts": [
    "Graded on an outside ratio, from a source with no history. You can neither train without leaking nor reproduce the number you are judged on. The first deliverable is change capture, and the ratio cannot be the success measure — its window shuts long before the payment year."
  ],
  "still_to_ask": [
    "coding",
    "peer",
    "fatigue",
    "history",
    "feed",
    "notes",
    "strata",
    "stepped"
  ],
  "counts": {
    "answered": 9,
    "stale": 0,
    "open": 8,
    "not_in_play": 3,
    "dropped": 0
  },
  "schema_version": "1.0",
  "problem_id": "clinical-risk",
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
