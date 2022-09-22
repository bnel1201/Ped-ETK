# plot fbp baseline mtf
datadir=/gpfs_projects/brandon.nelson/DLIR_Ped_Generalizability/geomtric_phantom_studies/CTP404/monochromatic/
output_fname=fbp_mtf_baseline.png
python plot_mtf_curves.py $datadir $output_fname

# plot redcnn mtf
output_fname=mtf_redcnn.png
python plot_mtf_curves.py $datadir $output_fname --processed

# python plot_proc_mtf_curves.py 

python plot_mtf_cutoffs.py

python plot_proc_mtf_cutoffs.py 

# python plot_diff_mtf_cutoffs.py