# This script ssh's into a random node and returns you
# to the original directory this script is called from
# option to include arguments to run scripts in the node
# once connection is started
# brandon.nelson@fda.hhs.gov
# 2022-09-16

ssh_args=$1
val=$(hostname)
nodes=("062" "077" "081" "083" "085" "089"\
       "093" "097" "099" "103" "104" "110"\
       "116" "121" "149" "151" "152" "153"\
       "154" "155" "156" "157" "159" "160"\
       "161" "162" "173" "181" "183" "185"\
       "190" "194" "195" "196" "197" "198"\
       "199" "200" "202" "203" "204" "205"\
       "206" "207" "208" "209" "210" "211"\
       "212" "213" "214" "215" "216")
RANDOM=$$$(date +%s)
cur_dir=$(pwd)
cmd=""
if [ $val == openhpc ]; then
    selectednode=${nodes[ $RANDOM % ${#nodes[@]} ]}
    echo entering node"${selectednode}"
    cmd+="ssh -X node${selectednode} -t cd ${cur_dir};"
    if [ $# != 0 ]; then
        cmd+="${ssh_args};"
    fi
    cmd+="bash -l;"
else
    echo already in $val
    cmd+=$ssh_args
fi
$cmd