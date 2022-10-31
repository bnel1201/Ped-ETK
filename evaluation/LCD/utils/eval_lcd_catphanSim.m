addpath('/home/brandon.nelson/Dev/PhantomSimulations/CT_simulator')
if ~exist('homedir', 'var') %checks if setpath has been run
    setpath
end

addpath([dirname(fileparts(mfilename('fullpath')), 2) '/utils'])

%%inserts info
insert_info = read_phantom_info(fullfile(base_data_folder, 'diameter112mm', 'phantom_info_pix_idx.csv'));
insert_info(:, end) = insert_info(:, end)/insert_info(1, end)*1000; insert_info = insert_info(2:end, [1 2 3 6]);
num_inserts = size(insert_info, 1);
n_recon_option = 2;
if ~exist('I0_vector', 'var')
    I0_vector = 3e5;
end
diameter_dirs = dir(base_data_folder); diameter_dirs=diameter_dirs(3:end)
n_diameters = length(diameter_dirs)

inserts_list = round(insert_info(:, 4))

n_reader = 10;
n_train = 100;
n_I0 = length(I0_vector);
auc_all = zeros(n_diameters, num_inserts, n_recon_option, n_I0, n_reader);
snr_all = zeros(n_diameters, num_inserts, n_recon_option, n_I0, n_reader);

for diam_idx=1:n_diameters
    diameter_dir=diameter_dirs(diam_idx).name;
    diameter = regexp(diameter_dir, '\d+', 'match'); diameter = str2num(diameter{:});
    diameters_list(diam_idx) = diameter;

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
        I0 = I0_vector(iI);
        for k=1:n_recon_option
            %% read data
            recon_option = all_recon_type{k};

            I0_string = ['I0_' sprintf('%07d', I0) ];
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
                center_x = nx - insert_centers(idx_insert, 2) + 1;
                center_y = insert_centers(idx_insert, 1);
                insert_r = insert_radii(idx_insert); %due to matlab coordinate system, the order is reversed.
                crop_r = ceil(3*max(insert_radii));
                % get roi
                sp_crop_yfov = center_x + [-crop_r:crop_r]; %signal present crop xfov
                sp_crop_xfov = center_y + [-crop_r:crop_r];
                roi_nx = 2*crop_r + 1;

                sa_center_x = [center_x center_x center_x center_x-crop_r center_x+crop_r];
                sa_center_y = [center_y-crop_r center_y center_y+crop_r center_y center_y];
                nroi = length(sa_center_x);
                sa_crop_xfov = zeros(nroi, roi_nx);
                sa_crop_yfov = zeros(nroi, roi_nx);
                for i=1:nroi
                    sa_crop_yfov(i,:) = sa_center_x(i) + [-crop_r:crop_r];
                    sa_crop_xfov(i,:) = sa_center_y(i) + [-crop_r:crop_r];
                end
                %check roi
                true_fname = fullfile(data_folder, 'true_disk.raw');
                fid = fopen(true_fname);
                xtrue = fread(fid,[nx nx],'int16') - offset;
                fclose(fid);
                
% %                 title("expected: "+num2str(expected_HU)+"HU / measured: "+num2str(measured_HU)+"HU")
                % figure(1); imshow(xtrue, [0 15]);
                
                expected_HU = round(insert_info(idx_insert, 4));
                expected_area = pi*insert_r^2;
                true_roi = xtrue(sp_crop_xfov, sp_crop_yfov);
                measured_roi = true_roi(true_roi >= expected_HU/2);
                measured_area = numel(measured_roi);
                area_error = measured_area - expected_area;
                if abs(area_error) > 10 % fix phantom such that this area is under 17
                    error("Error: Measured ROI area does not agree with expected value!")
                end
                rel_area_error = abs(area_error)/expected_area;
                if abs(area_error)/expected_area > 0.05
                    error("Error: Measured ROI area does not agree with expected value!")
                end
                measured_HU = mean(measured_roi);
                HU_error = measured_HU - expected_HU;
                if abs(HU_error) > 4
                    error("Error: Measured ROI HU does not match expected!")
                end

                actual_insert_HU = xtrue(center_y, center_x);
                if actual_insert_HU ~= expected_HU
                    disp('Warning: geometric mismatch! Quit.')
                    return;
                end

                measured_HU = mean(circle_roi(xtrue, center_x, center_y, insert_r));
                HU_error = measured_HU - expected_HU;
                if abs(HU_error) > 4
                    error("Error: True disk HU does not match expected!")
                end

                measured_area = numel(circle_roi(xtrue, center_x, center_y, insert_r));
                area_error = measured_area - expected_area;
                if abs(area_error) > 5
                    error("Error: True ROI area does not agree with expected value!")
                end

                n_sp = n_spfile;
                n_sa = n_safile*nroi;

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
                    filename = fullfile(folder_sp, ['fbp_sharp' '_' filenum_string '.raw']);

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

                    % run LG CHO
                    if string(recon_option) == "fbp" && I0 == 300000 && fov > 200
                        disp('stop here')
                    end
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
                set(gcf,'Position',[100 100 750 750])
                subplot(2, 2, 1)
                disp('stop here')
                imshow(xtrue, [-2, 15]);
                rectplot(center_x, center_y, insert_r);
                title("expected: "+num2str(expected_HU)+"HU / measured: "+num2str(round(measured_HU,1))+"HU")
                subplot(2, 2, 2)
                imshow(meanSP, [-2 15]);
                title("Mean SP, AUC:" + num2str(auc(i),3))
                subplot(2, 2, 3)
                imshow(tplimg,[0, max(tplimg(:))], 'Colormap', hot(256))
                title("Learned MO Template")
                subplot(2, 2, 4)
                ha = imshow(true_roi,[-2 15], 'Colormap', gray(256));
                hold on; hb = imshow(tplimg,[0 max(tplimg(:))], 'Colormap', hot(256)); hb.AlphaData=0.4; hold off
                title("Template Overlay on Truth ROI")
                if string(recon_option) == "fbp" && I0 == 300000 && fov > 200
                    saveas(gcf, "debug/bjn/lcd_"+num2str(expected_HU)+".png")
                end
                % figure(1); imshow(meanSA, [])
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
