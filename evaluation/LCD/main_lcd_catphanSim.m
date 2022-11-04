% %LCD test
addpath('utils')
if ~exist('basedir', 'var')
    disp('basedir not specified, using defaults')
    basedir = '/gpfs_projects/brandon.nelson/DLIR_Ped_Generalizability/geomtric_phantom_studies/'; %see ../../make_phantoms/make_phantoms.m
end

if ~exist('resultsdir', 'var')
    disp('resultsdir not specified, using defaults')
    resultsdir = '/home/brandon.nelson/Dev/DLIR_Ped_Generalizability/geomtric_phantom_studies/results'; %see ../../make_phantoms/make_phantoms.m
end

base_data_folder = fullfile(basedir, 'CCT189/monochromatic/');
outfolder = resultsdir;
if ~exist(outfolder, 'dir')
    mkdir(outfolder)
end

%%Data inputs
all_recon_type = {'fbp','dl_REDCNN'};

% I0_vector = 3e5*[30 55 70 85 100]/100;
run('utils/eval_lcd_catphanSim.m')

exit