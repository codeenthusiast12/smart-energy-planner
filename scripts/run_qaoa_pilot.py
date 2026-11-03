"""Fixed-budget S01 p=1 ideal-statevector QAOA pilot; no hardware claims."""
from pathlib import Path
import csv
import hashlib
import json
import platform
import sys
from datetime import datetime, timezone
from time import perf_counter
import numpy as np
import scipy
from scipy.optimize import minimize

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from qaoa_statevector import state_probabilities, sample_metrics


def main():
    out=ROOT/'results'
    raw=json.loads((out/'scenario_01_cost_diagonal.json').read_text())
    energies=np.array(raw['energies'],dtype=float)
    feasible=np.array(raw['feasible'],dtype=bool)
    valid=np.array(raw['valid'],dtype=bool)
    cost_scale=raw['penalty_cu']
    normalized=energies/cost_scale
    optimum=energies[feasible].min()
    optimal=feasible & np.isclose(energies,optimum,atol=1e-12,rtol=0)
    config=dict(scenario='S01',status='exploratory pilot',p=1,seeds=[42,7,21,123,2026],
                optimizer='COBYLA',max_function_evaluations=200,tolerance=1e-6,
                rhobeg=.5,gamma_bounds=[0,2*np.pi],beta_bounds=[0,np.pi],
                shots_per_method_per_seed=1024,cost_scale_cu=cost_scale,
                objective='exact expectation of E/P, including infeasible penalties',
                initialization='uniform superposition; random angles uniform in bounds',
                baselines=['uniform_bitstrings','uniform_valid_action_codes'],
                simulator='NumPy direct statevector; no Qiskit or hardware execution',
                created_at_utc=datetime.now(timezone.utc).isoformat())
    # Save protocol before executing any optimization run.
    (out/'qaoa_pilot_protocol.json').write_text(json.dumps(config,indent=2)+'\n')
    rows=[];runs=[];saved_probs={}
    baseline_probs={'uniform_bitstrings':np.ones(len(energies))/len(energies),
                    'uniform_valid_action_codes':valid.astype(float)/valid.sum()}
    for seed in config['seeds']:
        streams=np.random.SeedSequence(seed).spawn(4)
        initial_rng=np.random.default_rng(streams[0])
        x0=initial_rng.uniform([0,0],[2*np.pi,np.pi])
        trace=[]
        def objective(x):
            value=float(state_probabilities(normalized,x) @ normalized)
            trace.append(dict(evaluation=len(trace)+1,parameters=x.tolist(),normalized_expectation=value))
            return value
        start=perf_counter()
        result=minimize(objective,x0,method='COBYLA',bounds=[(0,2*np.pi),(0,np.pi)],
                        options={'maxiter':200,'tol':1e-6,'rhobeg':.5,'catol':1e-8})
        elapsed=perf_counter()-start
        probs=state_probabilities(normalized,result.x)
        saved_probs[f'seed_{seed}']=probs
        run=dict(seed=seed,initial_parameters=x0.tolist(),parameters=result.x.tolist(),
                 success=bool(result.success),message=str(result.message),nfev=int(result.nfev),
                 training_seconds=elapsed,trace=trace,sampling={})
        methods={'qaoa_p1':probs,**baseline_probs}
        for j,(name,probabilities) in enumerate(methods.items()):
            sample=sample_metrics(probabilities,energies,feasible,1024,np.random.default_rng(streams[j+1]))
            run['sampling'][name]=sample
            pfeas=float(probabilities[feasible].sum())
            popt=float(probabilities[optimal].sum())
            row=dict(seed=seed,method=name,feasible_probability=pfeas,optimum_probability=popt,
                     probability_hit_optimum_in_1024=float(-np.expm1(1024*np.log1p(-popt))),
                     conditional_feasible_mean_cost_cu=float(probabilities[feasible]@energies[feasible]/pfeas) if pfeas else None,
                     penalized_expected_energy_cu=float(probabilities@energies),
                     feasible_samples=sample['feasible_samples'],optimum_samples=sample['optimum_samples'],
                     best_feasible_cost_cu=sample['best_feasible_cost_cu'],gap_cu=sample['gap_cu'],
                     optimizer_success=bool(result.success) if name=='qaoa_p1' else '',
                     nfev=int(result.nfev) if name=='qaoa_p1' else 0,
                     training_seconds=elapsed if name=='qaoa_p1' else 0)
            rows.append(row)
        runs.append(run)
        print(f"seed={seed} feasible={rows[-3]['feasible_probability']:.4%} optimum={rows[-3]['optimum_probability']:.4%} sampled_best={rows[-3]['best_feasible_cost_cu']} nfev={result.nfev} success={result.success}",flush=True)
    with (out/'table_06_qaoa_pilot_by_seed.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    metadata=dict(protocol=config,environment={'python':platform.python_version(),'numpy':np.__version__,
                  'scipy':scipy.__version__,'platform':platform.platform()},exact_optimum_cu=float(optimum),runs=runs,
                  sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in
                          ['src/qaoa_statevector.py','scripts/run_qaoa_pilot.py','results/scenario_01_cost_diagonal.json']})
    (out/'qaoa_pilot_runs.json').write_text(json.dumps(metadata,indent=2)+'\n')
    np.savez_compressed(out/'qaoa_pilot_probabilities.npz',**saved_probs)
    plot(rows)


def plot(rows):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    methods=['uniform_bitstrings','uniform_valid_action_codes','qaoa_p1']
    labels=['Uniform bitstrings','Uniform action codes','QAOA, p = 1']
    colors=['#8895A4','#27856C','#176B99']
    fig,axes=plt.subplots(1,2,figsize=(10,4.5),layout='constrained')
    for ax,metric,title in zip(axes,['feasible_probability','optimum_probability'],['(a) Probability of a feasible schedule','(b) Probability of the exact optimum']):
        for i,method in enumerate(methods):
            values=[100*r[metric] for r in rows if r['method']==method]
            mean=np.mean(values)
            ax.scatter([mean],[i],color=colors[i],s=70,zorder=3)
            if method=='qaoa_p1':
                ax.scatter(values,i+np.linspace(-.13,.13,len(values)),color=colors[i],alpha=.55,s=20,zorder=3)
                ax.errorbar(mean,i,xerr=np.std(values,ddof=1),fmt='none',ecolor=colors[i],capsize=4)
        ax.set_yticks(range(3),labels)
        ax.invert_yaxis()
        ax.set_xlim(left=0)
        ax.set_xlabel('Probability per draw (%)')
        ax.set_title(title,fontsize=11)
        ax.grid(axis='x',alpha=.18)
    fig.suptitle('S01: first QAOA simulation versus random sampling\nExact statevector probabilities; five QAOA initializations',fontsize=13,fontweight='bold')
    fig.supxlabel('Small dots: individual seeds · Large dots: means · Intervals: ±1 sample SD\nSynthetic four-hour scenario; dense diagonal oracle; no hardware execution',fontsize=9)
    target=ROOT/'figures'/'fig_03_qaoa_pilot_probabilities'
    fig.savefig(target.with_suffix('.png'),dpi=220)
    fig.savefig(target.with_suffix('.pdf'))
    plt.close(fig)


if __name__=='__main__':main()
