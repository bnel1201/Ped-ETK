# %%
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

datadir = Path('/gpfs_projects/brandon.nelson/DLIR_Ped_Generalizability/geomtric_phantom_studies/CTP404/monochromatic/')
patient_dirs = sorted(list(datadir.glob('diameter*')))
idx = 0
df = pd.read_csv(patient_dirs[idx] / 'I0_3000000_processed' / 'fbp_sharp_v001_mtf.csv')
df
# %%
def plot_patient_diameter_mtf(patient_diameter_dir, ax=None):
    if ax is None:
        f, ax = plt.subplots()
    diameter = patient_diameter_dir.stem.split('diameter')[1]
    df = pd.read_csv(patient_diameter_dir / 'I0_3000000_processed' / 'fbp_sharp_v001_mtf.csv')
    freq_lpcm_lbl = 'frequencies [lp/cm]'
    df[freq_lpcm_lbl] = df['frequencies [1/mm]']*10
    HUs = sorted([int(h.split(' HU')[0]) for h in df.columns[1:-1]])
    cols = [freq_lpcm_lbl]
    cols += [f' {h} HU' for h in HUs]
    df = df[cols]
    df.plot(ax=ax, x=freq_lpcm_lbl, xlim=[0, 20], title=diameter, ylabel='MTF')
    return ax
# %%
plt.style.use('seaborn')
f, axs = plt.subplots(2, 3, figsize=(9, 7), sharex='col', sharey='row',
                      gridspec_kw=dict(hspace=0.1, wspace=0.1))
for d, ax in zip(patient_dirs, axs.flatten()):
    plot_patient_diameter_mtf(d, ax)
# %%
fname = 'mtf_redcnn.png'
f.savefig(fname, dpi=600)
print(f'File saved: {fname}')
