# Model from here: </gpfs_projects/prabhat.kc/lowdosect/transfers/transfers_4_spie/exps/exps/exps_4r_phan_insert/resolve_phan_exe.sh>
MODEL_FOLDER='/gpfs_projects/prabhat.kc/lowdosect/transfers/transfers_4_spie/exps/exps/w8_exps_4_spie_dose/checkpoints/p96/augTrTaTdT/redcnn/hvd_cpt_for_mse_tv-fbd_wd_0.0_lr_1e-05_bs_64/'

orginal_dir=$(pwd)
cd $(dirname $0)
bash denoise_CTP404.sh $MODEL_FOLDER

bash denoise_CCT189.sh $MODEL_FOLDER
cd $orginal_dir