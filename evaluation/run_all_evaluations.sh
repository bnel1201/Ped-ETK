bash ../ssh_node.sh "bash MTF/_1_run_MTF_analysis.sh; exit"

bash MTF/_2_generate_MTF_plots.sh

bash ../ssh_node.sh "bash NPS/_1_run_NPS_analysis.sh; exit"

bash NPS/_2_generate_NPS_plots.sh