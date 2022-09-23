import argparse
from pathlib import Path

import matplotlib.pyplot as plt
from utils.mtf_plot import plot_patient_diameter_mtf


def main(datadir=None, output_fname=None, processed=False):
    datadir = datadir or '/gpfs_projects/brandon.nelson/DLIR_Ped_Generalizability/geomtric_phantom_studies/CTP404/monochromatic/'
    patient_dirs = sorted(list(Path(datadir).glob('diameter*')))

    plt.style.use('seaborn')
    f, axs = plt.subplots(2, 3, figsize=(9, 7), sharex='col', sharey='row',
                        gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for patient_dir, ax in zip(patient_dirs, axs.flatten()):
        if processed:
            mtf_csv_fname = patient_dir / 'I0_3000000_processed' / 'fbp_sharp_v001_mtf.csv'
        else:
            mtf_csv_fname = patient_dir / 'I0_3000000' / 'fbp_sharp_v001_mtf.csv'
        plot_patient_diameter_mtf(mtf_csv_fname, ax=ax)

    if output_fname is None:
        plt.show()
    else:
        Path(output_fname).parent.mkdir(exist_ok=True, parents=True)
        f.savefig(output_fname, dpi=600)
        print(f'File saved: {output_fname}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plots MTF Curves')
    parser.add_argument('--datadir', '-d',
                        help="directory containing different patient diameter CT simulations")
    parser.add_argument('--output_fname','-o', required=False,
                        help="filename for the saved plot")
    parser.add_argument('--processed', action='store_true', default=False,
                        help='boolean to plot the processed results, defaults to false using the baseline')
    args = parser.parse_args()
    main(args.datadir, output_fname=args.output_fname, processed=args.processed)