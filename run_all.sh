# make phantoms
bash ssh_node.sh "bash make_phantoms/run_make_phantoms.sh; exit"

# run denoising
# conda activate DLIR #change to whatever virtual env needed or comment if already in env
bash ./denoising/run_denoising.sh

# run evaluations
bash ./evaluations/run_all_evaluations.sh
