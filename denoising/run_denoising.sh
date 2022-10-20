# Model from here: </gpfs_projects/prabhat.kc/lowdosect/transfers/transfers_4_spie/exps/exps/exps_4r_phan_insert/resolve_phan_exe.sh>
MODEL_FOLDER='/gpfs_projects/prabhat.kc/lowdosect/transfers/transfers_4_spie/exps/exps/w8_exps_4_spie_dose/checkpoints/p96/augTrTaTdT/redcnn/hvd_cpt_for_mse_tv-fbd_wd_0.0_lr_1e-05_bs_64/'
# MODEL_FOLDER='/gpfs_projects/prabhat.kc/lowdosect/transfers/transfers_4_spie/exps/exps/w9_exps_4r_didsr/checkpoints/d95_2_d75_2_d25_p96/augFrFaTdF_2_augTrTaTdT/redcnn/hvd_cpt_for_mse_tv-fbd_reg_0.0001_wd_0.0_lr_1e-05_bs_64/'
# MODEL_FOLDER'/gpfs_projects/prabhat.kc/lowdosect/transfers/transfers_4_spie/exps/exps/w9_exps_4r_didsr/checkpoints/8p_75d_2_50d_qd_p96/augFrFaTdF_2_augTrTaTdF/redcnn/hvd_cpt_for_mse_tv-fbd_reg_0.0001_wd_0.0_lr_1e-05_bs_64/'

orginal_dir=$(pwd)
cd $(dirname $0)
bash denoise_CTP404.sh $MODEL_FOLDER

bash denoise_CCT189.sh $MODEL_FOLDER
cd $orginal_dir