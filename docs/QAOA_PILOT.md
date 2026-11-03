# S01 QAOA pilot: ideal statevector simulation

## Status and scope

Five one-layer QAOA runs were completed on 3 November 2026 for the same synthetic four-hour scenario and 12-qubit encoding. This is an exploratory simulator experiment. The code implements the QAOA unitary mathematically using NumPy; it was **not executed in Qiskit or on quantum hardware**. Qiskit is not installed in this execution environment. Cross-checking the same circuit in the project's Colab/Qiskit environment remains a reproducibility task.

The original battery scheduler and encoded costs are unchanged. No demand forecasts or held-out household data were used.

## Circuit and optimization

The initial state is the uniform superposition of all 4,096 basis states. One layer applies:

1. Cost phase: multiply amplitude z by exp(−i gamma × E(z)/3.76).
2. X mixer: apply exp(−i beta X) to each of the 12 qubits, equivalent to Rx(2 beta).

This is the standard cost-then-mixer QAOA structure [1,2]. It uses the dense diagonal oracle already documented in [QAOA_ENCODING.md](QAOA_ENCODING.md). The diagonal operation is applied directly to amplitudes; no gate decomposition, routing, hardware resource estimate, or efficient QUBO implementation is claimed.

The classical optimizer minimizes the exact expectation of E/3.76, **including penalties for infeasible states**. That training objective is not the realized cost of a feasible schedule. Scaling the Hamiltonian preserves its minimizers; gamma refers to the scaled operator.

| Setting | Value |
|---|---|
| Layers p | 1 |
| Trainable parameters | gamma and beta |
| Initial-angle seeds | 42, 7, 21, 123, 2026 |
| Initial angles | Uniform within the bounds |
| Gamma bounds | 0 to 2π |
| Beta bounds | 0 to π |
| Optimizer | SciPy COBYLA |
| Budget | At most 200 objective evaluations per run |
| Initial trust-region radius | 0.5 |
| Tolerance / constraint tolerance | 1e-6 / 1e-8 |
| Training evaluation | Exact ideal statevector expectation, no measurement noise |
| Final sampling | 1,024 independent draws per method per seed |
| Repair or exact-solution fallback | None |

The protocol file was saved before these runs, within this exploratory workflow; it is not an externally preregistered experiment. COBYLA's maxiter controls objective evaluations, not necessarily iterations [3]. Four runs exhausted the 200-evaluation budget. Seed 42 stopped after 16 evaluations with a trust-region termination success flag; this does not certify a global optimum.

## Verification before training

All 21 tests passed: the 14 existing scheduler tests and seven new QAOA tests. The latter check two layers against independently constructed dense matrix exponentials on three qubits, least-significant-qubit ordering, zero-cost-phase and zero-mixer limits, 12-qubit norm preservation, invalid input shape, and absence of an exact-solution fallback when sampling returns no feasible state. The dense-matrix comparison agrees within 1e-12.

Command: `python -m unittest discover -s tests -v`. These checks need NumPy and SciPy in addition to the standard library. They validate simulator behavior, not physical hardware execution.

## Baselines and fairness

Both random methods use the same 1,024-draw reporting budget and the same physical feasibility checks.

- **Uniform bitstrings:** sample all 4,096 binary states equally, including unused action codes.
- **Uniform action codes:** choose among the 625 valid-code schedules equally. This removes unused codes but does not filter physical infeasibility.

The second is an essential stronger classical baseline: random generation need not waste draws on unused binary codes. Neither baseline has training overhead. Equal final sampling budgets do not make total computational budgets equal: QAOA also uses its optimization evaluations, and this prototype precomputes the entire diagonal by enumeration. No runtime advantage follows.

Sampling streams are independent of angle initialization and of one another, using child streams of NumPy SeedSequence for each recorded seed. Rejected samples remain counted. Samples are not repaired, and the exact optimum is never substituted for a failed draw.

## Table 6. Pilot results

Exact distribution probabilities are computed from the saved final statevectors; they are not estimated from the 1,024 samples. QAOA values below are mean ± sample standard deviation over five initializations.

| Method | Feasible probability per draw | Optimal probability per draw | Mean best sampled feasible cost (CU) | Batches sampling the optimum |
|---|---:|---:|---:|---:|
| Uniform bitstrings | 1.6602% | 0.0244% | 0.2820 | 0 / 5 |
| Uniform action codes | 10.8800% | 0.1600% | 0.1950 | 5 / 5 |
| QAOA, p = 1 | 7.0023% ± 1.7312 percentage points | 0.0887% ± 0.0332 percentage points | 0.2010 | 4 / 5 |

The exact optimum is 0.195 CU. With QAOA, seeds 42, 7, 21, and 2026 sampled that optimum; seed 123 returned a best sampled feasible cost of 0.225 CU, an absolute gap of 0.030 CU. All sampled batches contained at least one feasible schedule. The observed 4/5 versus 5/5 success counts are five random batches on one problem, not reliable general success-rate estimates.

The analytically implied chance of at least one optimum in 1,024 independent draws is 22.12% for uniform bitstrings and 80.60% for uniform action codes. The mean of the five QAOA run-specific probabilities is 57.48%. This distinction prevents overinterpreting the realized batch counts.

## Interpretation for the paper

The one-layer QAOA pilot increased feasible-state and optimal-state probabilities relative to uniform sampling over all binary strings. However, uniform sampling over valid action codes performed better on both distribution measures and attained a lower mean best sampled cost. Thus, this pilot does not establish a quantum advantage. The result highlights the importance of comparing against classical baselines that avoid unused binary encodings.

Limitations: one synthetic scenario, five initializations, one circuit layer, bounded angle search, a flat penalty for all infeasible states, four budget-limited runs, ideal exact-expectation training, no hardware noise, and an exponentially sized precomputed diagonal. Neither final forecasting performance nor forecast-to-operation value is measured here. The experiment is evidence about this implementation and budget, not the best performance achievable by QAOA.

## Artifacts and reproduction

- [Simulator](../src/qaoa_statevector.py)
- [Independent tests](../tests/test_qaoa_statevector.py)
- [Run and plotting script](../scripts/run_qaoa_pilot.py)
- [Protocol](../results/qaoa_pilot_protocol.json)
- [Table 6 per-run CSV](../results/table_06_qaoa_pilot_by_seed.csv)
- [Full optimizer traces, sampling counts, environment, and source hashes](../results/qaoa_pilot_runs.json)
- [Final probabilities, NumPy archive](../results/qaoa_pilot_probabilities.npz)
- [Figure 3 PNG](../figures/fig_03_qaoa_pilot_probabilities.png) and [vector PDF](../figures/fig_03_qaoa_pilot_probabilities.pdf)

Run from the repository root:

```bash
python -m unittest discover -s tests -v
python scripts/verify_binary_encoding.py
python scripts/run_qaoa_pilot.py
```

The runner overwrites pilot outputs; preserve an earlier run before changing settings. Actual versions were Python 3.12.14, NumPy 2.3.5, and SciPy 1.17.0. These are separate from the earlier Colab forecasting environment. Training-only elapsed times are saved for provenance, not compared with VQC training or used to claim quantum speedup.

## Next step

Cross-check the unitary in Colab with Qiskit's diagonal phase operation and Rx gates. Then define a small, fixed set of additional scenarios and a controlled depth/budget comparison before integration with forecasts. Keep the current negative baseline comparison in the record.

## Sources checked 3 November 2026

[1] IBM Quantum, *qiskit.circuit.library.qaoa_ansatz*. https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.library.qaoa_ansatz

[2] IBM Quantum, *RXGate*: Rx(theta) = exp(−i theta X/2). https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.library.RXGate

[3] SciPy, *minimize(method='COBYLA')*. https://docs.scipy.org/doc/scipy/reference/optimize.minimize-cobyla.html

Documentation supports the algorithm and optimizer conventions. Numerical results come from the saved experiment, not these references.
