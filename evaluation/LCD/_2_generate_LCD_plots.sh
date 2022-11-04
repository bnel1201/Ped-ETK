datadir=${1-'/gpfs_projects/brandon.nelson/DLIR_Ped_Generalizability/geomtric_phantom_studies/old_results/CCT189/monochromatic'}
results_dir=${2-'results/LCD'}

results_dir=$(realpath $results_dir)

orginal_dir=$(pwd)
cd $(dirname $0)


# plot LCD curves
plots_dir=$results_dir/plots
python plot_LCD_results.py $results_dir
bash ../utils/images_to_gif.sh $plots_dir/'LCD_v_dose_diameter_*mm.png' $results_dir'/lcd_v_dose_comparison.gif'

# plot images
images_dir=$results_dir/images
n_avg=10
python plot_LCD_images.py $results_dir/LCD_results.h5\
                          -d $datadir\
                          -n $n_avg\
                          -o $images_dir

bash ../utils/images_to_gif.sh $images_dir'/diameter*mm_lcd_comparison.png' $results_dir'/lcd_image_comparison.gif'

python plot_image_montage.py $results_dir/LCD_results.h5\
                             -d $datadir\
                             -n $n_avg\
                             -o $results_dir/montage.png\
                             -D "112 292"
cd $orginal_dir

