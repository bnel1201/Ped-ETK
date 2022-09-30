%LCD test
addpath('utils')
addpath('../utils')
clear all;
data_folder = '/gpfs_projects/rxz4/data/DLCT/phantom_sim/for_CT2020Conf/cct189/';
outfolder = '/home/brandon.nelson/Data/temp/CCT189/rz_results'
if ~exist(outfolder, 'dir')
    mkdir(outfolder)
end
% data_folder = '~/Data/temp/CCT189/monochromatic/diameter112mm/'
proc_data_folder = '/gpfs_projects/rxz4/data/DLCT/phantom_sim/for_CT2020Conf/cct189_proc/';
%%Data inputs
all_recon_type = {'fbp_sharp','fbp_sharp_dl_sharp', 'fbp_sharp_dl_smooth', 'fbp_smooth', 'fbp_smooth_dl_sharp', 'fbp_smooth_dl_smooth'};% 

% insert_info = read_phantom_info([parentfolder '/phantom_info_pix_idx.csv']);
% ig = read_geometry_info([parentfolder '/geometry_info.csv']);
% loc = phantom_info(2:end-1, 1:2);
% nx = ig.nx;
% dx = ig.dx;
% fov = ig.fov;

%%inserts info
nx = 320;%256;
dx = 0.664; %PixelSpacing
fov = dx*nx;  
d = 40;     % mm
% insert_info [x_center, y_center, r, HU]
insert_info = [...
    d*cosd(45)  d*sind(45)    3/2  14;      % 3mm, 14 HU
    -d*cosd(45)  d*sind(45)   5/2   7;      % 5 mm, 7 HU
    -d*cosd(45) -d*sind(45)   7/2   5;      % 7 mm, 5 HU
    d*cosd(45) -d*sind(45)   10/2   3;      % 10 mm, 3 HU
    ];
num_inserts = size(insert_info, 1);
n_recon_option = length(all_recon_type);
I0_vector = 3e5*[30 55 70 85 100]/100;
%I0 = I0_vector(1);%6e5*0.6;;
n_spfile = 200;
n_safile = 100;
n_reader = 10;
n_train = 100;
n_I0 = length(I0_vector);
auc_all = zeros(num_inserts, n_recon_option, n_I0, n_reader);
snr_all = zeros(num_inserts, n_recon_option, n_I0, n_reader);

for idx_insert=1:4
    % convert roi locations from mm to pixels (check these values against phantom_info_pix.csv)
    insert_centers = round(insert_info(:,1:2) * (nx/fov) + (nx+1)/2);
    insert_radii = insert_info(:,3) * (nx/fov);
    % select insert
    center_x = insert_centers(idx_insert, 1);
    center_y = nx-insert_centers(idx_insert, 2);
    insert_r = insert_radii(5-idx_insert); %due to matlab coordinate system, the order is reversed.
    crop_r = ceil(3*max(insert_radii));
    % get roi
    sp_crop_xfov = center_x + [-crop_r:crop_r]; %signal present crop xfov
    sp_crop_yfov = center_y + [-crop_r:crop_r];
    roi_nx = 2*crop_r + 1;

    nroi = 5;
    sa_crop_xfov = zeros(nroi, roi_nx);
    sa_crop_yfov = sa_crop_xfov;
    sa_center_x = [center_x center_x center_x center_x-crop_r center_x+crop_r];
    sa_center_y = [center_y-crop_r center_y center_y+crop_r center_y center_y];
    for i=1:nroi
        sa_crop_xfov(i,:) = sa_center_x(i) + [-crop_r:crop_r];
        sa_crop_yfov(i,:) = sa_center_y(i) + [-crop_r:crop_r];
    end
    %check roi
    fid = fopen('/gpfs_projects/rxz4/data/DLCT/phantom_sim/for_CT2020Conf/cct189/true.raw')
    % fid = fopen('/raida/rpz/data/DLCT/phantom_sim/for_CT2020Conf/cct189/true.raw');
    xtrue = fread(fid,[nx nx],'int16');
    fclose(fid);
    figure(1); imagesc(xtrue(sp_crop_xfov, sp_crop_yfov));

    actual_insert_HU = xtrue(center_x, center_y)
    if(actual_insert_HU ~= insert_info(idx_insert, 4))
        disp('Warning: geometric mismatch! Quit.')
        return;
    end

    n_sp = n_spfile;
    n_sa = n_safile*nroi;


    for iI = 1:n_I0
        iI
        I0 = I0_vector(iI);
        
        for k=1:n_recon_option
            %% read data
            recon_option = all_recon_type{k};

            I0_string = ['I0_' sprintf('%07d', I0) ];
            folder_sp = [data_folder I0_string  '/' recon_option '/disk/'];
            folder_sa = [data_folder I0_string '/' recon_option '/bkg/'];
            if(strfind(recon_option, 'dl'))
                id_underscore = strfind(recon_option,'_');
                fbp_string = recon_option(1:id_underscore(2)-1);
                dl_string = [recon_option(id_underscore(3)+1:end) 'M1-R0-S3'];
                folder_sp = [proc_data_folder I0_string  '/' fbp_string '/disk/' dl_string '/'];
                folder_sa = [proc_data_folder I0_string  '/' fbp_string '/bkg/' dl_string '/'];
            end

            sp_img = zeros(nx, nx, n_spfile);
            sp_roi = zeros(roi_nx,roi_nx, n_sp);
            for i=1:n_spfile
                filenum = i;
                filenum_string = ['v' sprintf('%03d', filenum)];
                filename = [folder_sp recon_option '_' filenum_string '.raw'];
                if(strfind(recon_option, 'dl'))
                    filename = [folder_sp fbp_string '_' filenum_string '_' dl_string 'proc.raw'];
                end
                fid = fopen(filename);
                
                im_current = fread(fid, [nx, nx], 'int16');
                img = im_current;
                fclose(fid);
                sp_img(:,:,i) = img;
                img_crop = img(sp_crop_xfov, sp_crop_yfov);
                sp_roi(:,:,i) = img_crop - mean(img_crop(:));
            end

            sa_img = zeros(nx,nx,n_safile);
            sa_roi = zeros(roi_nx,roi_nx, n_sa);
            for i=1:n_safile
                filenum = i;
                filenum_string = ['v' sprintf('%03d', filenum)];
                filename = [folder_sa recon_option '_' filenum_string '.raw'];
                if(strfind(recon_option, 'dl'))
                    filename = [folder_sa fbp_string '_' filenum_string '_' dl_string 'proc.raw'];
                end
                fid = fopen(filename);
                im_current = fread(fid, [nx, nx], 'int16');
                img = im_current;
                fclose(fid);
                sa_img(:,:,i) = img;    
                for j=1:5
                    img_crop = img(sa_crop_xfov(j,:), sa_crop_yfov(j,:));
                    sa_roi(:,:,(i-1)*5+j) = img_crop - mean(img_crop(:));
                end
            end
            for i=1:n_reader
                % shuffle training data
                idx_sa1 = randperm(n_sa);
                idx_sp1 = randperm(n_sp);

                idx_sa_tr = idx_sa1(1:n_train);
                idx_sp_tr = idx_sp1(1:n_train);
                idx_sa_test = idx_sa1(n_train+1:end);
                idx_sp_test = idx_sp1(n_train+1:end);

                % run LG CHO
                [auc(i), snr(i), chimg, tplimg, meanSP, meanSA, meanSig, kch, t_sp, t_sa] = ...
                    conv_LG_CHO_2d(sa_roi(:, :, idx_sa_tr), sp_roi(:, :, idx_sp_tr), ...
                    sa_roi(:, :, idx_sa_test), sp_roi(:, :, idx_sp_test), insert_r/1.5, 5, 0);
                auc_all(idx_insert, k, iI, i) = auc(i);
                snr_all(idx_insert, k, iI, i) = snr(i);
                if auc(i) == 0
                    error(sprintf('0 auc at lesion %d, I0 %d, recon %d, reader %d', idx_insert, iI, k, i))
                end
            end
        end
    end
end

results_fname = [outfolder filesep 'test_results.h5']
hdf5write(results_fname, '/auc', auc_all);
hdf5write(results_fname, '/recon_types', all_recon_type, 'WriteMode', 'append');
hdf5write(results_fname, '/readers', n_reader, 'WriteMode', 'append');
hdf5write(results_fname, '/dose_levels', I0_vector, 'WriteMode', 'append');
hdf5write(results_fname, '/snr', snr_all, 'WriteMode', 'append');
