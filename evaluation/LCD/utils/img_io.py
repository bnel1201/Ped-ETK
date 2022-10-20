import random
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import h5py

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
    r = 10
    roi = img[xc-nx//r:xc+nx//r, xc - nx//r:xc + nx//r]
    img_vmin = roi.mean() - nstds*roi.std()
    img_vmax = roi.mean() + nstds*roi.std()
    return img_vmin, img_vmax


def get_ww_wl(vmin, vmax):
    ww = abs(vmax - vmin)
    wl = (vmax+vmin)/2
    return ww, wl


def load_img_avg(fnames:list, nx, n_avg=1, offset=0):
    n_avg = n_avg or 1
    return np.stack([imread(o, nx) for o in random.sample(fnames, n_avg)]).mean(axis=0) - offset

def get_central_roi(img, r=10):
    nx = img.shape[0]
    xc = nx//2
    return img[xc-nx//r:xc+nx//r, xc - nx//r:xc + nx//r]

def get_std_noise(fnames, nx, offset=0):
    return (np.stack([get_central_roi(imread(o, nx)) for o in fnames]) - offset).std()

DOSELEVEL = 'I0_0300000'

def imshow_disk_comparison(patient, h5file, n_avg=20, output_dir=None, f=None, axs=None):

    nx = get_img_sz(patient / 'geometry_info.csv')
    offset = get_image_offset(patient / 'image_info.csv')
    proc_img = load_img_avg(sorted(list(patient.glob(f'{DOSELEVEL}_processed/disk/*.raw'))), nx=nx, n_avg=n_avg, offset=offset)
    fbp_img = load_img_avg(sorted(list(patient.glob(f'{DOSELEVEL}/disk/*.raw'))), nx=nx, n_avg=n_avg, offset=offset)
    fbp_noise_lvl = get_std_noise(sorted(list(patient.glob(f'{DOSELEVEL}/disk/*.raw'))), nx=nx, offset=offset)
    proc_noise_lvl = get_std_noise(sorted(list(patient.glob(f'{DOSELEVEL}_processed/disk/*.raw'))), nx=nx, offset=offset)

    # h5file = f'results/LCD/LCD_results.h5'
    lesion_locs = pd.read_csv(patient/'phantom_info_pix_idx.csv').iloc[1:, :]
    nx = get_img_sz(patient / 'geometry_info.csv')
    h5f = h5py.File(h5file, 'r')
    auc = h5f['auc'][:]
    snr = h5f['snr'][:]
    diameters = h5f['patient_diameters'][:]
    h5f.close()
    auc_mean, auc_std = auc.mean(axis=0), auc.std(axis=0)
    auc_fsize=6
    off_radius = 2.5*lesion_locs[' x radius'].max()
    auc_offsets=[(-off_radius, -off_radius), (off_radius, -off_radius), (off_radius, 1.5*off_radius), (-off_radius, 1.5*off_radius)]
    diam = patient.stem

    if axs is None:
        f, (ax0, ax1) = plt.subplots(1, 2, figsize=(4, 2),
                                    gridspec_kw=dict(hspace=0, wspace=0),
                                    sharex=True, sharey=True)
    else:
        ax0, ax1 = axs

    nstds = 2
    offset = 1000
    lbl_loc = (15, 35)
    vmin, vmax = get_display_settings(fbp_img, nstds=nstds)
    ww, wl = get_ww_wl(vmin, vmax)
    print(f'ww: {ww:3.2f}, wl: {wl:3.2f}, min: {vmin:3.2f}, max: {vmax:3.2f}')
    ax0.imshow(fbp_img[:, ::-1], cmap='gray', vmin=vmin, vmax=vmax)
    ax0.annotate(f'ww: {ww:2.0f} / wl: {wl:2.0f}\nStd Noise: {fbp_noise_lvl:2.0f} HU\nDetectability AUC $\pm$ 1 std:',
                 xy=lbl_loc,
                 fontsize=auc_fsize,
                 bbox=dict(boxstyle='round', fc='white'))
    ax0.set_xlabel('FBP')
    ax0.set_ylabel(f'{diam}')
    ax0.xaxis.set_major_locator(plt.NullLocator())
    ax0.yaxis.set_major_locator(plt.NullLocator())

    diam_idx = list(diameters).index(int(diam.split('diameter')[1].split('mm')[0]))
    n_lesions = auc_mean.shape[2]
    fbp_det_auc_str = [f'${auc_mean[0, 0, i, diam_idx]:2.2f}\pm{auc_std[0, 0, i, diam_idx]:2.2f}$' for i in range(n_lesions)]
    proc_det_auc_str = [f'${auc_mean[0, 1, i, diam_idx]:2.2f}\pm{auc_std[0, 0, i, diam_idx]:2.2f}$' for i in range(n_lesions)]
    [ax0.annotate(fbp_det_auc_str[i],
                 (nx - lesion_locs['x center'].iloc[i]+auc_offsets[i][0], nx - lesion_locs[' y center'].iloc[i]+auc_offsets[i][1]),
                 fontsize=auc_fsize,
                 color='black',
                 bbox=dict(boxstyle='round', fc='white'),
                 horizontalalignment='center') for i in range(n_lesions)]

    proc_bias = get_central_roi(proc_img).mean()
    vmin += proc_bias
    vmax += proc_bias
    ww, wl = get_ww_wl(vmin, vmax)
    print(f'ww: {ww:3.2f}, wl: {wl:3.2f}, min: {vmin:3.2f}, max: {vmax:3.2f}')
    ax1.imshow(proc_img[:, ::-1], cmap='gray', vmin=vmin, vmax=vmax)
    ax1.annotate(f'ww: {ww:2.0f} / wl: {wl:2.0f}\nStd Noise: {proc_noise_lvl:2.0f} HU\nDetectability AUC $\pm$ 1 std:',
                 xy=lbl_loc,
                 fontsize=auc_fsize,
                 bbox=dict(boxstyle='round', fc='white'))
    ax1.set_xlabel('REDCNN')
    ax1.xaxis.set_major_locator(plt.NullLocator())
    ax1.yaxis.set_major_locator(plt.NullLocator())
    [ax1.annotate(proc_det_auc_str[i],
                 (nx - lesion_locs['x center'].iloc[i]+auc_offsets[i][0], nx - lesion_locs[' y center'].iloc[i]+auc_offsets[i][1]),
                 fontsize=auc_fsize,
                 color='black',
                 bbox=dict(boxstyle='round', fc='white'),
                 horizontalalignment='center') for i in range(n_lesions)]

    if output_dir:
        Path(output_dir).mkdir(exist_ok=True, parents=True)
        output_fname = output_dir / f'{diam}_lcd_comparison.png'
        f.savefig(output_fname, dpi=600)
        print(f'File saved: {output_fname}')
    else:
        f.show()
