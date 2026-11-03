# Smart Energy Planner — Research Paper Blueprint

**Author:** Ilias Moulouki · Computer Science, Artificial Intelligence specialization · Al Akhawayn University  
**Working version:** 3 November 2026  
**Purpose:** A paper-shaped working document linking completed experiments to the remaining research. This is not a finished manuscript or a verified literature review.

## How to use this document

Keep the section structure when drafting the paper. Replace bracketed fields with verified information. Keep planning notes in this working copy; remove them from the submitted manuscript. Never turn a planned experiment into a past-tense claim before it has been run and checked.

Status labels: **Completed** = reported working implementation/results; **Pilot** = exploratory results; **Pending** = not yet completed or result not supplied; **Planned** = proposed remaining work. Completion here is based on the outputs shared in our conversation, not a fresh audit of the current notebook.

## Project scope and current position

**Working paper title:** Evaluating Variational Quantum Demand Forecasting and QAOA Battery Scheduling in a Small Simulated Solar–Battery Microgrid

**Plain-language purpose:** Predict how much electricity will be needed, decide when a battery should charge or discharge, and measure whether the resulting decisions reduce electricity costs while respecting battery limits.

**Core workflow:** Historical demand → classical/VQC forecasts → classical/QAOA scheduling → simulated operation using realized demand → cost and feasibility evaluation.

The quantum forecasting circuit and QAOA are different algorithms serving different jobs. The forecast estimates future demand. The scheduler chooses battery actions. A lower prediction error does not automatically establish lower operating cost.

| Component | Current status | Remaining requirement |
|---|---|---|
| Demand cleaning and hourly aggregation | Completed | Audit exact counts, units, and time alignment |
| Chronological splits and four input features | Completed | Confirm forecasting information available at each origin |
| Classical baseline models | Completed | Preserve corrected results and trained models |
| One-block and two-block VQC prototypes | Pilot | Repeat under corrected preprocessing |
| Five-seed corrected MLP and Random Forest | Completed | Save per-run metrics, predictions, settings, and warnings |
| Corrected two-block VQC seed 42 | Completed in uploaded notebook | MAE 0.4149 kW; iteration limit reached |
| Remaining corrected VQC runs | Pending | Complete fixed protocol without open-ended tuning |
| Solar–battery simulator and exact scheduler | Planned | Implement and verify before QAOA |
| QAOA scheduling | Planned | Compare against identical discrete classical problem |
| Forecast-to-operation experiments | Planned | Run matched scenarios and realized-demand evaluation |
| Final test evaluation | Reserved | Run only after methodological choices are fixed |
| Manuscript and defense | In progress | Use this structure to write alongside experiments |

**Core scope for the remaining month:** one household demand dataset; fixed solar and battery sizes; grid-connected operation; short scheduling horizons; simulated quantum circuits; transparent cost and feasibility comparisons.

**Outside the core scope:** wind generation, capacity sizing, flexible-load scheduling, multiple sites, hardware quantum advantage, and a new forecasting architecture search. Add these only as future work unless the core study is finished.

---

# Paper front matter

**Title:** [Finalize after the operational experiments.]  
**Author and affiliation:** Ilias Moulouki, Al Akhawayn University, [department details].  
**Supervisor:** [Confirm official name and title.]  
**Keywords:** variational quantum circuits; demand forecasting; QAOA; battery scheduling; microgrid; decision quality.

## Abstract — write last

**Status: Planned final synthesis.** Target approximately 150–250 words, subject to university requirements.

Use this structure:

> Electricity demand forecasting and battery scheduling are coupled tasks in renewable-energy management. This study evaluates [precise scope] using classical forecasting models and a four-qubit variational quantum regressor, followed by classical and QAOA scheduling methods. Demand data from [verified dataset citation and dates] are divided chronologically into training, validation, and test periods. Forecasting is evaluated using [metrics], while scheduling is evaluated using [cost, feasibility, and other retained metrics]. Experiments on [number and type of scenarios] show [verified principal results with units]. The findings indicate [supported interpretation], subject to [main limitations].

Do not insert the pilot validation MAEs as final test results. Do not describe a speedup or quantum advantage unless the evaluation actually supports it.

# 1. Introduction

## 1.1 Problem and motivation

Explain the operational problem: solar supply and household demand vary over time; a battery shifts energy between hours; charging now affects what is available later. Forecasting therefore supports decisions with intertemporal consequences. Support field-level claims with verified sources.

**Draft starting paragraph:**

> This study examines a small grid-connected solar–battery system in which demand forecasts inform battery scheduling. The objective is to evaluate both prediction accuracy and the quality of the resulting operating decisions. Classical forecasting and scheduling methods provide reference solutions against which variational quantum forecasting and QAOA scheduling are assessed.

## 1.2 Research questions

1. **RQ1 — Forecasting:** How does a small VQC compare with persistence, linear regression, Random Forest, and a small neural network under matched data conditions?
2. **RQ2 — Scheduling:** How closely does QAOA approximate the exact solution of the same small discrete battery-scheduling problem, and how often are its sampled schedules feasible?
3. **RQ3 — Decision quality:** How do classical and VQC forecasts affect realized operating cost when supplied to the same scheduler?

## 1.3 Intended contribution

Frame these as intended contributions until the corresponding work is complete:

- A reproducible, limited-data comparison of classical and VQC household demand forecasting.
- A verified small battery-scheduling formulation with exact and QAOA solutions.
- An evaluation separating the effect of forecasting from the effect of optimization on realized operating outcomes.

**Novelty boundary:** Combining VQC and QAOA is not, by itself, an established novel contribution. The related-work review must determine whether the precise formulation, experimental comparison, or operational analysis adds something not already demonstrated.

## 1.4 Paper organization

Briefly introduce the sections below after the final structure is fixed.

# 2. Related Work

**Status: Literature work was discussed earlier; a verified, focused synthesis is still needed for the final manuscript. This blueprint does not validate earlier references.**

## 2.1 Classical short-term demand forecasting

Cover persistence, linear models, tree ensembles, and small neural networks. Explain why these are meaningful baselines rather than claiming they exhaust the field.

## 2.2 Variational quantum regression

Cover feature encoding, trainable gates, readout, classical optimization, simulator versus hardware experiments, and evidence on comparisons with classical models.

## 2.3 Quantum optimization for energy scheduling

Cover QAOA, binary decision encoding, constraint penalties, qubit requirements, feasibility, and comparison with exact/classical optimization.

## 2.4 Forecast accuracy versus operational value

Review work evaluating downstream decisions rather than only prediction metrics. Explain why two forecasts with similar MAE can produce different battery decisions.

## 2.5 Literature matrix and gap

| Verified citation | Task/data | Forecast model | Scheduler | Classical reference | Operational metrics | Limitation relevant to this study |
|---|---|---|---|---|---|---|
| [Source 1] | [Fill] | [Fill] | [Fill] | [Fill] | [Fill] | [Fill] |
| [Source 2] | [Fill] | [Fill] | [Fill] | [Fill] | [Fill] | [Fill] |
| [Source 3] | [Fill] | [Fill] | [Fill] | [Fill] | [Fill] | [Fill] |

For every citation, verify title, authors, year, DOI/URL, and the claim supported. Draft the gap only after completing the matrix. Avoid unsupported statements that no previous study has connected forecasting and quantum scheduling.

# 3. Data and Forecasting Methodology

## 3.1 Dataset and scope

**Completed:** Individual Household Electric Power Consumption dataset, obtained through UCI tooling; household active power is the demand target. Insert the verified dataset citation and licensing details before submission.

Describe the household setting and observation dates. Household demand is not a complete measured microgrid dataset: solar generation, battery specifications, and tariffs used later must have their own provenance or be explicitly labeled scenario assumptions.

## 3.2 Cleaning and hourly aggregation

- Combine date and time into a timestamp.
- Convert active-power observations to numeric values.
- Compute hourly mean power and observation count.
- Retain an hourly target only when the hour contains all 60 minute observations.
- Preserve missing hourly positions before constructing lag features.

| Reported data check | Value |
|---|---:|
| Total hourly bins | 34,589 |
| Complete hourly bins | 34,085 |
| Incomplete hourly bins | 504 |
| Duplicate timestamps reported | 0 |

The earlier reported missing-minute proportion was approximately 1.25%; verify its exact denominator in the final notebook. Explain that an hour labeled 18:00 represents the interval starting at 18:00 under the implemented aggregation.

**Units:** mean demand is in kW. For a one-hour interval, energy in kWh equals mean kW multiplied by one hour. Keep power and stored energy distinct in the scheduling model.

## 3.3 Features and forecast timing

| Input | Meaning at target hour t |
|---|---|
| Previous-hour demand | Observed demand at t−1 |
| Previous-day demand | Observed demand at t−24 |
| Hour sine | sin(2π × hour/24) |
| Hour cosine | cos(2π × hour/24) |

Create lags on the regular hourly grid before removing incomplete examples. The current forecasting experiment is a one-hour-ahead task. A multi-hour scheduling forecast must use information available at its issue time; later previous-hour inputs must use recursive predictions or another explicitly implemented multi-step approach, not future actual demand.

## 3.4 Chronological splits and limited-data protocol

| Partition | Period | Current four-input count/use |
|---|---|---|
| Training pool | 2007–2008 | 17,341 usable examples |
| Selected training sample | Within training pool | 500 fixed rows: 256 from 2007, 244 from 2008 |
| Validation | 2009 | 8,602 usable examples |
| Test | Available 2010 observations through the dataset endpoint in November | Reserved; audit exact eligible endpoints, count, and monthly coverage |

Earlier counts from the one-input experiment differ and must not be mixed with the four-input counts. Sampling uses a fixed selection; the five model seeds vary model randomness, not the sample.

## 3.5 Corrected preprocessing

**Completed:** StandardScaler fitted on exactly 500 selected training examples. Apply this fitted scaler to validation inputs; use arctangent of standardized values as quantum input angles. Trees and linear regression currently use raw inputs.

**Pilot distinction:** the original scaler used the full training pool. This did not use validation/test data, but it does not meet the strict 500-example preprocessing protocol. Keep those earlier results separately labeled as pilots.

## 3.6 Classical models

| Model | Implemented configuration |
|---|---|
| Persistence | Predict previous-hour demand |
| Linear regression | Four raw inputs; ordinary linear regression |
| Random Forest | 100 trees; maximum depth 10; minimum leaf size 5 |
| MLP | Hidden layers (16, 8); ReLU; Adam; maximum 500 iterations |

Random Forest and MLP seeds: 42, 7, 21, 123, 2026. Record package versions and all remaining defaults with saved model settings. A 500-iteration MLP budget and a 50-iteration VQC budget are model-specific settings, not equal computational effort.

## 3.7 Variational quantum regressor

**Implemented on a statevector simulator:** four qubits; one Ry feature-encoding rotation per input; trainable Ry rotations; CNOT chain 0→1→2→3; last-qubit Z expectation as readout.

Prediction: demand_hat = a × expectation(Z on qubit 3) + b.

| Architecture | Trainable circuit angles | Readout parameters | Total parameters |
|---|---:|---:|---:|
| One block | 4 | Scale and bias | 6 |
| Two blocks | 8 | Scale and bias | 10 |

The two-block model repeats both trainable rotations and the CNOT chain. Train using MSE and L-BFGS-B with numerical gradients. Initial circuit angles are uniform in [−0.5, 0.5]; initial scale = 2 and bias = 1. The current budget is 50 optimizer iterations per run. Record termination message, iteration count, objective evaluations, and elapsed training time.

The one-block circuit contains adjacent same-axis input and weight rotations, which can combine into a single rotation. Describe it accurately as a simple reference architecture. Do not claim that entanglement or depth caused an improvement without a controlled experiment addressing that claim.

**Figure placeholder:** labeled circuit diagram showing encoding, trainable blocks, entangling gates, and readout.

# 4. Microgrid and Battery-Scheduling Methodology

**Status: Planned. No operational or QAOA results are available yet.**

## 4.1 Scenario specification

Begin with a four-hour worked example, then evaluate multiple documented windows. Fix parameters before comparing methods.

| Quantity | Value to define | Unit/provenance |
|---|---|---|
| Time step | 1 hour | h |
| Horizon | Initially 4 slots | Hours; later use only tractable sizes |
| Battery capacity and bounds | [Choose] | kWh; documented assumption |
| Initial stored energy | [Choose] | kWh |
| Maximum charge/discharge power | [Choose] | kW |
| Charge/discharge efficiency | [Choose] | Dimensionless |
| Solar generation | [Source or scenario profile] | kW; measured versus synthetic stated |
| Import tariff | [Profile] | Currency/kWh; source or scenario assumption |
| Export policy | [Disabled or modeled] | State explicitly |
| Terminal stored-energy rule | [Fix or value consistently] | Prevent artificial savings by emptying battery |

Use realistic but modest assumptions that can be explained and verified. Do not label synthetic solar or tariff profiles as measured data.

## 4.2 Physical equations and objective

Proposed continuous description, to be discretized consistently:

- Energy balance: grid_import_t + solar_used_t + discharge_t = demand_t + charge_t.
- Battery update: E_(t+1) = E_t + efficiency_charge × charge_t × Δt − discharge_t × Δt / efficiency_discharge.
- Enforce battery energy bounds, charge/discharge limits, nonnegative imports, and no simultaneous charging and discharging.
- Solar use plus curtailment equals available solar.
- Cost: sum of tariff_t × grid_import_t × Δt, plus any explicitly modeled battery-throughput cost.

These equations assume no export and grid import sufficient to meet demand. If import limits or unserved demand are introduced, add the corresponding variables and penalties explicitly. Do not report reliability improvements when unlimited grid supply makes unserved energy identically zero.

## 4.3 Exact classical reference — implement first

Define a small discrete battery action set. Enumerate all candidate schedules, reject infeasible trajectories, calculate the objective for each feasible schedule, and retain the minimum-cost one. This establishes the optimum for that exact discrete problem, not for a different continuous problem.

Verification cases: zero battery activity; zero solar; battery at its bounds; flat prices; expensive versus cheap hours; terminal-energy enforcement; manual energy-balance calculation for one schedule.

**Completion gate:** no QAOA implementation until schedule decoding and physical feasibility have been checked against this reference.

## 4.4 QAOA formulation

Specify the binary encoding of actions/states, objective coefficients, constraint encoding, penalty weights, cost Hamiltonian, mixer, initialization, circuit depth p, optimizer, and measurement settings. Count every decision and auxiliary qubit before simulation.

Keep the first implementation small enough for statevector simulation; reduce horizon or action resolution if necessary. Do not imply that a four-hour horizon automatically implies four qubits.

Check every bitstring for the initial small instances: encoded energy should match the intended objective plus penalties; low-energy solutions should decode consistently; feasible ground states should agree with the exact reference. Report penalty tuning and decoding/postprocessing rules.

Report raw feasible-sample probability and the cost of the chosen feasible schedule separately. Never count an infeasible low-penalty sample as a valid operating solution. If repair or fallback is used, describe it and report its frequency.

## 4.5 Additional classical comparator

Simulated annealing is optional if time permits. Exact enumeration of the identical discrete problem is the required core reference. Avoid adding comparison methods before the core pipeline works.

# 5. Experimental Design

## 5.1 Forecasting experiments

Complete the predefined five-seed comparison under corrected preprocessing. Use MAE as the main validation metric; report mean and sample standard deviation across seeds, individual runs, and training termination. Keep fixed data rows and preprocessing across runs. Finish the one-block comparison only within the agreed scope; if omitted, keep it explicitly a pilot result rather than silently implying a final comparison.

## 5.2 Optimization experiments

Use identical forecasts, solar profiles, tariffs, battery initial states, constraints, and action discretization when comparing exact optimization with QAOA. Evaluate multiple windows chosen by a documented rule, not selected because quantum methods perform well.

## 5.3 Forecast-to-decision comparison

| Forecast input | Exact discrete scheduler | QAOA scheduler |
|---|---|---|
| Perfect future demand | Reference benchmark | Isolates optimization behavior |
| Persistence forecast | Simple forecasting reference | Optional additional baseline |
| Selected classical forecast | Main classical pipeline | Isolates scheduler substitution |
| VQC forecast | Isolates forecast substitution | Combined quantum-method pipeline |

Use validation data to choose the classical model and operational settings. Predefine how forecasting seeds are used in operational experiments; report all retained runs or choose a representative seed by a documented rule. Do not select a seed based on final test performance.

At each forecast origin, generate the full horizon without future actual inputs. Specify whether schedules are executed open-loop or by receding horizon. For a receding-horizon design, execute the first action, update state using realized operation, and replan at the next hour. Define grid balancing, curtailment, and any action adjustment under forecast errors before evaluation. The perfect-information reference must use compatible constraints and horizon rules.

## 5.4 Metrics

| Metric | Purpose | Reporting rule |
|---|---|---|
| Forecast MAE, kW | Average absolute prediction error | Same timestamps for every model |
| Training MSE, kW² | Optimization progress | Do not compare directly with MAE |
| Realized import cost | Practical decision quality | Evaluate using actual demand and executed actions |
| Exact-solution cost gap | QAOA solution quality | Same forecast and discrete problem |
| Feasibility rate | Constraint satisfaction | Explain sampled/evaluated denominator |
| Curtailment, kWh | Unused solar energy | Only if modeled |
| Peak grid import, kW | Peak dependence on grid | Same evaluation intervals |
| Battery throughput, kWh | Amount of cycling | Do not equate with lifetime without a degradation model |
| Runtime | Computational burden | State hardware, simulator, and timed boundaries |

If an optimum cost is zero, percentage gap is undefined; use an absolute gap. A simulator runtime comparison does not establish a hardware quantum speedup. Across-seed standard deviation is not a confidence interval or uncertainty across households.

## 5.5 Reproducibility

Record dataset citation, code version, package versions, feature order, selected training timestamps, scaler parameters, seeds, model settings, circuit definitions, optimizer results, predictions, scenario parameters, and QAOA decoding rules. Save expensive run outputs after each completed run and download a checkpoint before ending a Colab session.

# 6. Results

## 6.1 Corrected validation forecasting results — available now

These are validation results, not final held-out test results.

| Model | Validation MAE mean, kW | Sample SD, kW | Runs |
|---|---:|---:|---:|
| Persistence | 0.4291 | Not applicable | Deterministic reference |
| Linear regression | 0.4147 | Not applicable | 1 |
| Random Forest | 0.4234 | 0.0023 | 5 |
| Neural network | 0.3960 | 0.0049 | 5 |
| Two-block VQC, corrected inputs | 0.4149 (seed 42 only) | Not yet available | 1 of 5 |

| Seed | MLP MAE, kW | MLP iterations | MLP convergence warning | RF MAE, kW |
|---|---:|---:|---|---:|
| 42 | 0.3917 | 500 | False | 0.4243 |
| 7 | 0.3938 | 500 | True | 0.4266 |
| 21 | 0.3944 | 500 | True | 0.4234 |
| 123 | 0.4044 | 240 | False | 0.4220 |
| 2026 | 0.3954 | 442 | False | 0.4208 |

Warnings are recorded as observed. Absence of a warning is not evidence of global optimality. Aggregate values above come from the reported outputs; calculate final statistics from saved full-precision values rather than rounded table entries.

**Permissible current interpretation:** under this fixed 500-example training sample and these model settings, the neural network has the lowest mean validation MAE among the corrected classical models. The result does not establish superiority across datasets or on the untouched test year.

## 6.2 Pilot results — keep separate

| Experiment | Reported outcome | Qualification |
|---|---|---|
| One-block VQC, 500 rows | MAE 0.4450 kW; training MSE 0.4736 kW² | Original full-training-pool scaler |
| Two-block VQC, seed 42 | MAE 0.4179 kW; MSE 0.4215 kW²; 315.6 s | 50-iteration limit; original scaler |
| Extended two-block training | MAE 0.4182 kW; MSE 0.4214 kW² | Restart plus 50 more iterations; total 636.2 s |
| Two-block VQC, seed 7 | MAE 0.4193 kW; MSE 0.4231 kW²; 330.5 s | 50-iteration limit; original scaler |

The two-block seed-42 pilot improved MAE by approximately 6.1% relative to the first VQC pilot. Additional training showed no validation improvement in that run. These observations motivated a fixed protocol; they are not final evidence of quantum advantage.

## 6.3 Scheduling results — to fill

| Scenario/window | Exact feasible cost | QAOA feasible cost | Absolute gap | Feasible-sample rate | Runtime |
|---|---|---|---|---|---|
| [Pending] | [Pending] | [Pending] | [Pending] | [Pending] | [Pending] |

## 6.4 Integrated operational results — to fill

| Forecast + scheduler | Realized cost | Curtailment | Peak import | Constraint violations | Evaluation windows |
|---|---|---|---|---|---|
| Classical + exact | [Pending] | [Pending] | [Pending] | [Pending] | [Pending] |
| VQC + exact | [Pending] | [Pending] | [Pending] | [Pending] | [Pending] |
| Classical + QAOA | [Pending] | [Pending] | [Pending] | [Pending] | [Pending] |
| VQC + QAOA | [Pending] | [Pending] | [Pending] | [Pending] | [Pending] |

# 7. Discussion

Answer each research question with measured evidence. Discuss whether MAE rankings match cost rankings, whether forecasting or optimization contributes more to performance differences, and whether quantum circuit depth provides useful benefits relative to computation in this setting.

Limitations to address: one household; one fixed small training sample; validation-guided development; model-specific optimization budgets; runs without confirmed convergence; simulator-only results; small discrete horizons; scenario-based solar/tariffs if used; mismatch between small experiments and deployment scale. Include negative results and failed feasibility cases.

An honest possible conclusion is that classical methods remain stronger in this setting while the implemented framework clarifies quantum-method limitations. Do not force the outcome to favor the project title.

# 8. Conclusion and Future Work

Write after final evaluation. State the task, principal quantified findings, practical interpretation, and boundaries. Future work may include more households, measured PV, larger horizons, hardware noise, richer circuits, alternative optimizers, and capacity planning. Keep future work distinct from completed contributions.

# References

[Insert verified references in the required university style. Every source must support a specific statement. This working template deliberately contains no invented bibliography.]

# Appendices

## A. Figure and table plan

The list below is a proposed final-manuscript arrangement, not the current repository numbering. For current numbered outputs and captions use [the figure register](../figures/README.md) and [the results tables](../results/README.md). Renumber consistently when assembling the final paper.

| Item | Intended content | Status |
|---|---|---|
| Figure 1 | Full forecasting-to-operation workflow | Planned |
| Figure 2 | Demand profile, missing hours, chronological splits | Data available; prepare final version |
| Figure 3 | VQC architecture with readout | Circuit diagram available; label for paper |
| Figure 4 | Corrected forecasting means and across-seed variation | Await corrected VQC runs |
| Figure 5 | Demand, solar, tariff, battery state, and actions for one scenario | Pending simulator |
| Figure 6 | QAOA feasible-solution gap and feasibility | Pending QAOA |
| Figure 7 | Realized operating costs for matched pipelines | Pending integration |
| Table 1 | Related-work comparison | Pending verification |
| Table 2 | Data and model configuration | Mostly available |
| Table 3 | Forecast results with convergence reporting | Partially complete |
| Table 4 | Operational comparison and limitations | Pending |

Do not add error bars until their meaning is explicit. Preserve units, readable labels, and consistent colors. Export vector figures where possible. Do not reuse the earlier pilot comparison graphic as the corrected final comparison.

## B. One-month execution plan

| Week | Required outcome | Writing in parallel | Stop condition |
|---|---|---|---|
| 1 | Verified four-hour simulator and exact discrete reference | Data, forecasting methods, scenario assumptions | Energy balance and feasibility checks pass |
| 2 | QAOA solves identical small instances; corrected forecast runs completed as time allows | QAOA formulation and experiment protocol | Decoding and comparison with enumeration verified |
| 3 | Matched forecast-to-operation experiments; freeze settings, then test evaluation | Results and discussion | Required result tables populated with saved outputs |
| 4 | Reproducible notebook, checked manuscript, defense slides | Abstract, conclusion, references, revision | A reviewer can trace every claim to a result or source |

These are target weeks, not guaranteed durations. If QAOA is too expensive, reduce horizon/action resolution while preserving a meaningful comparison. Stop optional model tuning and optional annealing before sacrificing verification or writing time.

## C. Experiment diary entry template

**Date / experiment ID:** [Fill]  
**Research question addressed:** [RQ1, RQ2, or RQ3]  
**Purpose:** [One sentence]  
**What changed:** [One controlled factor]  
**What stayed fixed:** [Data, features, architecture, budget, scenario]  
**Code section / saved artifact:** [Notebook section and output filename]  
**Configuration and seed:** [Fill]  
**Result:** [Metrics with units]  
**Termination / warnings:** [Fill]  
**Interpretation:** [What the result supports]  
**Limitations:** [What it does not establish]  
**Next action:** [One specific step]

## D. Supervisor progress summary

> I have implemented the demand-data pipeline, classical forecasting baselines, and one-block and two-block variational quantum regressors. I have also corrected the limited-data preprocessing protocol and completed five-seed comparisons for the neural network and Random Forest. The quantum forecasting results are still partly exploratory. My next priority is a verified small battery-scheduling simulator and exact reference, followed by QAOA on the identical discrete problem. The remaining evaluation will investigate whether differences in forecast accuracy translate into differences in realized operating cost. The scope is now fixed solar and battery capacities in a small simulated grid-connected system.

## E. Submission readiness checklist

- [ ] University formatting and supervisor requirements confirmed.
- [ ] Current notebook runs in order with documented dependencies.
- [ ] Dataset provenance, feature timing, and missing-data policy verified.
- [ ] Pilot and corrected experiments clearly separated.
- [ ] Fixed seeds, budgets, and all retained results documented.
- [ ] Operational constraints and terminal battery rule implemented.
- [ ] QAOA encoding checked against the identical exact problem.
- [ ] Future actual demand excluded from forecast inputs.
- [ ] Final test evaluation performed only after choices are fixed.
- [ ] Every figure/table traces to saved outputs.
- [ ] Related-work gap and references verified.
- [ ] No unsupported novelty, scalability, reliability, or quantum-advantage claims.
- [ ] Paper, notebook, figures, and defense materials backed up.

**Immediate next task:** build and verify the four-hour exact battery-scheduling example. The corrected seed-42 VQC result is recorded; do not let further forecasting tuning delay the scheduling core.


## Updated notebook evidence — 3 November 2026

Original cell 84 stores the corrected two-block VQC seed-42 result: training MSE 0.4177 kW²; validation MAE 0.4149 kW; training time 478.4 seconds; 50 iterations; success=False because the iteration limit was reached. Other corrected VQC seeds remain pending. These values supersede the earlier pending status.


### Test-period coverage and reporting

The reserved test set is the **available portion of 2010**, not a full calendar year. UCI describes the dataset as ending in November 2010 (https://archive.ics.uci.edu/dataset/235/individual+household+electric+power+consumption). Before final evaluation, export the exact first/last eligible timestamps, four-input row count, and monthly coverage from the processed data. Those processed endpoints and counts have not yet been audited. Report cost and energy over the observed interval, with per-day or per-kWh normalizations where appropriate; do not label partial-period totals annual savings or extrapolate seasonal performance to a full year.

### Evidence status

No scheduler, battery-simulation implementation, QAOA implementation, or associated 12-test suite was located in this chat's accessible workspace during the 3 November audit. The claim of “12 passing tests” is unverified and must not be cited. This does not establish what exists in a separate inaccessible workspace. Scheduling remains planned until code and verifiable test output are committed.

The rounded result CSVs are presentation transcriptions, not full-precision experimental artifacts. Export timestamp-aligned predictions, targets, model parameters, preprocessing state, and per-run diagnostics from the live experiment runtime; rerun only where those artifacts cannot be recovered. Recompute final statistics from these exports before final tables.
