import argparse
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

from utils.img_io import get_2D_nps_img, get_img

np.random.seed(42)

DOSELEVEL = 'I0_0300000'


def get_display_settings(img, nstds=0.5):
    nx = img.shape[0]
    roi = img[nx//8:nx-nx//8, nx//8:nx-nx//8]
    img_vmin = roi.mean() - nstds*roi.std()
    img_vmax = roi.mean() + nstds*roi.std()
    return img_vmin, img_vmax


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

    img_vmin, img_vmax = get_display_settings(fbp_img, nstds=0.5)

    axs[0, 0].imshow(fbp_img, cmap='gray', vmin=img_vmin, vmax=img_vmax)
    axs[0, 1].imshow(fbp_nps, cmap='gray')

    img_vmin, img_vmax = get_display_settings(proc_img, nstds=0.5) # <--- remove this once bias issue is addressed in model BJN 2022-09-27

    axs[1, 0].imshow(proc_img, cmap='gray', vmin=img_vmin, vmax=img_vmax)
    axs[1, 1].imshow(proc_nps, cmap='gray')
    axs[0, 0].set_xlabel('Image')
    axs[0, 1].set_xlabel('2D NPS')
    axs[0, 0].set_ylabel('FBP')
    axs[1, 0].set_ylabel('REDCNN')
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
    else:
        f.show()


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