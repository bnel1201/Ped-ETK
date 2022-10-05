import argparse
from pathlib import Path

import matplotlib.pyplot as plt

from utils.mtf_cutoffs import merge_patient_diameters, abs_HU
from utils.csv_io import (write_relative_sharpness_to_csv,
                          write_cutoffs_to_csv)


def plot_relative_cutoffs_by_contrast(mtf50_rel, mtf10_rel, output_fname=None):

    ylim = [0.5, 1.5]
    f, (ax0, ax1) = plt.subplots(1, 2, figsize=(8, 4))
    mtf50_rel.plot(ax=ax0, kind='bar', ylabel='REDCNN 50% MTF / FBP 50% MTF')
    ax0.set_ylim(ylim)
    mtf10_rel.plot(ax=ax1, kind='bar', ylabel='REDCNN 10% MTF / FBP 10% MTF')
    ax1.set_ylim(ylim)
    ax1.get_legend().remove()
    f.tight_layout()

    if output_fname is None:
        plt.show()
    else:
        Path(output_fname).parent.mkdir(exist_ok=True, parents=True)
        f.savefig(output_fname, dpi=600)
        print(f'File saved: {output_fname}')


def plot_relative_sharpness_by_diameter(mtf_baseline, mtf_proc, cutoff_val=50, contrasts=None, output_fname=None):

    mtf_baseline.columns = [int(c.split('mm')[0]) for c in mtf_baseline.columns]
    mtf_proc.columns = [int(c.split('mm')[0]) for c in mtf_proc.columns]

    if contrasts:
        contrasts = list(map(abs, contrasts))
        mtf_baseline = mtf_baseline.filter(items=contrasts, axis=0)
        mtf_proc = mtf_proc.filter(items=contrasts, axis=0)
    
    mtf_baseline *= 10 #convert from 1/mm to 1/cm
    mtf_proc *= 10

    mtf_rel = mtf_proc / mtf_baseline

    mtf_rel.sort_index(ascending=False, inplace=True)

    f, ax = plt.subplots(figsize=(4,4))
    mtf_rel.T.plot(ax=ax)
    
    relative_sharpness_fname = Path(output_fname).parent / f'mtf{cutoff_val}_relative_sharpness.png' if output_fname else None
    ax.set_ylabel(f'Relative Sharpness\n(REDCNN {cutoff_val}% MTF / FBP {cutoff_val}% MTF')
    ax.set_xlabel('Patient Diameter [mm]')
    f.tight_layout()
    if output_fname is None:
        plt.show()
    else:
        f.savefig(relative_sharpness_fname, dpi=600)
        print(f'File saved: {relative_sharpness_fname}')


def main(datadir=None, output_fname=None, contrasts=None):
    datadir = datadir or '/gpfs_projects/brandon.nelson/DLIR_Ped_Generalizability/geomtric_phantom_studies/CTP404/monochromatic/'
    patient_dirs = sorted(list(Path(datadir).glob('diameter*')))

    mtf50_baseline = merge_patient_diameters(patient_dirs, mtfval=50)
    mtf50_baseline = abs_HU(mtf50_baseline)
    mtf50_proc = merge_patient_diameters(patient_dirs, mtfval=50, processed=True)
    mtf50_proc = abs_HU(mtf50_proc)

    mtf10_baseline = merge_patient_diameters(patient_dirs, mtfval=10)
    mtf10_baseline = abs_HU(mtf10_baseline)
    mtf10_proc = merge_patient_diameters(patient_dirs, mtfval=10, processed=True)
    mtf10_proc = abs_HU(mtf10_proc)
    
    mtf10_rel = mtf10_proc / mtf10_baseline
    mtf50_rel = mtf50_proc / mtf50_baseline

    mtf_results_dir = Path(output_fname).parents[1]
    write_relative_sharpness_to_csv(mtf50_rel, mtf10_rel, mtf_results_dir / 'relative_sharpness_values.csv')
    write_cutoffs_to_csv(mtf50_baseline, mtf50_proc, 50, mtf_results_dir / 'mtf50.csv')
    write_cutoffs_to_csv(mtf10_baseline, mtf10_proc, 10, mtf_results_dir / 'mtf10.csv')

    with plt.style.context('seaborn'):
        plot_relative_cutoffs_by_contrast(mtf50_rel, mtf10_rel, output_fname)

        plot_relative_sharpness_by_diameter(mtf50_baseline, mtf50_proc, cutoff_val=50, contrasts=contrasts, output_fname=output_fname)
        plot_relative_sharpness_by_diameter(mtf10_baseline, mtf10_proc, cutoff_val=10, contrasts=contrasts, output_fname=output_fname)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plots MTF cutoff curves')
    parser.add_argument('--datadir', '-d',
                        help="directory containing different patient diameter CT simulations")
    parser.add_argument('--output_fname', '-o',
                        help="filename for the saved plot")
    parser.add_argument('--contrasts', '-c', nargs='+',
                        help="Contrast disks to include [list of integers: -1000, 15, 35, 120, 340, 990]")
    args = parser.parse_args()
    contrasts = list(map(int, args.contrasts[0].split(' '))) if args.contrasts else None
    main(args.datadir, output_fname=args.output_fname, contrasts=contrasts)
