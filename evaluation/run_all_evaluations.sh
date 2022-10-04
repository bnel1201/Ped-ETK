basedir=/gpfs_projects/brandon.nelson/DLIR_Ped_Generalizability/geomtric_phantom_studies
results_dir=../results

# Do Not Edit Below
cd $(dirname $0)
results_dir=$(realpath $results_dir)
orginal_dir=$(pwd)

# MTF
bash ../ssh_node.sh "bash MTF/_1_run_MTF_analysis.sh; exit"

bash MTF/_2_generate_MTF_plots.sh $basedir/CTP404/monochromatic/ $results_dir/MTF

# NPS
bash ../ssh_node.sh "bash NPS/_1_run_NPS_analysis.sh; exit"

bash NPS/_2_generate_NPS_plots.sh $basedir/CCT189/monochromatic/ $results_dir/NPS

# Objective Image Quality Summary

python plot_objective_iq_summary.py -d $results_dir -o $results_dir/objective_iq_summary.png

# LCD
bash ../ssh_node.sh "bash LCD/_1_run_LCD_analysis.sh; exit"

bash LCD/_2_generate_LCD_plots.sh $basedir/CCT189/monochromatic/ $results_dir/LCD

cd $orginal_dir