# %%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path


datadir = Path('/gpfs_projects/brandon.nelson/DLIR_Ped_Generalizability/geomtric_phantom_studies/CTP404/monochromatic/')
patient_dirs = sorted(list(datadir.glob('diameter*')))
# %%
idx = 0
proc_fnames = list(patient_dirs[idx].glob('I0_*_processed/fbp_sharp/*.raw'))
orig_fnames = list(patient_dirs[idx].glob('I0_*0/fbp_sharp/*.raw'))
# %%


def imread(fname, sz=512): return np.fromfile(open(fname), dtype=np.int16, count=sz*sz).reshape(sz, sz)

f, (ax0, ax1, ax2) = plt.subplots(1, 3, dpi=300, gridspec_kw=dict(hspace=0.1, wspace=0.1))

orig = imread(orig_fnames[0])
ax0.imshow(orig, cmap='gray')

redcnn = imread(proc_fnames[0])
ax1.imshow(redcnn, cmap='gray')

ax2.imshow(redcnn - orig, cmap='gray')
# %%
