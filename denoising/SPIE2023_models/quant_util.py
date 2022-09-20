import sys
#sys.path.append('/home/prabhat.kc/Implementations/python/')
#import global_files as gf
import numpy as np
import matplotlib.pyplot as plt
import os
import util
import io_func

def cnr_of_known_patches(img_path, img_tag, gt_img_path=None, dicom_input=False, savefig=True, imgrange=False):
	""" we determine CNR from two slides namely 116 & 129.
	A specific patch on each of the slides, 116 & 129, is selected to 
	determine the CNR
	
	"""
	# print(img_path)
	if dicom_input:
		full_img = io_func.pydicom_imread(img_path)
		if gt_img_path is not None: gt_img = io_func.pydicom_imread(gt_img_path)
	else:
		full_img = io_func.imageio_imread(img_path)
		if gt_img_path is not None: gt_img = io_func.imageio_imread(gt_img_path)

	if img_tag ==116:
		img_=full_img[135:185, 145:195]
		if gt_img_path is not None: gt_img_ = gt_img[135:185, 145:195]
	elif img_tag ==129:
		img_=full_img[218:268, 158:208]
		if gt_img_path is not None: gt_img_ = gt_img[218:268, 158:208]

	if gt_img_path is not None: img_ = util.normalize_data_ab(np.min(gt_img_), np.max(gt_img_), img_)
	if savefig:
		fdir = img_path.split('/')
		fdir = '/'.join(fdir[:-1])
		fdir = fdir+'_patch'
		if not os.path.isdir(fdir): os.makedirs(fdir)
		fname_cb = os.path.join(fdir, str(img_tag)+'_patch_cb.png')
		fname_no_cb = os.path.join(fdir, str(img_tag)+'_patch.tif')
		# just patch plot
		util.imsave((img_).astype('uint16'), fname_no_cb, type='original')
		# patch with colorbar plot
		plt.figure(figsize=[3,3])
		plt.imshow(img_,cmap='Greys_r')
		if imgrange: plt.clim(np.min(full_img), np.max(full_img))
		plt.colorbar()
		plt.savefig(fname_cb, bbox_inches='tight')
		plt.close()

	h, w = img_.shape
	nr = min(img_.shape)
	nc = nr
	nrdc = np.floor(nr/2)
	ncdc = np.floor(nc/2)
	r = np.arange(nr)-nrdc 
	c = np.arange(nc)-ncdc 
	[R,C] = np.meshgrid(r,c)
	index = np.round(np.sqrt(R**2+C**2))

	#util.plot2dlayers(index)
	maxindex = min(nr, nc)/2
	indices = []
	for i in np.arange(int(maxindex)):
		indices.append(np.where(index == i+1))

	in_tag = np.zeros(img_.shape)
	if img_tag ==116:
		for i in range(int(maxindex)):
		    if ((i)<=5):
		        in_tag[indices[i]]=-1
	elif img_tag ==129:
		for i in range(int(maxindex)):
		    if ((i)<=6):
		        in_tag[indices[i]]=-1
	'''
	plt.figure()
	plt.imshow(img_, cmap='gray')
	plt.imshow(in_tag, cmap='jet', alpha=0.1)
	'''
	in_ind = np.where(in_tag==-1)
	#in_region = np.zeros(img_.shape)
	#in_region[in_ind]=img_[in_ind]
	#util.plot2dlayers(in_region, cmap='jet')

	in_values=img_[in_ind]
	out_tag = np.zeros(img_.shape)

	if img_tag == 116:
		for i in range(int(maxindex)):
		    if ((i)>17 and i<=(int(maxindex-3))):
		        out_tag[indices[i]]=-1
	elif img_tag == 129:
		for i in range(int(maxindex)):
		    if ((i)>17 and i<=int(maxindex-3)):
		        out_tag[indices[i]]=-1

	out_ind = np.where(out_tag==-1)
	'''        
	out_region = np.zeros(img_.shape)
	out_region[out_ind]=img_[out_ind]
	util.plot2dlayers(out_region, cmap='gray_r')
	'''
	out_values=img_[out_ind]
	mu_s = np.mean(in_values)
	mu_b = np.mean(out_values)
	std_s = np.std(in_values)
	std_b = np.std(out_values)
	CNR = abs(mu_s-mu_b)/(0.5*(std_s+std_b))
	return(CNR)

def renormalize(cnn_output, lr_img, normalization_type=None):
	
	img_max, img_min = np.max(lr_img), np.min(lr_img)

	if(normalization_type=='max_val_independent' or normalization_type =='max_val_wrt_ld'):
		cnn_output = (cnn_output*img_max)
		if np.min(cnn_output)<0: cnn_output += (-np.min(cnn_output))
	elif(normalization_type=='std_independent' or normalization_type=='std_wrt_ld'):
		cnn_output = cnn_output*(img_max - img_min) + np.mean(lr_img)
		cnn_output[cnn_output<0]=0
		#if np.min(cnn_output)<0: cnn_output += (-np.min(cnn_output))
		#cnn_output = util.normalize_data_ab(img_min, img_max, cnn_output)
	elif(normalization_type=='dicom_std'):
		cnn_output = cnn_output*(2**12) + np.mean(lr_img)
		cnn_output = util.normalize_data_ab(img_min, img_max, cnn_output)
		#if np.min(cnn_output)<0: cnn_output += (-np.min(cnn_output))
	#elif(normalization_type=='unity'):
	#	cnn_output = util.normalize_data_ab(img_min, img_max, cnn_output)
	else:
		#if np.min(cnn_output)<0: cnn_output += (-np.min(cnn_output))
		cnn_output = util.normalize_data_ab(img_min, img_max, cnn_output)

	return(cnn_output)

def relative_mse(f_true, f_est):
	imdiff = f_true-f_est
	nume = np.sum(imdiff**2)
	deno = np.mean(f_true)-f_true
	deno = np.sum(deno**2)
	return(nume/deno)

def psnr(f_true, f_est, max_val=1.0):
    
    imdff = f_true - f_est
    rmse = np.sqrt(np.mean(imdff **2))
    psnr = 20.0*np.log10(max_val/rmse)
    return(psnr)