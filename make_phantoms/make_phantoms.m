clear all; close all;
% specify configs
% max_dose_level = 3e6
nsims = 5;
patient_diameters = [112, 131, 151, 185, 216, 292]; %From TG204 table 3 ICRU74 
aec_on = true; %automatic exposure control
add_noise = false;
basedataFolder = ['/gpfs_projects/brandon.nelson/DLIR_Ped_Generalizability/geomtric_phantom_studies/'];
% basedataFolder = '/home/brandon.nelson/Data/temp/noise_free/'; %temporary until /gpfs_projects gets fixed then switch back to above^^^ 

add_noise = false;
disp('Simulation series 1/3')
disp('Now running CTP404 Multicontrast Phantom simulations...')
run('./CTP404/make_CTP404.m')

add_noise = true;
max_dose_level = 3e5
disp('Simulation series 2/3')
disp('Now running CCT189 low contrast detectability simulations...')
run('./CCT189/make_CCT189.m')

disp('Simulation series 3/3')
disp('Now running Uniform Water Phantom simulations...')
run('./uniform/make_uniform.m')