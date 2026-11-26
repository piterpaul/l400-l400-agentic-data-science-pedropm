---
schema_version: "1.0"
problem_id: "clinical-risk"
target_tier: 1
recommended_rung: 1
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

- **Floor: Tier 1 — Serverless, In-Warehouse** — set by Which number are you graded on, and who works it out, How many a week the team can actually take on, What actually happens to someone the list flags, Where the number lands in someone else’s day, Can you rebuild the record as it stood that morning, Do you find out when they go somewhere else, Where the worry is written down: a box, or the notes, Who signs it off, and what have they turned down, How you will know a year from now that it worked
- **Ceiling:** nothing heard yet rules out the top of the ladder

## 3. What was asked, and what it steered

### 1. Which number are you graded on, and who works it out

**Asked:** Which number are you judged on at the end of the year, and who works that number out — you, or somebody outside?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** We carry the cost ourselves. Every one of these is money straight out.
- **Which means:** The customer is at risk, so a return is a direct loss rather than a retrospective fine. The arithmetic is simple, the feedback is fast, and the follow-up can be priced against it honestly.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** At risk for the cost. Every avoided return has a dollar value the sponsor already knows.
- **Why it was asked:** Whether the target belongs to this customer or to a third party. A penalty ratio computed elsewhere fixes the label definition, the comparison group and how long you wait to see any effect, and none of the three are yours to change.
- **What it forecloses:** The contract question, the penalty arithmetic, and every argument about what the model should optimise. If somebody outside computes the number, no model metric is the business case.

### 2. How many a week the team can actually take on

**Asked:** How many people a week can the team that does the following up actually take on — not the target, what they managed last week?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Forty or so a week across the two campuses.
- **Which means:** Now ordering earns its keep: forty out of several hundred eligible is a real selection. Report performance at exactly forty, and never as a single overall figure.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Forty a week. Evaluate at the top forty and publish nothing averaged over everybody.
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

- **Heard:** It goes on the round list the care team works through each morning.
- **Which means:** The cheapest and most durable option. It reaches the people whose job is the list, it cannot be dismissed by someone doing something else, and it needs no callout service.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Delivered to a worked list. No interruption, no in-record service, batch is sufficient.
- **Why it was asked:** The worklist. A number on a list somebody works through is a different build from a number that interrupts a clinician signing an order, and the second has a measured dismissal rate before you write a line.
- **What it forecloses:** The alert design questions and most of the integration scope. A list is a table. An interruption is a service inside the record system with a response budget and a change-control process.

### 5. Can you rebuild the record as it stood that morning

**Asked:** Can you rebuild what was written about someone exactly as it looked the morning they went home, or do you only have how it looks now?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Every change is kept with a timestamp. We can rewind it.
- **Which means:** Rare and valuable. Say so — it means the hardest and least visible part of this build is already paid for, and the first honest model can be fitted this quarter.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Change history available. Cut every feature at the decision timestamp from day one.
- **Why it was asked:** Whether point-in-time reconstruction is the project. Much of a record is finished by coders three to ten days later, and a model trained on those fields but run at the bedside is the standard failure in this field.
- **What it forecloses:** The entire leakage group and the feature-storage argument. If the extract is current-state only, nothing downstream is trustworthy and building the history comes first.

### 6. Do you find out when they go somewhere else

**Asked:** If the same person turns up somewhere else instead of coming back to you, do you ever find out?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** We see it on the bill, forty-five to ninety days later.
- **Which means:** Complete and useless for acting. It is an excellent training label and a hopeless trigger, and confusing the two is how a plan builds a beautiful retrospective report.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Billing only. Good enough to train on, far too late to act on.
- **Why it was asked:** Whether the label is complete. A single provider misses roughly a fifth to a quarter of returns because the person went down the road, and every one of those is trained on as though nothing happened.
- **What it forecloses:** The out-of-network questions, the identity-matching scope, and the argument about whether the unit is a visit or a person-month.

### 7. Where the worry is written down: a box, or the notes

**Asked:** The things that make your staff worry about someone going home — are those written in a box somewhere, or only in what people typed?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** It is mostly in the numbers. Results, observations, how long they stayed.
- **Which means:** Then the coded build is the whole build, which is good news for cost and for the review. Set expectations at the documented plateau and spend the effort on delivery instead.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Coded fields sufficient. No text in scope; expect the documented plateau and plan around it.
- **Why it was asked:** Whether free text is in scope, which is the largest single fork in this build. Text brings the housing, transport and caregiver context that the coded record simply does not carry, and it brings a governance review with it.
- **What it forecloses:** The whole modelling-approach argument. Coded fields alone plateau in a narrow band that is well documented, and no amount of tuning moves it.

### 8. Who signs it off, and what have they turned down

**Asked:** Who has to approve this before anyone sees it, how often do they meet, and can they show you something they turned down?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** Our informatics team reviews it and then it goes live.
- **Which means:** Faster and lighter, and the review will be technical rather than about who the model serves worse. Somebody should still ask the second question, and it may have to be you.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Technical review only. Raise group-by-group performance yourself; nobody else will.
- **Why it was asked:** The release process and the artefacts. It also sets the schedule: a committee that meets quarterly puts a hard floor under how fast anything ships, and no ladder rung shortens it.
- **What it forecloses:** Most of the governance group and the whole timeline argument. A previously accepted submission is worth more than any template, and asking for one is how you find out whether the process is real.

### 9. How you will know a year from now that it worked

**Asked:** A year from now, how will you know this worked — and what would convince somebody who thinks it did not?

*Keystone — this one opens or closes branches of everything below.*

- **Heard:** The rate on the monthly board should come down.
- **Which means:** It will move for reasons that have nothing to do with you. Worth tracking, worthless as proof, and the honest version needs a comparison group of some sort even a weak one.
- **Bounds:** not below Tier 1 — Serverless, In-Warehouse
- **For the brief:** Raw rate as endpoint. Insufficient alone; pair it with some form of comparison group.
- **Why it was asked:** Whether an effect will be measurable at all. The graded number is the worst available answer: its window is three years wide and closes fifteen months before the payment year it lands in.
- **What it forecloses:** The success-criteria conversation, which otherwise reappears at the end of the engagement when nothing can be done about it.

## 4. Still worth asking

**These are instructions, not blanks.** Ask each one. The possible answers below are authored, with what each would rule in or out, so a reply can be recognised rather than interpreted.

### 16. How long until the record for a month is stable

**Ask:** If you look at last month today, how much will that month still change over the next three months?

**Why it matters:** How old a training window has to be before it is honest, and how long anyone waits to learn whether a change worked. A month that is still filling in reads as a good month.

What the answers would mean:

- **We hold the month open for ninety days. After that it barely moves.** → Then the rule is simple and enforceable: train only on months past the settling point, and mark every recent month on every chart as provisional so nobody celebrates a filling gap. *(floor Tier 1 — Serverless, In-Warehouse)*
- **It keeps trickling in. Nobody has worked out when it stops.** → A day of work to measure and it prevents the most common false alarm in this whole domain. Plot the same month re-counted each week until the line flattens. *(floor Tier 1 — Serverless, In-Warehouse)*
- **The finance team corrects things later. I do not know the pattern.** → Ask them for the history of corrections. It is the same question they answer for their own close, so the analysis usually already exists in a different format.

## 5. Not worth asking yet

Each of these is gated behind a branch that is not open. They are listed so the absence is legible: they were not forgotten, they were ruled out.

- **How complete is the coding the adjustment runs on** — closed by *Which number are you graded on, and who works it out* → “We carry the cost ourselves. Every one of these is money straight out”.
- **Do you know who you are actually being compared against** — closed by *Which number are you graded on, and who works it out* → “We carry the cost ourselves. Every one of these is money straight out”.
- **What share of the current pop-ups get dismissed** — closed by *Where the number lands in someone else’s day* → “It goes on the round list the care team works through each morning”.
- **Which fields settle after the person goes home** — closed by *Can you rebuild the record as it stood that morning* → “Every change is kept with a timestamp. We can rewind it”.
- **How far do people travel for their care here** — closed by *Do you find out when they go somewhere else* → “We see it on the bill, forty-five to ninety days later”.
- **How many sources send, and how would you notice a gap** — closed by *Do you find out when they go somewhere else* → “We see it on the bill, forty-five to ninety days later”.
- **How much of a note is copied from the last one** — closed by *Where the worry is written down: a box, or the notes* → “It is mostly in the numbers. Results, observations, how long they stayed”.
- **Does the blankness track any group you must report on** — closed by *Where the worry is written down: a box, or the notes* → “It is mostly in the numbers. Results, observations, how long they stayed”.
- **Which groups, and do they want ranking or meaning** — closed by *Who signs it off, and what have they turned down* → “Our informatics team reviews it and then it goes live”.
- **Is there enough volume to see the size of effect you expect** — closed by *How you will know a year from now that it worked* → “The rate on the monthly board should come down”.

## 6. What is being suggested, and why the alternatives are out

### Tier 1 — Serverless, In-Warehouse

Fit it to your own people, and say why it fired

- **What it is:** Cloud Healthcare API repository → BigQuery under VPC Service Controls, CMEK → Dataform mart → BigQuery ML boosted tree
- **Google Cloud & open-weight options at this rung:** Cloud Healthcare API, BigQuery ML, AI.PREDICT, Dataform, Data Engineering Agent, VPC Service Controls
- **What it carries:** Build carried from Tier 0, still SQL in BigQuery. What changed is the surface: Tier 0 scored nothing fitted, this rung trains and scores nightly.
- **Why here:** Fits this case mix and this coding practice, which no vendor model does. ML.EXPLAIN_PREDICT hands the clinician three reasons to open the conversation with, and nothing leaves the perimeter.
- **Where it breaks:** Coded fields only, so it stalls around 0.70 to 0.72 and never sees housing or transport. The Data Engineering Agent will happily join the final billing code, which settles days after the patient left. Read every join it writes.
- **What would move it up:** The committee asks how it behaves for each group, or the coded-only model has stalled and the only signal left is in what people typed.

#### Architecture Decision Record (ADR) Matrix

A scenario-aware evaluation of the ladder against this customer's constraints. Where an adjacent tier serves as a viable A/B benchmark or a Phase 2 evolution, that role is explicitly called out:

| Rung | Role in this Engagement | Architecture & Stance | Deciding Constraint & Trade-off |
| --- | --- | --- | --- |
| Tier 0 — Out of the Box | **Adjacent Lower Tier (A/B Benchmark)** | Test the score they already own. Lower complexity and operational overhead. | Below the floor (Tier 1 — Serverless, In-Warehouse), set by Which number are you graded on, and who works it out, How many a week the team can actually take on, What actually happens to someone the list flags, Where the number lands in someone else’s day, Can you rebuild the record as it stood that morning, Do you find out when they go somewhere else, Where the worry is written down: a box, or the notes, Who signs it off, and what have they turned down, How you will know a year from now that it worked. Viable as an A/B comparator to quantify the performance/accuracy lift of Tier 1 — Serverless, In-Warehouse. |
| Tier 1 — Serverless, In-Warehouse | **Primary Baseline (MVP)** | Fit it to your own people, and say why it fired. Fits all bounded constraints. | Selected target. Fits floor (Tier 1 — Serverless, In-Warehouse). Wins: Fits this case mix and this coding practice, which no vendor model does. ML.EXPLAIN_PREDICT hands the clinician three reasons to open the conversation with, and nothing leaves the perimeter. |
| Tier 2 — Distributed & Custom ML | **Adjacent Higher Tier (Phase 2 Evolution)** | Read the notes, freeze the clock, check every group. Higher freshness, lower latency, or specialised modeling. | Inside the range, but nothing heard requires it yet. Step-up trigger: The committee asks how it behaves for each group, or the coded-only model has stalled and the only signal left is in what people typed. Propose as Phase 2 expansion once this condition is met. |
| Tier 3 — Real-Time & Specialised | In range, not required | Act on the discharge message, not on the bill. | Not ruled out, but nothing heard in the room requires it. |

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

- Tier 0 — Out of the Box — Test the score they already own. Out: the floor is Tier 1 — Serverless, In-Warehouse — Which number are you graded on, and who works it out, How many a week the team can actually take on, What actually happens to someone the list flags, Where the number lands in someone else’s day, Can you rebuild the record as it stood that morning, Do you find out when they go somewhere else, Where the worry is written down: a box, or the notes, Who signs it off, and what have they turned down, How you will know a year from now that it worked.

**Above it, and why that is theatre here.**

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

## 7. POC Data Discovery & Profiling Contract (Tier 1)

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
    "floor": 1,
    "ceiling": 1,
    "clash": false
  },
  "recommended_rung": 1,
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
        "key": "cost",
        "heard": "We carry the cost ourselves. Every one of these is money straight out.",
        "means": "The customer is at risk, so a return is a direct loss rather than a retrospective fine. The arithmetic is simple, the feedback is fast, and the follow-up can be priced against it honestly.",
        "floor": 1,
        "ceiling": null
      }
    },
    {
      "id": "capacity",
      "order": 2,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "dozens",
        "heard": "Forty or so a week across the two campuses.",
        "means": "Now ordering earns its keep: forty out of several hundred eligible is a real selection. Report performance at exactly forty, and never as a single overall figure.",
        "floor": 1,
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
        "key": "worklist",
        "heard": "It goes on the round list the care team works through each morning.",
        "means": "The cheapest and most durable option. It reaches the people whose job is the list, it cannot be dismissed by someone doing something else, and it needs no callout service.",
        "floor": 1,
        "ceiling": null
      }
    },
    {
      "id": "cutoff",
      "order": 5,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "asof",
        "heard": "Every change is kept with a timestamp. We can rewind it.",
        "means": "Rare and valuable. Say so — it means the hardest and least visible part of this build is already paid for, and the first honest model can be fitted this quarter.",
        "floor": 1,
        "ceiling": null
      }
    },
    {
      "id": "coverage",
      "order": 6,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "bills",
        "heard": "We see it on the bill, forty-five to ninety days later.",
        "means": "Complete and useless for acting. It is an excellent training label and a hopeless trigger, and confusing the two is how a plan builds a beautiful retrospective report.",
        "floor": 1,
        "ceiling": null
      }
    },
    {
      "id": "signal",
      "order": 7,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "fields",
        "heard": "It is mostly in the numbers. Results, observations, how long they stayed.",
        "means": "Then the coded build is the whole build, which is good news for cost and for the review. Set expectations at the documented plateau and spend the effort on delivery instead.",
        "floor": 1,
        "ceiling": null
      }
    },
    {
      "id": "equity",
      "order": 8,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "informatics",
        "heard": "Our informatics team reviews it and then it goes live.",
        "means": "Faster and lighter, and the review will be technical rather than about who the model serves worse. Somebody should still ask the second question, and it may have to be you.",
        "floor": 1,
        "ceiling": null
      }
    },
    {
      "id": "proof",
      "order": 9,
      "status": "answered",
      "keystone": true,
      "answer": {
        "key": "rate",
        "heard": "The rate on the monthly board should come down.",
        "means": "It will move for reasons that have nothing to do with you. Worth tracking, worthless as proof, and the honest version needs a comparison group of some sort even a weak one.",
        "floor": 1,
        "ceiling": null
      }
    },
    {
      "id": "coding",
      "order": 10,
      "status": "not_in_play",
      "gate": "The number is adjusted using codes your own staff enter",
      "closed_by": {
        "question": "scored",
        "answer": "cost"
      }
    },
    {
      "id": "peer",
      "order": 11,
      "status": "not_in_play",
      "gate": "You are compared against other providers, not a fixed target",
      "closed_by": {
        "question": "scored",
        "answer": "cost"
      }
    },
    {
      "id": "fatigue",
      "order": 12,
      "status": "not_in_play",
      "gate": "The number will interrupt someone in the middle of a task",
      "closed_by": {
        "question": "where",
        "answer": "worklist"
      }
    },
    {
      "id": "history",
      "order": 13,
      "status": "not_in_play",
      "gate": "The record cannot be rebuilt as it stood when the call was made",
      "closed_by": {
        "question": "cutoff",
        "answer": "asof"
      }
    },
    {
      "id": "blind",
      "order": 14,
      "status": "not_in_play",
      "gate": "Returns to other providers are invisible in your own data",
      "closed_by": {
        "question": "coverage",
        "answer": "bills"
      }
    },
    {
      "id": "feed",
      "order": 15,
      "status": "not_in_play",
      "gate": "An outside notification feed is the only near-real-time signal",
      "closed_by": {
        "question": "coverage",
        "answer": "bills"
      }
    },
    {
      "id": "lag",
      "order": 16,
      "status": "open",
      "options": [
        "We hold the month open for ninety days. After that it barely moves.",
        "It keeps trickling in. Nobody has worked out when it stops.",
        "The finance team corrects things later. I do not know the pattern."
      ]
    },
    {
      "id": "notes",
      "order": 17,
      "status": "not_in_play",
      "gate": "The signal everyone points to is in free text, not a coded field",
      "closed_by": {
        "question": "signal",
        "answer": "fields"
      }
    },
    {
      "id": "missing",
      "order": 18,
      "status": "not_in_play",
      "gate": "The fields carrying social context are mostly blank",
      "closed_by": {
        "question": "signal",
        "answer": "fields"
      }
    },
    {
      "id": "strata",
      "order": 19,
      "status": "not_in_play",
      "gate": "A standing committee must approve the model before go-live",
      "closed_by": {
        "question": "equity",
        "answer": "informatics"
      }
    },
    {
      "id": "stepped",
      "order": 20,
      "status": "not_in_play",
      "gate": "The rollout can be staged rather than switched on everywhere",
      "closed_by": {
        "question": "proof",
        "answer": "rate"
      }
    }
  ],
  "conflicts": [],
  "still_to_ask": [
    "lag"
  ],
  "counts": {
    "answered": 9,
    "stale": 0,
    "open": 1,
    "not_in_play": 10,
    "dropped": 0
  },
  "schema_version": "1.0",
  "problem_id": "clinical-risk",
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
