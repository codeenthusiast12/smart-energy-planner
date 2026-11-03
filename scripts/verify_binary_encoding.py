"""Exhaustively verify S01 binary encoding before QAOA optimization."""
from pathlib import Path
import json
import sys
import hashlib
from itertools import product

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
from battery_scheduler import BatteryParams, exact_schedule, simulate
from binary_encoding import encode_schedule, decode_index, build_diagonal


def main():
    scenario = json.loads((ROOT/'results/scenario_01_exact_scheduling.json').read_text())
    p = BatteryParams(**{**scenario['battery'], 'actions_kw':tuple(scenario['battery']['actions_kw'])})
    demand, solar, tariff = (scenario[k] for k in ['demand_kw','solar_kw','tariff_cu_per_kwh'])
    diagonal = build_diagonal(demand, solar, tariff, p)
    seen = set()
    for schedule in product(p.actions_kw, repeat=4):
        index = encode_schedule(schedule,p.actions_kw)
        assert index not in seen
        seen.add(index)
        assert decode_index(index,4,p.actions_kw) == schedule
        tr = simulate(schedule,demand,solar,tariff,p)
        assert diagonal['feasible'][index] == tr.feasible
        if tr.feasible:
            assert abs(diagonal['energies'][index]-tr.cost) < 1e-12
    for i, valid in enumerate(diagonal['valid']):
        assert valid == (i in seen)
        if not diagonal['feasible'][i]:
            assert diagonal['energies'][i] == diagonal['penalty_cu']
    best, total, feasible = exact_schedule(demand,solar,tariff,p)
    minimum = min(diagonal['energies'])
    ground = [i for i,e in enumerate(diagonal['energies']) if abs(e-minimum)<1e-12]
    assert all(diagonal['feasible'][i] for i in ground)
    assert abs(minimum-best.cost)<1e-12
    assert len(seen)==total==625 and sum(diagonal['feasible'])==feasible==68
    assert max(e for e,f in zip(diagonal['energies'],diagonal['feasible']) if f) < diagonal['penalty_cu']
    # Hand-derived ordering check: H4 H3 H2 H1 = 001 011 011 010.
    expected = int('001011011010',2)
    assert encode_schedule((0.0,1.0,1.0,-1.0),p.actions_kw)==expected
    assert decode_index(7,4,p.actions_kw) is None
    result = dict(scenario_id='S01', verification='passed',qubits=diagonal['qubits'],
                  basis_states=len(diagonal['energies']),valid_action_schedules=total,
                  unused_code_states=len(diagonal['energies'])-total,
                  physically_infeasible_schedules=total-feasible,feasible_schedules=feasible,
                  uniform_feasible_probability=feasible/len(diagonal['energies']),
                  feasible_cost_upper_bound_cu=diagonal['upper_bound_cu'],penalty_cu=diagonal['penalty_cu'],
                  ground_energy_cu=minimum,ground_state_count=len(ground),ground_state_indices=ground,
                  ground_state_bitstrings=[format(i,'012b') for i in ground],
                  exact_selected_index=expected,exact_selected_bitstring=format(expected,'012b'),
                  qaoa_training_performed=False,
                  source_hashes={name:hashlib.sha256((ROOT/'src'/name).read_bytes()).hexdigest() for name in ['binary_encoding.py','battery_scheduler.py']})
    (ROOT/'results/scenario_01_encoding_verification.json').write_text(json.dumps(result,indent=2)+'\n')
    (ROOT/'results/scenario_01_cost_diagonal.json').write_text(json.dumps(diagonal,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
