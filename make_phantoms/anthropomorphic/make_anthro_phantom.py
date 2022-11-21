# %%
from pathlib import Path
import pandas as pd
import numpy as np
import os

BASE_DIR = Path('/gpfs_projects/brandon.nelson/DLIR_Ped_Generalizability/anthropomorphic_phantom_studies/main/phantoms')
BASE_DIR.mkdir(exist_ok=True, parents=True)
GENERAL_PARAMS_FILE = os.path.abspath(Path('anthro_phantom.par'))
XCAT_dir = Path('/gpfs_projects/brandon.nelson/XCAT/XCAT_V2_LINUX/')
XCAT = 'dxcat2_linux_64bit'

XCAT_MODELFILES_DIR=Path('/gpfs_projects/brandon.nelson/XCAT/modelfiles')

# %%
ped_phantoms = pd.read_csv('selected_xcat_peds.csv')
peds_codes = ped_phantoms['Code #']

def get_diameter_from_age(age, units='mm'):
    """
    input: age [years]
    output: effective diameter [default units mm]

    Originally from ICRU 74, y = a + bx^1.5 + cx^0.5 + de^-x
    a = 18.788598
    b = 0.19486455
    c = -1.060056
    d = -7.6244784
    """
    a = 18.788598
    b = 0.19486455
    c = -1.060056
    d = -7.6244784
    effective_diameter_cm = a + b*age**1.5 + c*age**0.5 + d*np.exp(-age)
    if units == 'mm':
        effective_diameter = 10*effective_diameter_cm
    else:
        effective_diameter = effective_diameter_cm
    return effective_diameter

def get_nrb_filenames(phantom_df, code):
    if phantom_df['Code #'].dtype != int: code = str(code)
    idx = phantom_df[phantom_df['Code #'] == code].index[0]
    patient_num = phantom_df['Code #'][idx]
    gender = phantom_df['gender'][idx]
    gender_str = 'female' if gender == 'F' else 'male'
    if str(patient_num).split(' ')[0] == 'Reference':
        age = int(phantom_df['age (year)'][idx])
        age_str = 'infant' if age < 1 else f'{age}yr'
        patient = f'{gender_str}_{age_str}_ref'
    else:
        patient = f'{gender_str}_pt{patient_num}'
    patient_nrb_file = XCAT_MODELFILES_DIR / f'{patient}.nrb'
    patient_heart_nrb_file =  XCAT_MODELFILES_DIR / f'{patient}_heart.nrb'
    return patient_nrb_file, patient_heart_nrb_file, patient

fovs = []
heights = []
for code in peds_codes:
    patient_nrb_file, patient_heart_nrb_file, patient = get_nrb_filenames(ped_phantoms, code)
    age = ped_phantoms[ped_phantoms['Code #'] == code]['age (year)'].to_numpy()[0]
    height = ped_phantoms[ped_phantoms['Code #']==code]['height (cm)'].to_numpy()[0]
    diameter = get_diameter_from_age(age)
    fov = 1.1*diameter
    fovs.append(fov)
    heights.append(height)
    vox_size_mm = fov/512
    ds = 1 #detector size mm
    pixel_width_cm = ds/10/2.5 #pixel width of phantom in cm (using 2.5 to exceed min nyquist frequency)
    # array_size = 
    print(code, patient_nrb_file.exists(), patient_heart_nrb_file.exists(), f'age: {age} yrs, diameter: {diameter:.2f} mm, fov: {fov:.2f} mm')
max_fov_cm = max(fovs) / 10
max_height_cm = max(heights)
array_size = round(max_fov_cm / pixel_width_cm)
array_size
n_slices = round(max_height_cm / pixel_width_cm)

energy=60
# %%
adult_phantoms = pd.read_csv('selected_xcat_adults.csv')
adult_codes = adult_phantoms['Code #']

for code in adult_codes:
    patient_nrb_file, patient_heart_nrb_file, patient = get_nrb_filenames(adult_phantoms, code)
    print(code, patient_nrb_file.exists(), patient_heart_nrb_file.exists())

# %%
assert len(adult_phantoms) + len(ped_phantoms) == len(list(XCAT_MODELFILES_DIR.glob('*_heart.nrb')))
# %%

def get_height(phantom_df, code): return phantom_df[phantom_df['Code #']==code]['height (cm)'].to_numpy()[0]

def make_phantom(phantom_df, code):
    """
    energy [keV]
    """
    patient_nrb_file, patient_heart_nrb_file, patient = get_nrb_filenames(phantom_df, code)
    height = get_height(ped_phantoms, code)
    midslice = round(height / 1.7 / pixel_width_cm)
    cmd = f'cd {XCAT_dir}\n./{XCAT} {GENERAL_PARAMS_FILE}\
             --organ_file {patient_nrb_file}\
             --heart_base {patient_heart_nrb_file}\
             --pixel_width {pixel_width_cm}\
             --slice_width {pixel_width_cm}\
             --array_size {array_size}\
             --energy {energy}\
             --startslice {midslice}\
             --endslice {midslice}\
             {BASE_DIR}/{patient}'
    cmd
    os.system(cmd)
# %%

for code in peds_codes:
    print(code)
    make_phantom(ped_phantoms, code)
# %%
for code in adult_codes:
    print(code)
    make_phantom(adult_phantoms, code)