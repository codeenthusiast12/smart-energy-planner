"""Reproduce synthetic scenario S01, full-precision outputs, and Figure 2."""
from pathlib import Path
from dataclasses import asdict
import csv
import hashlib
import json
import platform
import sys
from itertools import product

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from battery_scheduler import BatteryParams, exact_schedule, baseline_no_battery, simulate


def main():
    p = BatteryParams(capacity_kwh=5.0, e_min_kwh=0.5, initial_kwh=2.5,
                      eta_charge=0.95, eta_discharge=0.95, dt_h=1.0,
                      actions_kw=(-2.0, -1.0, 0.0, 1.0, 2.0),
                      terminal_min_kwh=2.5, throughput_cost_per_kwh=0.0)
    demand = [1.0, 1.0, 1.0, 1.0]
    solar = [0.0, 1.5, 2.5, 0.5]
    tariff = [0.12, 0.15, 0.30, 0.35]
    best, total, feasible = exact_schedule(demand, solar, tariff, p)
    idle = baseline_no_battery(demand, solar, tariff, p)
    assert best is not None and best.feasible and idle.feasible
    # Check the exported optimum against the equations independently of simulator code.
    for t, a in enumerate(best.actions):
        balance = best.grid_import[t] + best.solar_used[t] + max(-a, 0) - demand[t] - max(a, 0)
        update = best.energy[t] + .95 * max(a, 0) - max(-a, 0) / .95
        assert abs(balance) < 1e-9 and abs(update - best.energy[t+1]) < 1e-9
        assert p.e_min_kwh - 1e-9 <= best.energy[t+1] <= p.capacity_kwh + 1e-9
    assert best.energy[-1] >= p.terminal_min_kwh - 1e-9
    assert abs(best.cost - sum(tariff[t] * best.grid_import[t] for t in range(4))) < 1e-9
    out = ROOT / 'results'
    out.mkdir(exist_ok=True)
    payload = dict(scenario_id='S01', data_kind='synthetic illustrative scenario; no forecasts',
                   currency='arbitrary currency units (CU); not a measured tariff',
                   intervals=['H1', 'H2', 'H3', 'H4'], demand_kw=demand,
                   solar_kw=solar, tariff_cu_per_kwh=tariff, battery=asdict(p),
                   total_schedules=total, feasible_schedules=feasible,
                   exact=asdict(best), idle_battery=asdict(idle),
                   cost_reduction_cu=idle.cost-best.cost,
                   cost_reduction_percent=100*(idle.cost-best.cost)/idle.cost,
                   python_version=platform.python_version(),
                   scheduler_sha256=hashlib.sha256((ROOT/'src/battery_scheduler.py').read_bytes()).hexdigest())
    (out/'scenario_01_exact_scheduling.json').write_text(json.dumps(payload, indent=2)+'\n')
    with (out/'table_04_four_hour_battery_schedule.csv').open('w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['interval','demand_kw','solar_kw','tariff_cu_per_kwh','action_kw','energy_start_kwh','energy_end_kwh','grid_import_kw','curtailment_kw','interval_cost_cu','idle_grid_import_kw'])
        for t in range(4):
            writer.writerow([f'H{t+1}',demand[t],solar[t],tariff[t],best.actions[t],best.energy[t],best.energy[t+1],best.grid_import[t],best.curtailment[t],tariff[t]*best.grid_import[t],idle.grid_import[t]])
    with (out/'scenario_01_enumerated_schedules.csv').open('w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['action_h1_kw','action_h2_kw','action_h3_kw','action_h4_kw','feasible','feasible_cost_cu','reason'])
        for actions in product(p.actions_kw, repeat=4):
            tr = simulate(actions,demand,solar,tariff,p)
            writer.writerow([*actions,tr.feasible,tr.cost if tr.feasible else '',tr.reason])
    print(json.dumps({k:payload[k] for k in ['total_schedules','feasible_schedules','cost_reduction_cu','cost_reduction_percent']}, indent=2))
    print('Actions:',best.actions,'Energy:',best.energy,'Costs:',idle.cost,best.cost)
    plot(payload)


def plot(data):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,
                         'axes.spines.right':False,'svg.fonttype':'none'})
    fig, axes = plt.subplots(4,1,figsize=(9,10),gridspec_kw={'height_ratios':[1,0.7,1,1]},layout='constrained')
    blue, green, orange = '#176B99','#27856C','#BA5B25'
    xs = [0.5,1.5,2.5,3.5]
    def step(ax, vals, **kw):
        ax.stairs(vals,[0,1,2,3,4],baseline=None,**kw)
    step(axes[0],data['demand_kw'],color='#3C4858',label='Demand',linewidth=2)
    step(axes[0],data['solar_kw'],color=green,label='Available solar',linewidth=2)
    axes[0].set(ylabel='Power (kW)',title='(a) Synthetic demand and solar')
    axes[0].legend(loc='upper left',ncol=2,frameon=False)
    step(axes[1],data['tariff_cu_per_kwh'],color=orange,linewidth=2)
    axes[1].set(ylabel='CU / kWh',title='(b) Assumed electricity tariff',ylim=(0,.42))
    a=data['exact']['actions']
    axes[2].bar(xs,a,width=.65,color=[blue if x>=0 else orange for x in a])
    for x,y in zip(xs,a):
        axes[2].annotate(f'{y:+.0f}',(x,y),xytext=(0,5 if y>=0 else -14),textcoords='offset points',ha='center')
    axes[2].axhline(0,color='#55606B',linewidth=.8)
    axes[2].set(ylabel='Battery power (kW)',title='(c) Exact schedule: positive = charge; negative = discharge',ylim=(-1.6,2.6))
    axes[3].plot(range(5),data['exact']['energy'],marker='o',color=blue,linewidth=2,label='Stored energy')
    axes[3].axhline(2.5,color='#687482',linestyle='--',label='Terminal minimum (2.5 kWh)')
    axes[3].set(ylabel='Stored energy (kWh)',title='(d) Energy at interval boundaries',ylim=(0,5.5),xlabel='Elapsed time (hours)')
    axes[3].axhline(.5,color='#AAB2BB',linestyle=':',linewidth=1)
    axes[3].axhline(5,color='#AAB2BB',linestyle=':',linewidth=1)
    axes[3].legend(loc='lower left',ncol=2,frameon=False)
    for ax in axes:
        ax.set_xlim(0,4)
        ax.grid(axis='y',alpha=.17)
        ax.set_axisbelow(True)
    for ax in axes[:3]:
        ax.set_xticks(xs,['H1','H2','H3','H4'])
    axes[3].set_xticks(range(5))
    fig.suptitle('Four-hour solar–battery scheduling reference\nSynthetic scenario S01 · exact enumeration',fontsize=15,fontweight='bold')
    target=ROOT/'figures'/'fig_02_four_hour_battery_schedule'
    target.parent.mkdir(exist_ok=True)
    fig.savefig(target.with_suffix('.png'),dpi=220)
    fig.savefig(target.with_suffix('.svg'))
    fig.savefig(target.with_suffix('.pdf'))
    plt.close(fig)


if __name__ == '__main__':
    main()
