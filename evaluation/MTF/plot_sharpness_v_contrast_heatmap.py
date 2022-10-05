import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns

from utils.csv_io import append_adult_data_to_mtf_cutoff_data


def plot_sharpness_heatmap(mtf_rel, cutoff_val, results_dir=None, ax=None):

    mtf_rel.columns = [int(c.split('mm')[0]) for c in mtf_rel.columns]
    mtf_rel = mtf_rel[sorted(mtf_rel.columns)]
    mtf_rel.sort_index(ascending=False, inplace=True)
    if ax is None:
        f, ax = plt.subplots()
    sns.heatmap(mtf_rel, annot=True, ax=ax,
                cbar_kws=dict(label=f'Relative Sharpness\n(REDCNN {cutoff_val}% MTF / FBP {cutoff_val}% MTF'))
    ax.set_xlabel('Patient Diameter [mm]')
    twiny = ax.twiny()

    fovs = np.round(mtf_rel.columns*1.1).astype(int).to_list()
    fovs[mtf_rel.columns.to_list().index(200)] = 212 # this is calculated from dx*nx in </home/rxz4/ct_deeplearning/make_phantom/make_CCT189_wD45_B30.m>
    twiny.set_xticks(ax.get_xticks(), fovs)
    twiny.set_xlim(ax.get_xlim())
    twiny.set_xlabel("Recon FOV [mm]")
    nrows = len(mtf_rel)
    rect = patches.Rectangle((4, 0.05), 1, nrows-0.1, linewidth=3, edgecolor='tab:blue', facecolor='none')
    ax.annotate("Adult Reference",
                xy=(4.75, nrows), xycoords='data',
                xytext=(0.55, 0.025), textcoords='figure fraction',
                color='tab:blue',
                arrowprops=dict(facecolor='tab:blue', shrink=0.05), weight='bold')
    ax.add_patch(rect)

    if results_dir is None:
        plt.show()
    else:
        output_fname = Path(results_dir) / f'mtf{cutoff_val}_sharpness_heatmap.png'
        f.savefig(output_fname, dpi=600)
        print(f'File saved: {output_fname}')


def get_cutoff_val_coords(mtf_df, cutoff_val):
    val = mtf_df.iloc[(np.abs(mtf_df - cutoff_val)).argmin()]
    freq = mtf_df.index[(np.abs(mtf_df - cutoff_val)).argmin()]
    return freq, val


def plot_sample_curves(diameter, contrast, cutoff_val=None, ax=None):
    fbp_color='tab:blue'
    redcnn_color='tab:red'

    datadir = Path('/gpfs_projects/brandon.nelson/DLIR_Ped_Generalizability/geomtric_phantom_studies/CTP404/monochromatic/')
    fbp_mtf_df = pd.read_csv(datadir / f'diameter{diameter}mm' / 'I0_3000000' / 'fbp_sharp_v001_mtf.csv')
    fbp_mtf_df['frequencies [lp/cm]'] = fbp_mtf_df['frequencies [1/mm]'] * 10
    fbp_mtf_df.pop('frequencies [1/mm]')
    fbp_mtf_df.set_index('frequencies [lp/cm]', inplace=True)
    fbp_mtf_df.columns = [abs(int(c.split(' HU')[0])) for c in fbp_mtf_df.columns]

    redcnn_mtf_df = pd.read_csv(datadir / f'diameter{diameter}mm' / 'I0_3000000_processed' / 'fbp_sharp_v001_mtf.csv')
    redcnn_mtf_df['frequencies [lp/cm]'] = redcnn_mtf_df['frequencies [1/mm]'] * 10
    redcnn_mtf_df.pop('frequencies [1/mm]')
    redcnn_mtf_df.set_index('frequencies [lp/cm]', inplace=True)
    redcnn_mtf_df.columns = [abs(int(c.split(' HU')[0])) for c in redcnn_mtf_df.columns]

    if ax is None:
        f, ax = plt.subplots()

    fbp_mtf_df[contrast].plot(ax=ax, label='FBP', color=fbp_color)
    redcnn_mtf_df[contrast].plot(ax=ax, label='REDCNN', color=redcnn_color)

    
    xlim = [0, 11]
    ax.hlines(y=0.5, xmin=0, xmax=xlim[1], linestyle='--', color='black')

    freq, val = get_cutoff_val_coords(fbp_mtf_df[contrast], cutoff_val/100)
    offset = 0.25

    ax.annotate('', xy=(freq-offset, 0), xycoords='data', xytext=(freq-offset, 0.5), arrowprops=dict(arrowstyle='->', color=fbp_color, linestyle='--'))
    ax.annotate(f'FBP 50% MTF\n{freq-offset:2.2f}', xy=(freq+1.6, 0.05), horizontalalignment='center')


    red_freq, val = get_cutoff_val_coords(redcnn_mtf_df[contrast], cutoff_val/100)
    ax.annotate('', xy=(red_freq-offset, 0), xycoords='data', xytext=(red_freq-offset, 0.5), arrowprops=dict(arrowstyle='->', color=redcnn_color, linestyle='--'))
    ax.annotate(f'REDCNN 50% MTF\n{red_freq-offset:2.2f}', xy=(red_freq-2.7, 0.05),  horizontalalignment='center')
    rel_sharp = red_freq/freq
    rel_sharp = f'{rel_sharp:2.3f}'[:-1]
    ax.annotate(f'Relative Sharpness\n{red_freq-offset:2.2f}/{freq-offset:2.2f}={rel_sharp}', xy=(8, 0.6),  horizontalalignment='center', bbox=dict(boxstyle='round', fc='tab:blue'), color='white')

    ax.legend()
    ax.set_ylabel('MTF')
    ax.set_xlim(xlim)
    ax.set_ylim([0, 1])


def main(mtf_results_dir, cutoff_val=50, contrasts=None):

    contrasts = contrasts or [15, 35, 120, 200, 340, 990, 1000]

    fbp_data, redcnn_data = append_adult_data_to_mtf_cutoff_data(mtf_results_dir, 50)
    mtf50_rel = redcnn_data / fbp_data
    mtf50_rel = mtf50_rel[mtf50_rel.index.isin(contrasts)]
    f, ax = plt.subplots()
    plot_sharpness_heatmap(mtf50_rel, cutoff_val=50, results_dir=None, ax=ax)
    output_fname = Path(mtf_results_dir) / 'plots/mtf50_relative_sharpness.png'
    f.savefig(output_fname, dpi=600)

    print(f'File saved: {output_fname}')

    diameter = 216
    contrast = 35

    f, ax = plt.subplots(figsize=(4,4))
    plot_sample_curves(diameter, contrast, cutoff_val=cutoff_val, ax=ax)
    ax.set_title(f'Patient Diameter: {diameter}mm\nContrast: {contrast}HU')
    output_fname = Path(mtf_results_dir) / 'plots/sample_mtf_curves.png'
    f.savefig(output_fname, dpi=600)
    print(f'File saved: {output_fname}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plots MTF cutoff curves')
    parser.add_argument('--datadir', '-d',
                        help="directory containing different patient diameter CT simulations")
    parser.add_argument('--contrasts', '-c', nargs='+',
                        help="Contrast disks to include [list of integers: -1000, 15, 35, 120, 340, 990]")
    args = parser.parse_args()
    contrasts = list(map(int, args.contrasts[0].split(' '))) if args.contrasts else None
    main(args.datadir, contrasts=contrasts)
