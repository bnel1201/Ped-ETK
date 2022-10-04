import random
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
random.seed(42)


def get_lesion_info(phantom_info_csv):
    "resused from MTF/plot_images.py"
    phantom_info = pd.read_csv(phantom_info_csv)
    water_atten = phantom_info[' mu [60 keV] '][0]
    phantom_info['CT Number [HU]'] = 1000*(phantom_info[' mu [60 keV] '])/water_atten
    phantom_info.pop(' angle degree')
    return phantom_info.iloc[1:, :]


def get_lesion_coords(lesion_info, HU):
    "resused from MTF/plot_images.py"
    all_lesions = lesion_info.round().astype(int)
    all_lesions.pop(' mu [60 keV] ')
    lesion = all_lesions[all_lesions['CT Number [HU]'] == HU]
    return (int(lesion['x center']), int(lesion[' y center'])), (int(lesion[' x radius']), int(lesion[' y radius']))


def get_img_sz(geometry_info_csv):
    temp_df = pd.read_csv(geometry_info_csv).T
    ig = pd.DataFrame({col: [rows] for col, rows in zip(temp_df.iloc[0, :], temp_df.iloc[1, :])})
    nx = int(ig.ny)
    return nx

def get_image_offset(image_info_csv): return int(pd.read_csv(image_info_csv).columns[1])

def imread(fname, sz=512): return np.fromfile(open(fname), dtype=np.int16, count=sz*sz).reshape(sz, sz)

def get_display_settings(img, nstds=0.5):
    nx = img.shape[0]
    xc = nx//2
    roi = img[xc-nx//8:xc+nx//8, xc - nx//8:xc + nx//8]
    img_vmin = roi.mean() - nstds*roi.std()
    img_vmax = roi.mean() + nstds*roi.std()
    return img_vmin, img_vmax

def get_ww_wl(vmin, vmax):
    ww = abs(vmax - vmin)
    wl = (vmax+vmin)/2
    return ww, wl

def load_img_avg(fnames:list, nx, n_avg, offset=0):
    return np.stack([imread(o, nx) for o in random.sample(fnames, n_avg)]).mean(axis=0) - offset


def imshow_disk_comparison(patient, n_avg=20, output_dir=None, f=None, axs=None):

    nx = get_img_sz(patient / 'geometry_info.csv')
    offset = get_image_offset(patient / 'image_info.csv')
    proc_img = load_img_avg(sorted(list(patient.glob('I0_*_processed/disk/*.raw'))), nx=nx, n_avg=n_avg, offset=offset)
    fbp_img = load_img_avg(sorted(list(patient.glob('I0_*0/disk/*.raw'))), nx=nx, n_avg=n_avg, offset=offset)

    diam = patient.stem

    if axs is None:
        f, (ax0, ax1) = plt.subplots(1, 2, figsize=(4, 2),
                                    gridspec_kw=dict(hspace=0, wspace=0),
                                    sharex=True, sharey=True)
    else:
        ax0, ax1 = axs

    nstds = 2
    vmin, vmax = get_display_settings(fbp_img, nstds=nstds)
    ww, wl = get_ww_wl(vmin, vmax)
    print(f'ww: {ww:3.2f}, wl: {wl:3.2f}, min: {vmin:3.2f}, max: {vmax:3.2f}')
    ax0.imshow(fbp_img[:, ::-1], cmap='gray', vmin=vmin, vmax=vmax)
    ax0.set_xlabel('FBP')
    ax0.set_ylabel(f'{diam}')
    ax0.xaxis.set_major_locator(plt.NullLocator())
    ax0.yaxis.set_major_locator(plt.NullLocator())

    vmin, vmax = get_display_settings(proc_img, nstds=nstds)
    ww, wl = get_ww_wl(vmin, vmax)
    print(f'ww: {ww:3.2f}, wl: {wl:3.2f}, min: {vmin:3.2f}, max: {vmax:3.2f}')
    ax1.imshow(proc_img[:, ::-1], cmap='gray', vmin=vmin, vmax=vmax)
    ax1.set_xlabel('REDCNN')
    ax1.xaxis.set_major_locator(plt.NullLocator())
    ax1.yaxis.set_major_locator(plt.NullLocator())

    if output_dir:
        Path(output_dir).mkdir(exist_ok=True, parents=True)
        output_fname = output_dir / f'{diam}_lcd_comparison.png'
        f.savefig(output_fname, dpi=600)
        print(f'File saved: {output_fname}')
    else:
        f.show()
