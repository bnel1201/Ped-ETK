orginal_dir=$(pwd)
cd $(dirname $0)
# make phantoms
bash ../ssh_node.sh "bash ./make_phantoms/run_make_test_phantoms.sh; exit"

# # run denoising
# # conda activate DLIR #change to whatever virtual env needed or comment if already in env
# bash ./denoising/run_denoising.sh

# # run evaluations
# bash ./evaluation/run_all_evaluations.sh

cd $orginal_dir