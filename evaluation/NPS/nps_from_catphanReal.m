% Purpose: calculate NPS from water phantom scans

clear all; 

%original FBP image folder
folder_path = '/gpfs_projects/rxz4/data/DLCT/phantom_realscan/NIH_Catphan600_Mar2020/4031_low/'; 
%folder_path = '/gpfs_projects/rxz4/data/DLCT/phantom_realscan/NIH_Catphan600_Mar2020/redcnn_processed/4031_low/sharpM1-R0-S3/';

%scan_start = 5; %394'7' for B30f-3mm
scan_start = 2; %403'2' for B30f-3mm
for i=1:5
    %scan_list{i} = ['394' num2str(scan_start + (i-1)*8)]; %for 3941 series
    %scan_list{i} = ['402' num2str(scan_start + (i-1)*8)]; %for 4021 series
    scan_list{i} = ['403' num2str(scan_start + (i-1)*8)]; %for 4031 series
end

slice_list = [43:2:46]; %3mm slice thickness
%slice_list = [126:2:142];%1mm slice thickness

%get image information
scan_path = [folder_path scan_list{1} '/'];
fileinfo = dir(scan_path);
file1 = [scan_path fileinfo(3).name]
img_tmp = dicomread(file1);
info = dicominfo(file1);
nx = size(img_tmp,1);
dx = info.PixelSpacing(1);
fov = nx*dx;
Fs = 1/dx;
pix_size = dx;

roi_xfov = nx/2+[-32:31];
roi_yfov = roi_xfov;
nx_roi = length(roi_xfov);
   
%Read in the repeatitive noisy scans
n_scan = length(scan_list)
n_sliceperscan =  length(slice_list)
n_slice = n_scan * n_sliceperscan;

allslice = zeros(nx,nx,n_sliceperscan,n_scan);
for i=1:n_scan
    i    
    file_path = [folder_path scan_list{i} '/'];
    fileinfo = dir(file_path);
    nfile = length(fileinfo)-2;
    
    %sort the filename in asending order
    for j=1:nfile
        filename = fileinfo(j+2).name;
        filenum(j) = str2num(filename);
    end
    [dummy,order] = sort(filenum,'ascend');

    %Read the uniform slices
    for j=1:n_sliceperscan
        filename = fileinfo(order(slice_list(j))+2).name
        filepath = [file_path filename];
        allslice(:,:,j,i) = dicomread(filepath);
    end

end

%three options
%img = reshape(allslice, nx, nx, n_slice); % Using all slices
%img = squeeze(allslice(:,:,j,1)); %Using the slices from one scan
%img = squeeze(allslice(:,:,2,:)); % Using the same one slice from all scans
nps = 0;
for j=1:size(allslice,3)
    img = squeeze(allslice(:,:,j,:)); % Using the same one slice from all scans
    %extract noise only images
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
    nps = compute_nps(noise_roi) + nps;
end
nps = nps/size(allslice,3);

%extract the 1D radial shape
ang = [0:1:180];
[cx, cy,c, mc] = radial_profiles_fulllength(nps, ang);
nps1d = mc;
fr = Fs/2 *linspace(0, 1, (length(nps1d)));

%save nps, nps1d, one slice of sample image, freq_vec 

%compute NPS (data efficient local nps method)
if(0)
   halfroi = 32;
   xfov = [200 300];
   yfov = [200 300];
   dsd = info.DistanceSourceToDetector;
   dso = info.DistanceSourceToPatient;
   [nx,ny]=size(img_mean);
   ig.x = [-(nx-1)/2:(nx-1)/2]*dx;
   ig.y = [-(ny-1)/2:(ny-1)/2]*dx;
   loc = [nx/2 nx/2];
   [localnps, radnps,avgnps,alpha_smth,mprof] = est_localnps_fan_fulllength(noise, 2*halfroi, [230 230], xfov, yfov,dso,dsd,ig.x, ig.y);
   [cx, cy, c, localnps1d] = radial_profiles_fulllength(localnps, [0:5:180]);
   [cx, cy, c, avgnps1d] = radial_profiles_fulllength(avgnps, [0:5:180]);
end

figure;
plot(fr,nps1d); %x-axis in lp/mm, range in [0, half of Nyquist]
plot(fr/Fs, nps1d); %x-axis unitless, range in [0, 0.5]; 
%hold on;
%plot(fr,localnps1d,'r');
%plot(fr,avgnps1d, 'g');
    
    
    
