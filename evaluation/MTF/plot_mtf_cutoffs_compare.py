# %%
import argparse
import matplotlib.pyplot as plt
from pathlib import Path
from utils.mtf_cutoffs import merge_patient_diameters, get_mtf_results


def main(datadir=None, output_fname=None, contrasts=None):
    datadir = datadir or '/gpfs_projects/brandon.nelson/DLIR_Ped_Generalizability/geomtric_phantom_studies/CTP404/monochromatic/'
    patient_dirs = sorted(list(Path(datadir).glob('diameter*')))
    mtf50_baseline = merge_patient_diameters(patient_dirs, mtfval=50)
    mtf50_proc = merge_patient_diameters(patient_dirs, mtfval=50, processed=True)
    mtf50_rel = mtf50_proc / mtf50_baseline

    mtf10_baseline = merge_patient_diameters(patient_dirs, mtfval=10)
    mtf10_proc = merge_patient_diameters(patient_dirs, mtfval=10, processed=True)
    mtf10_rel = mtf10_proc / mtf10_baseline

    plt.style.use('seaborn')

    ylim = [0, 1.8]
    f, (ax0, ax1) = plt.subplots(1, 2, figsize=(8, 4))
    mtf50_rel.plot(ax=ax0, kind='bar', ylabel='REDCNN 50% MTF / FBP 50% MTF')
    ax0.set_ylim(ylim)
    mtf10_rel.plot(ax=ax1, kind='bar', ylabel='REDCNN 10% MTF / FBP 10% MTF')
    ax1.set_ylim(ylim)
    ax1.get_legend().remove() 

    if output_fname is None:
        plt.show()
    else:
        Path(output_fname).parent.mkdir(exist_ok=True, parents=True)
        f.savefig(output_fname, dpi=600)
        print(f'File saved: {output_fname}')

    contrasts = contrasts or [15, 120, 340]
    mtf50_baseline_sub = mtf50_baseline.filter(contrasts, axis=0)*10
    mtf50_baseline_sub.columns = [int(c.split('mm')[0]) for c in mtf50_baseline_sub.columns]

    mtf50_proc_sub = mtf50_proc.filter(contrasts, axis=0)*10
    mtf50_proc_sub.columns = [int(c.split('mm')[0]) for c in mtf50_proc_sub.columns]

    f, ax = plt.subplots(figsize=(4,4))

    mtf50_rel_sub = mtf50_baseline_sub/ mtf50_proc_sub
    mtf50_rel_sub.T.plot(ax=ax)
    ax.set_xlabel('Patient Diameter [mm]')
    ax.set_ylabel('Relative Sharpness\n(REDCNN 50% MTF / FBP 50% MTF')
    ax.set_ylim([0.8, 1.1])

    f.tight_layout()
    fname = Path(output_fname).parent / 'relative_sharpness.png'
    f.savefig(fname, dpi=600)
    print(fname)


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
