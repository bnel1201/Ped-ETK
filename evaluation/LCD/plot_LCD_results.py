import argparse
from pathlib import Path

import numpy as np
import scipy.io
import matplotlib.pyplot as plt
import h5py


def load_adult_ref_data(basedir=None, dose_idx=-1):
    basedir = basedir or Path('/gpfs_projects/prabhat.kc/lowdosect/transfers/transfers_4_spie/exps/quant_analysis/mita_lcd/results/95d_2_75d_2_25d_p96_no_norm/no_norm/redcnn/augTrTaTdT/')
    auc_means = []
    auc_stds = []
    for i in range(4):
        data = scipy.io.loadmat(basedir / f'_idx_{i+1}.mat')
        auc_means.append(data['auc_all'][:].mean(axis=0)[1, dose_idx]) #get last dose level (highest)
        auc_stds.append(data['auc_all'][:].std(axis=0)[1, dose_idx]) # according to line 124 of </gpfs_projects/prabhat.kc/lowdosect/transfers/transfers_4_spie/exps/quant_analysis/mita_lcd/mita_lcd_plot_ct_poster.m> 0th index is fbp, 1st is DLIR
    return auc_means, auc_stds


def main(results_dir, output_fname):
    """
    Dimensions of AUC results array are [reader num, dose level, recon option, inserts num, patient diameter] 
    These are reversed from matlab which is F index, but Python is C indexed
    """

    plt.style.use('seaborn')

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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plots ESF Curves')
    parser.add_argument('--datadir', '-d', default=None,
                        help="directory containing LCD_results.h5 file")
    parser.add_argument('--output_fname','-o', required=False,
                        help="Output filename")
    args = parser.parse_args()
    main(args.datadir, args.output_fname)
