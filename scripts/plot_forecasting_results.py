"""Render Figure 1 from recorded summary values without retraining models."""
from pathlib import Path
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
ROOT = Path(__file__).resolve().parents[1]
with (ROOT / 'results/table_01_forecasting_performance_summary.csv').open() as f:
    rows = list(csv.DictReader(f))
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'pdf.fonttype':42})
fig, ax = plt.subplots(figsize=(9,5.0))
fig.subplots_adjust(left=.25,right=.75,bottom=.31,top=.78)
for i,row in enumerate(rows):
    quantum = row['model']=='Two-block VQC'
    color = '#176B91' if quantum else '#465667'
    sd = float(row['sample_sd_kw']) if row['sample_sd_kw'] else None
    value = float(row['validation_mae_kw'])
    ax.errorbar(value,i,xerr=sd,fmt='D' if quantum else 'o',color=color,
                markersize=7,capsize=4,elinewidth=1.6,zorder=3)
    label=f'{value:.4f}'+(f' ± {sd:.4f}' if sd is not None else '')
    ax.text(1.06,i,label,transform=ax.get_yaxis_transform(),va='center',
            color=color,fontweight='bold' if quantum else 'normal')
ax.set_yticks(range(len(rows)),[r['model'] for r in rows])
ax.set_ylim(len(rows)-.5,-.6)
ax.set_xlim(.38,.44)
ax.xaxis.set_major_locator(MultipleLocator(.01))
ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
ax.grid(axis='x',color='#E3E8ED',linewidth=.8)
ax.set_axisbelow(True)
ax.tick_params(axis='both',length=0,pad=8)
for side in ['top','right','left']: ax.spines[side].set_visible(False)
ax.spines['bottom'].set_color('#BBC5CE')
ax.set_xlabel('Validation MAE (kW) — lower is better',labelpad=12)
ax.text(1.06,1.07,'MAE ± SD (kW)',transform=ax.transAxes,fontsize=9,fontweight='bold')
fig.text(.06,.94,'Demand forecasting performance',fontsize=16,fontweight='bold',color='#172B40')
fig.text(.06,.875,'500 training examples · 8,602 validation hours · corrected preprocessing',fontsize=10,color='#566574')
fig.text(.06,.055,'Intervals: ±1 sample SD across five seeds for the neural network and Random Forest.\nVQC: one run; uncertainty not yet estimated. Validation results, not final test results.',fontsize=9,color='#566574',linespacing=1.5)
for ext in ['png','pdf']:
    fig.savefig(ROOT/f'figures/fig_01_validation_forecasting_performance.{ext}',dpi=300,bbox_inches='tight',facecolor='white')
plt.close(fig)
print('Saved Figure 1 as PNG and vector PDF.')
