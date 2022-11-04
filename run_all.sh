EXPERIMENT=${1-./experiments/main}

# load experiment parameters
EXPERIMENT=$(realpath $EXPERIMENT)
source $EXPERIMENT/protocol
# make phantoms
bash make_phantoms/run_make_phantoms.sh ${BASE_DIR} ${EXPERIMENT}

# run denoising
# conda activate DLIR #change to whatever virtual env needed or comment if already in env
bash denoising/run_denoising.sh $BASE_DIR $MODEL_FOLDER

# run evaluations
bash evaluation/run_all_evaluations.sh $BASE_DIR $RESULTS_DIR
