BASE_DIR=${1-/gpfs_projects/brandon.nelson/DLIR_Ped_Generalizability/geomtric_phantom_studies/main}
RESULTS_DIR=${2-../results}

# Do Not Edit Below
RESULTS_DIR=$(realpath $RESULTS_DIR)
cd $(dirname $0)
orginal_dir=$(pwd)

# MTF
cmd="bash MTF/_1_run_MTF_analysis.sh ${BASE_DIR}"
if [ $(hostname) == openhpc ]; then
    bash ../ssh_node.sh "$cmd; exit"
else
echo $cmd
    $cmd
fi
bash MTF/_2_generate_MTF_plots.sh $BASE_DIR/CTP404/monochromatic/ $RESULTS_DIR/MTF

# NPS
cmd="bash NPS/_1_run_NPS_analysis.sh ${BASE_DIR}"
if [ $(hostname) == openhpc ]; then
    bash ../ssh_node.sh "$cmd; exit"
else
    $cmd
fi
bash NPS/_2_generate_NPS_plots.sh $BASE_DIR/CCT189/monochromatic/ $RESULTS_DIR/NPS

# Objective Image Quality Summary

python plot_objective_iq_summary.py -d $RESULTS_DIR -o $RESULTS_DIR/objective_iq_summary.png

# LCD
cmd="bash LCD/_1_run_LCD_analysis.sh ${BASE_DIR} ${RESULTS_DIR}/LCD"
if [ $(hostname) == openhpc ]; then
    bash ../ssh_node.sh "$cmd; exit"
else
    $cmd
fi
bash LCD/_2_generate_LCD_plots.sh $BASE_DIR/CCT189/monochromatic $RESULTS_DIR/LCD

cd $orginal_dir