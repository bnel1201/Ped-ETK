addpath('/home/brandon.nelson/Dev/PhantomSimulations/CT_simulator')
if ~exist('homedir', 'var') %checks if setpath has been run
    setpath
end

addpath([dirname(fileparts(mfilename('fullpath')), 2) '/utils'])
diameter_dirs = dir(base_data_folder); diameter_dirs=diameter_dirs(3:end)

%%inserts info
insert_info = read_phantom_info(fullfile(base_data_folder, diameter_dirs(1).name, 'phantom_info_pix_idx.csv'));
insert_info(:, end) = insert_info(:, end)/insert_info(1, end)*1000; insert_info = insert_info(2:end, [1 2 3 6]);
num_inserts = size(insert_info, 1);
n_recon_option = 2;
if ~exist('I0_vector', 'var')
    I0_vector = 3e5;
end
n_diameters = length(diameter_dirs)

inserts_list = round(insert_info(:, 4))

n_reader = 10;
train_proportion = 0.5; %what proportion of data is to be saved for training [0, 1]
I0_dirs = dir(fullfile(diameter_dirs(1).folder, diameter_dirs(1).name, '/I0_*0'))
n_I0 = length(I0_dirs)
% n_I0 = length(I0_vector);
auc_all = zeros(n_diameters, num_inserts, n_recon_option, n_I0, n_reader);
snr_all = zeros(n_diameters, num_inserts, n_recon_option, n_I0, n_reader);

for diam_idx=1:n_diameters
    diameter_dir=diameter_dirs(diam_idx).name;
    diameter = regexp(diameter_dir, '\d+', 'match'); diameter = str2num(diameter{:});
    diameters_list(diam_idx) = diameter;

    I0_dirs = dir(fullfile(diameter_dirs(diam_idx).folder, diameter_dirs(diam_idx).name, '/I0_*0'))
    % n_I0 = length(I0_dirs)

    data_folder = fullfile(base_data_folder, diameter_dir);

    insert_info = read_phantom_info([data_folder '/phantom_info_pix_idx.csv']);
    insert_info(:, end) = insert_info(:, end)/insert_info(1, end)*1000; insert_info = insert_info(2:end, [1 2 3 6]);
    loc = insert_info(2:end-1, 1:2);

    ig = read_geometry_info([data_folder '/geometry_info.csv']);
    nx = ig.nx;
    dx = ig.dx;
    fov = ig.fov;

    vox_size(diam_idx) = dx;
    fov_size(diam_idx) = fov;

    ii = importdata([data_folder '/image_info.csv']);
    offset = ii.data;

    for iI = 1:n_I0
        I0 = str2num(I0_dirs(iI).name(4:end))
        I0_vector(iI) = I0;
        for k=1:n_recon_option
            %% read data
            recon_option = all_recon_type{k};

            % I0_string = ['I0_' sprintf('%07d', I0) ];
            I0_string = I0_dirs(iI).name
            folder_sp = fullfile(data_folder, I0_string, 'disk')
            folder_sa = fullfile(data_folder, I0_string, 'bkg')

            if(strfind(recon_option, 'dl'))
                I0_string = [I0_string '_processed'];
                folder_sp = fullfile(data_folder, I0_string, 'disk')
                folder_sa = fullfile(data_folder, I0_string, 'bkg')
            end
            n_spfile = length(dir(folder_sp)) - 2; % number signal present file
            n_safile = length(dir(folder_sa)) - 2; % number signal absent file

            for idx_insert=1:num_inserts
                % convert roi locations from mm to pixels (check these values against phantom_info_pix.csv)
                insert_centers = round(insert_info(:,1:2));
                insert_radii = insert_info(:,3);
                % select insert
                center_x = insert_centers(idx_insert, 1);
                center_y = nx - insert_centers(idx_insert, 2) + 1;
                insert_r = insert_radii(idx_insert); %due to matlab coordinate system, the order is reversed.
                crop_r = ceil(3*max(insert_radii));
                % get roi
                sp_crop_xfov = center_x + [-crop_r:crop_r]; %signal present crop xfov
                sp_crop_yfov = center_y + [-crop_r:crop_r];
                roi_nx = 2*crop_r + 1;

                sa_center_x = [center_x center_x center_x center_x-crop_r center_x+crop_r];
                sa_center_y = [center_y-crop_r center_y center_y+crop_r center_y center_y];
                nroi = length(sa_center_x);
                sa_crop_xfov = zeros(nroi, roi_nx);
                sa_crop_yfov = zeros(nroi, roi_nx);
                for i=1:nroi
                    sa_crop_xfov(i,:) = sa_center_x(i) + [-crop_r:crop_r];
                    sa_crop_yfov(i,:) = sa_center_y(i) + [-crop_r:crop_r];
                end
                %check roi
                true_fname = fullfile(data_folder, 'true_disk.raw');
                fid = fopen(true_fname);
                xtrue = fread(fid,[nx nx],'int16') - offset;
                fclose(fid);
                
                expected_HU = round(insert_info(idx_insert, 4));
                expected_area = pi*insert_r^2;
                true_roi = xtrue(sp_crop_xfov, sp_crop_yfov);
                measured_roi = true_roi(true_roi >= expected_HU/2);
                measured_area = numel(measured_roi);
                area_error = measured_area - expected_area;
                if abs(area_error) > 10 % fix phantom such that this area is under 17
                    error('Error: Measured ROI area does not agree with expected value!')
                end
                rel_area_error = abs(area_error)/expected_area;
                if abs(area_error)/expected_area > 0.1
                    error('Error: Measured ROI area does not agree with expected value!')
                end
                measured_HU = mean(measured_roi);
                HU_error = measured_HU - expected_HU;
                if abs(HU_error) > 4
                    error('Error: Measured ROI HU does not match expected!')
                end

                actual_insert_HU = xtrue(center_x, center_y);
                if actual_insert_HU ~= expected_HU
                    error('Warning: geometric mismatch! Quit.')
                end

                measured_HU = mean(circle_roi(xtrue, center_x, center_y, insert_r));
                HU_error = measured_HU - expected_HU;
                if abs(HU_error) > 4
                    error('Error: True disk HU does not match expected!')
                end

                measured_area = numel(circle_roi(xtrue, center_x, center_y, insert_r));
                area_error = measured_area - expected_area;
                if abs(area_error) > 5
                    error('Error: True ROI area does not agree with expected value!')
                end

                n_sp = n_spfile;
                n_sa = n_safile*nroi;
                n_train = n_spfile*train_proportion;

                sp_img = zeros(nx, nx, n_spfile);
                sp_roi = zeros(roi_nx, roi_nx, n_sp);
                for i=1:n_spfile
                    filenum = i;
                    filenum_string = ['v' sprintf('%03d', filenum)];
                    filename = fullfile(folder_sp, ['fbp_sharp' '_' filenum_string '.raw']);

                    fid = fopen(filename);
                    im_current = fread(fid, [nx, nx], 'int16') - offset;
                    img = im_current;
                    fclose(fid);
                    sp_img(:,:,i) = img;
                    img_crop = img(sp_crop_xfov, sp_crop_yfov);
                    sp_roi(:,:,i) = img_crop - mean(img_crop(:));
                end

                sa_img = zeros(nx, nx, n_safile);
                sa_roi = zeros(roi_nx, roi_nx, n_sa);
                for i=1:n_safile
                    filenum = i;
                    filenum_string = ['v' sprintf('%03d', filenum)];
                    filename = fullfile(folder_sa, ['fbp_sharp' '_' filenum_string '.raw']);

                    fid = fopen(filename);
                    im_current = fread(fid, [nx, nx], 'int16') - offset;
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

                    [auc(i), snr(i), chimg, tplimg, meanSP, meanSA, meanSig, kch, t_sp, t_sa] = ...
                        conv_LG_CHO_2d(sa_roi(:, :, idx_sa_tr), sp_roi(:, :, idx_sp_tr), ...
                        sa_roi(:, :, idx_sa_test), sp_roi(:, :, idx_sp_test), insert_r/1.5, 5, 0);
                    auc_all(diam_idx, idx_insert, k, iI, i) = auc(i);
                    snr_all(diam_idx, idx_insert, k, iI, i) = snr(i);
                    if auc(i) == 0
                        error(sprintf('0 auc at lesion %d, I0 %d, recon %d, reader %d', idx_insert, iI, k, i))
                    end
                end
                
                figure(1);
                set(gcf,'Position',[100 100 800 800])
                ax1 = subplot(2, 2, 1);
                imagesc(xtrue, [-2, 15]); colormap(ax1, gray); axis image;
                rectplot(center_x, center_y, insert_r);
                title(['expected: ' num2str(expected_HU) 'HU / measured: ' num2str(measured_HU,1) 'HU'])
                ax2 = subplot(2, 2, 2);
                imagesc(meanSP, [-2 15]); colormap(ax2, gray); axis image;
                title(['Mean SP, AUC:' num2str(auc(i),3)])
                ax3 = subplot(2, 2, 3);
                imagesc(tplimg,[0, max(tplimg(:))]); colormap(ax3, hot(256)); axis image;
                title('Learned MO Template')
                ax4 = subplot(2, 2, 4);
                ha = imagesc(true_roi,[-2 15]); colormap(ax4, gray(256)); axis image;
                hold on; hb = imagesc(tplimg,[0 max(tplimg(:))]); colormap(ax4, hot(256)); hb.AlphaData=0.4; hold off
                title('Template Overlay on Truth ROI')
                if strcmp(recon_option, 'fbp') & I0 == I0_vector(1) & fov > 200 & fov < 237
                    debug_img_dir = [outfolder '/' 'MO_template_assessment' '/' recon_option '/' num2str(I0) '/' num2str(fov,3)];
                    if ~exist(debug_img_dir, 'dir'); mkdir(debug_img_dir); end
                    debug_img_fname = [debug_img_dir filesep num2str(expected_HU) '.png']
                    saveas(gcf, debug_img_fname)
                end
            end
        end
    end
end

results_fname = [outfolder filesep 'LCD_results.h5']
hdf5write(results_fname, '/auc', auc_all);
hdf5write(results_fname, '/recon_types', all_recon_type, 'WriteMode', 'append');
hdf5write(results_fname, '/readers', n_reader, 'WriteMode', 'append');
hdf5write(results_fname, '/dose_levels', I0_vector, 'WriteMode', 'append');
hdf5write(results_fname, '/patient_diameters', diameters_list, 'WriteMode', 'append');
hdf5write(results_fname, '/insert_HUs', inserts_list, 'WriteMode', 'append');
hdf5write(results_fname, '/insert_radii_pix', insert_radii, 'WriteMode', 'append');
hdf5write(results_fname, '/vox_size_mm', vox_size, 'WriteMode', 'append');
hdf5write(results_fname, '/fov_size_mm', fov_size, 'WriteMode', 'append');
hdf5write(results_fname, '/snr', snr_all, 'WriteMode', 'append');
