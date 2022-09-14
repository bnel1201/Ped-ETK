val=$(hostname)
if [ "${val:0:4}" != "node" ]; then
    echo "It's not Equal"
    ssh -X node
fi

# # make phantoms
# matlab -nodesktop -nosplash ./make_phantoms/make_phantoms.m

# # run denoising
# bash ./denoising/run_denoising.sh

# # run evaluations
# matlab -nodesktop -nosplash ./evaluation/run_all.m

# # make plots
# bash ./evaluation/MTF/run.sh