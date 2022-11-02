# %%
import argparse
from pathlib import Path

import numpy as np
import scipy.io
import matplotlib.pyplot as plt
import h5py


def load_adult_dataset(basedir=None, recon='cnn', dose_idx=-1):
    basedir = basedir or Path('/gpfs_projects/prabhat.kc/lowdosect/transfers/transfers_4_spie/exps/quant_analysis/mita_lcd/results/95d_2_75d_2_25d_p96_no_norm/no_norm/redcnn/augTrTaTdT/')
    auc_means = []
    auc_stds = []
    recon_idx = 1 if recon=='cnn' else 0
    for i in range(4):
        data = scipy.io.loadmat(basedir / f'_idx_{i+1}.mat')
        auc_means.append(data['auc_all'][:].mean(axis=0)[recon_idx, dose_idx]) #get last dose level (highest)
        auc_stds.append(data['auc_all'][:].std(axis=0)[recon_idx, dose_idx]) # according to line 124 of </gpfs_projects/prabhat.kc/lowdosect/transfers/transfers_4_spie/exps/quant_analysis/mita_lcd/mita_lcd_plot_ct_poster.m> 0th index is fbp, 1st is DLIR
    return auc_means, auc_stds

def load_all_adult_data():
    basedir = Path("/gpfs_projects/prabhat.kc/lowdosect/transfers/transfers_4_spie/exps/quant_analysis/mita_lcd")
    resultsdir = basedir / "results/quarter/8p_uni_norm/dncnn/augTrTaTdT/"
    ndose_levels = 5
    nrecons = 2
    nlesions = 4
    auc_means = np.zeros([ndose_levels, nrecons, nlesions])
    auc_stds = np.zeros([ndose_levels, nrecons, nlesions])
    for dose_idx in range(ndose_levels):
        for recon_idx, recon in enumerate(['fbp', 'cnn']):
            auc_means[dose_idx, recon_idx, :], auc_stds[dose_idx, recon_idx, :] = load_adult_dataset(resultsdir, dose_idx=dose_idx, recon=recon)
    return auc_means, auc_stds

    # I should have all the adult data from Prabhat saved as a h5 file so I can easily swap it out for different results, i.e. to compare against Rongping's MITA_LCD.m to make sure everything is consistent
# %%



def main(results_dir, output_fname):
    """
    Dimensions of AUC results array are [reader num, dose level, recon option, inserts num, patient diameter] 
    These are reversed from matlab which is F index, but Python is C indexed
    """

    # plt.style.use('seaborn')

    # h5file = '/home/brandon.nelson/Dev/DLIR_Ped_Generalizability/geomtric_phantom_studies/results/LCD/LCD_results.h5'
    h5file = f'{results_dir}/LCD_results.h5'

    f = h5py.File(h5file, 'r')
    auc = f['auc'][:]
    snr = f['snr'][:]
    diameters = f['patient_diameters'][:]
    dose_levels = f['dose_levels'][:]
    # lesion_HUs = f['insert_HUs']
    lesion_HUs = [14, 7, 5, 3]
    lesion_radii_mm = [3, 5, 7, 10]
    lesion_radii_pix = [2.30, 3.99, 5.57, 7.97]
    recon_types = list(map(lambda x: x.decode('UTF-8'), f['recon_types'][:]))
    nreaders = f['readers'][:]
    f.close()

    auc_mean, auc_std = auc.mean(axis=0), auc.std(axis=0)
    snr_mean, snr_std = snr.mean(axis=0), auc.std(axis=0)

    adult_auc_means, adult_auc_stds = load_adult_ref_data()

    dose_idx=0
    recon_idx=recon_types.index('fbp')
    lesion_idxs = [0, 1, 3, 2]
    fig, axs = plt.subplots(2, 2, figsize=(6,6), sharex=True, sharey=True)
    subplot_idx = 0
    for lesion_idx, ax in zip(lesion_idxs , axs.flatten()):
        ax.errorbar(diameters, auc_mean[dose_idx, recon_idx, lesion_idx, :],
                    yerr=auc_std[dose_idx, recon_idx, lesion_idx, :],
                    label='FBP')
        ax.errorbar([200], adult_auc_means[lesion_idx],
                    yerr=adult_auc_stds[lesion_idx],
                    fmt='*', markersize=10,
                    color='black', label='Adult Reference\n(340 mm FOV)')
        ax.set_title(f'{lesion_radii_mm[lesion_idx]} mm diameter\n{lesion_HUs[lesion_idx]} HU disk')
        fovs = np.round(diameters*1.1).astype(int)
        twiny = ax.twiny()
        twiny.set_xlim(ax.get_xlim())
        twiny.set_xticks(np.linspace(min(fovs), max(fovs), 5).astype(int))
        if subplot_idx < 2:
            twiny.set_xlabel("Recon FOV [mm]")
        else:
            ax.set_xlabel('Patient Diameter [mm]')
            twiny.set_xticklabels([])
        if not subplot_idx % 2:
            ax.set_ylabel('Detectability AUC')
        twiny.grid(False)
        subplot_idx+=1

    recon_idx=recon_types.index('dl_REDCNN')
    for lesion_idx, ax in zip(lesion_idxs, axs.flatten()):
        ax.errorbar(diameters, auc_mean[dose_idx, recon_idx, lesion_idx, :],
        yerr=auc_std[dose_idx, recon_idx, lesion_idx, :],
        label='REDCNN')
        if lesion_idx==0:
            ax.legend()
    fig.tight_layout()
    if output_fname:
        Path(output_fname).parent.mkdir(exist_ok=True, parents=True)
        fig.savefig(output_fname, dpi=600)
        print(f'File saved: {output_fname}')
    else:
        fig.show()


# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description='Plots ESF Curves')
#     parser.add_argument('--datadir', '-d', default=None,
#                         help="directory containing LCD_results.h5 file")
#     parser.add_argument('--output_fname','-o', required=False,
#                         help="Output filename")
#     args = parser.parse_args()
#     main(args.datadir, args.output_fname)
# %%
results_dir = '../../results/LCD'
h5file = f'{results_dir}/LCD_results.h5'

f = h5py.File(h5file, 'r')
auc = f['auc'][:]
snr = f['snr'][:]
diameters = f['patient_diameters'][:].astype(int)
dose_levels = f['dose_levels'][:]
# lesion_HUs = f['insert_HUs']
lesion_HUs = [14, 7, 5, 3]
lesion_radii_mm = [3, 5, 7, 10]
lesion_radii_pix = [2.30, 3.99, 5.57, 7.97]
recon_types = list(map(lambda x: x.decode('UTF-8'), f['recon_types'][:]))
nreaders = f['readers'][:]
f.close()

auc_mean, auc_std = auc.mean(axis=0), auc.std(axis=0)
snr_mean, snr_std = snr.mean(axis=0), auc.std(axis=0)

# %% [markdown]
# save original adult ref data from CT conference poster <>
# %%
adult_auc_means, adult_auc_stds = load_all_adult_data()
adult_ref_h5file = f'{results_dir}/adult_ref_LCD_results.h5'
with h5py.File(adult_ref_h5file, 'w') as f:
    dset = f.create_dataset('auc', (10, )) 
# %%
dose_idx=0
recon_idx=recon_types.index('fbp')
lesion_idxs = [0, 1, 3, 2]
# %%
import seaborn as sns
import numpy as np
plt.style.use('seaborn')
fbp_idx = recon_types.index('fbp')
cnn_idx = recon_types.index('dl_REDCNN')
diam_idx = [0, 2, -1]
# diameters[diam_idx]
fig, axs = plt.subplots(2, 2, figsize=(6,6), sharex=True, sharey=True)
subplot_idx = 0
dose_levels_pct = np.ceil(dose_levels / dose_levels.max()*100)
for lesion_idx, ax in zip(lesion_idxs , axs.flatten()):
    auc_mean_diff = auc_mean[:, cnn_idx, lesion_idx, diam_idx]-auc_mean[:, fbp_idx, lesion_idx, diam_idx]
    auc_std_diff = auc_std[:, cnn_idx, lesion_idx, diam_idx]-auc_mean[:, fbp_idx, lesion_idx, diam_idx]

    if subplot_idx > 1:
        ax.set_xlabel('Dose Level [%]')
    for d in diam_idx:
        # ax.errorbar(dose_levels, auc_mean_diff[:, d], yerr=auc_std_diff[:, d], label=f'{diameters[d]}')
        ax.plot(dose_levels_pct, auc_mean_diff[:, d], label=f'{diameters[d]:0.0f} mm')
        ax.set_title(f'{lesion_radii_mm[lesion_idx]} mm diameter\n{lesion_HUs[lesion_idx]} HU disk')
        if not subplot_idx % 2:
            ax.set_ylabel('Difference in Detectability\nREDCNN - FBP [AUC]')
    if subplot_idx < 1:
        ax.legend()
    subplot_idx+=1
fig.tight_layout()
fig.savefig(Path(results_dir) / 'auc_diffs_.png', dpi=600)
# %%
import seaborn as sns
import numpy as np
fbp_idx = recon_types.index('fbp')
cnn_idx = recon_types.index('dl_REDCNN')
# diam_idx = [0, 2, -1]
# diameters[diam_idx]

output_dir = Path(results_dir) / 'LCD_v_dose'
output_dir.mkdir(exist_ok=True, parents=True)

for diam_idx, d in enumerate(diameters):
    fig, axs = plt.subplots(2, 2, figsize=(6,6), sharex=True, sharey=True)
    subplot_idx = 0
    dose_levels_pct = np.ceil(dose_levels / dose_levels.max()*100)
    for lesion_idx, ax in zip(lesion_idxs , axs.flatten()):

        if subplot_idx > 1:
            ax.set_xlabel('Dose Level [%]')
        # for d in diam_idx:
        ax.errorbar(dose_levels_pct, auc_mean[:, fbp_idx, lesion_idx, diam_idx], yerr=auc_std[:, fbp_idx, lesion_idx, diam_idx], label=f'FBP {diameters[diam_idx]:0.0f} mm')
        ax.errorbar(dose_levels_pct, auc_mean[:, cnn_idx, lesion_idx, diam_idx], yerr=auc_std[:, cnn_idx, lesion_idx, diam_idx], label=f'REDCNN {diameters[diam_idx]:0.0f} mm')
        ax.errorbar(dose_levels_pct, adult_auc_means[:, fbp_idx, lesion_idx],
                    yerr=adult_auc_stds[:, fbp_idx, lesion_idx],
                    fmt='--', markersize=10,
                    color='black', label='Adult FBP Reference\n(212 mm FOV)')
        ax.errorbar(dose_levels_pct, adult_auc_means[:, cnn_idx, lesion_idx],
                    yerr=adult_auc_stds[:, cnn_idx, lesion_idx],
                    fmt='--', markersize=10,
                    color='gray', label='Adult REDCNN Reference\n(212 mm FOV)')
        # ax.plot(dose_levels_pct, auc_mean_diff[:, d], label=f'{diameters[d]:0.0f} mm')
        ax.set_title(f'{lesion_radii_mm[lesion_idx]} mm diameter\n{lesion_HUs[lesion_idx]} HU disk')
        if not subplot_idx % 2:
            ax.set_ylabel('Detectability AUC')
        if subplot_idx < 1:
            ax.legend()
        subplot_idx+=1
        ax.set_ylim([0.4, 1])
    output_fname = output_dir / f'LCD_v_dose_diameter_{d}mm.png'
    fig.suptitle(f'Patient Diameter: {diameters[diam_idx]:0.0f} mm (FOV: {diameters[diam_idx]*1.1:0.0f} mm)')
    fig.savefig(output_fname, dpi=600) 
# %% [markdown]
# experimenting with 2D display
import pandas as pd
import seaborn as sns

lesion_HUs = [14, 7, 5, 3]
lesion_diameter_mm = [3, 5, 7, 10]

def get_auc_df(lesion_idx=0, recon='fbp'):
    recon_idx = 0 if recon=='fbp' else 1
    ped_fbp_auc = pd.DataFrame(auc_mean[:, recon_idx, lesion_idx, :], columns = diameters)
    ped_fbp_auc['Dose Level [%]'] = dose_levels_pct
    ped_fbp_auc.set_index('Dose Level [%]', inplace=True)

    adult_fbp_auc = pd.DataFrame(adult_auc_means[:, 0, lesion_idx], columns = [200])
    adult_fbp_auc['Dose Level [%]'] = dose_levels_pct
    adult_fbp_auc.set_index('Dose Level [%]', inplace=True)
    auc = ped_fbp_auc.join(adult_fbp_auc)
    return auc

get_auc_df(0, 'cnn')
# %%
import matplotlib.patches as patches
f, axs = plt.subplots(2, 2, figsize=(12,10),gridspec_kw=dict(hspace=0.4, wspace=0.2))
for lesion_idx, (ax, lesion_hu, lesion_diam) in enumerate(zip(axs.flatten(), lesion_HUs, lesion_diameter_mm)):

    fbp_auc = get_auc_df(lesion_idx, 'fbp')
    sns.heatmap(fbp_auc, annot=True, ax=ax, cbar_kws=dict(label=f'AUC'))
    ax.set_xlabel('Patient Diameter [mm]')
    twiny = ax.twiny()

    fovs = np.round(fbp_auc.columns*1.1).astype(int).to_list()
    fovs[fbp_auc.columns.to_list().index(200)] = 340 # From RZ, min FOV for adult scan protocol
    twiny.set_xticks(ax.get_xticks(), fovs)
    twiny.set_xlim(ax.get_xlim())
    twiny.set_xlabel("Recon FOV [mm]")
    twiny.grid(False)
    nrows = len(fbp_auc)
    rect = patches.Rectangle((6, 0.05), 0.97, nrows-0.1, linewidth=3, edgecolor='tab:blue', facecolor='none')
    ax.annotate("Adult Reference",
                xy=(6.75, nrows), xycoords='data',
                xytext=(0.75, 0.025), textcoords='figure fraction',
                color='tab:blue',
                arrowprops=dict(facecolor='tab:blue', shrink=0.05), weight='bold')
    ax.add_patch(rect)
    ax.set_title(f'{lesion_diam} mm, {lesion_hu} HU')
f.suptitle("FBP")
# %%
f, axs = plt.subplots(2, 2, figsize=(10,10))
for lesion_idx, (ax, lesion_hu, lesion_diam) in enumerate(zip(axs.flatten(), lesion_HUs, lesion_diameter_mm)):
    fbp_auc = get_auc_df(lesion_idx, 'cnn')
    sns.heatmap(fbp_auc, annot=True, ax=ax, cbar_kws=dict(label=f'AUC'))
    ax.set_xlabel('Patient Diameter [mm]')
    ax.set_title(f'{lesion_diam} mm, {lesion_hu} HU')
f.suptitle("REDCNN")
# %%
f, axs = plt.subplots(2, 2, figsize=(10,10), sharex=True, sharey=True)
for lesion_idx, (ax, lesion_hu, lesion_diam) in enumerate(zip(axs.flatten(), lesion_HUs, lesion_diameter_mm)):

    fbp_auc = get_auc_df(lesion_idx, 'fbp')
    cnn_auc = get_auc_df(lesion_idx, 'cnn')

    sns.heatmap(cnn_auc - fbp_auc, annot=False, ax=ax, cbar_kws=dict(label=f'AUC'))
    ax.set_xlabel('Patient Diameter [mm]')
    ax.set_title(f'{lesion_diam} mm, {lesion_hu} HU')
f.suptitle("REDCNN - FBP")

# %%
