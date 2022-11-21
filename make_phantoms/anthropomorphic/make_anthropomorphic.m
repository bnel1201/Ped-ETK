base_dir = '/gpfs_projects/brandon.nelson/DLIR_Ped_Generalizability/anthropomorphic_phantom_studies/main';
phantom_dir = fullfile(base_dir, 'phantoms')

addpath('utils')

patient_dirs = dir([phantom_dir '/*.bin']);

for idx=1:length(patient_dirs)
   patient = patient_dirs(idx).name(1:end-4)
   phantom_sims
end