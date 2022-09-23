
import argparse, os
from pathlib import Path
import glob
import numpy as np 
from skimage.transform import rescale, resize
from skimage.metrics import structural_similarity as compare_ssim
import natsort
import cv2
import pandas as pd

import torch
from torchvision.transforms import ToTensor
import util
import sys

import quant_util
import io_func

#Testing settings
parser = argparse.ArgumentParser(description='PyTorch application of trained weight on patient dicom images')
parser.add_argument('--model-name','--m', type=str, default='three_layers', 
                    help='choose the network architecture name that you are going to use. Other options include redcnn, dncnn, unet, gan.')
parser.add_argument('--input-folder', type=str, required=True, help='directory name containing noisy input test images.')
parser.add_argument('--gt-folder', type=str, required=False, default="", help='directory name containing test Ground Truth images')
parser.add_argument('--model-folder', type=str, required=True, help='directory name containing saved checkpoints')
parser.add_argument('--output-folder', type=str, help='path to save the output results')
parser.add_argument('--normalization-type', type=str, required=True, help='normalization stipulated while training weights')
parser.add_argument('--cuda', action='store_true', help='use cuda')
parser.add_argument('--input-img-type', type=str, default='dicom', help='dicom or raw or tif?')
parser.add_argument('--specific-epoch', action='store_true', help='If true only one specific epoch based on the chckpt-no will be applied to \
																   test images. Else all checkpoints (or every saved checkpoints corresponding to each epoch)\
																   will be applied to test images.')
parser.add_argument('--chckpt-no', type=int, required=False, default=-1, help='epoch no. of the checkpoint to be loaded\
																		to be applied to noisy images from the test set. Default is the last epoch')
parser.add_argument('--se-plot', action='store_true', help='If true denoised images from test set is saved inside the output-folder.\
															Else only test stats are saved in .txt format inside the output-folder.')
parser.add_argument('--out-dtype', type=str, default="uint16", help="data type to save/process desnoised output.")

args = parser.parse_args()

print('\n----------------------------------------')
print('Command line arguements')
print('----------------------------------------')
for i in args.__dict__: print((i),':',args.__dict__[i])
print('\n----------------------------------------\n')

input_folder = args.input_folder
gt_folder	 = args.gt_folder
output_folder= args.output_folder
model_folder = args.model_folder

cuda 		  = args.cuda 
normalization_type = args.normalization_type
specific_epoch= args.specific_epoch
chckpt_no	  = args.chckpt_no
num_channels  = 1
gt_available  = bool((args.gt_folder).strip())
out_dtype 	  = args.out_dtype
if (specific_epoch == True): 
	if (chckpt_no != -1): chckpt_no = chckpt_no-1


csv_file = Path(input_folder).parents[1] / 'image_info.csv'
if csv_file.exists():
	ig = pd.read_csv(csv_file, header=None)
	ig = pd.DataFrame({r:[c] for r,c in zip(ig.loc[:,0], ig.loc[:,1])})
	matrix_size = int(ig.nx.to_numpy())
else:
	matrix_size = 256

# =================================
# Importing model architecture:
# =================================
if args.model_name =='three_layers':
  from models.three_layers import three_layers
  main_model = three_layers(num_channels=num_channels)
if args.model_name =='redcnn':
  from models.redcnn import REDcnn10
  main_model = REDcnn10(idmaps=3)
if args.model_name == 'unet':
  from models.unet import UDnCNN
  main_model = UDnCNN(D=10) # D is no of layers
if args.model_name == 'dncnn':
  from models.dncnn import DnCNN
  main_model = DnCNN(channels=num_channels) # default: layers used is 17, bn=True
#if args.model_name == 'simpleGAN':
#  from models.gan import Generator
#  main_model = Generator(n_residual_blocks=16, upsample_factor=1, base_filter=64, num_channel=num_channels)

def main():
	# importing model all the checkpoint NAMES saved in the training phase
	if args.model_name == 'simpleGAN':
		model_names = natsort.natsorted(glob.glob(os.path.join(model_folder, "SRGAN_Generator*.*")))
	else:
		model_names = natsort.natsorted(glob.glob(os.path.join(model_folder, "*.*")))
	
	# =============================================================
	# Importing checkpoint paths & creating folders to save results
	# -------------------------------------------------------------
	# if last-model argument is true
	# import only the last checkpoint from training phase
	if specific_epoch is True:
		fm_name = model_names[chckpt_no]
		model_names = []
		model_names.append(fm_name)

		#declaring and creating folders to store results if specific check point no is fed in 
		sp_str = model_names[0].split('/')
		sp_str = sp_str[-1]
		sp_str = sp_str.split('.')
		sp_str = sp_str[0]
		cnn_hd_test_out   = os.path.join(output_folder, sp_str)	
		if not os.path.isdir(cnn_hd_test_out): os.makedirs(cnn_hd_test_out)
		if gt_available: quant_fname = os.path.join(output_folder, sp_str+'_quant_vals.txt') 
	else:
		# when all checkpoints are used to give their respective quant results
		# we save only quant values and not the individual CNN based Hd image results
		if not os.path.isdir(output_folder): os.makedirs(output_folder, exist_ok=True)
		if gt_available: quant_fname = os.path.join(output_folder, 'all_checkpoint_quant_vals.txt')

	# gt data is available save global metrics to a txt file
	if gt_available:
		quantfile = open(quant_fname, '+w')	
		quantfile.write('chckpt-no, CNN rMSE, (+,-std), CNN PSNR [dB], (+,-std), CNN SSIM, (+,-std), LD rMSE, (+,-std), LD PSNR [dB], (+,-std), LD SSIM, (+,-std)\n')
	
	# ===================================
	# Accessing all (or one) checkpoints
	# ===================================
	for ith_model in range(len(model_names)):
		if args.model_name =='simpleGAN':
			model = torch.load(model_names[ith_model], map_location=lambda storage, loc: storage)
			model = model.eval()
			if cuda: model = model.cuda()
		else:	
			model = main_model
			model = model.eval()
			if cuda: model = model.cuda()
			checkpoint = torch.load(model_names[ith_model], map_location=torch.device('cpu'))
			model.load_state_dict(checkpoint['model'])

		#read images from input-folder
		lr_img_names = sorted(glob.glob(os.path.join(input_folder, "*.*")))
		if gt_available:
			gt_img_names = sorted(glob.glob(os.path.join(gt_folder, "*.*")))
			lr_rMSE_arr, lr_psnr_arr, lr_ssim_arr    = [], [], []
			cnn_rMSE_arr, cnn_psnr_arr, cnn_ssim_arr = [], [], []

		# ====================================
		# Denoising all LD images from Test Set
		# =====================================
		for i in range(len(lr_img_names)):
			if args.input_img_type=='dicom':
				lr_img = io_func.pydicom_imread(lr_img_names[i])
				if gt_available: gt_img = io_func.pydicom_imread(gt_img_names[i])
			elif args.input_img_type=='raw':
				lr_img = io_func.raw_imread(lr_img_names[i], (matrix_size, matrix_size), dtype='int16')
				if gt_available: gt_img = io_func.raw_imread(gt_img_names[i], (matrix_size, matrix_size), dtype='int16')
			else:
				lr_img = io_func.imageio_imread(lr_img_names[i])
				if gt_available: gt_img = io_func.imageio_imread(gt_img_names[i])
			print('LR filename:', lr_img_names[i])
		
			if gt_available: gt_min, gt_max = np.min(gt_img), np.max(gt_img)
			lr_h, lr_w = lr_img.shape
			img_max, img_min = np.max(lr_img), np.min(lr_img)

			model_in_lr_img, _ = util.img_pair_normalization(lr_img, lr_img, normalization_type=normalization_type)
			#print('gt min/max', np.min(gt_img), np.max(gt_img), gt_img.dtype)
			print('lr min/max', np.min(lr_img), np.max(lr_img), lr_img.dtype)
			#sys.exit()
			#CNN hd part
			img_to_tensor = ToTensor()
			img_input     = img_to_tensor(model_in_lr_img).view(1, -1, lr_h, lr_w)
			if cuda: img_input = img_input.cuda()

			img_input  = img_input.float()
			cnn_output = model(img_input)
			cnn_output = cnn_output.cpu()
			cnn_output = cnn_output[0].detach().numpy()
			cnn_output = np.squeeze(cnn_output.transpose(1, 2, 0))

			# Renormalize CNN output and change back to original data type	
			# print('cnn min/max', np.min(cnn_output), np.max(cnn_output), cnn_output.dtype)	    
			cnn_output = quant_util.renormalize(cnn_output, lr_img, normalization_type=normalization_type)
			lr_img = lr_img.astype(out_dtype)
			cnn_output = (cnn_output).astype(out_dtype)
			# if gt_available: util.plot2dlayers(gt_img)
			util.plot2dlayers(lr_img)
			util.plot2dlayers(cnn_output)
			# sys.exit()
			# calculating global metrics when gt Images are available
			print('img no', i)
			if gt_available:
				gt_img = gt_img.astype(out_dtype)
				cnn_max, cnn_min = max(np.max(gt_img), np.max(cnn_output)), min(np.min(gt_img), np.min(cnn_output))
				cnn_rMSE = quant_util.relative_mse(gt_img, cnn_output)
				cnn_psnr = quant_util.psnr(gt_img, cnn_output, cnn_max)
				cnn_ssim = compare_ssim(cnn_output.reshape(lr_h, lr_w, 1), gt_img.reshape(lr_h, lr_w, 1), multichannel=True, data_range=(cnn_max-cnn_min))
				cnn_rMSE_arr.append(cnn_rMSE)
				cnn_psnr_arr.append(cnn_psnr)
				cnn_ssim_arr.append(cnn_ssim)

				lr_max, lr_min = max(np.max(gt_img), np.max(lr_img)), min(np.min(gt_img), np.min(lr_img))
				lr_rMSE = quant_util.relative_mse(gt_img, lr_img)
				lr_psnr = quant_util.psnr(gt_img, lr_img, lr_max)
				lr_ssim = compare_ssim(lr_img.reshape(lr_h, lr_w, 1), gt_img.reshape(lr_h, lr_w, 1), multichannel=True, data_range=(lr_max-lr_min))
				lr_rMSE_arr.append(lr_rMSE)
				lr_psnr_arr.append(lr_psnr)
				lr_ssim_arr.append(lr_ssim)

				print('cnn/ld psnr', cnn_psnr, lr_psnr)
				print('gt min/max', np.min(gt_img), np.max(gt_img), gt_img.dtype)
			
			print('lr min/max', np.min(lr_img), np.max(lr_img), lr_img.dtype)
			print('cnn min/max', np.min(cnn_output), np.max(cnn_output), cnn_output.dtype)
			
			# ==========================================================		    
			# saving feed forward results from specific epoch (if true)
			# ==========================================================
			if (specific_epoch == True and args.se_plot ==True):
				img_str = lr_img_names[i]	   
				img_str = img_str.split('/')[-1]
				img_no  = img_str.split('.')[0] 	
				io_func.imsave_raw((cnn_output), cnn_hd_test_out + '/' + img_no + '.raw')
		# command line print + quantfile print
		if gt_available:
			# extract checkpoint no to print
			chckpt_name = model_names[ith_model]
			chckpt_name = chckpt_name.split('/')[-1]
			chckpt_name = chckpt_name.split('.')[0]
			if (args.model_name=='simpleGAN'):
				prnt_chckpt_no = int(chckpt_name.split('_')[3])
			else:
				prnt_chckpt_no = int(chckpt_name.split('-')[1])

			print("%s => avg (std) CNN [rMSE: %.4f (%.4f), PSNR: %.4f (%.4f), SSIM: %.4f (%.4f)] \n\t\t avg LD (std), [rMSE: %.4f (%.4f), PSNR: %.4f (%.4f), SSIM: %.4f (%.4f)]" % \
			(chckpt_name, np.mean(cnn_rMSE_arr), np.std(cnn_rMSE_arr), np.mean(cnn_psnr_arr), np.std(cnn_psnr_arr), np.mean(cnn_ssim_arr), np.std(cnn_ssim_arr),\
		    np.mean(lr_rMSE_arr), np.std(lr_rMSE_arr), np.mean(lr_psnr_arr), np.std(lr_psnr_arr), np.mean(lr_ssim_arr), np.std(lr_ssim_arr)))

			quantfile.write("%9d,%9.4f,%9.4f,%14.4f,%9.4f,%9.4f,%9.4f,%8.4f,%9.4f,%13.4f,%9.4f,%8.4f,%9.4f\n" \
	        % (prnt_chckpt_no, np.mean(cnn_rMSE_arr), np.std(cnn_rMSE_arr), np.mean(cnn_psnr_arr), np.std(cnn_psnr_arr), np.mean(cnn_ssim_arr), np.std(cnn_ssim_arr),\
		    np.mean(lr_rMSE_arr), np.std(lr_rMSE_arr), np.mean(lr_psnr_arr), np.std(lr_psnr_arr), np.mean(lr_ssim_arr), np.std(lr_ssim_arr)))
		del model
	
	if gt_available: quantfile.close()

if __name__ == "__main__":
    main()