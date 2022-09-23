# make phantoms
bash ssh_node.sh "cd make_phantoms; bash ./run_make_phantoms.sh; exit; cd .."

# run denoising
# conda activate DLIR #change to whatever virtual env needed or comment if already in env
bash ./denoising/run_denoising.sh

# run evaluations
cd evaluation/MTF
bash ../../ssh_node.sh "bash ./_1_run_MTF_analysis.sh; exit"

# make plots
bash ./_2_generate_MTF_plots.sh