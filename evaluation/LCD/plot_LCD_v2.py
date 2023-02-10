import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

insert_HU_size = {14 : '3 mm', 7: '5 mm', 5: '7 mm', 3: '10 mm'}

def plot_insert_level_results(img_level_mean, img_level_std, observers, insert_HUs, ylabel, fig=None, legend=True):
    fig = fig or plt.figure()
    if len(insert_HUs) > 2:
        axs = fig.subplots(2,2, sharex=True, sharey=True).flatten()
    elif len(insert_HUs) == 2:
        axs = fig.subplots(1,2, sharex=True, sharey=True)
    elif len(insert_HUs) == 1:
        axs = [fig.subplots(1,1, sharex=True, sharey=True)]

    plt_idx=0
    for insert_HU, ax in zip(insert_HUs, axs):
        for observer in observers:
            series_mean = img_level_mean[insert_HU, observer]
            series_std = img_level_std[insert_HU, observer]
            series_mean.plot(ax=ax, yerr=series_std, label=observer, capsize=3)
        ax.set_title(f'{insert_HU} HU, {insert_HU_size[insert_HU]}')
        ax.set_ylabel(ylabel)

        if legend & (plt_idx < 1):
            fig.legend(bbox_to_anchor=(0.5, 1.1), loc = 'upper center', frameon=False, ncol=3)
        plt_idx += 1
    return fig, axs

class LCD_Plotter:
    def __init__(self, lcd_data):
        self.data = lcd_data
        self.reset()
        
    def reset(self):
        self.observers = self.data['observer'].unique()
        self.phantom_diameters = self.data['phantom diameter [mm]'].unique()
        self.insert_HUs = self.data['insert_HU'].unique()
        self.recons = self.data['recon'].unique()
        self.dose_levels = self.data['dose [%]'].unique()

    def plot(self, x='dose', restype='auc', recon_cmp_method='diff', transpose=False):
        if x == 'dose':
            row_data = self.phantom_diameters
        elif x == 'diameter':
            row_data = self.dose_levels
        recons = self.recons
        if not isinstance(row_data, list): row_data = np.array([row_data])
        if not isinstance(recons, list): recons = np.array([recons])
        nrecons = len(recons)

        figsize =  (3*len(row_data) + 1, 3*nrecons + 1) if transpose else (3*nrecons + 1, 3*len(row_data) + 1)
        master_fig = plt.figure(constrained_layout=True, figsize=figsize, dpi=150)
        figs = master_fig.subfigures(nrecons, len(row_data)) if transpose else master_fig.subfigures(len(row_data), nrecons)
        if nrecons + len(row_data) <= 2:
            figs = np.array(figs)
        figs = figs.T.flatten() if transpose else figs.flatten()
        fig_idx = 0
        fig_dict = {}
        # if len(row_data) == 1: row_data = [row_data]
        for rd in row_data:
            for recon in recons:
                legend = True if (fig_idx == 0) else False
                fig = figs[fig_idx]
                fig, axs = self.plot_img_level_results(rd, x=x, recontype=recon, restype=restype, fig=fig, legend=legend, recon_cmp_method=recon_cmp_method)
                fig_dict[f'fig{fig_idx}'] = [fig, axs] 
                fig_idx += 1
        return fig_dict
        
    def plot_img_level_results(self, row_data, x='dose', recontype='fbp', restype='auc', fig=None, legend=True, recon_cmp_method='diff'):
        if x == 'dose':
            grouped = self.data.groupby(["phantom diameter [mm]","recon", "insert_HU", "observer", "dose [%]"])
            fig_title = f'{row_data} mm '
        elif x == 'diameter':
            grouped = self.data.groupby(["dose [%]", "recon", "insert_HU", "observer", "phantom diameter [mm]"])
            fig_title = f'{row_data} % '
        lcd_mean = grouped.mean()
        lcd_std = grouped.std()
        
        fig = fig or plt.figure()
        ylabel = f'{restype.upper()}'
        if restype == 'snr': ylabel = '$d_{' + ylabel + '}$'
        
        insert_HUs = self.insert_HUs
        if isinstance(insert_HUs, int): insert_HUs = [insert_HUs]
        if isinstance(recontype, str):
            img_level_mean = lcd_mean[restype][row_data, recontype]
            img_level_std = lcd_std[restype][row_data, recontype]
            fig_title += f'{recontype}'
        else:
            dlir_mean = lcd_mean[restype][row_data, recontype[0]]
            dlir_std = lcd_std[restype][row_data, recontype[0]]
            fbp_mean = lcd_mean[restype][row_data, recontype[1]]
            fbp_std = lcd_std[restype][row_data, recontype[1]]
            if recon_cmp_method == 'diff':
                img_level_mean = dlir_mean - fbp_mean
                img_level_std = np.sqrt(fbp_std**2 + dlir_std**2)
                ylabel = '$\Delta$' + ylabel
            elif recon_cmp_method == 'div':
                img_level_mean  = dlir_mean / fbp_mean
                img_level_std = np.sqrt((fbp_std/fbp_mean)**2 + (dlir_std/dlir_mean)**2)
                ylabel +=  ' ratio'
            fig_title += f'{recontype[0]} - {recontype[1]}'
        fig.suptitle(fig_title)

        fig, axs = plot_insert_level_results(img_level_mean, img_level_std, self.observers, insert_HUs, ylabel, fig=fig, legend=legend)
        return fig, axs

    
def main():
    lcd_data = pd.read_csv('/home/brandon.nelson/Dev/DLIR_Ped_Generalizability/geomtric_phantom_studies/results/LCD/LCD_results.csv')

    lcd_data.replace('dl_REDCNN', 'dlir', inplace=True)
    lcd_data.rename(columns={'patient_diameter_mm': 'phantom diameter [mm]', 'dose_level_pct': 'dose [%]'}, inplace=True)
    lcd_data = lcd_data[lcd_data['phantom diameter [mm]'] != 200] #ref has large fov
    plotter = LCD_Plotter(lcd_data)

    plotter.insert_HUs = 7
    plotter.dose_levels = [100, 25]
    plotter.recons = [['dlir', 'fbp']]
    plotter.observers = ['Laguerre-Gauss CHO 2D', 'NPW 2D']
    ylim = (0.25, 6.75)
    fig_dict = plotter.plot(restype='snr', x='diameter', recon_cmp_method='div', transpose = True)
    fig_dict['fig0'][1][0].set_ylim(ylim)
    fig_dict['fig1'][1][0].set_ylim(ylim)
    plt.savefig("SNR_ratio_v_diameter.png", dpi=600)

if __name__ == "__main__":
    main()