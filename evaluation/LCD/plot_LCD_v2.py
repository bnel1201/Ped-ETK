# %%
import pandas as pd
import matplotlib.pyplot as plt
lcd_data = pd.read_csv('lcd_results.csv')
lcd_data['dose level [%]'] = 100 * lcd_data['dose level [photons]'] /  lcd_data['dose level [photons]'].max()
lcd_data.plot.scatter(x='patient diameter [mm]', y='snr', c='dose level [%]', cmap='jet')
plt.savefig('lcd_results.png', dpi=600)
# %%
lcd_data.plot.scatter(x='patient diameter [mm]', y='auc', c='dose level [%]', cmap='jet')

# %%
lcd_data['dose level [%]'] = lcd_data['dose level [photons]'] /  lcd_data['dose level [photons]'].max()
lcd_data['recon type'] = lcd_data['recon type'].astype('category')
lcd_data.plot.scatter(x='patient diameter [mm]', y='auc', s='dose level [%]', c='recon type', cmap='jet')
# %%
cnn_lcd = lcd_data[lcd_data['recon type'] == 'cnn'].reset_index(drop=True)
cnn_lcd.drop('recon type', axis=1, inplace=True)
fbp_lcd = lcd_data[lcd_data['recon type'] == 'fbp'].reset_index(drop=True)
fbp_lcd.drop('recon type', axis=1, inplace=True)

cnn_lcd['delta auc'] = cnn_lcd['auc'] - fbp_lcd['auc']
cnn_lcd['delta snr'] = cnn_lcd['snr'] - fbp_lcd['snr']

# %%
cnn_lcd.plot.scatter(x='patient diameter [mm]', y='delta snr', c='dose level [%]', cmap='jet')

# %%
cnn_lcd.plot.scatter(x='patient diameter [mm]', y='delta auc', c='dose level [%]', cmap='jet')

# %%
