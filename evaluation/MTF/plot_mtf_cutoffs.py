# %%
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path


def clean_column_names(df):
    HUs = [round(float(h.split(' HU')[0])) for h in df.columns[1:]]
    new_cols = [df.columns[0]] + [f' {h} HU' for h in HUs]
    return df.rename(columns={old:new for old,new in zip(df.columns, new_cols)})


def sort_HU_cols(df):
    HUs = sorted([int(h.split(' HU')[0]) for h in df.columns[1:]])
    cols = [df.columns[0]]
    cols += [f' {h} HU' for h in HUs]
    return df[cols]


def get_mtf_results(patient_dir, mtfval=10):
    df = pd.read_csv(patient_dir / 'I0_3000000' / f'results_MTF{mtfval}.csv')
    diameter = patient_dir.stem.split('diameter')[1]
    df = clean_column_names(df)
    df = sort_HU_cols(df)
    HUs = [int(h.split(' HU')[0]) for h in df.columns[1:]]
    mtf10 = df.iloc[1,1:].to_numpy()
    return pd.DataFrame({'Contrast [HU]': HUs, f'{diameter}': mtf10})
# %%
def merge_patient_diameters(patient_dirs, mtfval=10):
    mtf10 = get_mtf_results(patient_dirs[0], mtfval)
    for idx in range(1, len(patient_dirs)):
        other_mtf = get_mtf_results(patient_dirs[idx], mtfval)
        mtf10=mtf10.merge(other_mtf, how='inner', on='Contrast [HU]')
        mtf10 = mtf10.set_index('Contrast [HU]')
        # mtf10 = mtf10.merge(other_mtf.set_index('Contrast [HU]'))
    return mtf10

datadir = Path('/gpfs_projects/brandon.nelson/DLIR_Ped_Generalizability/geomtric_phantom_studies/CTP404/monochromatic/')
patient_dirs = sorted(list(datadir.glob('diameter*')))
# %%
plt.style.use('seaborn')

ylim = [0, 13]
f, (ax0, ax1) = plt.subplots(1, 2, figsize=(8, 4))
mtf50 = merge_patient_diameters(patient_dirs, mtfval=50)
mtf50*=10
mtf50.plot(ax=ax0, kind='bar', ylabel='50% MTF [lp/cm]')
ax0.set_ylim(ylim)
mtf10 = merge_patient_diameters(patient_dirs, mtfval=10)
mtf10*=10
mtf10.plot(ax=ax1, kind='bar', ylabel='10% MTF [lp/cm]')
ax1.set_ylim(ylim)
ax1.get_legend().remove() 

# %%
fname = 'mtf_cutoff_vals.png'
f.tight_layout()
f.savefig(fname, dpi=600)
print(f'File saved: {fname}')

# %%
