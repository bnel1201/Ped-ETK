%LCD test

%%Data inputs
all_recon_type = {'lcd/fbp_sharp','lcd/fbp_smooth','lcd_proc/fbp_sharp', 'lcd_proc/fbp_smooth'};

I0_vector = 4e5*[10 20 30 40 50 60]/100; %added 20% and 25%, can remove 60% 75% 100%
%I0 = I0_vector(1);%6e5*0.6;;
n_spfile = 200;
n_safile = 100;
n_reader = 10;
n_train = 120;
n_I0 = length(I0_vector);

%%inserts info
nx = 320;%256;
dx = 0.664; %PixelSpacing
fov = dx*nx;  
d = 40;     % mm
% insert_info [x_center, y_center, r, HU]
insert_info = [...
    d*cosd(45)  d*sind(45)    7/2  10;      % 7 mm, 10 HU
    -d*cosd(45)  d*sind(45)   7/2   10;      % 7 mm, 10 Hu
    -d*cosd(45) -d*sind(45)   7/2   15;      % 7 mm, 15 HU
    d*cosd(45) -d*sind(45)   7/2   15;      % 7 mm, 15 HU
    ];
num_inserts = size(insert_info, 1);

% convert roi locations from mm to pixels
insert_centers = round(insert_info(:,1:2) * (nx/fov) + (nx+1)/2);
insert_radii = insert_info(:,3) / dx;
% % select insert
% center_x = insert_centers(idx_insert, 1);
% center_y = nx-insert_centers(idx_insert, 2);
% insert_r = insert_radii(5-idx_insert); %due to matlab coordinate system, the order is reversed.
% crop_r = ceil(3*max(insert_radii));
% get roi
sp_crop_xfov = center_x + [-crop_r:crop_r];
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
fid = fopen('/raida/rpz/data/DLCT/phantom_sim/tv_sart/CCT189/true.raw');
xtrue = fread(fid,[nx nx],'int16');
fclose(fid);
figure(1); imagesc(xtrue(sp_crop_xfov, sp_crop_yfov));
actual_insert_HU = xtrue(center_x, center_y)
if(actual_insert_HU ~= insert_info(idx_insert, 4))
    disp('Warning: geometric mismatch! Quit.')
    return;
end


n_recon_option = length(all_recon_type);
n_sp = n_spfile;
n_sa = n_safile*nroi;

auc_all = zeros(n_reader, n_recon_option, n_I0);

for iI = 1:n_I0
    iI
    I0 = I0_vector(iI);
    
    for k=1:n_recon_option
        %% read data
        recon_option = all_recon_type{k};

        I0_string = ['I0_' sprintf('%07d', I0) ];
        folder_sp = ['/raida/rpz/data/DLCT/phantom_sim/tv_sart/CCT189/' I0_string  '/' recon_option '/'];
        folder_sa = ['/raida/rpz/data/DLCT/phantom_sim/tv_sart/uniform/' I0_string '/' recon_option '/'];
        if(strcmp(recon_option, 'mbir'))
            folder_sp = ['/raida/rpz/data/DLCT/phantom_sim/tv_sart/CCT189/' I0_string  '/' recon_option '_iter6/'];
            folder_sa = ['/raida/rpz/data/DLCT/phantom_sim/tv_sart/uniform/' I0_string '/' recon_option '_iter6/'];
        end
        
        
        prefix_cct189 = ['CCT189_' recon_option '_' I0_string '_'];
        prefix_water = ['water_' recon_option '_' I0_string '_'];
        if (strcmp(recon_option, 'cnn3') | strcmp(recon_option, 'redcnn'))
            prefix_cct189 = ['CCT189_' 'fbp_ramp' '_' I0_string '_'];
            prefix_water = ['water_' 'fbp_ramp' '_' I0_string '_'];
            suffix = '_proc';
        else
            suffix = '';
        end

        sp_img = zeros(nx, nx, n_spfile);
        sp_roi = zeros(roi_nx,roi_nx, n_sp);
        for i=1:n_spfile
            filenum = i;
            filenum_string = ['v' sprintf('%03d', filenum)];
            filename = [folder_sp prefix_cct189 filenum_string suffix '.raw'];
            fid = fopen(filename);
            

%             if(strcmp(recon_option,'mbir'))
%                 im_current = fread(fid, 'int16');
%                 im_current = reshape(im_current,[nx nx 6]);
%                 img = im_current(:,:,6);
%             else
                im_current = fread(fid, [nx, nx], 'int16');
                img = im_current;
%            end
            %img = fread(fid,[nx nx],'int16')';
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
            filename = [folder_sa prefix_water filenum_string suffix '.raw'];
            fid = fopen(filename);
%             if(strcmp(recon_option,'mbir'))
%                 im_current = fread(fid, 'int16');
%                 im_current = reshape(im_current,[nx nx 6]);
%                 img = im_current(:,:,6);
%             else
                im_current = fread(fid, [nx, nx], 'int16');
                img = im_current;
%            end
            %img = fread(fid,[nx nx],'int16')';
            fclose(fid);
            sa_img(:,:,i) = img;    
            for j=1:5
                img_crop = img(sa_crop_xfov(j,:), sa_crop_yfov(j,:));
                sa_roi(:,:,(i-1)*5+j) = img_crop - mean(img_crop(:));
            end
        end

        %%detection

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

          end
        auc_all(:,k,iI) = auc;
        snr_all(:,k,iI) = snr;
    end
end
