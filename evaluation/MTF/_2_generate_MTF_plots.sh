## plot MTF curves

# plot fbp baseline mtf
datadir=/gpfs_projects/brandon.nelson/DLIR_Ped_Generalizability/geomtric_phantom_studies/CTP404/monochromatic/
output_fname=results/plots/fbp_mtf_baseline.png
python plot_mtf_curves.py -d $datadir -o $output_fname

# plot redcnn mtf
output_fname=results/plots/mtf_redcnn.png
python plot_mtf_curves.py -d $datadir -o $output_fname --processed

## plot MTF cutoff values

output_fname=results/plots/mtf_cutoff_vals.png
python plot_mtf_cutoffs.py -d $datadir -o $output_fname

output_fname=results/plots/mtf_cutoff_vals_processed.png
python plot_mtf_cutoffs.py -d $datadir -o $output_fname --processed

output_fname=results/plots/mtf_cutoff_vals_rel.png
python plot_mtf_cutoffs_compare.py -d $datadir -o $output_fname

# plot images

python plot_images.py
