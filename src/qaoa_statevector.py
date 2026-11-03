"""Ideal QAOA statevector evolution: dense diagonal phase and Rx(2 beta).

NumPy simulator, not a Qiskit/hardware execution or efficient oracle synthesis.
Parameters alternate gamma, beta for each layer; qubit 0 is least significant.
"""
import numpy as np


def apply_x_mixer(state, beta, qubit):
    """Apply exp(-i beta X) on one qubit, returning a new state."""
    size = 1 << qubit
    blocks = state.reshape(-1, 2, size)
    out = np.empty_like(blocks)
    c, s = np.cos(beta), -1j * np.sin(beta)
    out[:, 0, :] = c * blocks[:, 0, :] + s * blocks[:, 1, :]
    out[:, 1, :] = s * blocks[:, 0, :] + c * blocks[:, 1, :]
    return out.reshape(-1)


def qaoa_state(energies, parameters):
    energies = np.asarray(energies, dtype=float)
    parameters = np.asarray(parameters, dtype=float)
    n = energies.size
    if energies.ndim != 1 or n < 2 or n & (n - 1):
        raise ValueError('Cost diagonal length must be a power of two >= 2')
    if parameters.ndim != 1 or len(parameters) % 2:
        raise ValueError('Parameters must be gamma,beta pairs')
    if not np.all(np.isfinite(energies)) or not np.all(np.isfinite(parameters)):
        raise ValueError('Finite inputs required')
    state = np.full(n, 1 / np.sqrt(n), dtype=complex)
    for gamma, beta in parameters.reshape(-1, 2):
        state *= np.exp(-1j * gamma * energies)
        for qubit in range(n.bit_length() - 1):
            state = apply_x_mixer(state, beta, qubit)
    return state


def state_probabilities(energies, parameters):
    state = qaoa_state(energies, parameters)
    probabilities = np.abs(state) ** 2
    if not np.isclose(probabilities.sum(), 1.0, atol=1e-10):
        raise ArithmeticError('State norm lost')
    return probabilities / probabilities.sum()


def sample_metrics(probabilities, energies, feasible, shots, rng):
    """Unconditional sampling; infeasible samples counted, no repair/fallback."""
    probabilities = np.asarray(probabilities)
    energies = np.asarray(energies)
    feasible = np.asarray(feasible, dtype=bool)
    indices = rng.choice(len(probabilities), size=shots, p=probabilities)
    good = indices[feasible[indices]]
    optimum = float(energies[feasible].min())
    unique, counts = np.unique(indices, return_counts=True)
    best = int(good[np.argmin(energies[good])]) if len(good) else None
    return dict(shots=shots, feasible_samples=int(len(good)),
                feasible_sample_rate=float(len(good) / shots),
                optimum_samples=int(np.sum(np.isclose(energies[indices],optimum,atol=1e-12,rtol=0) & feasible[indices])),
                best_feasible_index=best,
                best_feasible_cost_cu=None if best is None else float(energies[best]),
                gap_cu=None if best is None else float(energies[best]-optimum),
                counts={str(int(i)):int(c) for i,c in zip(unique,counts)})
