# Experiment record

Status reconstructed from the uploaded notebook and its saved outputs on 3 November 2026. Forecasting experiments were not rerun during initial repository preparation. Later scheduler checks and experiments are recorded below.

| Experiment | Protocol | Reported outcome | Interpretation |
|---|---|---|---|
| One-block VQC | Pilot scaler, 500 rows | Validation MAE 0.4450 kW | Initial quantum reference |
| Two-block VQC, seed 42 | Pilot scaler, 50 iterations | MAE 0.4179 kW | Improved single-run pilot, iteration limit |
| Two-block VQC, extended | Pilot scaler, restart +50 iterations | MAE 0.4182 kW | Extra training did not help validation in this run |
| Two-block VQC, seed 7 | Pilot scaler, 50 iterations | MAE 0.4193 kW | Similar pilot result, not proof of broad stability |
| Corrected MLP, five seeds | Scaler fitted on 500 rows | Mean 0.3960; SD 0.0049 kW | Two runs raised convergence warnings |
| Corrected Random Forest, five seeds | Same 500 raw-input rows | Mean 0.4234; SD 0.0023 kW | Fixed-sample randomness only |
| Corrected VQC, seed 42 | Scaler fitted on 500 rows | MAE 0.4149 kW; MSE 0.4177 kW² | 478.4 s; 50-iteration limit; four seeds still pending |

## Scheduler verification — 3 November 2026

- Purpose: verify the author's separately supplied classical battery simulator and exact enumeration in the repository layout.
- Files: `src/battery_scheduler.py` and `tests/test_battery_scheduler.py`, preserved unchanged.
- Command: `python3 -m unittest discover -s tests -v`.
- Result: 14 tests passed, exit code 0, Python 3.12.14.
- Evidence: `results/battery_scheduler_test_log.txt`.
- Coverage: energy balance, battery bounds, no export, discharge clipping, terminal constraint, small-instance enumeration and optimality checks.
- Limitation: these are synthetic test cases; no QAOA or integrated cost experiment was executed. See `SCHEDULER_REVIEW.md` for parameter-validation gaps.
- Next: save a documented scheduling scenario, then verify the QAOA encoding against the exact reference.

## Next entry

- Date / experiment ID:
- Research question:
- Configuration and data:
- Controlled change:
- Seed and compute budget:
- Result files:
- Metrics and units:
- Termination / warnings:
- Supported interpretation:
- Remaining limitation:
- Next action:

## S01 — synthetic exact scheduling example, 3 November 2026

Purpose: establish a saved classical reference for QAOA. Reused the existing cost-consistency test fixture; no forecasting or test-period data used. Enumerated 625 schedules with 68 feasible. Selected actions: (0, +1, +1, −1) kW. Exact cost: 0.195 CU; idle-battery cost: 0.295 CU. Final energy: 3.347368421052632 kWh. Selected-trajectory energy balance, energy update, bounds, terminal energy, and import-cost assertions passed. Configuration, full trajectories, all candidate feasibility records, Table 4, and Figure 2 are saved. See [SCENARIO_01.md](SCENARIO_01.md). Next: verify QAOA encoding on the identical discrete problem.

## S01 binary encoding verification — 3 November 2026

Three bits per interval encode the five battery actions; four intervals require 12 qubits. Exhaustive verification passed for all 4,096 basis states: 625 valid-code schedules, 68 physically feasible, and one minimum-energy state (index 730, displayed string 001011011010) with cost 0.195 CU. All infeasible states receive 3.76 CU; the feasible-cost upper bound is 2.76 CU. Uniform feasible probability is 1.66015625%. Saved the cost diagonal, feasibility masks, and verification summary with source hashes. See [QAOA_ENCODING.md](QAOA_ENCODING.md). No quantum circuit was trained. Next: verify cost-phase/mixer implementation and measure small-instance QAOA performance against equal-budget uniform sampling.

## S01 one-layer QAOA pilot — 3 November 2026

Implemented ideal NumPy statevector cost-phase and X-mixer evolution; all 21 tests pass, including seven new independent simulator checks. Ran seeds 42, 7, 21, 123, and 2026 with COBYLA (200 evaluations maximum) and 1,024 final samples per method/seed. Four runs reached the evaluation limit. Mean exact feasible probability: 7.0023%; optimum probability: 0.0887%. Uniform valid-action sampling achieved 10.88% and 0.16%, respectively, exceeding QAOA. QAOA sampled the 0.195 CU optimum in four of five batches; seed 123's best was 0.225 CU. Saved protocol, traces, parameters, probabilities, counts, Table 6, and Figure 3. No forecasts, Qiskit execution, or hardware were used. See [QAOA_PILOT.md](QAOA_PILOT.md). Next: Qiskit cross-check and a controlled multi-scenario protocol; retain the unfavorable classical comparison.
