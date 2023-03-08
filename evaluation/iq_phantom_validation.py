"""
The goal of this script is to correlate the RMSE reduction of DLIR in IQ phantoms to that in the anthropomorphic XCAT phantoms
Since we have ground truth phantoms for each we can caluclate RMSE for each. Normally, when scanning physical phantoms
we do not have access to ground truth so when we measure a uniform region we assume it to be uniform and that its `true` std noise 
is zero, thus when we measure the std `noise` following noise reduction we assume we are getting closer to the true underlying sample.

The purpose of this figure is to provide evidence that the noise reduction we are characterizing on the image quality phantoms is representative
of that achieved in patients, which we model here as anthropomorphic phantoms. This is important to do since these models were trained on patient data
and we are evaluating on phantoms. While, some argue that the these models won't generalize, these plots suggest that these models aren't so 
concerned with anatomy and organs as they are local noise textures influence by FOV size. This makes sense since these models are built upon convolutions
which are sensitive to texture and local frequencies.
"""

# %%
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
anthro_results = pd.read_csv('/home/brandon.nelson/Dev/DLIR_Ped_Generalizability/geomtric_phantom_studies/results/anthropomorphic/anthro_mse_dataset.csv')
anthro_results['Dose [%]'] = 100*anthro_results['Dose (photons)']/anthro_results['Dose (photons)'].max()
anthro_results['Dose [%]'] = anthro_results['Dose [%]'].astype(int)
anthro_results.replace({'cnn': 'DLIR', 'fbp': 'FBP'}, inplace=True)
anthro_results['Diameter [mm]'] = anthro_results['effective diameter (cm)']*10
anthro_results
# %%
iq_results = pd.read_csv('/home/brandon.nelson/Dev/DLIR_Ped_Generalizability/geomtric_phantom_studies/results/NPS/NPS_results.csv')
iq_results.rename(columns = {'rmse': 'RMSE', 'phantom_diameter_mm': 'Diameter [mm]', 'dose_level_pct': 'Dose [%]'}, inplace=True)
iq_results = iq_results[iq_results['Diameter [mm]'] != 200]
iq_results.replace({'dl_REDCNN': 'DLIR', 'fbp': 'FBP'}, inplace=True)
iq_results

# %% [markdown]
## rmse vs phantom diameter across different dose levels and recon types
### IQ Phantom
# We see that as phantom diameter increases the RMSE decreases, this is primarily due to reduced
# influence of spatial resolution being less of an influence at large patient diameters.
# DL noise reduction reduces RMSE more effectively at larger diameters and lower doses.
sns.lineplot(x='Diameter [mm]', y='RMSE', style='recon', hue='Dose [%]', data=iq_results, palette='crest')
# %% [markdown]
### Anthropomorphic Phantom
# With anthropomorphic phantoms based upon real patients the results are expectedly noisier but exhibit a similar trend that
# at higher effective diameters the DL model is more effective at reducing RMSE than at smaller diameters
sns.lineplot(x='Diameter [mm]', y='RMSE', style='recon', hue='Dose [%]', data=anthro_results, palette='crest')
# %%
f, axs = plt.subplots(1, 2, sharey=True, tight_layout=True, figsize=(8, 4))
sns.lineplot(ax=axs[0], x='Diameter [mm]', y='RMSE', style='recon', hue='Dose [%]', data=iq_results, palette='crest')
sns.lineplot(ax=axs[1], x='Diameter [mm]', y='RMSE', style='recon', hue='Dose [%]', data=anthro_results, palette='crest')
axs[0].set_title('Image Quality Phantoms')
axs[1].set_title('Anthropomorphic Phantoms')
# %% [markdown]
# to clean this up, focus on RMSE *reduction* [%] = 100*(RMSE_fbp - RMSE_DLIR)/RMSE_fbp

def get_rmse_reduction(results_df):
    fbp_df = results_df[results_df['recon'] == 'FBP']
    dlir_df = results_df[results_df['recon'] != 'FBP']
    return 100*(fbp_df['RMSE'].to_numpy() - dlir_df['RMSE'].to_numpy())/fbp_df['RMSE'].to_numpy()

iq_rmse_reduction_df = iq_results[iq_results['recon'] == 'FBP']
iq_rmse_reduction_df = iq_rmse_reduction_df[['Diameter [mm]', 'Dose [%]']]
iq_rmse_reduction_df['RMSE Reduction [%]'] = get_rmse_reduction(iq_results)
iq_rmse_reduction_df['Phantom'] = 'Uniform Water'
iq_rmse_reduction_df

# %%%
anthro_rmse_reduction_df = anthro_results[anthro_results['recon'] == 'FBP']
anthro_rmse_reduction_df = anthro_rmse_reduction_df[['Diameter [mm]', 'Dose [%]']]
anthro_rmse_reduction_df['RMSE Reduction [%]'] = get_rmse_reduction(anthro_results)
anthro_rmse_reduction_df['Phantom'] = 'Anthropomorphic'
anthro_rmse_reduction_df['Diameter [mm]'] = anthro_rmse_reduction_df['Diameter [mm]'].astype(int)
# %%
rmse_reduction_df = pd.concat([iq_rmse_reduction_df, anthro_rmse_reduction_df])
rmse_reduction_df
# %%
f, ax = plt.subplots(figsize=(4, 3.5), tight_layout=True)
plot = sns.lineplot(ax=ax, x='Diameter [mm]', y='RMSE Reduction [%]', style='Phantom', hue='Dose [%]', data=rmse_reduction_df, palette='crest')
handles, labels = plot.get_legend_handles_labels()
plot.get_legend().remove()
f.legend(handles, labels, ncol=3, loc='upper center', 
                bbox_to_anchor=(0.5, 1.25), frameon=False)
f.tight_layout()
f.savefig('rmse_reduction_v_diameter.png', dpi=600, bbox_inches='tight')
# %%
iq_rmse_reduction_df.join(anthro_rmse_reduction_df, on=['Dose [%]'], rsuffix=' anthro', how='outer')
# %%

merged = pd.merge_asof(iq_rmse_reduction_df.sort_values(by=['Diameter [mm]', 'Dose [%]']), anthro_rmse_reduction_df.sort_values(by=['Diameter [mm]', 'Dose [%]']), on=['Diameter [mm]'],suffixes=[' IQ', ' Anthro'])
merged
# %%
merged = pd.merge_ordered(iq_rmse_reduction_df, anthro_rmse_reduction_df, on=['Diameter [mm]', 'Dose [%]', 'Phantom'], fill_method='ffill', suffixes=[' IQ', ' Anthro'])
merged
# %%
sns.scatterplot(x='RMSE Reduction [%] IQ', y='RMSE Reduction [%] Anthro')
# %%
anthro_rmse_reduction_df[anthro_rmse_reduction_df['Dose [%]'] == 25]

# %%
anthro_rmse = anthro_rmse_reduction_df.sort_values(by=['Diameter [mm]', 'Dose [%]'])['RMSE Reduction [%]']
# %%
iq_rmse = iq_rmse_reduction_df.sample(len(anthro_rmse_reduction_df)).sort_values(by=['Diameter [mm]', 'Dose [%]'])['RMSE Reduction [%]']
# %%
plt.scatter(x=iq_rmse, y=anthro_rmse)
plt.xlabel('IQ RMSE Reduction [%]')
plt.ylabel('Anthropomorphic RMSE Reduction [%]')

# %%
anthro_rmse_reduction_df
# %%
grouped = rmse_reduction_df.groupby(['Phantom', 'Dose [%]', 'Diameter [mm]'])
# %%
rmse_mean = grouped.mean()['RMSE Reduction [%]']
rmse_std = grouped.std()['RMSE Reduction [%]']
# %%
from sklearn.linear_model import LinearRegression
sns.set_theme('paper')

f, ax = plt.subplots(figsize=(3.5,3.5))
for dl  in [100, 55, 25, 10]:
    ant_rmse_mean = rmse_mean['Anthropomorphic'][dl].to_numpy()
    iq_rmse_interp = np.interp(rmse_mean['Anthropomorphic'][dl].index, rmse_mean['Uniform Water'][dl].index, rmse_mean['Uniform Water'][dl])
    iq_rmse_std = np.interp(rmse_std['Anthropomorphic'][dl].index, rmse_std['Uniform Water'][dl].index, rmse_std['Uniform Water'][dl])


    reg = LinearRegression().fit(iq_rmse_interp.reshape(-1, 1), ant_rmse_mean.reshape(-1, 1))
    print(f'{dl} Dose, R2: {reg.score(iq_rmse_interp.reshape(-1, 1), ant_rmse_mean.reshape(-1, 1)):0.3f}\nslope: {reg.coef_[0][0]}\nintercept: {reg.intercept_[0]}\n')
    ax.errorbar(ant_rmse_mean, iq_rmse_interp,
                yerr=iq_rmse_std,
                xerr=rmse_std['Anthropomorphic'][dl], label=dl, fmt='o', capsize=3)
    ax.set_ylabel('Uniform Water RMSE Reduction [%]')
    ax.set_xlabel('Anthropomorphic RMSE Reduction [%]')
    ax.plot(np.linspace(0, 70),np.linspace(0, 70), 'k--')
ax.legend(title='Dose [%]')
f.savefig('iq_validation.png', dpi=600, bbox_inches='tight')
# %%
