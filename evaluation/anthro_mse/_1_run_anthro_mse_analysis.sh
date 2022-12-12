BASE_DIR=${1-/gpfs_projects/brandon.nelson/DLIR_Ped_Generalizability/anthropomorphic_phantom_studies/main/simulations} #directory containing simulations
RESULTS_DIR=${2-anthro_results}

results_csv_name=$(realpath $RESULTS_DIR/anthro_mse_dataset.csv) #csv to be generated containing mean squared error measurements

cd $(dirname $0)
orginal_dir=$(pwd)

patient_info_csv=$(realpath ../../make_phantoms/anthropomorphic/selected_xcat_patients.csv) #selected_xcat_patients.csv #from XCAT

# generate results csv file
python measure_anthro_mse.py $BASE_DIR $patient_info_csv -o $results_csv_name

# plot results
python plot_anthro_mse.py $results_csv_name -o $RESULTS_DIR

cd $orginal_dir
