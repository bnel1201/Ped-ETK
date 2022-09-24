# %%
import matplotlib.pyplot as plt
import h5py
# %%
h5file = '/home/brandon.nelson/Data/temp/CCT189/rz_results/test_results.h5'
f = h5py.File(h5file, 'r')
f.keys()
# %% [markdown]
# shape: [dose level, recon option, reader num, inserts num] 
# reversed from matlab which is F index, but Python is C indexed
# %%
auc = f['auc'][:]
snr = f['snr'][:]
dose_levels = f['dose_levels'][:]
recon_types = f['recon_types'][:2]
nreaders = f['readers'][:]
# %%

# %%
auc.shape
# %%
plt.bar?
# %%
recon_idx=[0, 1]
reader_idx=0
dose_idx=0
lesion_aucs = auc[dose_idx, recon_idx[0], reader_idx, :]
lesion_snrs = snr[dose_idx, recon_idx[0], reader_idx, :]
# %%
