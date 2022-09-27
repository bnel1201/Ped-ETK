# %%
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import pandas as pd

np.random.seed(42)

DOSELEVEL = 'I0_0300000'


def imread(fname, sz=512, dtype=np.int16): return np.fromfile(open(fname), dtype=dtype, count=sz*sz).reshape(sz, sz)


def get_2D_nps_img(nps_dir):
    raw_fname=next(nps_dir.glob('2D_nps_*.raw'))
    sz = int(raw_fname.stem.split('_')[-1])
    return imread(raw_fname, sz=sz, dtype=np.float32)


def get_img_sz(img_dir):
    temp_df = pd.read_csv(img_dir.parents[1] / 'geometry_info.csv').T
    ig = pd.DataFrame({col: [rows] for col, rows in zip(temp_df.iloc[0, :], temp_df.iloc[1, :])})
    nx = int(ig.ny)
    return nx


def get_img(img_dir):
    sz = get_img_sz(img_dir)
    fname =  np.random.choice(list(img_dir.glob('*.raw')), 1)[0]
    return imread(fname, sz=sz, dtype=np.int16)

def plot_noise_images(patient_dir, outdir=None):
    fbp_nps_dir = patient_dir / DOSELEVEL / 'NPS'
    proc_nps_dir = patient_dir / (DOSELEVEL + '_processed') / 'NPS'

    fbp_img_dir = patient_dir / DOSELEVEL / 'bkg'
    proc_img_dir = patient_dir / (DOSELEVEL + '_processed') / 'bkg'

    fbp_nps = get_2D_nps_img(fbp_nps_dir)
    proc_nps = get_2D_nps_img(proc_nps_dir)

    fbp_img = get_img(fbp_img_dir)
    proc_img =  get_img(proc_img_dir)


    figsize=5
    f, axs = plt.subplots(2, 2, dpi=300,
                        gridspec_kw=dict(hspace=0, wspace=0), figsize=[figsize]*2)

    nx = get_img_sz(fbp_img_dir)

    nstds = 0.5
    roi = fbp_img[nx//8:nx-nx//8, nx//8:nx-nx//8]
    img_vmin = roi.mean() - nstds*roi.std()
    img_vmax = roi.mean() + nstds*roi.std()

    axs[0, 0].imshow(fbp_img, cmap='gray', vmin=img_vmin, vmax=img_vmax)
    axs[0, 1].imshow(fbp_nps, cmap='gray')
    axs[1, 0].imshow(proc_img, cmap='gray', vmin=img_vmin, vmax=img_vmax)
    axs[1, 1].imshow(proc_nps, cmap='gray')
    axs[0, 0].set_xlabel('Image')
    axs[0, 1].set_xlabel('2D NPS')
    axs[0, 0].set_ylabel('FBP')
    axs[1, 0].set_ylabel('REDCNN-TV')
    [ax.xaxis.set_major_locator(plt.NullLocator()) for ax in axs.flatten()]
    [ax.yaxis.set_major_locator(plt.NullLocator()) for ax in axs.flatten()]

    diam = patient_dir.stem
    f.suptitle(diam)

    if outdir:
        outdir = Path(outdir)
        outdir.mkdir(exist_ok=True, parents=True)
        output_fname = outdir / f'{diam}_noise_comparison.png'
        f.savefig(output_fname, dpi=600)
        print(f'saved to: {output_fname}')
# %%
base_dir = Path('/home/brandon.nelson/Data/temp/CCT189/monochromatic')
diam_dirs = sorted(list(base_dir.glob('diameter*')))

for patient_dir in diam_dirs:
    plot_noise_images(patient_dir, 'results/images')
# %%
