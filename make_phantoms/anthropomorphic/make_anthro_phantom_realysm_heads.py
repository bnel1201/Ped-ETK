import argparse
import re
from pathlib import Path
import os

import pandas as pd
import numpy as np

XCAT_dir = '/gpfs_projects/brandon.nelson/XCAT/XCAT_V2_LINUX/'
XCAT_MODELFILES_DIR='/gpfs_projects/brandon.nelson/XCAT/modelfiles'
XCAT = 'dxcat2_linux_64bit'


XCAT_MODELFILES_DIR = Path(XCAT_MODELFILES_DIR)

def get_diameter(df, code, units='mm'):
    diameter = float(df[df['Code #'] == code]['effective diameter (cm)'])
    if units == 'mm':
        diameter *= 10
    return diameter

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


def make_phantom(phantoms_dir, phantom_df, code, fov=None, array_size = 1024, energy=60):
    """
    energy [keV]
    """
    GENERAL_PARAMS_FILE = os.path.abspath(Path(__file__).parent / 'realysm_phantom.par')
    phantoms_dir.mkdir(exist_ok=True, parents=True)
    
    patient_nrb_file, patient_heart_nrb_file, patient = get_nrb_filenames(phantom_df, code) 
    
    patient_info = phantom_df[phantom_df['Code #'] == code]
    gender = 0 if patient_info['gender'].iloc[0] == 'M' else 1

    height = patient_info['height (cm)'].iloc[0]

    estimated_eff_diameter = get_diameter(phantom_df, code, units='cm')
    fov = fov or min(1.1*estimated_eff_diameter, 48) #in cm
    pixel_width_cm = fov / array_size


    endslice = int(height/pixel_width_cm)+100
    cmd = f'cd {XCAT_dir}\n./{XCAT} {GENERAL_PARAMS_FILE}\
             --organ_file {patient_nrb_file}\
             --heart_base {patient_heart_nrb_file}\
             --pixel_width {pixel_width_cm}\
             --slice_width {pixel_width_cm}\
             --array_size {array_size}\
             --energy {energy}\
             --startslice {endslice-500}\
             --endslice {endslice}\
             --arms_flag 0\
             --gender {gender}\
             {phantoms_dir}/{patient}'
    cmd
    os.system(cmd)
# %%

def main(phantoms_dir, xcat_patients_csv='selected_xcat_patients.csv'):

    phantoms_dir = Path(phantoms_dir)
    phantoms_dir.mkdir(exist_ok=True, parents=True)

    phantoms_df = pd.read_csv(xcat_patients_csv)

    codes = phantoms_df['Code #']
    for code in codes:
        patient_nrb_file, patient_heart_nrb_file, _ = get_nrb_filenames(phantoms_df, code)
        assert patient_nrb_file.exists()
        assert patient_heart_nrb_file.exists()

    for code in codes:
        fov = 48
        print(f'making full fov: {fov} cm phantoms {code}')
        make_phantom(phantoms_dir, phantoms_df, code, fov=fov)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Make Anthropomorphic Phantoms using XCAT')
    parser.add_argument('base_dir',
                        help="output directory to save XCAT phantom bin files")
    parser.add_argument('-csv', '--patient_info_csv_file', default=Path(__file__).parent / 'selected_xcat_patients.csv', required=False,
                        help="csv file containing virtual patient info in XCAT format")
    args = parser.parse_args()
    main(phantoms_dir=Path(args.base_dir), xcat_patients_csv=args.patient_info_csv_file)
