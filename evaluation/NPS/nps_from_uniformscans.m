% Purpose: calculate NPS from water phantom scans

clear all; 

%original FBP image folder
fbp_kernel = 'fbp_smooth';
folder_path =['/gpfs_projects/rxz4/data/DLCT/phantom_sim/for_CT2020Conf/uniform/' fbp_kernel '/'];

%Processed images folders
fbp_kernel = 'fbp_smooth';%'fbp_mooth';
proc_kernel = 'sharpM1-R0-S3'; %'sharpM1-R0-S3';
% folder_path = ['/raida/rpz/data/DLCT/phantom_sim/for_CT2020Conf/uniform_proc/' fbp_kernel '/' proc_kernel '/'];
%folder_path = ['/gpfs_projects/rxz4/data/DLCT/phantom_sim/for_CT2020Conf/uniform_proc/' fbp_kernel '/' proc_kernel '/'];

folder_path = '/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/uniform_quarter/';
folder_path1 = '/gpfs_projects/prabhat.kc/lowdosect/transfers/transfers_4_spie/exps/exps/exps_4r_phan_insert/results/'; 
proc_path = {'REDCNN_sg2/checkpoint-25/','DnCNN_sg2/checkpoint-20/', 'UNet/checkpoint-6/','GAN/SRGAN_Generator_model_19/', 'CNN3/checkpoint-25/', 'REDCNN_sg3/checkpoint-20/','DnCNN_sg3/checkpoint-20/'};
id=1
folder_path = [folder_path1 'uniform_quarter_' proc_path{id}]


fileinfo = dir(folder_path);
nfile = length(fileinfo)-2;
nsim = nfile;

% image information
nx = 256;
dx = 0.664; %mm
fov = nx*dx;
Fs = 1/dx;
pix_size = dx;

half_roisize = 32;
roi_xfov = nx/2+[-half_roisize:half_roisize-1];
roi_yfov = roi_xfov;
nx_roi = length(roi_xfov);
   
%Read in the repeatitive noisy scans
img = zeros(nx,nx,nsim);
for i=1:nsim
    i
    filename = fileinfo(i+2).name
    filepath = [folder_path filename];
    fid = fopen(filepath);
    img(:,:,i) = fread(fid,[256 256], 'int16');
    fclose(fid);
end

%extract noise only images
img_mean = mean(img,3);
noise_roi = zeros(nx_roi, nx_roi, nsim); 
for i=1:nsim
    noise = img(:,:,i) - img_mean;
    noise_roi(:,:,i) =  noise(roi_xfov, roi_yfov);
end
noise_roi = noise_roi *sqrt(nsim/(nsim-1)); %Bias correction

%Compute NPS
nps = compute_nps(noise_roi);

maxnps = max(nps(:));
if(nps(half_roisize+1,half_roisize+1)==maxnps) 
   nps(half_roisize+1+[-1:1],half_roisize+1+[-1:1]) = 0;
end

%extract the 1D radial shape
ang = [0:1:180];
[cx, cy,c, mc] = radial_profiles_fulllength(nps, ang);
nps1d = mc;
fr = 1/2 *linspace(0, 1, (length(nps1d)));

%save nps, nps1d, one slice of sample image, freq_vec 

figure;
subplot(121); imagesc(nps); colormap(gray), daspect([1 1 1]);
subplot(122), plot(fr,nps1d); xlabel 'cyc/pixel'; ylabel 'Magnitude';

%check mean HU variations in the set of images
t=(img(128+[-5:5],128+[-5:5],:));tmean=mean(reshape(t, [11*11 25])); [mean(tmean) std(tmean)]
tvar=std(reshape(t, [11*11 25])); [mean(tvar) std(tvar)]



%fr = Fs/2 *linspace(0, 1, (length(nps1d))); %this is not correct because with fulllength radial profile the highest freq is about sqrt(2) time the half Nyquist freq.

%--11/17/2021
% "dfr" is freq unit in lp/mm
% "dfr_dft" is freq unit in cyc/pixel
dfr = Fs/(nx_roi-1);
fr = dfr*(0:length(nps1d-1));

dfr_dft = 1/(nx_roi-1);
fr_dft = dfr_dft*(0:length(nps1d-1)); %freq points in cyc/pix;
%--end of 11/17/2021 
 
%save nps, nps1d, one slice of sample image, freq_vec 
img_sample = img(:,:,20);

if(~exist('proc_kernel'))
    filename = ['nps_' fbp_kernel '.mat'];
else
    filename = ['nps_' fbp_kernel '_' proc_kernel '.mat'];
end
%save(filename, 'nps', 'nps1d', 'fr','img_sample');


    
    
    