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
lcd_data = lcd_data[lcd_data['patient_diameter_mm'] != 200] #ref has large fov
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
grouped = lcd_data.groupby(["patient_diameter_mm","recon", "insert_HU", "observer", "dose_level_pct"])

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
            series_mean.plot(ax=ax, yerr=series_std, label=observer)
        ax.set_title(f'{insert_HU} HU, {insert_HU_size[insert_HU]}')
        ax.set_ylabel(ylabel)

        if legend & (plt_idx < 1):
            fig.legend(bbox_to_anchor=(0.5, 1.1), loc = 'upper center', frameon=False, ncol=3)
        plt_idx += 1

def plot_img_level_results(recontype, diam, restype, insert_HUs=[14, 7, 5, 3], fig=None, legend=True):
    fig = fig or plt.figure()
    ylabel = f'{restype}'
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
        img_level_mean = dlir_mean - fbp_mean
        img_level_std = np.sqrt(fbp_std**2 + dlir_std**2)
        ylabel = '$\Delta$' + ylabel
        fig_title += f'{recontype[0]} - {recontype[1]}'
    fig.suptitle(fig_title)

    plot_insert_level_results(img_level_mean, img_level_std, insert_HUs, ylabel, fig=fig, legend=legend)


# %%
plot_img_level_results('fbp', 292, 'auc', insert_HUs = 7)
# %%
plot_img_level_results('dlir', 292, 'auc')
# %%
plot_img_level_results(['dlir', 'fbp'], 292, 'snr')
# %%
plot_img_level_results(['dlir', 'fbp'], 292, 'snr', insert_HUs = [5, 14])
    
# %%
def plot_all_results(restype='auc', patient_diameters=[292, 185, 112], recontypes=['fbp', 'dlir', ['dlir', 'fbp']], insert_HUs=[14, 7, 5, 3]):
    master_fig = plt.figure(constrained_layout=True, figsize=(3*len(recontypes) + 1, 3*len(patient_diameters) + 1), dpi=150)
    figs = master_fig.subfigures(len(patient_diameters), len(recontypes))

    fig_idx = 0
    for fig_row, diam in zip(figs, patient_diameters):
        for fig, recontype in zip(fig_row, recontypes):
            legend = True if (fig_idx == 0) else False
            plot_img_level_results(recontype, diam, restype, insert_HUs=insert_HUs, fig=fig, legend=legend)
            fig_idx += 1
# %% [markdown]
# ### Let's look at everything (warning a bit overwhelming) AUC
# these could be included in the paper appendix, but for the main figures we'll want to distill this down to
# the main effects (described below)
patient_diameters = sorted(lcd_data['patient_diameter_mm'].unique(), reverse=True)
print(patient_diameters)
plot_all_results('auc', patient_diameters=patient_diameters, recontypes=['fbp', 'dlir', ['dlir', 'fbp']])
# %% [markdown]
# ## First look at everything (warning a bit overwhelming) SNR
# Same as above, these could be included in the paper appendix, but for the main figures we'll want to distill this down to
# the main effects (described below)
plot_all_results('snr', patient_diameters=patient_diameters, recontypes=['fbp', 'dlir', ['dlir', 'fbp']])
# %% [markdown]
# ## Let's now break this down into smaller chunks to better understand the relationships between variables
# ### Starting with insert size and HU
# Let's first see if there's any noticeable difference in detectability based on insert size and contrast
# 
# #### all 4 inserts auc vs dose (no diffs)
# this shows that there's not much difference between inserts
plot_all_results('auc', patient_diameters=[292, 185, 112], recontypes=['fbp', 'dlir'])
# %% [markdown]
# ## all 4 inserts snr vs dose (no diffs)
# this shows that there's not much difference between inserts
plot_all_results('snr', patient_diameters=[292, 185, 112], recontypes=['fbp', 'dlir'])
# %% [markdown]
# ## Now just 1 insert but show diffs auc
plot_all_results('auc', patient_diameters=[292, 185, 112], recontypes=['fbp', 'dlir', ['dlir', 'fbp']], insert_HUs=14)

# %% [markdown]
# ## Now just 1 insert but show diffs snr
plot_all_results('snr', patient_diameters=[292, 185, 112], recontypes=['fbp', 'dlir', ['dlir', 'fbp']], insert_HUs=14)

# %% [markdown]
# # diff auc vs diam
grouped = lcd_data.groupby(["recon", "insert_HU", "observer", "dose_level_pct", "patient_diameter_mm"])

lcd_mean = grouped.mean()
lcd_std = grouped.std()
lcd_mean
# %% [markdown]
#  dlir - fbp diff auc

master_fig = plt.figure(constrained_layout=True, figsize=(10, 5), dpi=150)
figs = master_fig.subfigures(1, 3)

for idx, dose_level in enumerate([100, 25, 10]):

    restype='auc'
    fig = figs[idx]
    axs = fig.subplots(2,2, sharex=True, sharey=True)
    for insert_HU, ax in zip(insert_HU_size, axs.flatten()):
        for observer in observers:
            fbp_mean = lcd_mean[restype]['fbp', insert_HU, observer, dose_level]
            fbp_std = lcd_std[restype]['fbp', insert_HU, observer, dose_level]

            dlir_mean = lcd_mean[restype]['dlir', insert_HU, observer, dose_level]
            dlir_std = lcd_std[restype]['dlir', insert_HU, observer, dose_level]

            series_mean = dlir_mean - fbp_mean
            series_std = np.sqrt(fbp_std**2 + dlir_std**2)
            series_mean.plot(ax=ax, yerr=series_std, label=observer)
        ax.set_title(f'{insert_HU} HU, {insert_HU_size[insert_HU]}')
        ax.set_ylabel(restype)
        if (idx == 1) & (insert_HU == 14):
            fig.legend(bbox_to_anchor=(0.5, 1.1), loc = 'upper center', frameon=False, ncol=3)
    fig.suptitle(f'{dose_level}% dose')
    # axs[0, 0].legend()
# %%
# plot_all_results('snr', patient_diameters=[292, 185, 112], recontypes=['fbp', 'dlir', ['dlir', 'fbp']], insert_HUs=14)
# %% [markdown]
# note above that sometimes NPWE can exceed NPW in \Delta AUC because the AUC is saturated, this cross-over doesn't occur in SNR
# since we showed this earlier we probs only need to show SNR moving forward in the paper if we show the auc saturation once
# %% [markdown]
# dlir - fbp diff snr
# %%
master_fig = plt.figure(constrained_layout=True, figsize=(8, 5), dpi=150)
figs = master_fig.subfigures(1, 2)

for idx, dose_level in enumerate([100, 10]):

    restype='snr'
    fig = figs[idx]
    axs = fig.subplots(2,2, sharex=True, sharey=True)
    for insert_HU, ax in zip(insert_HU_size, axs.flatten()):
        for observer in observers:
            fbp_mean = lcd_mean[restype]['fbp', insert_HU, observer, dose_level]
            fbp_std = lcd_std[restype]['fbp', insert_HU, observer, dose_level]

            dlir_mean = lcd_mean[restype]['dlir', insert_HU, observer, dose_level]
            dlir_std = lcd_std[restype]['dlir', insert_HU, observer, dose_level]

            series_mean = dlir_mean - fbp_mean
            series_std = np.sqrt(fbp_std**2 + dlir_std**2)
            series_mean.plot(ax=ax, yerr=series_std, label=observer)
        ax.set_title(f'{insert_HU} HU, {insert_HU_size[insert_HU]}')
        ax.set_ylabel(f"$\Delta${restype.upper()}")
        ax.set_xlabel("phantom diameter\n[mm]")
        if (idx == 0) & (insert_HU == 14):
            fig.legend(bbox_to_anchor=(0.5, 1.1), loc = 'upper center', frameon=False, ncol=3)
    fig.suptitle(f'{dose_level}% dose')
# %% [markdown] 
# ## SNR ratios
master_fig = plt.figure(constrained_layout=True, figsize=(8, 5), dpi=150)
figs = master_fig.subfigures(1, 2)

for idx, dose_level in enumerate([100, 25]):

    restype='snr'
    fig = figs[idx]
    ax = fig.subplots()
    insert_HU = 7
    for observer in ['Laguerre-Gauss CHO 2D', 'NPW 2D']:
        fbp_mean = lcd_mean[restype]['fbp', insert_HU, observer, dose_level]
        fbp_std = lcd_std[restype]['fbp', insert_HU, observer, dose_level]

        dlir_mean = lcd_mean[restype]['dlir', insert_HU, observer, dose_level]
        dlir_std = lcd_std[restype]['dlir', insert_HU, observer, dose_level]

        series_mean = dlir_mean.abs() / fbp_mean.abs()
        series_std = np.sqrt(fbp_std**2 + dlir_std**2)
        series_mean.plot(ax=ax, yerr=series_std, label=observer)
    ax.set_title(f'{insert_HU} HU, {insert_HU_size[insert_HU]}')
    ax.set_ylabel(f"{restype.upper()} Ratio\n(DLIR SNR / FBP SNR)")
    ax.set_xlabel("phantom diameter\n[mm]")
    if (idx == 0):
        fig.legend(bbox_to_anchor=(0.5, 1.1), loc = 'upper center', frameon=False, ncol=3)
    fig.suptitle(f'{dose_level}% dose')

# %%
