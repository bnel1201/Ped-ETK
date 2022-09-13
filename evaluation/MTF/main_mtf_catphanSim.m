%contrast-dependent MTF from catphan scans
clear all;
%Load slice in
addpath('utils')
% folder_path = '/gpfs_projects/rxz4/data/DLCT/phantom_sim/for_CT2020Conf/ctp404_proc/'; %Bv44d, Bf32d
basedir = '/gpfs_projects/brandon.nelson/DLIR_Ped_Generalizability/geomtric_phantom_studies/'; %see ../../make_phantoms/make_phantoms.m

datadir = fullfile(basedir, 'CTP404/monochromatic/');
dose_level = 'I0_3000000';
kernel = 'fbp_sharp';
dir_contents = dir(datadir);
diams = dir_contents(3:end);
for idx=1:length(diams)
    folder_path = [datadir filesep diams(idx).name filesep dose_level filesep kernel filesep]
    run('utils/eval_CTP404_MTF.m')
end
