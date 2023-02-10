# %% [markdown]
# # Low Contrast Detectability Evaluations with Pediatric-Sized QA Phantoms
# Brandon J. Nelson
# 2023-02-03
# # Background
# This script generates plots from the `LCD_results.csv` file produced by `main_lcd_catphanSim.m` to visualize 
# the relationships between phantom size, reconstruction method, lesion size, dose level on low contrast
# detectability in terms of area under the roc curve (AUC) and detectability signal to noise (SNR) which are
# outputs from the model observers available here <https://github.com/DIDSR/LCD_CT>
# ## Looking at the results from `main_lcd_catphanSim.m`
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
lcd_data = pd.read_csv('/home/brandon.nelson/Dev/DLIR_Ped_Generalizability/geomtric_phantom_studies/results/LCD/LCD_results.csv')

lcd_data.replace('dl_REDCNN', 'dlir', inplace=True)
lcd_data.rename(columns={'patient_diameter_mm': 'phantom diameter [mm]', 'dose_level_pct': 'dose [%]'}, inplace=True)
lcd_data = lcd_data[lcd_data['phantom diameter [mm]'] != 200] #ref has large fov
print(f'{len(lcd_data)} rows')
lcd_data.head()
# %%
lcd_data.tail() 
# %%
insert_HU_size = {14 : '3 mm', 7: '5 mm', 5: '7 mm', 3: '10 mm'}
observers = lcd_data['observer'].unique()
observers
# %% [markdown]
# ## Getting the Mean and Standard Deviation
# Use the dataframe `groupby` method to group the data by the following groups (all groups except reader number), and then take the mean
# and standard deviation across readers
grouped = lcd_data.groupby(["phantom diameter [mm]","recon", "insert_HU", "observer", "dose [%]"])

lcd_mean = grouped.mean()
lcd_std = grouped.std()
lcd_mean
# %% [markdown]
# # AUC and SNR vs dose
# ## First build up our plotting routines
# %%
insert_HUs = lcd_data['insert_HU'].unique()

def plot_insert_level_results(img_level_mean, img_level_std, insert_HUs, ylabel, fig=None, legend=True):
    fig = fig or plt.figure()
    if len(insert_HUs) > 2:
        axs = fig.subplots(2,2, sharex=True, sharey=True).flatten()
    elif len(insert_HUs) == 2:
        axs = fig.subplots(1,2, sharex=True, sharey=True)
    elif len(insert_HUs) == 1:
        axs = [fig.subplots(1,1, sharex=True, sharey=True)]

    plt_idx=0
    for insert_HU, ax in zip(insert_HUs, axs):
        for observer in observers:
            series_mean = img_level_mean[insert_HU, observer]
            series_std = img_level_std[insert_HU, observer]
            series_mean.plot(ax=ax, yerr=series_std, label=observer, capsize=3)
        ax.set_title(f'{insert_HU} HU, {insert_HU_size[insert_HU]}')
        ax.set_ylabel(ylabel)

        if legend & (plt_idx < 1):
            fig.legend(bbox_to_anchor=(0.5, 1.1), loc = 'upper center', frameon=False, ncol=3)
        plt_idx += 1
# <-- these v_dose and v_diam functions are so similar only differing by diam vs dose, thereshould be a way to refactor them into 1
# also a way to change diff to ratio as a simple parameter
def plot_img_level_results_v_dose(recontype, diam, restype, insert_HUs=[14, 7, 5, 3], fig=None, legend=True, recon_cmp_method='diff'):
    fig = fig or plt.figure()
    ylabel = f'{restype.upper()}'
    fig_title = f'{diam} mm '
    if isinstance(insert_HUs, int): insert_HUs = [insert_HUs]
    if isinstance(recontype, str):
        img_level_mean = lcd_mean[restype][diam, recontype]
        img_level_std = lcd_std[restype][diam, recontype]
        fig_title += f'{recontype}'
    else:
        dlir_mean = lcd_mean[restype][diam, recontype[0]]
        dlir_std = lcd_std[restype][diam, recontype[0]]
        fbp_mean = lcd_mean[restype][diam, recontype[1]]
        fbp_std = lcd_std[restype][diam, recontype[1]]
        if recon_cmp_method == 'diff':
            img_level_mean = dlir_mean - fbp_mean
            img_level_std = np.sqrt(fbp_std**2 + dlir_std**2)
            ylabel = '$\Delta$' + ylabel
        elif recon_cmp_method == 'div':
            img_level_mean  = dlir_mean / fbp_mean
            img_level_std = np.sqrt((fbp_std/fbp_mean)**2 + (dlir_std/dlir_mean)**2)
            ylabel +=  ' ratio'
        fig_title += f'{recontype[0]} - {recontype[1]}'
    fig.suptitle(fig_title)

    plot_insert_level_results(img_level_mean, img_level_std, insert_HUs, ylabel, fig=fig, legend=legend)

def plot_img_level_results_v_diam(recontype, dose_level, restype, insert_HUs=[14, 7, 5, 3], fig=None, legend=True, recon_cmp_method='diff'):
    fig = fig or plt.figure()
    ylabel = f'{restype.upper()}'
    fig_title = f'{dose_level} % '
    if isinstance(insert_HUs, int): insert_HUs = [insert_HUs]
    if isinstance(recontype, str):
        img_level_mean = lcd_mean[restype][dose_level, recontype]
        img_level_std = lcd_std[restype][dose_level, recontype]
        fig_title += f'{recontype}'
    else:
        dlir_mean = lcd_mean[restype][dose_level, recontype[0]]
        dlir_std = lcd_std[restype][dose_level, recontype[0]]
        fbp_mean = lcd_mean[restype][dose_level, recontype[1]]
        fbp_std = lcd_std[restype][dose_level, recontype[1]]
        if recon_cmp_method == 'diff':
            img_level_mean = dlir_mean - fbp_mean
            img_level_std = np.sqrt(fbp_std**2 + dlir_std**2)
            ylabel = '$\Delta$' + ylabel
        elif recon_cmp_method == 'div':
            img_level_mean  = dlir_mean / fbp_mean
            img_level_std = np.sqrt((fbp_std/fbp_mean)**2 + (dlir_std/dlir_mean)**2)
            ylabel +=  ' ratio'
        fig_title += f'{recontype[0]} - {recontype[1]}'
    fig.suptitle(fig_title)

    plot_insert_level_results(img_level_mean, img_level_std, insert_HUs, ylabel, fig=fig, legend=legend)

# <-- similar to plot_img_level_results_v_dose and plot_img_level_results_v_diam, these two functions below are too similar and can be refactored (code smell)
def plot_all_results_v_dose(restype='auc', patient_diameters=[292, 185, 112], recontypes=['fbp', 'dlir', ['dlir', 'fbp']], insert_HUs=[14, 7, 5, 3], recon_cmp_method='diff'):
    master_fig = plt.figure(constrained_layout=True, figsize=(3*len(recontypes) + 1, 3*len(patient_diameters) + 1), dpi=150)
    figs = master_fig.subfigures(len(patient_diameters), len(recontypes))

    fig_idx = 0
    for fig_row, diam in zip(figs, patient_diameters):
        if not isinstance(fig_row, np.ndarray): fig_row = np.array([fig_row])
        for fig, recontype in zip(fig_row, recontypes):
            legend = True if (fig_idx == 0) else False
            plot_img_level_results_v_dose(recontype, diam, restype, insert_HUs=insert_HUs, fig=fig, legend=legend, recon_cmp_method=recon_cmp_method)
            fig_idx += 1

def plot_all_results_v_diam(restype='auc', dose_levels=[10, 55, 100], recontypes=['fbp', 'dlir', ['dlir', 'fbp']], insert_HUs=[14, 7, 5, 3], recon_cmp_method='diff'):
    master_fig = plt.figure(constrained_layout=True, figsize=(3*len(recontypes) + 1, 3*len(dose_levels) + 1), dpi=150)
    figs = master_fig.subfigures(len(dose_levels), len(recontypes))

    fig_idx = 0
    for fig_row, dose_level in zip(figs, dose_levels):
        if not isinstance(fig_row, np.ndarray): fig_row = np.array([fig_row])
        for fig, recontype in zip(fig_row, recontypes):
            legend = True if (fig_idx == 0) else False
            plot_img_level_results_v_diam(recontype, dose_level, restype, insert_HUs=insert_HUs, fig=fig, legend=legend, recon_cmp_method=recon_cmp_method)
            fig_idx += 1

# %%
plot_img_level_results_v_dose('fbp', 292, 'auc', insert_HUs = 7)
# %%
plot_img_level_results_v_dose('dlir', 292, 'auc')
# %%
plot_img_level_results_v_dose(['dlir', 'fbp'], 292, 'snr')
# %%
plot_img_level_results_v_dose(['dlir', 'fbp'], 292, 'snr', insert_HUs = [5, 14])
    
# %% [markdown]
# ### Let's look at everything (warning a bit overwhelming) AUC
# these could be included in the paper appendix, but for the main figures we'll want to distill this down to
# the main effects (described below)
patient_diameters = sorted(lcd_data['phantom diameter [mm]'].unique(), reverse=True)
print(patient_diameters)
plot_all_results_v_dose('auc', patient_diameters=patient_diameters, recontypes=['fbp', 'dlir', ['dlir', 'fbp']])
# %% [markdown]
# ## First look at everything (warning a bit overwhelming) SNR
# Same as above, these could be included in the paper appendix, but for the main figures we'll want to distill this down to
# the main effects (described below)
plot_all_results_v_dose('snr', patient_diameters=patient_diameters, recontypes=['fbp', 'dlir', ['dlir', 'fbp']])
# %% [markdown]
# ## Let's now break this down into smaller chunks to better understand the relationships between variables
# ### Starting with insert size and HU
# Let's first see if there's any noticeable difference in detectability based on insert size and contrast
# 
# #### all 4 inserts auc vs dose (no diffs)
# this shows that there's not much difference between inserts
plot_all_results_v_dose('auc', patient_diameters=[292, 185, 112], recontypes=['fbp', 'dlir'])
# %% [markdown]
# ## all 4 inserts snr vs dose (no diffs)
# this shows that there's not much difference between inserts
plot_all_results_v_dose('snr', patient_diameters=[292, 185, 112], recontypes=['fbp', 'dlir'])
# %% [markdown]
# ## Now just 1 insert but show diffs auc
plot_all_results_v_dose('auc', patient_diameters=[292, 185, 112], recontypes=['fbp', 'dlir', ['dlir', 'fbp']], insert_HUs=14)

# %% [markdown]
# ## Now just 1 insert but show diffs snr
plot_all_results_v_dose('snr', patient_diameters=[292, 185, 112], recontypes=['fbp', 'dlir', ['dlir', 'fbp']], insert_HUs=14)

# %% [markdown]
# # diff auc vs diam
grouped = lcd_data.groupby(["dose [%]", "recon", "insert_HU", "observer", "phantom diameter [mm]"])

lcd_mean = grouped.mean()
lcd_std = grouped.std()
lcd_mean
# %% [markdown]
#  dlir - fbp diff auc
dose_level = 100
restype = 'auc'
recontype = 'fbp'
img_level_mean = lcd_mean[restype][dose_level, recontype]
img_level_std = lcd_std[restype][dose_level, recontype]
plot_insert_level_results(img_level_mean, img_level_std, insert_HUs, 'auc')

# %%
plot_all_results_v_diam('auc', dose_levels=[100, 10], recontypes=['fbp', 'dlir', ['dlir', 'fbp']])
# %%
plot_all_results_v_diam('auc', dose_levels=[100, 10], recontypes=['fbp', 'dlir', ['dlir', 'fbp']], insert_HUs=14)

# %% [markdown]
# note above that sometimes NPWE can exceed NPW in \Delta AUC because the AUC is saturated, this cross-over doesn't occur in SNR
# since we showed this earlier we probs only need to show SNR moving forward in the paper if we show the auc saturation once
# %% [markdown]
# dlir - fbp diff snr
plot_all_results_v_diam('snr', dose_levels=[100, 55, 10], recontypes=['fbp', 'dlir', ['dlir', 'fbp']], insert_HUs=14)
# %%

# %% [markdown] 
# ## SNR ratios
plot_all_results_v_diam('snr', dose_levels=[100, 55, 10], recontypes=['fbp', 'dlir', ['dlir', 'fbp']], recon_cmp_method='div')
# %% [markdown]
# the ratio becomes too noisy due to NPWE 2D (eye filter) so remove it from the list of observers
observers = ['Laguerre-Gauss CHO 2D', 'NPW 2D']
plot_all_results_v_diam('snr', dose_levels=[100, 55, 10], recontypes=['fbp', 'dlir', ['dlir', 'fbp']], recon_cmp_method='div')
# %%
plot_all_results_v_diam('snr', dose_levels=[100, 25], recontypes=['fbp', 'dlir', ['dlir', 'fbp']], insert_HUs=7, recon_cmp_method='div')
# %%
plot_all_results_v_diam('auc', dose_levels=[100, 25], recontypes=[['dlir', 'fbp']], recon_cmp_method='div')
# %%
plot_all_results_v_diam('snr', dose_levels=[100, 25], recontypes=[['dlir', 'fbp']], recon_cmp_method='div')
# %%
plot_all_results_v_diam('snr', dose_levels=[100, 25], recontypes=[['dlir', 'fbp']], insert_HUs=7, recon_cmp_method='div')
# %%