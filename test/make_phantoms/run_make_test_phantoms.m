clear all; close all;
% specify configs

% CTP404 for contrast dependent MTF measures
nsims = 1;
image_matrix_size=512;
nangles = 2320;
patient_diameters = [112, 292]; %From TG204 table 3 ICRU74 
aec_on = true; %automatic exposure control
add_noise = false;
reference_dose_level=3e6;
basedataFolder = ['/gpfs_projects/brandon.nelson/DLIR_Ped_Generalizability/geomtric_phantom_studies/'];
offset = 1000; %needed for some models
disp('Simulation series 1/2')
disp('Now running CTP404 Multicontrast Phantom simulations...')
run('./CTP404/make_CTP404.m')

% CCT189 for NPS and LCD
add_noise = true;
reference_dose_level = 3e5*[30 55 100]/100;
nangles = 580;
add_noise = true;
nsims = 2;
offset = 1000; %needed for some models
disp('Simulation series 2/2')
disp('Now running CCT189 low contrast detectability simulations...')
run('./CCT189/make_CCT189.m')

exit