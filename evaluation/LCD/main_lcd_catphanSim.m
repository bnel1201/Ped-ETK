% %LCD test
addpath('utils')

base_data_folder = '/gpfs_projects/brandon.nelson/DLIR_Ped_Generalizability/geomtric_phantom_studies/CCT189/monochromatic/';
% base_data_folder = '/home/brandon.nelson/Data/temp/CCT189/monochromatic/'
outfolder = '/home/brandon.nelson/Dev/DLIR_Ped_Generalizability/geomtric_phantom_studies/results/LCD'
if ~exist(outfolder, 'dir')
    mkdir(outfolder)
end

%%Data inputs
all_recon_type = {'fbp','dl_REDCNN'};

I0_vector = 3e5*[30 55 70 85 100]/100;
run('utils/eval_lcd_catphanSim.m')

exit