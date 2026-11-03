# Figures and captions

Figure numbers are provisional working-paper references. Supplementary figures preserve the exploratory record. Refer to figures by number in the manuscript and use descriptive filenames when inserting artwork.

## Figure 1. Validation forecasting performance

![Figure 1. Validation forecasting performance](fig_01_validation_forecasting_performance.png)

**Caption.** Forecasting performance under the corrected 500-example protocol, using the same selected training examples from 2007–2008 and 8,602 validation hours from 2009. Scaling for neural-network and VQC inputs was fitted exclusively on the selected training examples. Points show recorded MAE; intervals show ±1 sample standard deviation across five predefined seeds for the neural network and Random Forest. Linear regression and persistence are deterministic references. The two-block VQC point represents seed 42 only; no variability estimate is available. Two neural-network runs raised convergence warnings, and the VQC reached its 50-iteration limit. These validation results do not establish statistical superiority or quantum advantage.

[PNG](fig_01_validation_forecasting_performance.png) · [Vector PDF](fig_01_validation_forecasting_performance.pdf) · [Source table](../results/table_01_forecasting_performance_summary.csv)

Reproduce with `python scripts/plot_forecasting_results.py`.

## Figure S1. Household demand profile

![Figure S1. Household demand profile](fig_S1_household_demand_profile.png)

**Caption.** Hourly mean household active-power demand on 17 December 2006. Hour labels indicate interval start times. This descriptive example illustrates intraday variation; it is not a forecast evaluation or a representative-performance claim.

Stored exploratory figure preserved without alteration. Provenance: original notebook cell 13.

## Figure S2. Linear-regression demand predictions

![Figure S2. Linear-regression demand predictions](fig_S2_linear_regression_demand_predictions.png)

**Caption.** Observed and predicted hourly demand on 1 January 2009 for the exploratory two-input linear-regression model using previous-hour and previous-day demand. This single-day illustration is from the earlier experiment, not the corrected four-input limited-data comparison.

Stored exploratory figure preserved without alteration. Provenance: original notebook cell 31.

## Figure S3. Pilot forecasting comparison

![Figure S3. Pilot forecasting comparison](fig_S3_pilot_forecasting_comparison.png)

**Caption.** Single-run validation MAE for the initial 500-example forecasting experiments. Neural-network and quantum inputs use the pilot scaler fitted on the full training pool. The dashed line represents persistence on the same validation rows. The two-block VQC and neural network reached their iteration limits without confirmed convergence. This pilot figure must not be presented as the corrected result in Figure 1.

Stored exploratory figure preserved without alteration. Provenance: original notebook cell 72.
