# %%
import matplotlib.pyplot as plt
import h5py
import numpy as np
import pandas as pd
import seaborn as sns

from measure_anthro_mse import load_patient

# %%
with h5py.File('test.h5', 'r') as f:
    fbp_mses = f['/fbp/mse'][:]
    cnn_mses = f['/cnn/mse'][:]
    patients = f['/patients/names'][:]
    effective_diameters = f['/patients/effective_diameters'][:]
    doselevels = f['/doselevels'][:]
    basedir = f['/patients/names'].attrs['base_dir']
# %%
def get_patient_name(patients, idx): return ' '.join(patients[idx].astype(str).split('_')[:2])

patient_names = [get_patient_name(patients, i) for i in range(len(patients))]

patient_info = pd.read_csv('/home/brandon.nelson/Dev/DLIR_Ped_Generalizability/geomtric_phantom_studies/make_phantoms/anthropomorphic/selected_xcat_peds.csv')


def get_patient_code(patient_name):
    """
    this is the inverse of get_nrb_filenames
    """
    if patient_name.split(' ')[1][:2] == 'pt':
        code = patient_name.split(' ')[1][2:]
        return code
    
    code = 'Reference '
    if patient_name.split(' ')[1] == 'infant':
        code += 'newborn'
        return code
    age_int = int(patient_name.split(' ')[1][:-2])

    code += f'{age_int} yr old'
    if age_int < 15:
        return code
    
    gender = 'M' if patient_name.split(' ')[0] == 'male' else 'F'
    code += f' {gender}'
    return code

def get_patient_info(patient_code): return patient_info[patient_info['Code #'] == patient_code]

def get_patient_age(patient_code): return float(patient_info[patient_info['Code #'] == patient_code]['age (year)'])

def get_patient_weight(patient_code): return float(patient_info[patient_info['Code #'] == patient_code]['weight (kg)'])

def get_closest_doselevel_idx(desired_doselevel):
    dose_idx = np.argmin(np.abs(doselevels_pct - desired_doselevel))
    print(f'desired: {desired_doselevel}, closest: {doselevels_pct[dose_idx]}')
    return dose_idx

patient_codes = [get_patient_code(patient_name) for patient_name in patient_names]
ages = [get_patient_age(code) for code in patient_codes]
weights = [get_patient_weight(code) for code in patient_codes]

assert set(patient_info['Code #']) == set(patient_codes)
patient_info = patient_info.set_index('Code #').join(pd.DataFrame({'Code #': patient_codes, 'effective diameter (cm)': effective_diameters/10}).set_index('Code #')).reset_index()
patient_info
# %%
doselevels_pct = doselevels / max(doselevels)

for idx in range(3):
    patient_name = get_patient_name(patients, idx)
    patient_code = get_patient_code(patient_name)
    age_yrs = get_patient_age(patient_code)
    weight_kg = get_patient_weight(patient_code)
    eff_diameter = effective_diameters[idx]

    desired_doselevels = [1, 0.5, 0.1]
    doseidxs = [get_closest_doselevel_idx(desired_doselevel) for desired_doselevel in desired_doselevels]

    img_dict = load_patient(basedir, patients[idx].astype(str))
    base_images = np.concatenate([img_dict['true'], img_dict['noiseless']],axis=1)
    noisey_images = np.concatenate([np.concatenate([img_dict['fbp'][d, 0], img_dict['cnn'][d, 0]],axis=1) for d in doseidxs],axis=0)
    f, ax = plt.subplots(dpi=300)
    ww = 400
    wl = 100
    offset = 1000
    ax.imshow(np.concatenate([base_images,
                            noisey_images])-offset, cmap='gray', vmin=wl-ww/2, vmax=wl+ww/2)
    ax.tick_params(left = False, right = False , labelleft = False ,
                    labelbottom = False, bottom = False)
    nx = img_dict['true'].shape[0]
    ax.annotate('Ground Truth', (nx//2, nx//6),
                xycoords='data',
                color='white',
                fontsize=8,
                horizontalalignment='center')
    ax.annotate('Noiseless FBP', (nx + nx//2, nx//6),
                xycoords='data',
                color='white',
                fontsize=8,
                horizontalalignment='center')
    ax.annotate('Noiseless FBP', (nx + nx//2, nx//6),
                xycoords='data',
                color='white',
                fontsize=8,
                horizontalalignment='center')
    for idx, dl in enumerate(doselevels_pct[doseidxs]):
        ax.annotate(f'FBP {int(dl*100)}% dose', (nx//2, nx*(idx+1) + nx//6),
                xycoords='data',
                color='white',
                fontsize=6,
                horizontalalignment='center')
        ax.annotate(f'CNN {int(dl*100)}% dose', (nx + nx//2, nx*(idx+1) + nx//6),
                    xycoords='data',
                    color='white',
                    fontsize=6,
                    horizontalalignment='center')
    ax.set_title(f"{patient_code}\nAge: {age_yrs} yrs, Weight: {weight_kg} kg\nEff. Diameter {eff_diameter} mm", fontsize=8)
    f.savefig(f'{patient_code}_montage.png', dpi=600)
# %%
fbp_mse_mean, fbp_mse_std = fbp_mses.mean(axis=-1), fbp_mses.std(axis=-1)
cnn_mse_mean, cnn_mse_std = cnn_mses.mean(axis=-1), cnn_mses.std(axis=-1)

def make_mse_effdiameter_dataframe(doselevels, mse_mean, effective_diameters):
    mse_df = pd.DataFrame({diam : mse_mean[idx] for (idx, diam) in enumerate(effective_diameters)})
    doselevels_pct = doselevels / max(doselevels)
    mse_df['doselevels [%]'] = (doselevels_pct*100).astype(int)
    mse_df.set_index('doselevels [%]', inplace=True)
    return mse_df

fbp_mse_df = make_mse_effdiameter_dataframe(doselevels, fbp_mse_mean, effective_diameters)
fbp_mse_std_df = make_mse_effdiameter_dataframe(doselevels, fbp_mse_std, effective_diameters)

cnn_mse_df = make_mse_effdiameter_dataframe(doselevels, cnn_mse_mean, effective_diameters)
cnn_mse_std_df = make_mse_effdiameter_dataframe(doselevels, cnn_mse_std, effective_diameters)


f, axs = plt.subplots(2,2, sharex=True, sharey=True)
for patient_idx, ax in enumerate(axs.flatten()):
    patient_name = get_patient_name(patients, patient_idx)
    eff_diam = fbp_mse_df.columns[patient_idx]
    ax.errorbar(doselevels_pct, fbp_mse_df[eff_diam], yerr=fbp_mse_std_df[eff_diam], label='FBP')
    ax.errorbar(doselevels_pct, cnn_mse_df[eff_diam], yerr=cnn_mse_std_df[eff_diam], label='CNN')
    ax.set_title(patient_name)
    ax.legend()
# %%
mse_reduction_df = 100*abs(cnn_mse_df-fbp_mse_df)/fbp_mse_df
mse_reduction_df = mse_reduction_df[sorted(mse_reduction_df.columns)]
sns.heatmap(mse_reduction_df,annot=True, cbar_kws=dict(label=f'Relative MSE Reduction [%]\n$|MSE(REDCNN) - MSE(FBP)| / MSE(FBP)\\times 100$'))
plt.xlabel('Effective Diameter [mm]')
plt.savefig('mse_reduction_v_diameter_heatmap.png', dpi=600)

# %%
def make_mse_age_dataframe(doselevels, mse_mean, ages):
    mse_df = pd.DataFrame({age : mse_mean[idx] for (idx, age) in enumerate(ages)})
    doselevels_pct = doselevels / max(doselevels)
    mse_df['doselevels [%]'] = (doselevels_pct*100).astype(int)
    mse_df.set_index('doselevels [%]', inplace=True)
    return mse_df

fbp_mse_df = make_mse_age_dataframe(doselevels, fbp_mse_mean, ages)
fbp_mse_std_df = make_mse_age_dataframe(doselevels, fbp_mse_std, ages)

cnn_mse_df = make_mse_age_dataframe(doselevels, cnn_mse_mean, ages)
cnn_mse_std_df = make_mse_age_dataframe(doselevels, cnn_mse_std, ages)

mse_reduction_df = 100*abs(cnn_mse_df-fbp_mse_df)/fbp_mse_df
mse_reduction_df = mse_reduction_df[sorted(mse_reduction_df.columns)]
sns.heatmap(mse_reduction_df, annot=True, cbar_kws=dict(label=f'Relative MSE Reduction [%]\n$|MSE(REDCNN) - MSE(FBP)| / MSE(FBP)\\times 100$'))
plt.xlabel('Patient Age [years]')
plt.savefig('mse_reduction_v_age_heatmap.png', dpi=600)

# %%
plt.scatter(ages, weights)
# %%
patient_info.plot.scatter(x='age (year)', y='weight (kg)')
# %%
patient_info.plot.scatter(x='effective diameter (cm)', y='weight (kg)')
# %%
patient_info.plot.scatter(x='effective diameter (cm)', y='age (year)')
# %%
