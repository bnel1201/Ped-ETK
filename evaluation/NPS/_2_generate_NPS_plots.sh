orginal_dir=$(pwd)
cd $(dirname $0)
input_dir=/home/brandon.nelson/Data/temp/CCT189/monochromatic
results_dir=../../results/NPS

# plot NPS curves
python plot_NPS_curves.py -d $input_dir -o $results_dir

# plot images
images_dir=$results_dir/images
python plot_2D_nps_images.py -d $input_dir -o $images_dir

bash ../utils/images_to_gif.sh $images_dir'/diameter*mm_noise_comparison.png' $results_dir'/nps_comparison.gif'
cd $orginal_dir