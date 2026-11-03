# Smart Energy Planner

**VQC demand forecasting and QAOA battery scheduling — undergraduate research in progress**

Ilias Moulouki · Computer Science, Artificial Intelligence specialization · Al Akhawayn University

This capstone investigates whether differences in demand forecasts translate into better battery-scheduling decisions in a small simulated solar–battery microgrid. Classical forecasting models provide reference performance for variational quantum regression. The planned scheduling study compares QAOA with exact solutions to the same small discrete problem.

## Current status

Forecasting is implemented. Battery scheduling, QAOA, and integrated operational evaluation are **not yet implemented**. No quantum advantage, operational savings, or final test performance is claimed.

The notebook includes the exploration history and a corrected limited-data experiment. The corrected protocol uses 500 fixed training examples from 2007–2008, 8,602 validation examples from 2009, and preprocessing fitted exclusively on those 500 training examples. The 2010 test period remains reserved.

| Model | Validation MAE (kW) | Across-seed sample SD (kW) | Runs |
|---|---:|---:|---:|
| Persistence | 0.4291 | — | Deterministic |
| Linear regression | 0.4147 | — | 1 |
| Random Forest | 0.4234 | 0.0023 | 5 |
| Neural network | 0.3960 | 0.0049 | 5 |
| Two-block VQC | 0.4149 | Not yet available | 1 |

VQC seed 42 reached the 50-iteration limit: training MSE 0.4177 kW², runtime 478.4 seconds, no confirmed convergence. Two neural-network runs raised convergence warnings. Do not compare one VQC run with the classical averages as evidence of statistical superiority. The notebook uses statevector simulation, not quantum hardware.

## Research figures and tables

- [Figure 1 and supplementary figures](figures/README.md): descriptive filenames, numbered captions, and a vector PDF for the corrected comparison.
- [Tables 1–3: recorded forecasting results](results/README.md): summary, individual seeds, and training diagnostics.

![Figure 1. Validation forecasting performance](figures/fig_01_validation_forecasting_performance.png)

Intervals show across-seed sample SD where five runs are available. VQC has one corrected run.

## Repository contents

- `notebooks/Smart_Energy_Planner.ipynb`: original code and stored outputs, with added section headings.
- `docs/PAPER_BLUEPRINT.md`: full paper outline, completed work, remaining methods, results placeholders, and diary template.
- `docs/ROADMAP.md`: four-week priorities and completion criteria.
- `docs/EXPERIMENT_LOG.md`: experiment summaries and limitations.
- `docs/NOTEBOOK_REVIEW.md`: review findings and reproducibility gaps.
- `docs/NOTEBOOK_PROVENANCE.json`: original upload fingerprint and cell mapping.
- `results/table_02_forecasting_results_by_seed.csv`: per-seed values transcribed from rounded printed outputs.
- `results/experiment_execution_log.txt`: stored stream outputs exported from the notebook.
- `figures/`: existing notebook figures; see their README for pilot labeling.
- `scripts/validate_notebook.py`: structural and Python syntax checks, without running training.
- `scripts/capture_environment.py`: record actual package versions in the runtime executing it.

## Run in Google Colab

1. Open Google Colab and choose **File → Open notebook → GitHub** after the repository is uploaded, or upload the notebook directly.
2. Run cells in order. The notebook downloads UCI dataset 235 and installs its UCI and Qiskit dependencies.
3. Quantum runs can take several minutes each. A full run repeats exploratory training too; do not use Run all merely to inspect saved results.
4. Keep the final test period unused while developing methods.
5. Save the notebook back to the repository after meaningful milestones. Commit the updated results and document what changed.

The notebook's installation cells are currently unpinned. For a controlled rerun, use the dependency file and record actual installed versions before experimentation. The dependency file lists imported packages and pins the observed Qiskit version; it is **not** a complete environment lock.

## Local setup (optional)

```bash
python -m venv .venv
# Activate the environment using your platform's command.
python -m pip install -r requirements.txt
python scripts/validate_notebook.py
python scripts/capture_environment.py
```

Use a Jupyter-capable editor or install Jupyter separately to execute the notebook locally. Python 3.13 was reported in the original Colab environment; this package has not undergone a complete clean-environment rerun.

## Data and reproducibility

Demand comes from UCI's Individual Household Electric Power Consumption dataset (`fetch_ucirepo(id=235)`). Raw data are downloaded at runtime, not included in the repository. Verify the dataset citation and redistribution terms before including raw data elsewhere.

Original pilot preprocessing used the full training pool. Only the corrected section fits scaling on the selected 500 examples. Do not combine these protocols in a final-results table. Saved notebook outputs are evidence from the uploaded file; they were not regenerated while packaging this repository. Per-run CSV values are rounded and cannot replace full-precision exports from a live runtime.

## Next milestone

Implement a four-hour battery simulator and exact discrete scheduler. Verify energy balance, battery bounds, efficiency, and terminal energy before implementing QAOA on the identical problem. Forecasting improvements alone do not demonstrate energy-cost savings.

## Publication and licensing

This is a working research repository. A software license has not yet been selected. Dataset terms remain separate. Confirm the supervisor's publication expectations before making the repository public.
