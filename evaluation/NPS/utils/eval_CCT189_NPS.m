
% Purpose: calculate NPS from water phantom scans

% clear all;
addpath('/home/brandon.nelson/Dev/PhantomSimulations/CT_simulator')
if ~exist('homedir', 'var') %checks if setpath has been run
    setpath
end
addpath('utils')
addpath([dirname(fileparts(mfilename('fullpath')), 2) '/utils'])

if ~exist('folder_path', 'var')
    folder_path = '/home/brandon.nelson/Data/temp/CCT189/monochromatic/diameter112mm/I0_0300000/bkg';
end
results_path = fullfile(dirname(folder_path, 2), 'NPS');
if ~exist(results_path)
    mkdir(results_path)
end

fileinfo = dir(folder_path);
nfile = length(fileinfo)-2;
nsim = nfile;

% image information
parentfolder = dirname(folder_path, 3);

ig = read_geometry_info([parentfolder '/geometry_info.csv']);
nx = ig.nx;
dx = ig.dx; %in mm
fov = ig.fov; %in mm

relative_roisize = 1/4;
half_roisize = nx*relative_roisize/2;
% half_roisize = 32;
roi_xfov = nx/2+[-half_roisize:half_roisize-1];
roi_yfov = roi_xfov;
nx_roi = length(roi_xfov);
   
%Read in the repeatitive noisy scans
img = zeros(nx,nx,nsim);

for i=1:nsim
    filename = fileinfo(i+2).name;
    filepath = fullfile(folder_path, filename);
    fnames{i} = filepath;
    fid = fopen(filepath);
    img(:,:,i) = fread(fid,[nx nx], 'int16');
    fclose(fid);
end

%extract noise only images
img_mean = mean(img,3);
noise_roi = zeros(nx_roi, nx_roi, nsim); 
for i=1:nsim
    noise = img(:,:,i) - img_mean;
    noise_roi(:,:,i) =  noise(roi_xfov, roi_yfov);
end

noise_roi = noise_roi * sqrt(nsim/(nsim-1)); %Bias correction

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

parts = regexp(parentfolder, '/', 'split');

nps_raw_fname = fullfile(results_path, sprintf('2D_nps_float32_%d.raw', nx_roi));
my_write_rawfile(nps_raw_fname, single(nps), 'single');
%check mean HU variations in the set of images
tiny_roi = round(nx/10/2);
t=(img(nx/2+[-tiny_roi:tiny_roi],nx/2+[-tiny_roi:tiny_roi],:));
diam = parts(end);
tmean=mean(reshape(t, numel(t(:,:,1)), nsim));
tstd=std(reshape(t, numel(t(:,:,1)), nsim));

disp(sprintf('%s NPS evaluation. Center ROI summary of %d simulations', diam{:}, nsim))
disp(sprintf('mean of means: %3.4f, std of means: %3.4f', mean(tmean), std(tmean)))
disp(sprintf('mean of stds: %3.4f, std of stds: %3.4f', mean(tstd), std(tstd)))

roi_stats_csv_fname = fullfile(results_path, 'roi_stats.csv');
fid = fopen(roi_stats_csv_fname, 'w');
fprintf(fid, '%s\r\n', 'filename, mean [HU], std [HU]');
for i = 1:nsim
    fprintf(fid, '%s, %3.4f, %3.4f\r\n', fnames{i}, tmean(i), tstd(i));
end
fclose(fid);

Fs = 1/dx; %units of lp/mm
dfr = Fs/(nx_roi-1);
fr = dfr*(0:length(nps1d)-1);

dfr_dft = 1/(nx_roi-1);
fr_dft = dfr_dft*(0:length(nps1d)-1); %freq points in cyc/pix;

nps_1d_csv_fname = fullfile(results_path, '1D_nps.csv');
fid = fopen(nps_1d_csv_fname, 'w');
fprintf(fid, '%s\r\n', 'spatial frequency [cyc/pix], magnitude');
fprintf(fid, '%3.4f, %3.4f\r\n', cat(1, fr_dft, nps1d));
fclose(fid);
disp('files written:')
disp(sprintf('%s\r\n', nps_raw_fname, roi_stats_csv_fname, nps_1d_csv_fname))
disp(repmat('-', 1, 20))