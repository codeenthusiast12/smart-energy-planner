# Completion roadmap

Target: remaining four weeks, with paper writing alongside implementation.

## Week 1 — exact scheduling reference

Update, 3 November 2026: supplied simulator and exact scheduler are implemented; all 14 supplied tests pass. See `SCHEDULER_REVIEW.md` and `../results/battery_scheduler_test_log.txt`. Test fixtures define small scenarios; a saved paper experiment and final assumptions are still pending.

- [ ] Define a four-hour scenario: demand, solar, tariff, battery capacity, initial state, efficiencies, and action levels.
- [x] Define no-export/import policy and terminal battery-energy rule.
- [x] Enumerate schedules and reject physically infeasible trajectories.
- [x] Check simple cases by hand and verify energy balance.
- [ ] Write the system-model section and record assumptions.

Done when the optimum of the chosen discrete problem is verifiable, not merely when a cost prints.

## Week 2 — QAOA and remaining forecasting protocol

- [ ] Specify binary variables, auxiliary variables, penalties, Hamiltonian, mixer, and qubit count.
- [ ] Verify encoding against exact enumeration on the same instances.
- [ ] Record sampled feasibility and feasible solution quality.
- [ ] Complete predefined corrected forecasting runs without adding new architectures.
- [ ] Finalize methods and a focused verified related-work matrix.

## Week 3 — integrated experiments

- [ ] Generate multi-hour forecasts without using future actual lag inputs.
- [ ] Specify action execution and balancing under forecast errors.
- [ ] Compare classical/VQC forecasts with exact/QAOA schedulers on matched windows.
- [ ] Freeze model selection and scenario settings before final test evaluation.
- [ ] Export full-precision results and publication figures.

## Week 4 — paper and defense

- [ ] Complete results, limitations, conclusion, and abstract.
- [ ] Verify citations, units, tables, and result provenance.
- [ ] Check a clean notebook run or document reproducibility limitations explicitly.
- [ ] Prepare defense slides and rehearse questions on assumptions and negative results.

## Scope control

No wind, capacity optimization, flexible loads, new architecture search, or unsupported hardware speedup claims in the core study. Reduce horizon/action resolution if QAOA is too expensive. Exact enumeration is the core comparator; simulated annealing is optional.
