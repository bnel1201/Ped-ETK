% make_phantom_sims.m
% Author: Brandon Nelson, Rongping Zeng
% date: August 1, 2022

% Purpose: To simulate the MITA LCD body phantom CCT189 and a uniform phantom. This generates 
% multiple noise realization for a range of noise levels, specified by
% 'I0_vector'.
%
% Derived from </home/rxz4/ct_deeplearning/make_phantom/make_CCT189_wD45_B30.m>
% which was written by Sarah Divel & Rongping Zeng
% Date: July 23, 2018

% Run path setup
run('/home/brandon.nelson/Dev/DLIR_Ped_Generalizability/geomtric_phantom_studies/make_phantoms/configs/SiemensSomatomDefinitionAS.m')

run('/home/brandon.nelson/Dev/DLIR_Ped_Generalizability/geomtric_phantom_studies/make_phantoms/utils/setup.m') % need to double check that this isn't overwriting anything from the base config

% base_dir = '/gpfs_projects/brandon.nelson/DLIR_Ped_Generalizability/anthropomorphic_phantom_studies/main';
% phantom_dir = fullfile(base_dir, 'phantoms')
% patient = 'male_infant_ref_atn_1'

patient_filename = fullfile(phantom_dir, [patient '.bin']);
nslices = 1;
nx=715;
fid = fopen(patient_filename,'r'); img = reshape(fread(fid,[nx, nx*nslices], 'single'), nx, nx, nslices); fclose(fid);
slice_num = 1;
phantom = img(:,:,slice_num);

sg = sino_geom('fan', 'units', 'mm', ...
    'nb', nb, 'na', na, 'ds', ds, ...
    'dsd', sdd, 'dod', dod, 'offset_s', offset_s, ...
    'down', down);

basedataFolder = fullfile(base_dir, 'simulations');
sampleFolder = fullfile(basedataFolder, patient)
if ~exist(sampleFolder, 'dir')
    mkdir(sampleFolder)
end
physics_type_folder = fullfile(sampleFolder, 'monochromatic/');
if ~exist(physics_type_folder, 'dir')
    mkdir(physics_type_folder)
end

mu_water = 0.007263; %figure out why there is a disagreement between atten_table.dat and the generated phantoms mu_water = 0.2059 / 10;     % in mm-1
if ~exist('reference_diameter', 'var')
    reference_diameter = 200; % in mm, from /home/rxz4/ct_deeplearning/make_phantom/make_CCT189_wD45_B30.m line 81
end
if ~any(patient_diameters == reference_diameter)
    patient_diameters = [reference_diameter patient_diameters]
end
if ~exist('reference_fov', 'var')
    reference_fov = 340
end

aec_factors = exp(mu_water*patient_diameters)./exp(mu_water*reference_diameter);
ndiams = 1; 
for diam_idx=1:ndiams
    patient_diameter = patient_diameters(diam_idx);
    fov = reference_fov;
%     if patient_diameter == reference_diameter
%         fov = reference_fov;
%         % patient_folder = [physics_type_folder '/reference_diameter' num2str(patient_diameter) 'mm/']
%     else
%         fov = 1.1*patient_diameter;
%     end
    patient_folder = physics_type_folder;
    aec_factor = aec_factors(diam_idx);
    ig = image_geom('nx', nx, 'fov', fov, 'down', down);
    A = Gtomo2_dscmex(sg, ig);
    sino = A*phantom;

    close all;
    sg.plot(ig)
    hold off; titlef('Scanner FOV = %g mm, Recon FOV = %g mm', round(2*sg.rfov), round(fov)); hold on;
    saveas(gca, fullfile(patient_folder, 'image_geometry.png'))

    for I0=I0_vector
        I0_string = ['I0_' sprintf('%07d', I0)];

        files_disk = [patient_folder I0_string '/fbp_sharp/'];
        if ~exist(files_disk, 'dir')
            mkdir(files_disk);
        end
        % FBP reconstruction operator
        ig = image_geom('nx', 512, 'fov', fov, 'down', down);
        fg = fbp2(sg, ig,'type','std:mat'); %choose 'std:mat' to be able to using different recon filter
                                            %default would be 'std:mex' but only ramp filter was implemented in it
        if aec_on
            I0 = aec_factor*I0; %accounts for different patient size
        end

        if has_bowtie
            I0_afterbowtie=apply_bowtie_filter(I0, sg, mu_water, patient_diameter);           
        else
            I0_afterbowtie=I0*0.2;            
        end

        proj_noisefree = I0_afterbowtie .* exp(-sino);

        nx=512;
        ig = image_geom('nx', nx, 'fov', fov, 'down', down);
        atten_true = imresize(phantom, [nx nx], 'bicubic');
        fbp_hu = 1000*(atten_true - mu_water)/mu_water + offset;
        my_write_rawfile(fullfile(patient_folder, 'true.raw'), fbp_hu, 'int16');
        
        atten_fbp = fbp2(sino, fg, 'window', 'hann205');
        fbp_hu = 1000*(atten_fbp - mu_water)/mu_water + offset;
        my_write_rawfile(fullfile(patient_folder, 'noise_free.raw'), fbp_hu, 'int16');

        write_geometry_info([patient_folder filesep 'geometry_info.csv'], ig);

        for sim_idx = batch
            total_idx = sim_idx+(diam_idx-1)*nsims;
            total_sim = ndiams*nsims;
            disp(sprintf('%s, diameter: %dmm (FOV: %dmm) [%d/%d], simulation: [%d/%d], Total: %3.2f%% [%d/%d]', mfilename, patient_diameter, round(fov), diam_idx, ndiams, sim_idx, nsims, total_idx/total_sim*100, total_idx, total_sim))
            if add_noise   
                proj = poisson(proj_noisefree); %This poisson generator respond to the seed number setby rand('sate',x');
            else
                proj = disk_proj_noisefree;
            end

            proj = replace_zeros(proj);
            sino_log = -log(proj ./ I0_afterbowtie);            % noisy fan-beam sinogram

            atten_fbp = fbp2(sino_log, fg, 'window', 'hann205');
            fbp_hu = 1000*(atten_fbp - mu_water)/mu_water + offset;

            file_prefix = [files_disk 'fbp_sharp_'];
            file_num = sim_idx;
            filename_disk_fbp = [file_prefix 'v' sprintf('%03d', file_num) '.raw'];
            my_write_rawfile(filename_disk_fbp, fbp_hu, 'int16');
        end
    end
end
