# Binary encoding and diagonal cost model for S01

## Status

Implemented and exhaustively verified on 3 November 2026. This document records the encoding stage. A subsequent five-seed ideal statevector experiment is now documented in [QAOA_PILOT.md](QAOA_PILOT.md); no hardware execution is claimed.

## Table 5. Binary battery-action encoding

| Code (most significant bit first) | Action (kW) |
|---|---:|
| 000 | −2 |
| 001 | −1 |
| 010 | 0 |
| 011 | +1 |
| 100 | +2 |
| 101, 110, 111 | Unused; invalid |

Three bits encode five actions per interval. Four intervals therefore require 12 decision qubits in this direct representation; no auxiliary qubits are included in the abstract diagonal oracle. This is not a claim of minimum qubit count or efficient hardware implementation.

Hour 1 uses qubits 0–2, hour 2 uses 3–5, hour 3 uses 6–8, and hour 4 uses 9–11. If c_t is the integer action code, the basis index is sum(c_t × 2^(3t)), with t starting at zero. Qiskit statevector index ordering puts qubit 0 in the least significant position [1]. A displayed 12-bit string therefore contains hour groups in the order H4 H3 H2 H1.

For the exact schedule (0, +1, +1, −1), the chronological codes are 010, 011, 011, 001. Its displayed basis string is **001011011010**, corresponding to index **730**. Never interpret the displayed string as chronological hour order without decoding.

## Cost Hamiltonian

Define E(z) as the original import-cost objective for a physically feasible decoded schedule, and P for every other state, including unused action codes. The diagonal Hamiltonian is:

H_C = sum_z E(z) |z><z|.

For S01, every feasible cost is bounded above by U = sum_t tariff_t × (demand_t + maximum_charge) × dt = 2.76 CU. This follows because solar is nonnegative and imports cannot exceed demand plus maximum charging. The implementation also includes a throughput-cost upper bound when that optional cost is nonzero. Set P = U + 1 CU = **3.76 CU**, strictly above any feasible cost. The construction preserves the feasible minimum without using the known optimal cost to choose P.

This is a **general diagonal truth-table formulation**, not a quadratic unconstrained binary optimization (QUBO) model. It can contain high-order interactions when expanded in Pauli Z operators. Preparing the table requires classical enumeration; generic phase-gate synthesis may be expensive. It is appropriate as a small simulator reference, not evidence of an efficient quantum encoding or quantum speedup. A structured QUBO or constraint-preserving mixer would be a separate formulation needing separate verification.

All infeasible states share the same penalty. This simple choice gives no gradient in violation severity and may make optimization difficult. The uniform initial state has only 68/4096 = **1.6602% feasible probability**. These are material limitations to report and compare against, not grounds for assuming QAOA will perform well.

## Exhaustive verification

| Check | Result |
|---|---:|
| Binary basis states | 4,096 |
| States with valid action codes | 625 |
| States containing unused codes | 3,471 |
| Valid-code schedules violating physical constraints | 557 |
| Feasible schedules | 68 |
| Minimum diagonal energy | 0.195 CU |
| Ground states within 1e-12 tolerance | 1 |
| Ground-state basis index | 730 |
| Ground-state schedule | (0, +1, +1, −1) kW |

The verifier checks all 625 encode/decode round trips, uniqueness, all 4,096 valid/invalid classifications, feasible costs against the existing simulator, penalty assignment, physical feasibility of every ground state, and agreement with the exact enumerator. A hand-derived bit-order check verifies index 730. The numerical optimum is unique for this S01 cost table within the stated tolerance. This conclusion is separate from generic deterministic tie-breaking in the scheduler.

These checks verify encoding consistency with the existing simulator; they do not independently validate every physical modeling assumption.

## Reproduce

From the repository root:

```bash
python scripts/verify_binary_encoding.py
```

Only Python's standard library is needed for this step.

- Source: [binary_encoding.py](../src/binary_encoding.py)
- Verification: [verify_binary_encoding.py](../scripts/verify_binary_encoding.py)
- Summary and source hashes: [verification JSON](../results/scenario_01_encoding_verification.json)
- All energies and masks in basis-index order: [cost diagonal JSON](../results/scenario_01_cost_diagonal.json)

## QAOA protocol and subsequent pilot

Use the uniform superposition as the initial state, alternate a cost phase exp(−i gamma H_C) with an X mixer exp(−i beta sum_j X_j), and optimize the expected encoded cost. IBM's generalized QAOA documentation describes cost operators and the default uniform initialization and X mixer [2]. In a simulator, the diagonal phase can be applied directly to amplitudes; this must not be reported as efficient compiled hardware execution.

Before training, verify the simulator's bit ordering, norm preservation, and cost/mixer application on a small independently checked circuit. Start with p = 1 and a documented seed and evaluation budget. Save all parameters and termination diagnostics. Report raw feasible probability, probability of the exact optimum, best feasible cost observed under a stated sampling budget, and the gap to 0.195 CU. Compare with uniform sampling under the same number of shots. Report failed runs and do not substitute an exact schedule while attributing its cost to QAOA.

## Sources checked 3 November 2026

[1] IBM Quantum, *Bit-ordering in the Qiskit SDK*. https://quantum.cloud.ibm.com/docs/en/guides/bit-ordering

[2] IBM Quantum, *qiskit.circuit.library.qaoa_ansatz*. https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.library.qaoa_ansatz

These sources support the Qiskit conventions and QAOA structure. The action mapping, penalty construction, and numerical verification above are this project's implementation choices and computed results.
