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
grouped = lcd_data.groupby(["observer", "patient_diameter_mm", "insert_HU", "recon", "dose_level_pct"])

lcd_mean = grouped.mean()
lcd_std = grouped.std()
lcd_mean
# %% [markdown]
# # AUC and SNR vs dose
# ## First look at everything (warning a bit overwhelming) AUC
# %%
master_fig = plt.figure(constrained_layout=True, figsize=(10, 10), dpi=150)
figs = master_fig.subfigures(3, 3)
restype = 'auc' 

for idx, diam in enumerate([292, 185, 112]):

    recontype = 'fbp'
    fig = figs[idx, 0]
    axs = fig.subplots(2,2, sharex=True, sharey=True)
    fig.suptitle(f"{diam} mm {recontype}")
    for insert_HU, ax in zip(insert_HU_size, axs.flatten()):
        for observer in observers:
            series_mean = lcd_mean[restype][observer, diam, insert_HU, recontype]
            series_std = lcd_std[restype][observer, diam, insert_HU, recontype]
            series_mean.plot(ax=ax, yerr=series_std, label=observer)
        ax.set_title(f'{insert_HU} HU, {insert_HU_size[insert_HU]}')
        ax.set_ylabel(restype)


    recontype = 'dlir'
    fig = figs[idx, 1]
    axs = fig.subplots(2,2, sharex=True, sharey=True)
    fig.suptitle(f"{diam} mm {recontype}")
    for insert_HU, ax in zip(insert_HU_size, axs.flatten()):
        for observer in observers:
            series_mean = lcd_mean[restype][observer, diam, insert_HU, recontype]
            series_std = lcd_std[restype][observer, diam, insert_HU, recontype]
            series_mean.plot(ax=ax, yerr=series_std, label=observer)
        ax.set_title(f'{insert_HU} HU, {insert_HU_size[insert_HU]}')
        ax.set_ylabel(restype)
        if (idx == 0) & (insert_HU == 14):
            fig.legend(bbox_to_anchor=(0.5, 1.1), loc = 'upper center', frameon=False, ncol=3)

    fig = figs[idx, 2]
    axs = fig.subplots(2,2, sharex=True, sharey=True)
    fig.suptitle(f"{diam} mm DLIR-FBP")
    for insert_HU, ax in zip(insert_HU_size, axs.flatten()):
        for observer in observers:
            fbp_mean = lcd_mean[restype][observer, diam, insert_HU, 'fbp']
            fbp_std = lcd_std[restype][observer, diam, insert_HU, 'fbp']

            dlir_mean = lcd_mean[restype][observer, diam, insert_HU, 'dlir']
            dlir_std = lcd_std[restype][observer, diam, insert_HU, 'dlir']

            series_mean = dlir_mean - fbp_mean
            series_std = np.sqrt(fbp_std**2 + dlir_std**2)
            series_mean.plot(ax=ax, yerr=series_std, label=observer)
        ax.set_title(f'{insert_HU} HU, {insert_HU_size[insert_HU]}')
        ax.set_ylabel(f"$\Delta${restype}")
# %% [markdown]
# ## First look at everything (warning a bit overwhelming) SNR
# %%
master_fig = plt.figure(constrained_layout=True, figsize=(10, 10), dpi=150)
figs = master_fig.subfigures(3, 3)
restype = 'snr' 

for idx, diam in enumerate([292, 185, 112]):

    recontype = 'fbp'
    fig = figs[idx, 0]
    axs = fig.subplots(2,2, sharex=True, sharey=True)
    fig.suptitle(f"{diam} mm {recontype}")
    for insert_HU, ax in zip(insert_HU_size, axs.flatten()):
        for observer in observers:
            series_mean = lcd_mean[restype][observer, diam, insert_HU, recontype]
            series_std = lcd_std[restype][observer, diam, insert_HU, recontype]
            series_mean.plot(ax=ax, yerr=series_std, label=observer)
        ax.set_title(f'{insert_HU} HU, {insert_HU_size[insert_HU]}')
        ax.set_ylabel(restype)

    recontype = 'dlir'
    fig = figs[idx, 1]
    axs = fig.subplots(2,2, sharex=True, sharey=True)
    fig.suptitle(f"{diam} mm {recontype}")
    for insert_HU, ax in zip(insert_HU_size, axs.flatten()):
        for observer in observers:
            series_mean = lcd_mean[restype][observer, diam, insert_HU, recontype]
            series_std = lcd_std[restype][observer, diam, insert_HU, recontype]
            series_mean.plot(ax=ax, yerr=series_std, label=observer)
        ax.set_title(f'{insert_HU} HU, {insert_HU_size[insert_HU]}')
        ax.set_ylabel(restype)
        if (idx == 0) & (insert_HU == 14):
            fig.legend(bbox_to_anchor=(0.5, 1.1), loc = 'upper center', frameon=False, ncol=3)

    fig = figs[idx, 2]
    axs = fig.subplots(2,2, sharex=True, sharey=True)
    fig.suptitle(f"{diam} mm DLIR-FBP")
    for insert_HU, ax in zip(insert_HU_size, axs.flatten()):
        for observer in observers:
            fbp_mean = lcd_mean[restype][observer, diam, insert_HU, 'fbp']
            fbp_std = lcd_std[restype][observer, diam, insert_HU, 'fbp']

            dlir_mean = lcd_mean[restype][observer, diam, insert_HU, 'dlir']
            dlir_std = lcd_std[restype][observer, diam, insert_HU, 'dlir']

            series_mean = dlir_mean - fbp_mean
            series_std = np.sqrt(fbp_std**2 + dlir_std**2)
            series_mean.plot(ax=ax, yerr=series_std, label=observer)
        ax.set_title(f'{insert_HU} HU, {insert_HU_size[insert_HU]}')
        ax.set_ylabel(f"$\Delta${restype}")
# %% [markdown]
# ## all 4 inserts auc vs dose (no diffs)
# this shows that there's not much difference between inserts
# %%
import numpy as np
master_fig = plt.figure(constrained_layout=True, figsize=(10, 10), dpi=150)
figs = master_fig.subfigures(2, 3)
restype = 'auc' 

for idx, diam in enumerate([292, 185, 112]):

    recontype = 'fbp'
    fig = figs[0, idx]
    axs = fig.subplots(2,2, sharex=True, sharey=True)
    fig.suptitle(f"{diam} mm {recontype}")
    for insert_HU, ax in zip(insert_HU_size, axs.flatten()):
        for observer in observers:
            series_mean = lcd_mean[restype][observer, diam, insert_HU, recontype]
            series_std = lcd_std[restype][observer, diam, insert_HU, recontype]
            series_mean.plot(ax=ax, yerr=series_std, label=observer)
        ax.set_title(f'{insert_HU} HU, {insert_HU_size[insert_HU]}')
        ax.set_ylabel(restype)
        if (idx == 1) & (insert_HU == 14):
            fig.legend(bbox_to_anchor=(0.5, 1.1), loc = 'upper center', frameon=False, ncol=3)

    recontype = 'dlir'
    fig = figs[1, idx]
    axs = fig.subplots(2,2, sharex=True, sharey=True)
    fig.suptitle(f"{diam} mm {recontype}")
    for insert_HU, ax in zip(insert_HU_size, axs.flatten()):
        for observer in observers:
            series_mean = lcd_mean[restype][observer, diam, insert_HU, recontype]
            series_std = lcd_std[restype][observer, diam, insert_HU, recontype]
            series_mean.plot(ax=ax, yerr=series_std, label=observer)
        ax.set_title(f'{insert_HU} HU, {insert_HU_size[insert_HU]}')
        ax.set_ylabel(restype)

# %% [markdown]
# ## all 4 inserts snr vs dose (no diffs)
# this shows that there's not much difference between inserts
# %%
import numpy as np
master_fig = plt.figure(constrained_layout=True, figsize=(10, 10), dpi=150)
figs = master_fig.subfigures(2, 3)
restype = 'snr' 

for idx, diam in enumerate([292, 185, 112]):

    recontype = 'fbp'
    fig = figs[0, idx]
    axs = fig.subplots(2,2, sharex=True, sharey=True)
    fig.suptitle(f"{diam} mm {recontype}")
    for insert_HU, ax in zip(insert_HU_size, axs.flatten()):
        for observer in observers:
            series_mean = lcd_mean[restype][observer, diam, insert_HU, recontype]
            series_std = lcd_std[restype][observer, diam, insert_HU, recontype]
            series_mean.plot(ax=ax, yerr=series_std, label=observer)
        ax.set_title(f'{insert_HU} HU, {insert_HU_size[insert_HU]}')
        ax.set_ylabel(restype)
        if (idx == 1) & (insert_HU == 14):
            fig.legend(bbox_to_anchor=(0.5, 1.1), loc = 'upper center', frameon=False, ncol=3)


    recontype = 'dlir'
    fig = figs[1, idx]
    axs = fig.subplots(2,2, sharex=True, sharey=True)
    fig.suptitle(f"{diam} mm {recontype}")
    for insert_HU, ax in zip(insert_HU_size, axs.flatten()):
        for observer in observers:
            series_mean = lcd_mean[restype][observer, diam, insert_HU, recontype]
            series_std = lcd_std[restype][observer, diam, insert_HU, recontype]
            series_mean.plot(ax=ax, yerr=series_std, label=observer)
        ax.set_title(f'{insert_HU} HU, {insert_HU_size[insert_HU]}')
        ax.set_ylabel(restype)

# %% [markdown]
# ## Now just 1 insert but show diffs auc
# %%
master_fig = plt.figure(constrained_layout=True, figsize=(10, 10), dpi=150)
figs = master_fig.subfigures(3, 3)
restype = 'auc' 

for idx, diam in enumerate([292, 185, 112]):

    recontype = 'fbp'
    row_figs = figs[idx]
    fig = row_figs[0]
    ax = fig.subplots(sharex=True, sharey=True)
    insert_HU = 14
    fig.suptitle(f"{diam} mm {recontype}")
    for observer in observers:
        series_mean = lcd_mean[restype][observer, diam, insert_HU, recontype]
        series_std = lcd_std[restype][observer, diam, insert_HU, recontype]
        series_mean.plot(ax=ax, yerr=series_std, label=observer)
    ax.set_ylabel(restype)
    ax.set_title(f'{insert_HU} HU, {insert_HU_size[insert_HU]}')
    # axs[0, 0].legend()

    recontype = 'dlir'
    row_figs = figs[idx]
    fig = row_figs[1]
    ax = fig.subplots(sharex=True, sharey=True)
    fig.suptitle(f"{diam} mm {recontype}")
    for observer in observers:
        series_mean = lcd_mean[restype][observer, diam, insert_HU, recontype]
        series_std = lcd_std[restype][observer, diam, insert_HU, recontype]
        series_mean.plot(ax=ax, yerr=series_std, label=observer)
    ax.set_ylabel(restype)
    ax.set_title(f'{insert_HU} HU, {insert_HU_size[insert_HU]}')
    if (idx == 0):
        fig.legend(bbox_to_anchor=(0.5, 1.1), loc = 'upper center', frameon=False, ncol=3)

    row_figs = figs[idx]
    fig = row_figs[2]
    ax = fig.subplots(sharex=True, sharey=True)
    fig.suptitle(f"{diam} mm DLIR-FBP")

    recon_series = lcd_mean[restype]

    for observer in observers:
        fbp_mean = lcd_mean[restype][observer, diam, insert_HU, 'fbp']
        fbp_std = lcd_std[restype][observer, diam, insert_HU, 'fbp']

        dlir_mean = lcd_mean[restype][observer, diam, insert_HU, 'dlir']
        dlir_std = lcd_std[restype][observer, diam, insert_HU, 'dlir']

        series_mean = dlir_mean - fbp_mean
        series_std = np.sqrt(fbp_std**2 + dlir_std**2)
        series_mean.plot(ax=ax, yerr=series_std, label=observer)
    ax.set_ylabel(f"$\Delta${restype}")
    ax.set_title(f'{insert_HU} HU, {insert_HU_size[insert_HU]}')
# %% [markdown]
# ## Now just 1 insert but show diffs snr
# %%
master_fig = plt.figure(constrained_layout=True, figsize=(10, 10), dpi=150)
figs = master_fig.subfigures(3, 3)
restype = 'snr' 

for idx, diam in enumerate([292, 185, 112]):

    recontype = 'fbp'
    row_figs = figs[idx]
    fig = row_figs[0]
    ax = fig.subplots(sharex=True, sharey=True)
    insert_HU = 14
    fig.suptitle(f"{diam} mm {recontype}")
    for observer in observers:
        series_mean = lcd_mean[restype][observer, diam, insert_HU, recontype]
        series_std = lcd_std[restype][observer, diam, insert_HU, recontype]
        series_mean.plot(ax=ax, yerr=series_std, label=observer)
    ax.set_ylabel(restype)
    ax.set_title(f'{insert_HU} HU, {insert_HU_size[insert_HU]}')
    # axs[0, 0].legend()

    recontype = 'dlir'
    row_figs = figs[idx]
    fig = row_figs[1]
    ax = fig.subplots(sharex=True, sharey=True)
    fig.suptitle(f"{diam} mm {recontype}")
    for observer in observers:
        series_mean = lcd_mean[restype][observer, diam, insert_HU, recontype]
        series_std = lcd_std[restype][observer, diam, insert_HU, recontype]
        series_mean.plot(ax=ax, yerr=series_std, label=observer)
    ax.set_ylabel(restype)
    ax.set_title(f'{insert_HU} HU, {insert_HU_size[insert_HU]}')
    if (idx == 0):
        fig.legend(bbox_to_anchor=(0.5, 1.1), loc = 'upper center', frameon=False, ncol=3)

    row_figs = figs[idx]
    fig = row_figs[2]
    ax = fig.subplots(sharex=True, sharey=True)
    fig.suptitle(f"{diam} mm DLIR-FBP")

    recon_series = lcd_mean[restype]

    for observer in observers:
        fbp_mean = lcd_mean[restype][observer, diam, insert_HU, 'fbp']
        fbp_std = lcd_std[restype][observer, diam, insert_HU, 'fbp']

        dlir_mean = lcd_mean[restype][observer, diam, insert_HU, 'dlir']
        dlir_std = lcd_std[restype][observer, diam, insert_HU, 'dlir']

        series_mean = dlir_mean - fbp_mean
        series_std = np.sqrt(fbp_std**2 + dlir_std**2)
        series_mean.plot(ax=ax, yerr=series_std, label=observer)
    ax.set_ylabel(f"$\Delta${restype}")
    ax.set_title(f'{insert_HU} HU, {insert_HU_size[insert_HU]}')

# %% [markdown]
# # diff auc vs diam

grouped = lcd_data.groupby(["observer", "insert_HU", "recon", "dose_level_pct", "patient_diameter_mm"])

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
            fbp_mean = lcd_mean[restype][observer, insert_HU, 'fbp', dose_level,]
            fbp_std = lcd_std[restype][observer, insert_HU, 'fbp', dose_level,]

            dlir_mean = lcd_mean[restype][observer, insert_HU, 'dlir', dose_level,]
            dlir_std = lcd_std[restype][observer, insert_HU, 'dlir', dose_level,]

            series_mean = dlir_mean - fbp_mean
            series_std = np.sqrt(fbp_std**2 + dlir_std**2)
            series_mean.plot(ax=ax, yerr=series_std, label=observer)
        ax.set_title(f'{insert_HU} HU, {insert_HU_size[insert_HU]}')
        ax.set_ylabel(restype)
        if (idx == 1) & (insert_HU == 14):
            fig.legend(bbox_to_anchor=(0.5, 1.1), loc = 'upper center', frameon=False, ncol=3)
    fig.suptitle(f'{dose_level}% dose')
    # axs[0, 0].legend()
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
            fbp_mean = lcd_mean[restype][observer, insert_HU, 'fbp', dose_level,]
            fbp_std = lcd_std[restype][observer, insert_HU, 'fbp', dose_level,]

            dlir_mean = lcd_mean[restype][observer, insert_HU, 'dlir', dose_level,]
            dlir_std = lcd_std[restype][observer, insert_HU, 'dlir', dose_level,]

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
        fbp_mean = lcd_mean[restype][observer, insert_HU, 'fbp', dose_level]
        fbp_std = lcd_std[restype][observer, insert_HU, 'fbp', dose_level]

        dlir_mean = lcd_mean[restype][observer, insert_HU, 'dlir', dose_level]
        dlir_std = lcd_std[restype][observer, insert_HU, 'dlir', dose_level]

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
