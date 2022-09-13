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

addpath('/home/brandon.nelson/Dev/PhantomSimulations/CT_simulator')
if exist('homedir', 'var') == false %checks if setpath has been run
    setpath
end
addpath('./utils')
addpath('./configs')
if exist('max_dose_level', 'var') == false
    max_dose_level = 3e6
end
I0_vector = max_dose_level; %[30 55 70 85 100]/100;

if exist('patient_diameters', 'var') == false
    patient_diameters = [112, 131, 151, 185, 216, 292]; %newborn, 8 yr-old, 18 year old
end

if exist('nsims', 'var') == false
    nsims = 5
end

if exist('aec_on', 'var') == false
    aec_on = true;
end

if exist('add_noise', 'var') == false
    add_noise = true;
end

batch = 1:nsims;
rand('state', batch(end));
% Set save folder
if exist('basedataFolder', 'var') == false
    basedataFolder = '/home/brandon.nelson/Data/temp/'; %temporary until /gpfs_projects gets fixed then switch back to above^^^ 
end
sampleFolder = [basedataFolder 'CTP404/']
if exist(sampleFolder, 'dir') == false
    mkdir(sampleFolder)
end

%% Set parameters
% ------ Scan Parameters ------
SiemensSomatomDefinitionAS

sg = sino_geom('fan', 'units', 'mm', ...
    'nb', nb, 'na', na, 'ds', ds, ...
    'dsd', sdd, 'dod', dod, 'offset_s', offset_s, ...
    'down', down);

physics_type_folder = [sampleFolder 'monochromatic/'];
if exist(physics_type_folder, 'dir') == false
    mkdir(physics_type_folder)
end

mu_water = 0.2059 / 10;     % in mm-1

aec_factors = exp(mu_water*patient_diameters)./exp(mu_water*patient_diameters(1));

for idx=1:length(patient_diameters)
    patient_diameter = patient_diameters(idx)
    fov = 1.1*patient_diameter
    aec_factor = aec_factors(idx);

    ig = image_geom('nx', nx, 'fov', fov, 'down', down);
    % ig <-- write this to text file and read in later
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
        x_true_hu = 1000*(x_true - mu_water)/mu_water;
        filename = [patient_folder  filesep 'true.raw'];
        write_phantom_info([patient_folder filesep 'phantom_info_mm.csv'], ell);
        write_phantom_info([patient_folder filesep 'phantom_info_pix_idx.csv'], ellipse_mm_to_pix(ell, fov, nx));
        write_image_geom_info([patient_folder filesep 'image_geom_info.csv'], ig)
        if ~exist(filename, 'file')
            my_write_rawfile(filename, x_true_hu, 'int16');
        end

        % Get sinogram
        sino = ellipse_sino(sg, ell, 'oversample', 4);

        % FBP reconstruction operator
        fg = fbp2(sg, ig,'type','std:mat'); %choose 'std:mat' to be able to using different recon filter
                                            %default would be 'std:mex' but only ramp filter was implemented in it
        if aec_on == true
            I0 = aec_factor*I0; %accounts for different patient size
        end

        if(has_bowtie==1)
            I0_afterbowtie=apply_bowtie_filter(I0, sg, mu_water, patient_diameter);           
        else
            I0_afterbowtie=I0;            
        end        
        proj = I0_afterbowtie .* exp(-sino);
        for isim = batch      
            isim
            if add_noise == true      
                proj = poisson(proj); %This poisson generator respond to the seed number setby rand('sate',x');
            end

            if any(proj(:) == 0)
                warn('%d of %d values are 0 in sinogram!', ...
                    sum(proj(:)==0), length(proj(:)));
                proj(proj==0) = 1;
            end

            sino_noisy = -log(proj ./ I0_afterbowtie);            % noisy fan-beam sinogram

            x_fbp_sharp = fbp2(sino_noisy, fg, 'window', 'hann205');
            x_fbp_sharp_hu = 1000*(x_fbp_sharp - mu_water)/mu_water;
            file_prefix = [files_sharp 'fbp_sharp_'];
            file_num = isim;
            filename_fbp_sharp = [file_prefix 'v' sprintf('%03d', file_num) '.raw'];
            my_write_rawfile(filename_fbp_sharp, x_fbp_sharp_hu, 'int16');

            % files_smooth = [patient_folder I0_string '/fbp_smooth/'];
            % if(~exist(files_smooth,'dir'))
            %     mkdir(files_smooth);
            % end
            % x_fbp_smooth = fbp2(sino_noisy, fg,'window','hann85');
            % x_fbp_smooth_hu = 1000*(x_fbp_smooth - mu_water)/mu_water;
            % file_prefix = [files_smooth 'fbp_smooth_'];
            % file_num = isim;
            % filename_fbp_smooth = [file_prefix 'v' sprintf('%03d', file_num) '.raw'];
            % my_write_rawfile(filename_fbp_smooth, x_fbp_smooth_hu, 'int16');
        end
    end
end
