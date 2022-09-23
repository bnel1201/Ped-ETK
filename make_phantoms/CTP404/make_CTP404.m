% make_CTP404.m
% Author: Brandon Nelson, Rongping Zeng
% date: September 4, 2022
%
% Purpose: To simulate traditional IQ phantom similar to the CTP404 
% layer in the Catphan 600. Match the reconstruction kernel D45 
% and B30in the Siemens CT scanner, which have MTF50% of 5.6 lp/cm and 3.5 lp/cm, 
% MTF10% of 9.4 and 5.9 lp/cm, with Hann205 and Hann85. My measurement show that
% Hann205 and Hann85 has mtf50% of 5.6 lp/cm and 3.5 lp/cm, mtf10% of 10.4 lp/cm and
% 6.2 lp/cm. They matches pretty well the commercial filters.

% Derived from </home/rxz4/ct_deeplearning/make_phantom/make_CTP189_wD45_B30.m>

% Run path setup

%% Set parameters
run('../configs/SiemensSomatomDefinitionAS.m')

run('../utils/setup.m')

sg = sino_geom('fan', 'units', 'mm', ...
    'nb', nb, 'na', na, 'ds', ds, ...
    'dsd', sdd, 'dod', dod, 'offset_s', offset_s, ...
    'down', down);

sampleFolder = [basedataFolder 'CTP404/']
if ~exist(sampleFolder, 'dir')
    mkdir(sampleFolder)
end
physics_type_folder = [sampleFolder 'monochromatic/'];
if ~exist(physics_type_folder, 'dir')
    mkdir(physics_type_folder)
end

mu_water = 0.2059 / 10;     % in mm-1

aec_factors = exp(mu_water*patient_diameters)./exp(mu_water*patient_diameters(1));

for idx=1:length(patient_diameters)
    patient_diameter = patient_diameters(idx)
    fov = 1.1*patient_diameter
    aec_factor = aec_factors(idx);

    ig = image_geom('nx', nx, 'fov', fov, 'down', down);

    patient_folder = [physics_type_folder '/diameter' num2str(patient_diameter) 'mm/']
    if exist(patient_folder, 'dir') == false
        mkdir(patient_folder)
    end

    for I0=I0_vector
        I0_string = ['I0_' sprintf('%07d', I0)];

        files_sharp = [patient_folder I0_string '/fbp_sharp/'];

        if(~exist(files_sharp,'dir'))
            mkdir(files_sharp);
        end

        relative_lesion_diameter = 0.08;
        relative_lesion_location = 0.38;

        ell = CTP404(patient_diameter, mu_water, relative_lesion_diameter, relative_lesion_location);
        x_true = ellipse_im(ig, ell, 'oversample', 4, 'rot', 0);
        x_true_hu = 1000*(x_true - mu_water)/mu_water + offset;
        filename = [patient_folder  filesep 'true.raw'];
        write_phantom_info([patient_folder filesep 'phantom_info_mm.csv'], ell);
        write_phantom_info([patient_folder filesep 'phantom_info_pix_idx.csv'], ellipse_mm_to_pix(ell, fov, nx));
        ii.offset = offset;
        write_image_info([patient_folder filesep 'image_info.csv'], ii);
        write_geometry_info([patient_folder filesep 'geometry_info.csv'], ig);
        if ~exist(filename, 'file')
            my_write_rawfile(filename, x_true_hu, 'int16');
        end

        % Get sinogram
        sino = ellipse_sino(sg, ell, 'oversample', 4);

        % FBP reconstruction operator
        fg = fbp2(sg, ig,'type','std:mat'); %choose 'std:mat' to be able to using different recon filter
                                            %default would be 'std:mex' but only ramp filter was implemented in it
        if aec_on
            I0 = aec_factor*I0; %accounts for different patient size
        end

        if has_bowtie
            I0_afterbowtie=apply_bowtie_filter(I0, sg, mu_water, patient_diameter);           
        else
            I0_afterbowtie=I0;            
        end        
        proj = I0_afterbowtie .* exp(-sino);
        for isim = batch      
            isim
            if add_noise     
                proj = poisson(proj); %This poisson generator respond to the seed number setby rand('sate',x');
            end

            proj = replace_zeros(proj);

            sino_log = -log(proj ./ I0_afterbowtie);            % noisy fan-beam sinogram

            x_fbp_sharp = fbp2(sino_log, fg, 'window', 'hann205');
            x_fbp_sharp_hu = 1000*(x_fbp_sharp - mu_water)/mu_water + offset;
            file_prefix = [files_sharp 'fbp_sharp_'];
            file_num = isim;
            filename_fbp_sharp = [file_prefix 'v' sprintf('%03d', file_num) '.raw'];
            my_write_rawfile(filename_fbp_sharp, x_fbp_sharp_hu, 'int16');
        end
    end
end
