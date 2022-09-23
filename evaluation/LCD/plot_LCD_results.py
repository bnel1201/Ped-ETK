# %%
import h5py
h5file = '/home/brandon.nelson/Data/temp/CCT189/rz_results/test_results.h5'
f = h5py.File(h5file, 'r')
f.keys()
# %% [markdown]
# shape: [dose level, recon option, reader num, inserts num] 
# reversed from matlab which is F index, but Python is C indexed
# %%
auc = f['auc'][:]

auc.shape
# %%
snr = f['snr'][:]

snr.shape
# %%
f['dose_levels'][:]
# %%
f['recon_types'][:]
# %%
f['readers'][:]
# %%
