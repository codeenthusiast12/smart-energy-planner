"""Four-hour battery simulator and exact discrete scheduler.

Implements blueprint Sections 4.1-4.3 for a grid-connected solar-battery
household with NO export. All parameter values are SCENARIO ASSUMPTIONS, not
measurements. Solar and tariff profiles must be labelled synthetic in the paper
unless a real source is supplied.

Conventions
-----------
* Time step dt = 1 h, so kW * dt = kWh.
* An action is a signed battery power in kW at the battery terminals:
    a > 0  -> charge  (power drawn from the bus)
    a < 0  -> discharge (power delivered to the bus)
  Charging and discharging cannot happen together by construction.
* Energy update (blueprint 4.2):
    E[t+1] = E[t] + eta_c * charge * dt - discharge * dt / eta_d
* Bus balance with no export:
    net = demand + charge - discharge          (must be >= 0)
    solar_used = min(solar, net)
    import = net - solar_used
    curtailment = solar - solar_used
"""
from __future__ import annotations

from dataclasses import dataclass, field
from itertools import product
from typing import Optional, Sequence

TOL = 1e-9


@dataclass(frozen=True)
class BatteryParams:
    capacity_kwh: float = 5.0
    e_min_kwh: float = 0.5
    initial_kwh: float = 2.5
    eta_charge: float = 0.95
    eta_discharge: float = 0.95
    dt_h: float = 1.0
    # Discrete action set (kW). Negative = discharge.
    actions_kw: tuple = (-2.0, -1.0, 0.0, 1.0, 2.0)
    # Terminal rule: final energy must be >= this value. None disables it.
    # Default (set in __post_init__-free style) is to require >= initial.
    terminal_min_kwh: Optional[float] = 2.5
    throughput_cost_per_kwh: float = 0.0


@dataclass
class Trajectory:
    actions: tuple
    energy: list = field(default_factory=list)       # length H+1
    grid_import: list = field(default_factory=list)  # kW, length H
    solar_used: list = field(default_factory=list)
    curtailment: list = field(default_factory=list)
    charge: list = field(default_factory=list)
    discharge: list = field(default_factory=list)
    cost: float = 0.0
    throughput_kwh: float = 0.0
    peak_import_kw: float = 0.0
    feasible: bool = True
    reason: str = ""
    discharge_clipped_kwh: float = 0.0


def _check_inputs(demand, solar, tariff):
    if not (len(demand) == len(solar) == len(tariff)):
        raise ValueError("demand, solar and tariff must have equal length")


def simulate(
    actions: Sequence[float],
    demand: Sequence[float],
    solar: Sequence[float],
    tariff: Sequence[float],
    p: BatteryParams,
    strict: bool = True,
) -> Trajectory:
    """Apply a schedule.

    strict=True  : planning mode. Any violated constraint marks the schedule
                   infeasible (the first violation is recorded in `reason`).
    strict=False : execution mode with REALIZED demand. If discharge would
                   exceed what the load can absorb (export), discharge is
                   clipped to the absorbable amount and the clipped energy is
                   recorded. Battery bounds and terminal rule are still
                   checked and flagged, not silently repaired.
    """
    _check_inputs(demand, solar, tariff)
    H = len(demand)
    if len(actions) != H:
        raise ValueError("schedule length must equal horizon")
    tr = Trajectory(actions=tuple(actions))
    e = p.initial_kwh
    tr.energy.append(e)
    for t in range(H):
        a = float(actions[t])
        charge = max(a, 0.0)
        discharge = max(-a, 0.0)
        net = demand[t] + charge - discharge
        if net < -TOL:
            if strict:
                tr.feasible, tr.reason = False, f"t={t}: discharge exceeds load (export disabled)"
                return tr
            # execution mode: clip discharge so that net == 0
            clipped = -net
            discharge -= clipped
            tr.discharge_clipped_kwh += clipped * p.dt_h
            net = 0.0
        net = max(net, 0.0)
        solar_used = min(solar[t], net)
        grid = net - solar_used
        e_next = e + p.eta_charge * charge * p.dt_h - discharge * p.dt_h / p.eta_discharge
        if e_next > p.capacity_kwh + TOL or e_next < p.e_min_kwh - TOL:
            tr.feasible = False
            tr.reason = tr.reason or f"t={t}: battery bound violated (E={e_next:.4f})"
            if strict:
                return tr
        e = e_next
        tr.energy.append(e)
        tr.grid_import.append(grid)
        tr.solar_used.append(solar_used)
        tr.curtailment.append(solar[t] - solar_used)
        tr.charge.append(charge)
        tr.discharge.append(discharge)
        tr.cost += tariff[t] * grid * p.dt_h
        tr.throughput_kwh += (charge + discharge) * p.dt_h
    tr.cost += p.throughput_cost_per_kwh * tr.throughput_kwh
    tr.peak_import_kw = max(tr.grid_import) if tr.grid_import else 0.0
    if p.terminal_min_kwh is not None and tr.energy[-1] < p.terminal_min_kwh - TOL:
        tr.feasible = False
        tr.reason = tr.reason or (
            f"terminal energy {tr.energy[-1]:.4f} < required {p.terminal_min_kwh:.4f}"
        )
    return tr


def exact_schedule(demand, solar, tariff, p: BatteryParams):
    """Enumerate every schedule in actions_kw^H and return the optimum.

    Tie-break (deterministic): lowest cost, then lowest throughput, then
    lexicographically smallest action tuple. Returns (Trajectory, n_total,
    n_feasible). Returns (None, n_total, 0) if nothing is feasible.
    """
    _check_inputs(demand, solar, tariff)
    H = len(demand)
    best, best_key = None, None
    n_total = n_feasible = 0
    for sched in product(p.actions_kw, repeat=H):
        n_total += 1
        tr = simulate(sched, demand, solar, tariff, p, strict=True)
        if not tr.feasible:
            continue
        n_feasible += 1
        key = (round(tr.cost, 12), round(tr.throughput_kwh, 12), sched)
        if best_key is None or key < best_key:
            best, best_key = tr, key
    return best, n_total, n_feasible


def baseline_no_battery(demand, solar, tariff, p: BatteryParams) -> Trajectory:
    """All-zero schedule. Useful as a savings reference."""
    return simulate((0.0,) * len(demand), demand, solar, tariff, p, strict=False)
