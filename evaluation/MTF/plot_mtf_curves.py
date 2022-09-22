# %%
import matplotlib.pyplot as plt
from pathlib import Path
from utils.mtf_plot import plot_patient_diameter_mtf


def main():
    datadir = Path('/gpfs_projects/brandon.nelson/DLIR_Ped_Generalizability/geomtric_phantom_studies/CTP404/monochromatic/')
    patient_dirs = sorted(list(datadir.glob('diameter*')))

    plt.style.use('seaborn')
    f, axs = plt.subplots(2, 3, figsize=(9, 7), sharex='col', sharey='row',
                        gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for patient_dir, ax in zip(patient_dirs, axs.flatten()):
        mtf_csv_fname = patient_dir / 'I0_3000000' / 'fbp_sharp_v001_mtf.csv'
        plot_patient_diameter_mtf(mtf_csv_fname, ax=ax)
    # %%
    fname = 'fbp_mtf_baseline.png'
    f.savefig(fname, dpi=600)
    print(f'File saved: {fname}')

# %%
if __name__ == '__main__':
    main()