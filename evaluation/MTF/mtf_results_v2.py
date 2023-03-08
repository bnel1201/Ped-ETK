# %%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
# %%
ctp404_results = pd.read_csv('/home/brandon.nelson/Dev/DLIR_Ped_Generalizability/geometric_phantom_studies/results/MTF/MTF_results.csv')
ctp404_results.rename(columns={'phantom_diameter_mm': 'Diameter [mm]'}, inplace=True)
ctp404_results = ctp404_results[ctp404_results['Diameter [mm]'] < 300]
ctp404_results = ctp404_results[ctp404_results['Diameter [mm]'] != 150]
# %%
sns.lineplot(x='fov_size_mm', y='MTF25', hue='expected_HU', style='recon', data=ctp404_results)
# %%
sns.lineplot(x='fov_size_mm', y='measured_HU', style='recon', hue='expected_HU', data=ctp404_results)

# %%
ctp404_results['HU error'] = ctp404_results['measured_HU'] - ctp404_results['expected_HU']
# %%
sns.lineplot(x='fov_size_mm', y='HU error', hue='expected_HU', style='recon', data=ctp404_results)
# %%
HU_errors = ctp404_results[ctp404_results['recon'] != 'fbp']['measured_HU'].to_numpy() - ctp404_results[ctp404_results['recon'] == 'fbp']['measured_HU'].to_numpy()
HU_error_df = ctp404_results[ctp404_results['recon'] != 'fbp'][['Diameter [mm]', 'fov_size_mm', 'expected_HU']].copy()
HU_error_df['HU error'] = HU_errors
HU_error_df
# %%
f, ax = plt.subplots(figsize=(4, 3))
plot = sns.lineplot(ax=ax, x='Diameter [mm]', y='HU error', hue='expected_HU', data=HU_error_df, palette='crest')
handles, labels = plot.get_legend_handles_labels()
ax.set_ylabel('HU Error\nDLIR - FBP')
plot.get_legend().remove()
f.legend(handles, labels, ncol=3, loc='upper center', 
                bbox_to_anchor=(0.5, 1.2), frameon=False, title='Contrast [HU]')
f.tight_layout()
f.savefig('hu_accuracy.png', dpi=600, bbox_inches='tight')
# %%
