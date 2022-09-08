%NPS from simulated patient images
%
%clear all;

folder_path = '/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/patient/L506_3mm_sharp/sim_quarter_066/'; 

folder_path1 = '/gpfs_projects/prabhat.kc/lowdosect/transfers/transfers_4_spie/exps/exps/exps_4r_phan_insert/results/';
proc_path = {'REDCNN_sg2/checkpoint-25/','DnCNN_sg2/checkpoint-20/', 'UNet/checkpoint-6/','GAN/SRGAN_Generator_model_19/', 'CNN3/checkpoint-25/','REDCNN_sg3/checkpoint-20/','DnCNN_sg3/checkpoint-20/'};
id = 2;
%folder_path = [folder_path1 'sim_half_066_' proc_path{id}];
folder_path = [folder_path1 'sim_quarter_066_' proc_path{id}];

loc = [270 360];
half_roisize = 32;

nx = 512;
ny = 512;

%get image information
fileinfo = dir(folder_path);
nfile = length(fileinfo)-2;

roi_xfov = loc(1)+[-half_roisize: half_roisize-1];
roi_yfov = loc(2)+[-half_roisize: half_roisize-1];
nx_roi = length(roi_xfov);
   
%Read in the repeatitive noisy scans
img = zeros(nx, ny, nfile);
for j=1:nfile
    j       
   filename = fileinfo(j+2).name
   filepath = [folder_path filename];
   filetype = filename(end-2:end);

   if (strcmp(filetype,'raw'))
       out = my_read_rawimage(filepath,[512 512], 'int16');
       img(:,:,j) = out';
       pixsz = 340/512;
   else
      img(:,:,j)=dicomread(filepath);
      imginfo = dicominfo(filepath);
      pixelsz = imginfo.PixelSpacing(1);
   end
end
img = single(img);

nps = 0;
n_img = size(img,3);
img_mean = mean(img,3);
noise = zeros(nx, nx, n_img);
for i=1:n_img
    noise(:,:,i) = img(:,:,i) - img_mean;
    noise_roi(:,:,i) =  noise(roi_xfov, roi_yfov);
end
noise = noise *sqrt(n_img/(n_img-1));
noise_roi = noise(roi_xfov, roi_yfov,:);

%Compute NPS (empirical method)
nps = compute_nps(noise_roi);

maxnps = max(nps(:));
if(nps(half_roisize+1,half_roisize+1)==maxnps) 
   nps(half_roisize+[-1:1]+1,half_roisize+[-1:1]+1) = 0;
   nps(half_roisize+1,half_roisize+1) = 0;
end

%extract the 1D radial shape
ang = [0:1:180];
[cx, cy,c, mc] = radial_profiles_fulllength(nps, ang);
nps1d = mc;
nps1d(nps1d<0)=0; % occasionally there may be negative values near DC due to interpolation.
fr = 1/2 *linspace(0, 1, (length(nps1d)));

%save nps, nps1d, one slice of sample image, freq_vec 

figure;
subplot(121); imagesc(nps); colormap(gray), daspect([1 1 1]);
subplot(122), plot(fr,nps1d); xlabel 'cyc/pixel'; ylabel 'Magnitude';

%check mean HU variations in the set of images
t=(img(loc(1)+[-5:5],loc(2)+[-5:5],:));tmean=mean(reshape(t, [11*11 25])); [mean(tmean) std(tmean)]
tvar=std(reshape(t, [11*11 25])); [mean(tvar) std(tvar)]

%compute NPS (data efficient local nps method)
if(0)
   halfroi = 16;
   xfov = [100 300];
   yfov = [120 260];
   info = dicominfo(filename);
   dsd = info.DistanceSourceToDetector;
   dso = info.DistanceSourceToPatient;
   dpixel = info.PixelSpacing(1);
   [nx,ny]=size(img_mean);
   xx = [-(nx-1)/2:(nx-1)/2]*dpixel;
   yy = [-(ny-1)/2:(ny-1)/2]*dpixel;
 %  loc = [nx/2 nx/2];
   [localnps, radnps,avgnps,alpha_smth,mprof] = est_localnps_fan_fulllength(noise, 2*halfroi, loc, xfov, yfov,dso, dsd, xx, yy);
   [cx, cy, c, localnps1d] = radial_profiles_fulllength(localnps, [0:5:180]);
   [cx, cy, c, avgnps1d] = radial_profiles_fulllength(avgnps, [0:5:180]);
   figure;
   subplot(121); imagesc(localnps); colormap(gray), daspect([1 1 1]);
   subplot(122), plot(fr,localnps1d); xlabel 'cyc/pixel'; ylabel 'Magnitude';

end

    
    
    
