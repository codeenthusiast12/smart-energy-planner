# Completion roadmap

Target: remaining four weeks, with paper writing alongside implementation.

## Week 1 — exact scheduling reference

Update, 3 November 2026: supplied simulator and exact scheduler are implemented; all 14 supplied tests pass. See `SCHEDULER_REVIEW.md` and `../results/battery_scheduler_test_log.txt`. Synthetic scenario S01 is now documented with assumptions, full-precision outputs, Table 4, and Figure 2 in `SCENARIO_01.md`. The broader operational evaluation protocol remains pending.

- [x] Define a four-hour scenario: demand, solar, tariff, battery capacity, initial state, efficiencies, and action levels.
- [x] Define no-export/import policy and terminal battery-energy rule.
- [x] Enumerate schedules and reject physically infeasible trajectories.
- [x] Check simple cases by hand and verify energy balance.
- [x] Document the S01 system model and assumptions; adapt the report into the final methods section.

Done when the optimum of the chosen discrete problem is verifiable, not merely when a cost prints.

## Week 2 — QAOA and remaining forecasting protocol

- [x] Specify a 12-qubit direct action encoding, diagonal penalty Hamiltonian, uniform initialization, and planned X mixer (see `QAOA_ENCODING.md`; no auxiliary qubits in the abstract oracle).
- [x] Implement ideal QAOA statevector evolution and independently verify against dense matrix exponentials (seven new tests).
- [ ] Cross-check the equivalent circuit in Colab/Qiskit. The dense cost table is a simulator prototype, not an efficient QUBO or hardware synthesis.
- [x] Verify S01 encoding against exact enumeration over all 4,096 basis states; repeat for any changed scenario.
- [x] Record S01 pilot feasibility, solution quality, five seeds, optimizer termination, and two random baselines (see `QAOA_PILOT.md`).
- [ ] Extend to a fixed set of scenarios and budgets before making broader comparisons.
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
