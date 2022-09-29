# %%
import argparse
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from utils.csv_io import (get_stats_df,
                          write_results_to_csv,
                          load_csv,
                          write_1D_nps_results_to_csv)

DOSELEVEL = 'I0_0300000'

plt.style.use('seaborn-talk')


def plot_1D_nps(fbp_dir, proc_dir, fig=None, ax=None):
    fbp_nps_df = pd.read_csv(fbp_dir / '1D_nps.csv')
    proc_nps_df = pd.read_csv(proc_dir / '1D_nps.csv')
    if ax is None or fig is None:
        fig, ax = plt.subplots()
    diam = fbp_dir.parents[1].stem
    fbp_nps_df.plot(ax=ax, x='spatial frequency [cyc/pix]', y=' magnitude', label='FBP', title=f'{diam}')
    proc_nps_df.plot(ax=ax, x='spatial frequency [cyc/pix]', y=' magnitude', label='REDCNN')


def plot_1D_nps_all_diams(base_dir, output_fname=None, **subplots_kwargs):
    diam_dirs = sorted(list(base_dir.glob('diameter*')))
    f, axs = plt.subplots(2, 3, dpi=300, **subplots_kwargs)
    for ax, patient_dir in zip(axs.flatten(), diam_dirs):
        fbp_dir = patient_dir / DOSELEVEL / 'NPS'
        proc_dir = patient_dir / (DOSELEVEL + '_processed') / 'NPS'
        plot_1D_nps(fbp_dir, proc_dir, fig=f, ax=ax)
    [ax.get_legend().remove() for ax in axs.flatten()[1:]]
    f.tight_layout()
    if output_fname:
        Path(output_fname).parent.mkdir(exist_ok=True, parents=True)
        f.savefig(output_fname, dpi=600)
    else:
        plt.show()


def make_summary_df(fbp_stats_df, proc_stats_df):
    return pd.DataFrame({'Series': ['FBP', 'REDCNN'],
                         'noise mean [ROI std in HU]': [fbp_stats_df[' std [HU]'].mean(), proc_stats_df[' std [HU]'].mean()],
                         'noise std [ROI std in HU]': [fbp_stats_df[' std [HU]'].std(), proc_stats_df[' std [HU]'].std()]})

def plot_noise_summary(fbp_dir, proc_dir, fig=None, ax=None):
    fbp_stats_df = get_stats_df(fbp_dir)
    proc_stats_df = get_stats_df(proc_dir)

    noise_summary_df = make_summary_df(fbp_stats_df, proc_stats_df)

    if ax is None or fig is None:
        fig, ax = plt.subplots()
    diam = fbp_dir.parents[1].stem
    noise_summary_df.set_index('Series', inplace=True)
    noise_summary_df.plot(ax=ax, kind='bar', y='noise mean [ROI std in HU]',
                          yerr='noise std [ROI std in HU]',
                          capsize=10,
                          xlabel='',
                          ylabel='Noise level (ROI std) [HU]',
                          title=f'{diam}',
                          rot='horizontal')
    ax.get_legend().remove()
    return fig, ax


def plot_noise_curves(fbp_dir, proc_dir, fig=None, ax=None):
    fbp_stats_df = get_stats_df(fbp_dir)
    proc_stats_df = get_stats_df(proc_dir)

    if ax is None or fig is None:
        fig, ax = plt.subplots()
    diam = fbp_dir.parents[1].stem

    color='blue'
    ax.plot(fbp_stats_df[' mean [HU]'], color=color, linestyle='-', label='FBP')
    ax.plot(proc_stats_df[' mean [HU]'], color=color, linestyle='--', label='REDCNN')
    ax.tick_params(axis='y', labelcolor=color)
    ax.set_ylabel('mean [HU]', color=color)
    ax.set_title(diam)
    ax.set_ylim(990, 1060)
    axtwin = ax.twinx()
    color='red'
    axtwin.plot(fbp_stats_df[' std [HU]'], color=color)
    axtwin.plot(proc_stats_df[' std [HU]'], color=color, linestyle='--', label='REDCNN')
    axtwin.set_ylabel('std [HU]', color=color)
    axtwin.tick_params(axis='y', labelcolor=color)
    axtwin.set_ylim(8, 32)

    return fig, ax


def plot_CT_number_noise_v_diameter(fbp_summary_df, proc_summary_df, output_fname=None, **subplotkwargs):
    f, (ax0, ax1) = plt.subplots(1, 2, **subplotkwargs)
    fbp_summary_df.plot(ax=ax0, x='Patient Diameter [mm]', y='mean CT number [HU]', label='FBP',)
    proc_summary_df.plot(ax=ax0, x='Patient Diameter [mm]', y='mean CT number [HU]', label='REDCNN')
    ax0.set_ylabel('CT Number [HU]')

    fbp_summary_df.plot(ax=ax1, x='Patient Diameter [mm]', y='mean noise (ROI std) [HU]', label='FBP')
    proc_summary_df.plot(ax=ax1, x='Patient Diameter [mm]', y='mean noise (ROI std) [HU]', label='REDCNN')
    ax1.set_ylabel('CT Noise (ROI std) [HU]')
    f.tight_layout()
    if output_fname:
        Path(output_fname).parent.mkdir(exist_ok=True, parents=True)
        f.savefig(output_fname, dpi=600)
    else:
        plt.show()


def plot_relative_denoising(fbp_summary_df, proc_summary_df, output_fname=None, fig=None, ax=None):
    relative_denoising_df = proc_summary_df.set_index('Patient Diameter [mm]') / fbp_summary_df.set_index('Patient Diameter [mm]')
    relative_denoising_df.pop('mean CT number [HU]')
    relative_denoising_df*=100
    if fig is None or ax is None:
        fig, ax = plt.subplots(figsize=(4,4))
    relative_denoising_df.plot(ax=ax, ylabel='Noise Level Relative to FBP [%]\n$\sigma_{REDCNN} / \sigma_{FBP} \\times 100$')
    ax.get_legend().remove()
    if output_fname:
        Path(output_fname).parent.mkdir(exist_ok=True, parents=True)
        fig.savefig(output_fname, dpi=600)
    else:
        plt.show()
    return fig, ax


def get_noise_reduction_df(csv_fname):
    fbp_summary_df, proc_summary_df = load_csv(csv_fname)
    fbp_summary_df.set_index('Patient Diameter [mm]', inplace=True)
    proc_summary_df.set_index('Patient Diameter [mm]', inplace=True)
    noise_reduction_df = abs((proc_summary_df - fbp_summary_df)/fbp_summary_df*100)
    noise_reduction_df.pop('mean CT number [HU]')
    return noise_reduction_df


def plot_noise_reduction(csv_fname, output_fname=None, fig=None, ax=None):
    noise_reduction_df = get_noise_reduction_df(csv_fname)

    if fig is None or ax is None:
        fig, ax = plt.subplots(figsize=(4,4))
    noise_reduction_df.plot(ax=ax, ylabel='Relative Noise Reduction [%]\n$|\sigma_{REDCNN} - \sigma_{FBP}| / \sigma_{FBP}\\times 100$')
    ax.get_legend().remove()
    fig.tight_layout()
    if output_fname:
        Path(output_fname).parent.mkdir(exist_ok=True, parents=True)
        fig.savefig(output_fname, dpi=600)
    else:
        plt.show()
    return fig, ax


def get_bias_df(csv_fname):
    fbp_summary_df, proc_summary_df = load_csv(csv_fname)
    bias_df = proc_summary_df.set_index('Patient Diameter [mm]') - fbp_summary_df.set_index('Patient Diameter [mm]')
    bias_df.pop('mean noise (ROI std) [HU]')
    return bias_df


def plot_CT_bias(csv_fname, output_fname=None, fig=None, ax=None):
    bias_df = get_bias_df(csv_fname)
    if fig is None or ax is None:
        fig, ax = plt.subplots(figsize=(4,4))
    bias_df.plot(ax=ax, ylabel='CT number bias [HU]\n$REDCNN - FBP$')
    ax.get_legend().remove()
    fig.tight_layout()
    if output_fname:
        Path(output_fname).parent.mkdir(exist_ok=True, parents=True)
        fig.savefig(output_fname, dpi=600)
    else:
        plt.show()
    return fig, ax

# %% [markdown]
# Plot NPS Curves
# %%
base_dir = Path('/home/brandon.nelson/Data/temp/CCT189/monochromatic')
output_fname = 'results/plots/1D_nps.png'
plot_1D_nps_all_diams(base_dir, output_fname, sharex=True, sharey=True)
print(output_fname)

# %% [markdown]
# Summarize CT number and noise vs. patient diameter
# %%
output_fname = 'results/diameter_summary.csv'
csv_fname = write_results_to_csv(base_dir, output_fname, DOSELEVEL)
print(csv_fname)
fbp_summary_df, proc_summary_df = load_csv(csv_fname)
fbp_summary_df, proc_summary_df
# %%
output_fname = 'results/plots/CT_number_noise_v_diameter.png'
plot_CT_number_noise_v_diameter(fbp_summary_df, proc_summary_df, output_fname)
print(output_fname)
# %%
output_fname = 'results/plots/relative_noise_vs_diameter.png'
_, rel_denoise_ax = plot_relative_denoising(fbp_summary_df, proc_summary_df)
print(output_fname)
# %%
output_fname = 'results/plots/noise_reduction_vs_diameter.png'
_, noise_redux_ax = plot_noise_reduction(csv_fname, output_fname)
print(output_fname)
# %%
output_fname = 'results/plots/CT_number_bias.png'
plot_CT_bias(csv_fname, output_fname)
print(output_fname)

# %%
bias_df = get_bias_df(csv_fname)
noise_reduction_df = get_noise_reduction_df(csv_fname)
f, ax = plt.subplots(figsize=(4,4))
patient_diameter = bias_df.index
im = ax.scatter(noise_reduction_df['mean noise (ROI std) [HU]'], bias_df['mean CT number [HU]'], c=patient_diameter)
ax.set_xlabel('Relative Noise Reduction [%]\n$|\sigma_{REDCNN} - \sigma_{FBP}| / \sigma_{FBP}\\times 100$')
ax.set_ylabel('CT Number Bias [HU]')
cbar = plt.colorbar(im, label='Patient Diameter [mm]')
f.tight_layout()

output_fname = 'results/plots/bias_v_noise_reduction.png'
f.savefig(output_fname, dpi=600)
print(output_fname)
# %%

nps_csv_fname = 'results/diameter_1D_nps.csv'
write_1D_nps_results_to_csv(base_dir, nps_csv_fname, DOSELEVEL)
print(nps_csv_fname)

fbp_nps, proc_nps = load_csv(nps_csv_fname)
# %%
def get_noise_level_from_nps(delfreq, mag): return np.sqrt(sum(delfreq*mag))
# %%
delfreq = fbp_nps['spatial frequency [cyc/pix]'].diff()[1]
diameters = [int(d.split('diameter')[1].split('mm')[0]) for d in fbp_nps.columns[1:]]
fbp_noise_levels = [get_noise_level_from_nps(delfreq, fbp_nps[d]) for d in fbp_nps.columns[1:]]
proc_noise_levels = [get_noise_level_from_nps(delfreq, proc_nps[d]) for d in proc_nps.columns[1:]]

nps_noise_levels = pd.DataFrame({'Patient Diameter [mm]': diameters, 'FBP': fbp_noise_levels, 'REDCNN': proc_noise_levels}).set_index('Patient Diameter [mm]')
nps_noise_levels
# %%
fbp_summary_df, proc_summary_df = load_csv(csv_fname)
fbp_summary_df.set_index('Patient Diameter [mm]', inplace=True)
fbp_summary_df.pop('mean CT number [HU]')
proc_summary_df.set_index('Patient Diameter [mm]', inplace=True)
proc_summary_df.pop('mean CT number [HU]')
roi_noise_levels = fbp_summary_df.join(proc_summary_df, rsuffix='_REDCNN-TV')
roi_noise_levels.columns = [c + ' ROI' for c in nps_noise_levels.columns]
nps_noise_levels.columns = [c + ' NPS' for c in nps_noise_levels.columns]
# %%
noise_levels_df = pd.concat((roi_noise_levels, nps_noise_levels), axis=1)
noise_levels_df.columns = sorted(noise_levels_df.columns)
noise_levels_df.to_csv('results/nps_vs_roi_noise_levels.csv')
# %%
