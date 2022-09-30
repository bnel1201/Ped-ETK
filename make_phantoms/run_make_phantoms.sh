# this scripts assumes user is in a node with matlab
# to enter a node:
# 1. join a random node: `../ssh_node.sh` see script for more details including how to run with arguments
# 2. join a node manually: `ssh -X nodexyz` where `xyz` is one of the nodes available see `clusterTop`
#    to see available nodes
orginal_dir=$(pwd)
cd $(dirname $0)

matlab -nodesktop -nodisplay -r "run('./make_phantoms.m'), exit;"

cd $orginal_dir