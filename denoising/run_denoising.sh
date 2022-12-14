BASE_DIR=${1-/gpfs_projects/brandon.nelson/DLIR_Ped_Generalizability/geomtric_phantom_studies/main}
# Model from here: </gpfs_projects/prabhat.kc/lowdosect/transfers/transfers_4_spie/exps/exps/exps_4r_phan_insert/resolve_phan_exe.sh>
MODEL_FOLDER=${2-'/gpfs_projects/prabhat.kc/lowdosect/transfers/transfers_4_spie/exps/exps/w8_exps_4_spie_dose/checkpoints/p96/augTrTaTdT/redcnn/hvd_cpt_for_mse_tv-fbd_wd_0.0_lr_1e-05_bs_64/'}
# MODEL_FOLDER='/gpfs_projects/prabhat.kc/lowdosect/transfers/transfers_4_spie/exps/exps/w9_exps_4r_didsr/checkpoints/d95_2_d75_2_d25_p96/augFrFaTdF_2_augTrTaTdT/redcnn/hvd_cpt_for_mse_tv-fbd_reg_0.0001_wd_0.0_lr_1e-05_bs_64/'
# MODEL_FOLDER'/gpfs_projects/prabhat.kc/lowdosect/transfers/transfers_4_spie/exps/exps/w9_exps_4r_didsr/checkpoints/8p_75d_2_50d_qd_p96/augFrFaTdF_2_augTrTaTdF/redcnn/hvd_cpt_for_mse_tv-fbd_reg_0.0001_wd_0.0_lr_1e-05_bs_64/'

orginal_dir=$(pwd)
cd $(dirname $0)

for PHANTOM_TYPE in $BASE_DIR/*; do
    if [ $(basename $PHANTOM_TYPE) == anthropomorphic ]; then
    PHANTOM_TYPE=$PHANTOM_TYPE/simulations
    fi
    for PHANTOM in $PHANTOM_TYPE/*; do
        for DIAMETER in $PHANTOM/monochromatic/*; do
            for DOSELEVEL in $DIAMETER/I0*0/; do
                DOSELEVEL=${DOSELEVEL:0:-1}
                if [ $(basename $PHANTOM) == CCT189 ]; then
                    for OBJ in disk bkg; do
                    INPUT_FOLDER="$DOSELEVEL"/$OBJ/
                    OUTPUT_FOLDER="$DOSELEVEL"_processed/$OBJ/
                    bash denoise.sh $INPUT_FOLDER $OUTPUT_FOLDER $MODEL_FOLDER

                    mkdir -p $OUTPUT_FOLDER/
                    mv $OUTPUT_FOLDER/checkpoint-25/*.raw $OUTPUT_FOLDER/
                    rm -r $OUTPUT_FOLDER/checkpoint-25
                    done
                else
                    INPUT_FOLDER="$DOSELEVEL"/fbp_sharp/
                    OUTPUT_FOLDER="$DOSELEVEL"_processed/
                    bash denoise.sh $INPUT_FOLDER $OUTPUT_FOLDER $MODEL_FOLDER
            
                    mkdir -p $OUTPUT_FOLDER/fbp_sharp
                    mv $OUTPUT_FOLDER/checkpoint-25/*.raw $OUTPUT_FOLDER/fbp_sharp/
                    rm -r $OUTPUT_FOLDER/checkpoint-25
                fi
            done
        done
    done
done
cd $orginal_dir