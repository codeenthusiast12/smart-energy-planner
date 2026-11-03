"""Compact action encoding and small-instance diagonal cost oracle.

This is a dense truth-table prototype, not a QUBO or efficient gate synthesis.
Hour 1 occupies the least significant bits, matching statevector indices.
"""
from math import isfinite
from battery_scheduler import simulate


def bits_per_action(actions):
    if not actions or len(set(actions)) != len(actions):
        raise ValueError('Actions must be a nonempty sequence of unique values')
    return max(1, (len(actions) - 1).bit_length())


def encode_schedule(schedule, actions):
    width = bits_per_action(actions)
    lookup = {a: i for i, a in enumerate(actions)}
    try:
        return sum(lookup[a] << (width * t) for t, a in enumerate(schedule))
    except KeyError as exc:
        raise ValueError('Action outside the specified action set') from exc


def decode_index(index, horizon, actions):
    width = bits_per_action(actions)
    if horizon < 1 or not isinstance(index, int) or not 0 <= index < 2 ** (width * horizon):
        raise ValueError('Basis index or horizon outside range')
    codes = [(index >> (width * t)) & ((1 << width) - 1) for t in range(horizon)]
    if any(c >= len(actions) for c in codes):
        return None  # unused binary codes; never silently map to idle
    return tuple(actions[c] for c in codes)


def build_diagonal(demand, solar, tariff, p):
    """Feasible energy = cost; all infeasible energies = proven upper bound + 1.

    Bound requires nonnegative loads, solar, tariffs, throughput cost and valid
    physical parameters. Intended only for small, fully enumerated instances.
    """
    h = len(demand)
    if h < 1 or len(solar) != h or len(tariff) != h:
        raise ValueError('Nonempty equal-length profiles required')
    values = [*demand, *solar, *tariff, *p.actions_kw, p.capacity_kwh,
              p.e_min_kwh, p.initial_kwh, p.eta_charge, p.eta_discharge,
              p.dt_h, p.throughput_cost_per_kwh]
    if p.terminal_min_kwh is not None:
        values.append(p.terminal_min_kwh)
    if not all(isfinite(x) for x in values):
        raise ValueError('All numeric inputs must be finite')
    if any(x < 0 for x in [*demand, *solar, *tariff, p.throughput_cost_per_kwh]):
        raise ValueError('Nonnegative profiles and throughput cost required')
    if not (0 < p.eta_charge <= 1 and 0 < p.eta_discharge <= 1 and p.dt_h > 0
            and 0 <= p.e_min_kwh <= p.initial_kwh <= p.capacity_kwh):
        raise ValueError('Invalid battery parameters')
    width = bits_per_action(p.actions_kw)
    qubits = width * h
    if qubits > 16:
        raise ValueError('Dense reference oracle is restricted to at most 16 qubits')
    max_charge = max(0.0, max(p.actions_kw))
    max_power = max(abs(a) for a in p.actions_kw)
    upper = sum(c * (d + max_charge) * p.dt_h for d, c in zip(demand, tariff))
    upper += p.throughput_cost_per_kwh * max_power * h * p.dt_h
    penalty = upper + 1.0
    energies, feasible, valid = [], [], []
    for index in range(2 ** qubits):
        schedule = decode_index(index, h, p.actions_kw)
        valid.append(schedule is not None)
        tr = None if schedule is None else simulate(schedule, demand, solar, tariff, p)
        ok = tr is not None and tr.feasible
        feasible.append(ok)
        energies.append(tr.cost if ok else penalty)
    if not any(feasible):
        raise ValueError('No feasible schedule; no feasible ground state exists')
    return dict(qubits=qubits, bits_per_action=width, upper_bound_cu=upper,
                penalty_cu=penalty, energies=energies, feasible=feasible, valid=valid)
