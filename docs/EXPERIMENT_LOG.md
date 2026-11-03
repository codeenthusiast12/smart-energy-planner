# Experiment record

Status reconstructed from the uploaded notebook and its saved outputs on 3 November 2026. No experiment was rerun during repository preparation.

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
