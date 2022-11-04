%NPS measures from catphan scans
% clear all;
addpath('utils')
if ~exist('basedir', 'var')
    disp('basedir not specified, using defaults')
    basedir = '/gpfs_projects/brandon.nelson/DLIR_Ped_Generalizability/geomtric_phantom_studies/'; %see ../../make_phantoms/make_phantoms.m
end

datadir = fullfile(basedir, 'CCT189/monochromatic/')
dose_level = 'I0_0300000';
kernel = 'bkg';
dir_contents = dir(datadir);
diams = dir_contents(3:end);
for idx=1:length(diams)
    folder_path = [datadir filesep diams(idx).name filesep dose_level filesep kernel filesep];
    run('utils/eval_CCT189_NPS.m')
end

% run eval on DLIR images

datadir = fullfile(basedir, 'CCT189/monochromatic/');
dose_level = [dose_level '_processed'];
kernel = 'bkg';
dir_contents = dir(datadir);
diams = dir_contents(3:end);
for idx=1:length(diams)
    folder_path = [datadir filesep diams(idx).name filesep dose_level filesep kernel filesep]
    run('utils/eval_CCT189_NPS.m')
end

% exit