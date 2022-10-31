datadir=${1-'/home/brandon.nelson/Data/temp/CCT189/monochromatic'}
datadir='/gpfs_projects/brandon.nelson/DLIR_Ped_Generalizability/geomtric_phantom_studies/CCT189/monochromatic'
results_dir=${2-'../../results/LCD'}

orginal_dir=$(pwd)
cd $(dirname $0)


# plot LCD curves
python plot_LCD_results.py -d $results_dir -o $results_dir/plots/lcd_v_diameter.png
plots_dir=$results_dir'/LCD_v_dose'
bash ../utils/images_to_gif.sh $plots_dir'/LCD_v_dose_diameter_*mm.png' $results_dir'/lcd_v_dose_comparison.gif'

# plot images
images_dir=$results_dir/images
n_avg=10
python plot_LCD_images.py $results_dir/LCD_results.h5 \
                          -d $datadir \
                          -n $n_avg \
                          -o $images_dir

bash ../utils/images_to_gif.sh $images_dir'/diameter*mm_lcd_comparison.png' $results_dir'/lcd_image_comparison.gif'

python plot_image_montage.py $results_dir/LCD_results.h5 \
                             -d $datadir \
                             -n $n_avg \
                             -o $results_dir/montage.png \
                             -D "112 292"
cd $orginal_dir

