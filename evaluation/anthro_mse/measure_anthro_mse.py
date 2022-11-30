# %%
import argparse
import numpy as np
from pathlib import Path
import pandas as pd
import os
import h5py


def imread(fname, sz=None):
    sz = sz or int(pd.read_csv(Path(fname).parents[2] / 'geometry_info.csv').columns[1])
    return np.fromfile(open(fname), dtype=np.int16, count=sz*sz).reshape(sz, sz)

def get_eff_diameter(true_im, pix_size):
    phantom_area = np.sum(true_im > 0)*pix_size
    return int(2*np.sqrt(phantom_area/np.pi))

def get_dose_levels(base_dir, patient_name):
    return [int(o.stem.split('_')[1]) for o in (base_dir / patient_name / 'monochromatic').glob('I0_*0')]
    

def load_patient(base_dir, patient_name):
    base_dir = Path(base_dir)
    dose_levels = sorted(get_dose_levels(base_dir, patient_name))

    fbp_stack = []
    cnn_stack = []
    for dose_level in dose_levels:
        fbp_dir = base_dir / patient_name / f'monochromatic/I0_{dose_level:07.0f}/fbp_sharp/'
        cnn_dir = base_dir / patient_name / f'monochromatic/I0_{dose_level:07.0f}_processed/fbp_sharp/'   
        fbp_singledose_stack = np.stack([imread(o) for o in fbp_dir.glob('*.raw')])
        cnn_singledose_stack = np.stack([imread(o) for o in cnn_dir.glob('*.raw')])
        fbp_stack.append(fbp_singledose_stack)
        cnn_stack.append(cnn_singledose_stack)
    geom = pd.read_csv(base_dir / patient_name / 'monochromatic/geometry_info.csv').set_index('nx').T
    pix_size = float(geom['dx'])
    matrix_size = int(geom['ny'])
    true_im = imread(base_dir / patient_name / 'monochromatic/true.raw', matrix_size)
    eff_diameter = get_eff_diameter(true_im, pix_size)
    noiseless_im = imread(base_dir / patient_name / 'monochromatic/noise_free.raw', matrix_size)

    return {'fbp': np.stack(fbp_stack),
            'cnn' : np.stack(cnn_stack),
            'true' : true_im,
            'noiseless' : noiseless_im,
            'dose_levels' : dose_levels,
            'pix_size': pix_size,
            'effective_diameter':  eff_diameter}


def mse(a,b): return np.sqrt((np.sum((a.ravel() - b.ravel())**2)))/a.size


def mse_summary(a_stack, b_true): return np.array([mse(a, b_true) for a in a_stack])

# %%
base_dir = Path('/gpfs_projects/brandon.nelson/DLIR_Ped_Generalizability/anthropomorphic_phantom_studies/main/simulations')
patients = os.listdir(base_dir)
img_dict = load_patient(base_dir, patients[0])
# %%

def main(base_dir=None, results_fname='untitled.h5'):
    base_dir = base_dir or '/gpfs_projects/brandon.nelson/DLIR_Ped_Generalizability/anthropomorphic_phantom_studies/main/simulations'
    base_dir = Path(base_dir)
    patients = os.listdir(base_dir)

    fbp_mses = []
    cnn_mses = []
    eff_diameters = []
    for patient in patients:
        img_dict = load_patient(base_dir, patient)
        fbp_mse = [mse_summary(img_dict['fbp'][doseidx], img_dict['true']) for doseidx in range(len(img_dict['dose_levels']))]
        cnn_mse = [mse_summary(img_dict['cnn'][doseidx], img_dict['true']) for doseidx in range(len(img_dict['dose_levels']))]
        fbp_mses.append(fbp_mse)
        cnn_mses.append(cnn_mse)
        eff_diameters.append(img_dict['effective_diameter'])
    fbp_mses = np.stack(fbp_mses)
    cnn_mses = np.stack(cnn_mses)

    patients = np.array(patients, dtype='S')
    eff_diameters = np.array(eff_diameters)
    doselevels = np.array(img_dict['dose_levels'])

    with h5py.File(results_fname, 'w') as f:
        fbp_mse_dset = f.create_dataset('/fbp/mse', fbp_mses.shape, fbp_mses.dtype)
        fbp_mse_dset[...] = fbp_mses
        patient_dset = f.create_dataset('/patients/names', patients.shape, patients.dtype)
        patient_dset[...] = patients
        patient_dset.attrs['base_dir'] = str(base_dir)
        eff_diameter_dset = f.create_dataset('/patients/effective_diameters', eff_diameters.shape, eff_diameters.dtype)
        eff_diameter_dset[...] = eff_diameters
        doselevels_dset = f.create_dataset('/doselevels', doselevels.shape, doselevels.dtype)
        doselevels_dset[...] = doselevels
        cnn_mse_dset = f.create_dataset('/cnn/mse', cnn_mses.shape, cnn_mses.dtype)
        cnn_mse_dset[...] = cnn_mses

    print(results_fname)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Make Mean Squared Error Measurements on Anthropomorphic Phantoms')
    parser.add_argument('base_dir',
                        help="directory containing simulated CT data")
    parser.add_argument('-o', '--output_filename',
                        help="h5 file storing measured MSE values")
    args = parser.parse_args()
    main(base_dir=args.base_dir, results_fname=args.output_filename)
