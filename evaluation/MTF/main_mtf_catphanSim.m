%contrast-dependent MTF from catphan scans
% clear all;
addpath('utils')
if ~exist('basedir', 'var')
    disp('basedir not specified, using defaults')
    basedir = '/gpfs_projects/brandon.nelson/DLIR_Ped_Generalizability/geomtric_phantom_studies/'; %see ../../make_phantoms/make_phantoms.m
end

datadir = fullfile(basedir, 'CTP404/monochromatic/');
dose_level = 'I0_3000000';
kernel = 'fbp_sharp';
dir_contents = dir(datadir);
diams = dir_contents(3:end);
for idx=1:length(diams)
    folder_path = [datadir filesep diams(idx).name filesep dose_level filesep kernel filesep]
    run('utils/eval_CTP404_MTF.m')
end

% run eval on DLIR images

datadir = fullfile(basedir, 'CTP404/monochromatic/');
dose_level = 'I0_3000000_processed';
kernel = 'fbp_sharp';
dir_contents = dir(datadir);
diams = dir_contents(3:end);
for idx=1:length(diams)
    folder_path = [datadir filesep diams(idx).name filesep dose_level filesep kernel filesep]
    run('utils/eval_CTP404_MTF.m')
end

exit