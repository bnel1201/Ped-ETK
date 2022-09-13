% make_CCT189.m
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

addpath('/home/brandon.nelson/Dev/PhantomSimulations/CT_simulator')
if exist('homedir', 'var') == false %checks if setpath has been run
    setpath
end
addpath('./utils')
addpath('./configs')
if exist('max_dose_level', 'var') == false
    max_dose_level = 3e5
end
I0_vector = max_dose_level*[30 55 70 85 100]/100;

if exist('patient_diameters', 'var') == false
    patient_diameters = [132, 188, 243, 300, 354]; %newborn, 8 yr-old, 18 year old
end

if exist('nsims', 'var') == false
    nsims = 5
end
batch = 1:nsims;
rand('state', batch(end)); %need this for the first time run to control

% Set save folder
if exist('basedataFolder', 'var') == false
    basedataFolder = '/home/brandon.nelson/Data/temp/'; %temporary until /gpfs_projects gets fixed then switch back to above^^^ 
end
sampleFolder = [basedataFolder 'CCT189/']
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
% dx = fov / nx

physics_type_folder = [sampleFolder 'monochromatic/'];
if exist(physics_type_folder, 'dir') == false
    mkdir(physics_type_folder)
end

mu_water = 0.2059 / 10;     % in mm-1

for idx=1:length(patient_diameters)
    patient_diameter = patient_diameters(idx)
    fov = 1.1*patient_diameter
    relative_size = patient_diameter / min(patient_diameters);
    aec_factor = exp(1 - relative_size);
    ig = image_geom('nx', nx, 'fov', fov, 'down', down);

    patient_folder = [physics_type_folder '/diameter' num2str(patient_diameter) 'mm/']
    if exist(patient_folder, 'dir') == false
        mkdir(patient_folder)
    end

    for I0=I0_vector
        I0_string = ['I0_' sprintf('%07d', I0)];

        files_sharp = [patient_folder I0_string '/fbp_sharp/'];
        files_smooth = [patient_folder I0_string '/fbp_smooth/'];

        if(~exist(files_sharp,'dir'))
            mkdir(files_sharp);
        end
        if(~exist(files_smooth,'dir'))
            mkdir(files_smooth);
        end
        relative_lesion_diameter = 0.4;
        ell = CCT189(patient_diameter, mu_water, relative_lesion_diameter);
        x_true = ellipse_im(ig, ell, 'oversample', 4, 'rot', 0);
        x_true_hu = 1000*(x_true - mu_water)/mu_water;
        filename = [patient_folder  '/' 'true.raw'];
        if ~exist(filename, 'file')
            my_write_rawfile(filename, x_true_hu, 'int16');
        end

        sino = ellipse_sino(sg, ell, 'oversample', 4);

        % FBP reconstruction operator
        fg = fbp2(sg, ig,'type','std:mat'); %choose 'std:mat' to be able to using different recon filter
                                            %default would be 'std:mex' but only ramp filter was implemented in it

        if(has_bowtie==1)
            I0_afterbowtie=apply_bowtie_filter(I0, sg, mu_water, patient_diameter);           
        else
            I0_afterbowtie=I0;            
        end        
        proj = I0_afterbowtie .* exp(-sino);

        for isim = batch      
            isim
            if aec_on == true
                proj = aec_factor*proj; %accounts for different patient size
            end
            proj_noisy = poisson(proj); %This poisson generator respond to the seed number setby rand('sate',x');
            
            if any(proj_noisy(:) == 0)
                warn('%d of %d values are 0 in sinogram!', ...
                    sum(proj_noisy(:)==0), length(proj_noisy(:)));
                proj_noisy(proj_noisy==0) = 1;
            end

            sino_noisy = -log(proj_noisy ./ I0_afterbowtie);            % noisy fan-beam sinogram

            x_fbp_sharp = fbp2(sino_noisy, fg, 'window', 'hann205');
            x_fbp_sharp_hu = 1000*(x_fbp_sharp - mu_water)/mu_water;
            x_fbp_smooth = fbp2(sino_noisy, fg,'window','hann85');
            x_fbp_smooth_hu = 1000*(x_fbp_smooth - mu_water)/mu_water;

            file_prefix = [files_sharp 'fbp_sharp_'];
            file_num = isim;
            filename_fbp_sharp = [file_prefix 'v' sprintf('%03d', file_num) '.raw'];
            my_write_rawfile(filename_fbp_sharp, x_fbp_sharp_hu, 'int16');

            file_prefix = [files_smooth 'fbp_smooth_'];
            file_num = isim;
            filename_fbp_smooth = [file_prefix 'v' sprintf('%03d', file_num) '.raw'];
            my_write_rawfile(filename_fbp_smooth, x_fbp_smooth_hu, 'int16');
        end
    end
end
