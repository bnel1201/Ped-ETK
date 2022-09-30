orginal_dir=$(pwd)
cd $(dirname $0)

# MTF
bash ../ssh_node.sh "bash MTF/_1_run_MTF_analysis.sh; exit"

bash MTF/_2_generate_MTF_plots.sh

# NPS

bash ../ssh_node.sh "bash NPS/_1_run_NPS_analysis.sh; exit"

bash NPS/_2_generate_NPS_plots.sh

cd $orginal_dir