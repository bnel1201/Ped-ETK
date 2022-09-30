import argparse
import matplotlib.pyplot as plt
from pathlib import Path
from utils.mtf_cutoffs import merge_patient_diameters


def plot_relative_cutoffs_by_contrast(mtf50_rel, mtf10_rel, output_fname=None):
    plt.style.use('seaborn')

    ylim = [0, 1.8]
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
    contrasts = contrasts or [15, 120, 340]
    mtf_baseline_sub = mtf_baseline.filter(contrasts, axis=0)*10
    mtf_baseline_sub.columns = [int(c.split('mm')[0]) for c in mtf_baseline_sub.columns]

    mtf_proc_sub = mtf_proc.filter(contrasts, axis=0)*10
    mtf_proc_sub.columns = [int(c.split('mm')[0]) for c in mtf_proc_sub.columns]

    mtf_rel_sub = mtf_proc_sub / mtf_baseline_sub

    f, ax = plt.subplots(figsize=(4,4))
    mtf_rel_sub.T.plot(ax=ax)
    
    relative_sharpness_fname = Path(output_fname).parent / f'mtf{cutoff_val}_relative_sharpness.png' if output_fname else None
    f, ax = plt.subplots(figsize=(4,4))
    ax.set_ylabel(f'Relative Sharpness\n(REDCNN {cutoff_val}% MTF / FBP {cutoff_val}% MTF')
    f.tight_layout()
    if output_fname is None:
        plt.show()
    else:
        Path(output_fname).parent.mkdir(exist_ok=True, parents=True)
        f.savefig(relative_sharpness_fname, dpi=600)
        print(f'File saved: {relative_sharpness_fname}')
    ax.set_xlabel('Patient Diameter [mm]')
    return ax


def main(datadir=None, output_fname=None, contrasts=None):
    datadir = datadir or '/gpfs_projects/brandon.nelson/DLIR_Ped_Generalizability/geomtric_phantom_studies/CTP404/monochromatic/'
    patient_dirs = sorted(list(Path(datadir).glob('diameter*')))

    mtf50_baseline = merge_patient_diameters(patient_dirs, mtfval=50)
    mtf50_proc = merge_patient_diameters(patient_dirs, mtfval=50, processed=True)

    mtf10_baseline = merge_patient_diameters(patient_dirs, mtfval=10)
    mtf10_proc = merge_patient_diameters(patient_dirs, mtfval=10, processed=True)

    mtf10_rel = mtf10_proc / mtf10_baseline
    mtf50_rel = mtf50_proc / mtf50_baseline
    plot_relative_cutoffs_by_contrast(mtf50_rel, mtf10_rel, output_fname)

    plot_relative_sharpness_by_diameter(mtf50_baseline, mtf50_proc, cutoff_val=50, contrasts=contrasts)
    plot_relative_sharpness_by_diameter(mtf10_baseline, mtf10_proc, cutoff_val=10, contrasts=contrasts)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plots MTF Curves')
    parser.add_argument('--datadir', '-d',
                        help="directory containing different patient diameter CT simulations")
    parser.add_argument('--output_fname', '-o',
                        help="filename for the saved plot")
    parser.add_argument('--contrasts', '-c',
                        help="Contrast disks to include [list of integers: -1000, 15, 35, 120, 340, 990]")
    args = parser.parse_args()
    main(args.datadir, output_fname=args.output_fname)
