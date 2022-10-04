import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from utils.img_io import get_2D_nps_img, get_img
from utils.nps_plot import plot_1D_nps

np.random.seed(42)

DOSELEVEL = 'I0_0300000'


def get_display_settings(img, nstds=0.5):
    nx = img.shape[0]
    xc = nx//2
    roi = img[xc-nx//8:xc+nx//8, xc - nx//8:xc + nx//8]
    img_vmin = roi.mean() - nstds*roi.std()
    img_vmax = roi.mean() + nstds*roi.std()
    return img_vmin, img_vmax


def plot_noise_images(patient_dir, outdir=None):
    fbp_nps_dir = patient_dir / DOSELEVEL / 'NPS'
    proc_nps_dir = patient_dir / (DOSELEVEL + '_processed') / 'NPS'
    fbp_nps = get_2D_nps_img(fbp_nps_dir)
    proc_nps = get_2D_nps_img(proc_nps_dir)

    fbp_img = get_img(patient_dir / DOSELEVEL / 'bkg')
    proc_img =  get_img(patient_dir / (DOSELEVEL + '_processed') / 'bkg')

    nps_lims = [0, 6000]


    figsize=4
    fig = plt.figure(constrained_layout=False, figsize=[figsize*2, figsize])
    gs1 = plt.GridSpec(2, 2, wspace=0, hspace=0, left=0.01, right=0.5,)
    ax0 = fig.add_subplot(gs1[0, 0])
    ax1 = fig.add_subplot(gs1[:, 1])
    ax2 = fig.add_subplot(gs1[1, 0])

    img_vmin, img_vmax = get_display_settings(fbp_img, nstds=0.5)
    ax0.imshow(fbp_img, cmap='gray', vmin=img_vmin, vmax=img_vmax)
    ax0.set_ylabel('FBP')
    im = ax1.imshow(np.concatenate((fbp_nps, proc_nps), axis=0), cmap='gray')
    ax1.set_xlabel('2D NPS')

    plt.colorbar(im, ax=ax1, use_gridspec=True)
    img_vmin, img_vmax = get_display_settings(proc_img, nstds=0.5) # <--- remove this once bias issue is addressed in model BJN 2022-09-27

    ax2.imshow(proc_img, cmap='gray', vmin=img_vmin, vmax=img_vmax)
    ax2.set_xlabel('Image')
    ax2.set_ylabel('REDCNN')

    [ax.xaxis.set_major_locator(plt.NullLocator()) for ax in [ax0, ax1, ax2]]
    [ax.yaxis.set_major_locator(plt.NullLocator()) for ax in [ax0, ax1, ax2]]

    gs2 = fig.add_gridspec(wspace=0, hspace=0, left=0.65, right=0.95, bottom=0.2, top=0.8)
    ax4 = fig.add_subplot(gs2[0])
    plot_1D_nps(fbp_nps_dir, proc_nps_dir, fig=fig, ax=ax4)
    ax4.set_ylim(nps_lims)
    ax4.set_ylabel("magnitude")
    ax4.set_title('NPS radial average')

    diam = patient_dir.stem
    fig.suptitle(diam)

    if outdir:
        outdir = Path(outdir)
        outdir.mkdir(exist_ok=True, parents=True)
        output_fname = outdir / f'{diam}_noise_comparison.png'
        fig.savefig(output_fname, dpi=600)
        print(f'saved to: {output_fname}')
    else:
        fig.show()


def main(datadir=None, outdir=None):
    datadir = datadir or '/home/brandon.nelson/Data/temp/CCT189/monochromatic'
    patient_dirs = sorted(list(Path(datadir).glob('diameter*')))


    for patient_dir in patient_dirs:
        plot_noise_images(patient_dir, outdir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plots 2D NPS images')
    parser.add_argument('--datadir', '-d', default=None,
                        help="directory containing different patient diameter CT simulations")
    parser.add_argument('--output_dir','-o', required=False,
                        help="Directory to save image files")
    args = parser.parse_args()
    main(args.datadir, outdir=args.output_dir)