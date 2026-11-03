# Recorded forecasting results

Recorded validation results from the uploaded notebook, rounded to four decimals. No model was retrained to prepare this report. Final held-out test results and operational/QAOA results are not yet available.

## Table 1. Forecasting performance under corrected preprocessing

| Model | Validation MAE (kW) | Sample SD (kW) | Training runs | Training status |
|---|---:|---:|---:|---|
| Neural network | **0.3960** | 0.0049 | 5 | Two runs raised convergence warnings |
| Linear regression | 0.4147 | — | 1 | Deterministic fitted reference |
| Two-block VQC | 0.4149 | — | 1 | Seed 42; iteration limit reached |
| Random Forest | 0.4234 | 0.0023 | 5 | Five predefined seeds |
| Persistence | 0.4291 | — | 0 | Untrained reference |

**Caption.** Forecasting performance on 8,602 validation hours from 2009 using 500 fixed training examples from 2007–2008. Where required, scaling was fitted only on those 500 examples. MAE is averaged across runs for models with five seeds; VQC has one completed corrected run. SD describes model randomness on a fixed sample, not a confidence interval or cross-dataset uncertainty. A dash means no variability estimate, not zero variability. Aggregate statistics are the values printed by the notebook from its in-memory results.

[Table 1 CSV](table_01_forecasting_performance_summary.csv) · [Figure 1](../figures/README.md)

## Table 2. Validation error by random seed

| Seed | Neural network MAE (kW) | Random Forest MAE (kW) | Two-block VQC MAE (kW) |
|---|---:|---:|---:|
| 42 | 0.3917 | 0.4243 | 0.4149 |
| 7 | 0.3938 | 0.4266 | Pending |
| 21 | 0.3944 | 0.4234 | Pending |
| 123 | 0.4044 | 0.4220 | Pending |
| 2026 | 0.3954 | 0.4208 | Pending |

**Caption.** Individual validation MAEs for the predefined model seeds under corrected preprocessing. Training rows, features, and validation timestamps remain fixed. Pending VQC runs are not zeros. CSV values were transcribed from rounded output; export full-precision live-runtime metrics before subsequent statistical analysis.

[Table 2 CSV](table_02_forecasting_results_by_seed.csv)

## Table 3. Training termination and runtime

| Model | Seed | Iterations | Training time (s) | Reported termination |
|---|---:|---:|---:|---|
| Neural network | 42 | 500 | 0.8538 | No convergence warning recorded |
| Neural network | 7 | 500 | 0.9329 | Convergence warning |
| Neural network | 21 | 500 | 1.0994 | Convergence warning |
| Neural network | 123 | 240 | 0.8722 | No convergence warning recorded |
| Neural network | 2026 | 442 | 1.4097 | No convergence warning recorded |
| Two-block VQC | 42 | 50 | 478.4 | Iteration limit; success=False |

**Caption.** Training diagnostics recorded in the uploaded notebook. Absence of warnings is not proof of global optimality. MLP and VQC iterations represent different computations. Timings come from the respective Colab runs, not a controlled hardware benchmark; they do not establish a quantum speedup. Corrected VQC training MSE was 0.4177 kW².

## Supporting record

[Experiment execution log](experiment_execution_log.txt) preserves printed outputs. Historical pilots remain in the notebook and [experiment diary](../docs/EXPERIMENT_LOG.md), separate from the corrected tables. Notebook cell identifiers are retained only for provenance, not as manuscript titles.
