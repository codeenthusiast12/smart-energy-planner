# Classical battery scheduler: implementation and verification

## Provenance and status

The author supplied the source and test files on 3 November 2026. Both are preserved unchanged under `src/` and `tests/`. All 14 supplied tests pass in that layout. The full command, Python version, timestamp, and output are recorded in `../results/battery_scheduler_test_log.txt`.

The initial repository audit lacked these separate uploads. Their inclusion supersedes the earlier missing-code status. Neither file implements QAOA.

## Implemented behavior

- Signed battery power actions: positive charge, negative discharge; one action per interval prevents simultaneous charging and discharging.
- Charge/discharge efficiency, battery energy bounds, grid imports, solar use and curtailment.
- No export in planning; execution mode clips discharge exceeding realized load and records the clipped energy.
- Terminal minimum energy, import cost, optional throughput cost, and peak import.
- Exhaustive enumeration over the chosen action set, with deterministic tie-breaking using costs and throughput rounded to 12 decimals.
- An idle-battery baseline.

Defaults are scenario assumptions: 5 kWh capacity, 0.5 kWh minimum, 2.5 kWh initial energy, 0.95 charge/discharge efficiencies, 1-hour intervals, actions of −2, −1, 0, 1, and 2 kW, and a 2.5 kWh terminal minimum. A four-hour default-action problem has 625 candidate schedules. Exactness applies to this chosen discrete problem.

## Verification boundaries and follow-up

The supplied tests cover simple energy/cost calculations, bounds, no-export behavior, clipping, flat and variable prices, terminal energy, enumeration count, optimum consistency, and an infeasible instance. Passing these cases does not establish correctness for every input or operational benefit.

- The terminal minimum defaults to a fixed **2.5 kWh**. It does not automatically follow a changed initial energy, despite the source comment. Set both explicitly for each scenario.
- Input validation checks array lengths but does not comprehensively reject nonfinite values, invalid efficiencies, negative demand/solar, or inconsistent initial/bound parameters.
- Direct calls to `simulate` do not enforce action membership or separate power limits; `exact_schedule` restricts candidates to `actions_kw`.
- Execution mode flags battery/terminal violations rather than repairing them. Preserve and report those flags in integrated evaluation.
- Grid supply is unlimited in this prototype, so it does not demonstrate improved reliability or reduced unserved energy.
- Solar and tariffs in tests are synthetic assumptions. A documented scenario, saved trajectories, and publication figures are still needed.
- QAOA encoding, feasibility checks against enumeration, and forecast-driven operational experiments remain pending.

## Reproduce

From the repository root:

```bash
python3 -m unittest discover -s tests -v
```

These two files require only the Python standard library.
