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


def plot_1D_nps_all_diams(output_fname=None, **subplots_kwargs):
    f, axs = plt.subplots(2, 3, dpi=300, **subplots_kwargs)
    for ax, diam in zip(axs.flatten(), diam_dirs):
        patient_dir = base_dir / diam
        fbp_dir = patient_dir / DOSELEVEL / 'NPS'
        proc_dir = patient_dir / (DOSELEVEL + '_processed') / 'NPS'
        plot_1D_nps(fbp_dir, proc_dir, fig=f, ax=ax)
    f.tight_layout()
    if output_fname:
        Path(output_fname).parent.mkdir(exist_ok=True, parents=True)
        f.savefig(output_fname, dpi=600)
    else:
        plt.show()
    [ax.get_legend().remove() for ax in axs.flatten()[1:]]


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


def plot_noise_summary_all_diams(output_fname=None, **subplots_kwargs):
    f, axs = plt.subplots(2, 3, dpi=300, sharex=True, sharey=True)
    for ax, diam in zip(axs.flatten(), diam_dirs):
        patient_dir = base_dir / diam
        fbp_dir = patient_dir / DOSELEVEL / 'NPS'
        proc_dir = patient_dir / (DOSELEVEL + '_processed') / 'NPS'
        plot_noise_summary(fbp_dir, proc_dir, fig=f, ax=ax)
    f.tight_layout()
    if output_fname:
        Path(output_fname).parent.mkdir(exist_ok=True, parents=True)
        f.savefig(output_fname, dpi=600)
    else:
        plt.show()

# %%
base_dir = Path('/home/brandon.nelson/Data/temp/CCT189/monochromatic')
diam_dirs = sorted(list(base_dir.glob('diameter*')))
output_fname = 'results/1D_nps_shared_axes.png'
plot_1D_nps_all_diams(output_fname, sharex=True, sharey=True)
print(output_fname)

output_fname = 'results/1D_nps_nonshared_axes.png'
plot_1D_nps_all_diams(output_fname, sharex=True, sharey=False)
print(output_fname)
# %%
output_fname = 'results/noise_summary.png'
plot_noise_summary_all_diams(output_fname)
print(output_fname)

# %%
