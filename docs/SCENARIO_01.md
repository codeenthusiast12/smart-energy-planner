# Scenario S01: four-hour exact scheduling reference

## Purpose and provenance

This synthetic example documents the classical scheduling reference before QAOA integration. Its demand, solar, and tariff arrays reproduce the existing `test_returned_optimum_is_feasible_and_cost_consistent` fixture, rather than a scenario chosen after comparing quantum performance. It uses no forecasting model and no held-out household data. Currency units (CU) are arbitrary; these are not measured Moroccan tariffs.

## Fixed assumptions

Four one-hour intervals; 5 kWh battery capacity; 0.5 kWh minimum energy; 2.5 kWh initial energy; 95% charge and discharge efficiency; actions −2, −1, 0, +1, +2 kW. The final energy must be at least 2.5 kWh. There is no export, no grid import limit, no throughput charge, and no terminal salvage credit. Positive action charges the battery. H1–H4 are relative intervals, not timestamps.

For each interval, charge = max(action, 0), discharge = max(−action, 0), and net load = demand + charge − discharge. Planning requires nonnegative net load. Solar use is the lesser of available solar and net load; grid import supplies the remainder. Stored energy changes by 0.95 × charge − discharge / 0.95 kWh. The objective is the sum of tariff × import × one hour. All candidate schedules use the same bounds and terminal constraint.

## Table 4. Four-hour exact battery schedule

| Interval | Demand (kW) | Solar (kW) | Tariff (CU/kWh) | Action (kW) | End energy (kWh) | Import (kW) | Curtailment (kW) |
|---|---:|---:|---:|---:|---:|---:|---:|
| H1 | 1.0 | 0.0 | 0.12 | 0 | 2.5000 | 1.0 | 0.0 |
| H2 | 1.0 | 1.5 | 0.15 | +1 | 3.4500 | 0.5 | 0.0 |
| H3 | 1.0 | 2.5 | 0.30 | +1 | 4.4000 | 0.0 | 0.5 |
| H4 | 1.0 | 0.5 | 0.35 | −1 | 3.3474 | 0.0 | 0.5 |

Caption: exact enumeration of the specified synthetic discrete problem. Displayed values are rounded; machine-readable outputs preserve Python floating-point precision. Stored energy is measured at interval ends; initial energy is 2.5 kWh.

## Results and interpretation

Of 625 candidate schedules, 68 satisfy the implemented constraints. The selected optimum is (0, +1, +1, −1) kW. Import cost is 0.195 CU versus 0.295 CU with an idle battery: a reduction of 0.100 CU (33.8983%) within this example.

The idle baseline uses the same solar profile, battery parameters, and terminal rule, with all actions zero. It is not a system without solar. Optimized grid energy is 1.5 kWh, equal to the idle baseline, but purchases occur at cheaper times. Both peak imports are 1 kW. Optimized curtailment is 1 kWh versus 2 kWh for idle operation; throughput is 3 kWh. Final stored energy is higher than the initial energy, so the cost reduction does not come from emptying the battery.

At H2, charging draws 0.5 kW from the grid in addition to surplus solar. At H4, the 1 kW discharge covers the full demand and 0.5 kW of solar is curtailed. This is an effect of the coarse action set and the cost objective: a 0.5 kW discharge is unavailable. The model does not separately minimize curtailment. The returned schedule minimizes cost with throughput and lexicographic tie-breaks; it need not be the unique minimum-cost schedule.

These results establish a reproducible small classical benchmark. They do not demonstrate forecast benefits, quantum advantage, general savings, battery lifetime improvement, or final test-set performance.

## Paper-ready results paragraph

For the illustrative four-hour scenario, exhaustive enumeration evaluated 625 discrete schedules, of which 68 were feasible. The selected minimum-cost schedule was (0, +1, +1, −1) kW and yielded an electricity-import cost of 0.195 CU, compared with 0.295 CU for the idle-battery reference. Final stored energy was 3.3474 kWh, exceeding the prescribed 2.5 kWh terminal minimum. The 33.9% cost reduction is specific to the synthetic profiles and chosen action discretization; no forecasting or quantum optimization was used in this experiment.

## Reproduce and inspect

Run from the repository root with Python and Matplotlib installed:

```bash
python scripts/run_scheduling_scenario.py
```

The script uses the original scheduler unchanged, checks the selected trajectory against energy-balance and battery-update equations, and exports:

- [Scenario configuration and full trajectories](../results/scenario_01_exact_scheduling.json)
- [Table 4 CSV](../results/table_04_four_hour_battery_schedule.csv)
- [All 625 candidates and feasibility decisions](../results/scenario_01_enumerated_schedules.csv); infeasible costs are left blank because early-return trajectories are incomplete.
- [Figure 2 PNG](../figures/fig_02_four_hour_battery_schedule.png), [vector PDF](../figures/fig_02_four_hour_battery_schedule.pdf), and [SVG](../figures/fig_02_four_hour_battery_schedule.svg).

The JSON records Python version and scheduler SHA-256. Figure numbering follows the repository register and may be renumbered consistently for the final manuscript. Broader input-validation limitations remain documented in [the scheduler review](SCHEDULER_REVIEW.md).

## Next experiment

Define a binary representation of the same action set and constraints, count the qubits, and verify every encoded candidate against this exact reference before running QAOA. If simulation requires a smaller action set or horizon, enumerate that revised problem separately and compare both solvers on identical inputs.
