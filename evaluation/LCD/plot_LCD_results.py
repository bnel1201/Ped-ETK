import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import h5py


def main(results_dir, output_fname):
    """
    Dimensions of AUC results array are [reader num, dose level, recon option, inserts num, patient diameter] 
    These are reversed from matlab which is F index, but Python is C indexed
    """

    plt.style.use('seaborn')

    # h5file = '/home/brandon.nelson/Dev/DLIR_Ped_Generalizability/geomtric_phantom_studies/results/LCD/LCD_results.h5'
    h5file = f'{results_dir}/LCD_results.h5'

    f = h5py.File(h5file, 'r')
    f.keys()
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
    auc_mean.shape
    dose_idx=0
    recon_idx=recon_types.index('fbp')
    fig, axs = plt.subplots(1, 4, figsize=(9,3), sharex=True, sharey=True)
    for lesion_idx, ax in zip(range(auc_mean.shape[-1]), axs.flatten()):
        ax.errorbar(diameters, auc_mean[dose_idx, recon_idx, lesion_idx, :],
                    yerr=auc_std[dose_idx, recon_idx, lesion_idx, :],
                    label='FBP')
        ax.set_title(f'{lesion_HUs[lesion_idx]} HU disk\n ({lesion_radii_mm[lesion_idx]} mm diameter)')
    [ax.set_xlabel('Patient Diameter [mm]') for ax in axs]
    axs[0].set_ylabel('Detectability AUC')

    recon_idx=recon_types.index('dl_REDCNN')
    for lesion_idx, ax in zip(range(auc_mean.shape[-1]), axs.flatten()):
        ax.errorbar(diameters, auc_mean[dose_idx, recon_idx, lesion_idx, :],
        yerr=auc_std[dose_idx, recon_idx, lesion_idx, :],
        label='REDCNN')
    axs[0].legend()
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