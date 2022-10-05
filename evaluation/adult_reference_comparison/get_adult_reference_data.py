# %%
from pathlib import Path
import scipy.io
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.patches as patches
# %%
def append_adult_data_to_mtf_cutoff_data(mtf_results_dir, cutoff_val):
    ped_data = pd.read_csv(Path(mtf_results_dir) / f'mtf{cutoff_val}.csv')
    ped_fbp = ped_data[ped_data['Series'] == 'FBP Baseline']
    ped_redcnn = ped_data[ped_data['Series'] == 'REDCNN']
    ped_redcnn.pop('Series')
    ped_redcnn.pop('%MTF cutoff')
    ped_fbp.pop('Series')
    ped_fbp.pop('%MTF cutoff')

    adult_mtf_dir = Path('/gpfs_projects/prabhat.kc/lowdosect/transfers/transfers_4_spie/exps/quant_analysis/mtf/results/matfiles')
    adult_redcnn = scipy.io.loadmat(adult_mtf_dir / 'no_norm/redcnn/sharp_augTrTaTdT.mat')
    # These Contrast values are from PKC's poster located here: <S:\DIDSR\Research\DLIR Project\ConferencePresentations\ct_2022>
    redcnn_data = ped_redcnn.sort_values(by='Contrast [HU]').set_index('Contrast [HU]')
    redcnn_data = redcnn_data.join(pd.DataFrame({'Contrast [HU]': [35, 120, 340, 990], '200mm (Adult Reference)': adult_redcnn[f'mtf{cutoff_val}_all'][::-1].squeeze()}).set_index('Contrast [HU]'))

    adult_fbp = scipy.io.loadmat(adult_mtf_dir / 'sharp_fbp.mat')
    fbp_data = ped_fbp.sort_values(by='Contrast [HU]').set_index('Contrast [HU]')
    fbp_data = fbp_data.join(pd.DataFrame({'Contrast [HU]': [35, 120, 340, 990], '200mm (Adult Reference)': adult_fbp[f'mtf{cutoff_val}_all'][::-1].squeeze()}).set_index('Contrast [HU]'))
    return fbp_data, redcnn_data


def plot_sharpness_heatmap(mtf_rel, cutoff_val, output_fname=None):

    mtf_rel.columns = [int(c.split('mm')[0]) for c in mtf_rel.columns]
    mtf_rel = mtf_rel[sorted(mtf_rel.columns)]
    mtf_rel.sort_index(ascending=False, inplace=True)
    f, ax = plt.subplots()
    sns.heatmap(mtf_rel, annot=True, ax=ax,
                cbar_kws=dict(label=f'Relative Sharpness\n(REDCNN {cutoff_val}% MTF / FBP {cutoff_val}% MTF'))
    ax.set_xlabel('Patient Diameter [mm]')
    twiny = ax.twiny()

    fovs = np.round(mtf_rel.columns*1.1).astype(int).to_list()
    fovs[mtf_rel.columns.to_list().index(200)] = 212
    twiny.set_xticks(ax.get_xticks(), fovs)
    twiny.set_xlim(ax.get_xlim())
    twiny.set_xlabel("Recon FOV [mm]")
    rect = patches.Rectangle((4, 0.05), 1, 6.9, linewidth=3, edgecolor='tab:blue', facecolor='none')
    ax.annotate("Adult Reference",
                xy=(4.75, 7), xycoords='data',
                xytext=(0.55, 0.025), textcoords='figure fraction',
                color='tab:blue',
                arrowprops=dict(facecolor='tab:blue', shrink=0.05), weight='bold')
    ax.add_patch(rect)

    if output_fname is None:
        plt.show()
    else:
        output_fname = Path(output_fname).parent / f'mtf{cutoff_val}_sharpness_heatmap.png'
        f.savefig(output_fname, dpi=600)
        print(f'File saved: {output_fname}')

mtf_results_dir = Path('../../results/MTF')
fbp_data, redcnn_data = append_adult_data_to_mtf_cutoff_data(mtf_results_dir, 50)
mtf_rel = redcnn_data / fbp_data
mtf_rel


cutoff_val=50
plot_sharpness_heatmap(mtf_rel, cutoff_val)


# %%
