# %%
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import pandas as pd

# %%

def imread(fname, sz=512): return np.fromfile(open(fname), dtype=np.int16, count=sz*sz).reshape(sz, sz)


def image_comparison_by_diameter(fbp_fname, proc_fname, outdir=None):
    f, (ax0, ax1, ax2) = plt.subplots(1, 3, dpi=300,
                                    gridspec_kw=dict(hspace=0, wspace=0),
                                    sharex=True, sharey=True)
    orig = imread(fbp_fname)
    ax0.imshow(orig, cmap='gray')
    ax0.set_title('FBP')
    ax0.xaxis.set_major_locator(plt.NullLocator())
    ax0.yaxis.set_major_locator(plt.NullLocator())

    redcnn = imread(proc_fname)
    ax1.imshow(redcnn, cmap='gray')
    ax1.set_title('RedCNN-TV')
    ax1.xaxis.set_major_locator(plt.NullLocator())
    ax1.yaxis.set_major_locator(plt.NullLocator())

    im = ax2.imshow(redcnn - orig, cmap='gray')
    ax2.set_title('RedCNN-TV - FBP')
    ax2.xaxis.set_major_locator(plt.NullLocator())
    ax2.yaxis.set_major_locator(plt.NullLocator())
    cbar_ax = plt.gcf().add_axes([0.91, 0.325, 0.02, 0.34])
    plt.colorbar(im, cax=cbar_ax)

    diam = fbp_fname.parents[2].stem
    if outdir is None: outdir = Path(__file__).parent / 'results' / 'images'
    outdir.mkdir(exist_ok=True, parents=True)
    fname = outdir / f'{diam}_image_comparison.png'
    f.savefig(fname, dpi=600)
    print(f'File saved: {fname}')
# %%

datadir = Path('/gpfs_projects/brandon.nelson/DLIR_Ped_Generalizability/geomtric_phantom_studies/CTP404/monochromatic/')
patient_dirs = sorted(list(datadir.glob('diameter*')))

for patient in patient_dirs:
    fbp_fname = sorted(list(patient.glob('I0_*_processed/fbp_sharp/*.raw')))[0]
    proc_fname = sorted(list(patient.glob('I0_*0/fbp_sharp/*.raw')))[0]
    image_comparison_by_diameter(fbp_fname, proc_fname)
# %%
