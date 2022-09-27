# %%
import argparse
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

DOSELEVEL = 'I0_0300000'

plt.style.use('seaborn-talk')

def plot_1D_nps(fbp_dir, proc_dir, fig=None, ax=None):
    fbp_nps_df = pd.read_csv(fbp_dir / '1D_nps.csv')
    proc_nps_df = pd.read_csv(proc_dir / '1D_nps.csv')
    if ax is None or fig is None:
        fig, ax = plt.subplots()
    diam = fbp_dir.parents[1].stem
    fbp_nps_df.plot(ax=ax, x='spatial frequency [lp/mm]', y=' magnitude', label='FBP', title=f'{diam}')
    proc_nps_df.plot(ax=ax, x='spatial frequency [lp/mm]', y=' magnitude', label='REDCNN-TV')


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


def plot_noise_summary(fbp_dir, proc_dir, fig=None, ax=None):
    fbp_stats_df = pd.read_csv(fbp_dir / 'roi_stats.csv')
    proc_stats_df = pd.read_csv(proc_dir / 'roi_stats.csv')

    noise_summary_df = pd.DataFrame({'Series': ['FBP', 'REDCNN-TV'],
                                    'noise mean [ROI std in HU]': [fbp_stats_df[' std [HU]'].mean(), proc_stats_df[' std [HU]'].mean()],
                                    'noise std [ROI std in HU]': [fbp_stats_df[' std [HU]'].std(), proc_stats_df[' std [HU]'].std()]})

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


def plot_noise_summary_all_diams(base_dir, output_fname=None, **subplots_kwargs):
    diam_dirs = sorted(list(base_dir.glob('diameter*')))
    f, axs = plt.subplots(2, 3, dpi=300, sharex=True, sharey=True)
    for ax, patient_dir in zip(axs.flatten(), diam_dirs):
        fbp_dir = patient_dir / DOSELEVEL / 'NPS'
        proc_dir = patient_dir / (DOSELEVEL + '_processed') / 'NPS'
        plot_noise_summary(fbp_dir, proc_dir, fig=f, ax=ax)
    f.tight_layout()
    if output_fname:
        Path(output_fname).parent.mkdir(exist_ok=True, parents=True)
        f.savefig(output_fname, dpi=600)
    else:
        plt.show()


def plot_noise_curves(fbp_dir, proc_dir, fig=None, ax=None):
    fbp_stats_df = pd.read_csv(fbp_dir / 'roi_stats.csv')
    proc_stats_df = pd.read_csv(proc_dir / 'roi_stats.csv')

    if ax is None or fig is None:
        fig, ax = plt.subplots()
    diam = fbp_dir.parents[1].stem

    color='blue'
    ax.plot(fbp_stats_df[' mean [HU]'], color=color, linestyle='-', label='FBP')
    ax.plot(proc_stats_df[' mean [HU]'], color=color, linestyle='--', label='REDCNN-TV')
    ax.tick_params(axis='y', labelcolor=color)
    ax.set_ylabel('mean [HU]', color=color)
    ax.set_title(diam)
    ax.set_ylim(990, 1060)
    axtwin = ax.twinx()
    color='red'
    axtwin.plot(fbp_stats_df[' std [HU]'], color=color)
    axtwin.plot(proc_stats_df[' std [HU]'], color=color, linestyle='--', label='REDCNN-TV')
    axtwin.set_ylabel('std [HU]', color=color)
    axtwin.tick_params(axis='y', labelcolor=color)
    axtwin.set_ylim(8, 32)

    return fig, ax


def plot_all_noise_curves(base_dir, output_fname=None, **subplots_kwargs):
    diam_dirs = sorted(list(base_dir.glob('diameter*')))
    f, axs = plt.subplots(2, 3, dpi=300, **subplots_kwargs)
    for ax, patient_dir in zip(axs.flatten(), diam_dirs):
        fbp_dir = patient_dir / DOSELEVEL / 'NPS'
        proc_dir = patient_dir / (DOSELEVEL + '_processed') / 'NPS'
        plot_noise_curves(fbp_dir, proc_dir, fig=f, ax=ax)
    axs[0,0].legend()
    f.tight_layout()
    if output_fname:
        Path(output_fname).parent.mkdir(exist_ok=True, parents=True)
        f.savefig(output_fname, dpi=600)
    else:
        plt.show()

# %%
base_dir = Path('/home/brandon.nelson/Data/temp/CCT189/monochromatic')
output_fname = 'results/plots/1D_nps_shared_axes.png'
plot_1D_nps_all_diams(base_dir, output_fname, sharex=True, sharey=True)
print(output_fname)

output_fname = 'results/plots/1D_nps_nonshared_axes.png'
plot_1D_nps_all_diams(base_dir, output_fname, sharex=True, sharey=False)
print(output_fname)
# %%
output_fname = 'results/plots/noise_summary.png'
plot_noise_summary_all_diams(base_dir, output_fname)
print(output_fname)

# %%
output_fname = 'results/plots/noise_curves.png'
plot_all_noise_curves(base_dir, output_fname, figsize=(14, 7))
print(output_fname)
# %%