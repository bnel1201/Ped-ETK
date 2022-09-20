

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CNN3 - MSE with L1 prior 
# Learning rate:0.001 batch size:128 patch size:55
# trained over psuedo augmented as in our SPIE paper
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
<<COMMENT
MODEL_FOLDER='../w8_exps_4_spie_dose/checkpoints/p55/augTrTaTdT/three_layers/hvd_cpt_for_mse_l1_wd_0.0_lr_0.001_bs_128/'
NORM_TYPE=None

INPUT_FOLDER="/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/patient/L506_3mm_sharp/patient_disk_066/"
OUTPUT_FOLDER='./results/patient_disk_066_CNN3/'
python resolve_fly.py --m 'three_layers' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
--output-folder $OUTPUT_FOLDER --cuda --normalization-type $NORM_TYPE --specific-epoch --se-plot \
--input-img-type 'dicom' --gt-folder '' --out-dtype 'uint16'

INPUT_FOLDER="/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/patient/L506_3mm_sharp/patient_wire_066/"
OUTPUT_FOLDER='./results/patient_wire_066_CNN3/'
python resolve_fly.py --m 'three_layers' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
--output-folder $OUTPUT_FOLDER --cuda --normalization-type $NORM_TYPE --specific-epoch --se-plot \
--input-img-type 'dicom' --gt-folder ' ' --out-dtype 'uint16'

INPUT_FOLDER="/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/patient/L506_3mm_sharp/sim_half_066/"
OUTPUT_FOLDER='./results/sim_half_CNN3/'
python resolve_fly.py --m 'three_layers' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
--output-folder $OUTPUT_FOLDER --cuda --normalization-type $NORM_TYPE --specific-epoch --se-plot \
--input-img-type 'dicom' --gt-folder ' ' --out-dtype 'uint16'


INPUT_FOLDER="/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/patient/L506_3mm_sharp/sim_quarter_066/"
OUTPUT_FOLDER='./results/sim_quarter_066/'
python resolve_fly.py --m 'three_layers' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
--output-folder $OUTPUT_FOLDER --cuda --normalization-type $NORM_TYPE --specific-epoch --se-plot \
--input-img-type 'dicom' --gt-folder ' ' --out-dtype 'uint16'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# UNet - MSE with L1 prior 
# Learning rate:0.001 batch size:64 patch size:55
# checkpoint 6
# trained over psuedo augmented as in our SPIE paper
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
MODEL_FOLDER='../w8_exps_4_spie_dose/checkpoints/p55_uni_ind/augTrTaTdT/unet/hvd_cpt_for_mse_l1_wd_0.0_lr_0.001_bs_64/'
NORM_TYPE='unity_independent'

INPUT_FOLDER="/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/patient/L506_3mm_sharp/patient_disk_066/"
OUTPUT_FOLDER='./results/patient_disk_066_UNet/'
python resolve_fly.py --m 'unet' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
 --output-folder $OUTPUT_FOLDER --cuda --normalization-type $NORM_TYPE --input-img-type 'dicom' \
 --specific-epoch --se-plot --chckpt-no 6 --gt-folder ' ' --out-dtype 'uint16'

INPUT_FOLDER="/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/patient/L506_3mm_sharp/patient_wire_066/"
OUTPUT_FOLDER='./results/patient_wire_066_UNet/'
python resolve_fly.py --m 'unet' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
 --output-folder $OUTPUT_FOLDER --cuda --normalization-type $NORM_TYPE --input-img-type 'dicom' \
 --specific-epoch --se-plot --chckpt-no 6 --gt-folder ' ' --out-dtype 'uint16'

INPUT_FOLDER="/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/patient/L506_3mm_sharp/sim_half_066/"
OUTPUT_FOLDER='./results/sim_half_066_UNet/'
python resolve_fly.py --m 'unet' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
 --output-folder $OUTPUT_FOLDER --cuda --normalization-type $NORM_TYPE --input-img-type 'dicom' \
 --specific-epoch --se-plot --chckpt-no 6 --gt-folder ' ' --out-dtype 'uint16'

INPUT_FOLDER="/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/patient/L506_3mm_sharp/sim_quarter_066/"
OUTPUT_FOLDER='./results/sim_quarter_066_UNet/'
python resolve_fly.py --m 'unet' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
 --output-folder $OUTPUT_FOLDER --cuda --normalization-type $NORM_TYPE --input-img-type 'dicom' \
 --specific-epoch --se-plot --chckpt-no 6 --gt-folder ' ' --out-dtype 'uint16'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GAN
# Learning rate:0.0001 batch size:32 patch size:55
# checkpoint 18
# trained over psuedo augmented as in our SPIE paper
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
MODEL_FOLDER='../../gan/GAN-dn2/checkpoints/uni_ind/augment/augTrTaTdT_p55_32_lr_0.0001/'
NORM_TYPE='unity_independent'

INPUT_FOLDER="/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/patient/L506_3mm_sharp/patient_disk_066/"
OUTPUT_FOLDER='./results/patient_disk_066_GAN/'
python resolve_fly.py --m 'simpleGAN' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
 --gt-folder ' ' --output-folder $OUTPUT_FOLDER --cuda --normalization-type $NORM_TYPE --input-img-type 'dicom' \
 --specific-epoch --chckpt-no 18 --se-plot  --out-dtype 'uint16'

INPUT_FOLDER="/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/patient/L506_3mm_sharp/patient_wire_066/"
OUTPUT_FOLDER='./results/patient_wire_066_GAN/'
python resolve_fly.py --m 'simpleGAN' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
 --gt-folder ' ' --output-folder $OUTPUT_FOLDER --cuda --normalization-type $NORM_TYPE --input-img-type 'dicom' \
 --specific-epoch --chckpt-no 18 --se-plot  --out-dtype 'uint16'

INPUT_FOLDER="/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/patient/L506_3mm_sharp/sim_half_066/"
OUTPUT_FOLDER='./results/sim_half_066_GAN/'
python resolve_fly.py --m 'simpleGAN' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
 --gt-folder ' ' --output-folder $OUTPUT_FOLDER --cuda --normalization-type $NORM_TYPE --input-img-type 'dicom' \
 --specific-epoch --chckpt-no 18 --se-plot  --out-dtype 'uint16'

INPUT_FOLDER="/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/patient/L506_3mm_sharp/sim_quarter_066/"
OUTPUT_FOLDER='./results/sim_quarter_066_GAN/'
python resolve_fly.py --m 'simpleGAN' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
 --gt-folder ' ' --output-folder $OUTPUT_FOLDER --cuda --normalization-type $NORM_TYPE --input-img-type 'dicom' \
 --specific-epoch --chckpt-no 18 --se-plot  --out-dtype 'uint16'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DnCNN - MSE with L1 prior 
# Learning rate:0.0001 batch size:32 patch size:55
# checkpoint: last one
# trained over psuedo augmented as in our SPIE paper (sg2)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
MODEL_FOLDER='../w8_exps_4_spie_dose/checkpoints/p55_uni_ind/augTrTaTdT/dncnn/hvd_cpt_for_mse_l1_wd_0.0_lr_0.0001_bs_32/'
NORM_TYPE='unity_independent'

INPUT_FOLDER="/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/patient/L506_3mm_sharp/patient_disk_066/"
OUTPUT_FOLDER='./results/patient_disk_066_DnCNN_sg2/'
python resolve_fly.py --m 'dncnn' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
 --output-folder $OUTPUT_FOLDER --cuda  --normalization-type $NORM_TYPE --input-img-type 'dicom' \
 --specific-epoch --se-plot --gt-folder ' ' --out-dtype 'uint16'

INPUT_FOLDER="/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/patient/L506_3mm_sharp/patient_wire_066/"
OUTPUT_FOLDER='./results/patient_wire_066_DnCNN_sg2/'
python resolve_fly.py --m 'dncnn' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
 --output-folder $OUTPUT_FOLDER --cuda  --normalization-type $NORM_TYPE --input-img-type 'dicom' \
 --specific-epoch --se-plot --gt-folder ' ' --out-dtype 'uint16'

INPUT_FOLDER="/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/patient/L506_3mm_sharp/sim_half_066/"
OUTPUT_FOLDER='./results/sim_half_066_DnCNN_sg2/'
python resolve_fly.py --m 'dncnn' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
 --output-folder $OUTPUT_FOLDER --cuda  --normalization-type $NORM_TYPE --input-img-type 'dicom' \
 --specific-epoch --se-plot --gt-folder ' ' --out-dtype 'uint16'

INPUT_FOLDER="/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/patient/L506_3mm_sharp/sim_quarter_066/"
OUTPUT_FOLDER='./results/sim_quarter_066_DnCNN_sg2/'
python resolve_fly.py --m 'dncnn' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
 --output-folder $OUTPUT_FOLDER --cuda  --normalization-type $NORM_TYPE --input-img-type 'dicom' \
 --specific-epoch --se-plot --gt-folder ' ' --out-dtype 'uint16'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DnCNN - lasso/MAE/lasso-wd 
# Learning rate:0.0001 batch size:32 patch size:55
# checkpoint: last one
# trained over sg1/sg2 8 patients
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
MODEL_FOLDER='../w6_exps_4_spie/checkpoints/p55_w_patient8/dncnn/hvd_cpt_for_l1__wd_0.0_lr_0.0001_bs_32/'
NORM_TYPE='unity_independent'

INPUT_FOLDER="/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/patient/L506_3mm_sharp/patient_disk_066/"
OUTPUT_FOLDER='./results/patient_disk_066_DnCNN_sg1_8p/mae/'
python resolve_fly.py --m 'dncnn' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
 --output-folder $OUTPUT_FOLDER --cuda  --normalization-type $NORM_TYPE --input-img-type 'dicom' \
 --specific-epoch --se-plot --gt-folder ' ' --out-dtype 'uint16'

#sg2
MODEL_FOLDER='../w8_exps_4_spie_dose/checkpoints/p55_uni_ind/augTrTaTdT_8p/dncnn/hvd_cpt_for_mse_l1_wd_0.0001_lr_0.0001_bs_32/'
NORM_TYPE='unity_independent'
INPUT_FOLDER="/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/patient/L506_3mm_sharp/patient_disk_066/"
OUTPUT_FOLDER='./results/patient_disk_066_DnCNN_sg2_8p/lasso_wd/'
python resolve_fly.py --m 'dncnn' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
 --output-folder $OUTPUT_FOLDER --cuda  --normalization-type $NORM_TYPE --input-img-type 'dicom' \
 --specific-epoch --se-plot --gt-folder ' ' --out-dtype 'uint16'

#sg3
MODEL_FOLDER='../w9_exps_4r_didsr/checkpoints/8p_75d_2_50d_qd_p55_uni_ind/augFrFaTdF_2_augTrTaTdF/dncnn/hvd_cpt_for_mse_l1_reg_1e-08_wd_1e-05_lr_0.0001_bs_32/'
NORM_TYPE='unity_independent'
INPUT_FOLDER="/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/patient/L506_3mm_sharp/patient_disk_066/"
OUTPUT_FOLDER='./results/patient_disk_066_DnCNN_sg3_8p/lasso_wd/'
python resolve_fly.py --m 'dncnn' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
 --output-folder $OUTPUT_FOLDER --cuda  --normalization-type $NORM_TYPE --input-img-type 'dicom' \
 --specific-epoch --se-plot --gt-folder ' ' --out-dtype 'uint16'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DnCNN - MSE with L1 prior 
# Learning rate:0.0001 batch size:32 patch size:55
# checkpoint: last one
# trained over realistic augmented as in our augmentation paper (sg3)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
MODEL_FOLDER='../w9_exps_4r_didsr/checkpoints/d95_2_d75_2_d25_p55_uni_ind/augFrFaTdF_2_augTrTaTdT/dncnn/hvd_cpt_for_mse_l1_reg_1e-07_wd_0.0_lr_0.0001_bs_32/'
NORM_TYPE='unity_independent'

INPUT_FOLDER="/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/patient/L506_3mm_sharp/patient_disk_066/"
OUTPUT_FOLDER='./results/patient_disk_066_DnCNN_sg3/'
python resolve_fly.py --m 'dncnn' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
 --output-folder $OUTPUT_FOLDER --cuda  --normalization-type $NORM_TYPE --input-img-type 'dicom' \
 --specific-epoch --se-plot --gt-folder ' ' --out-dtype 'uint16'

INPUT_FOLDER="/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/patient/L506_3mm_sharp/patient_wire_066/"
OUTPUT_FOLDER='./results/patient_wire_066_DnCNN_sg3/'
python resolve_fly.py --m 'dncnn' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
 --output-folder $OUTPUT_FOLDER --cuda  --normalization-type $NORM_TYPE --input-img-type 'dicom' \
 --specific-epoch --se-plot --gt-folder ' ' --out-dtype 'uint16'

INPUT_FOLDER="/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/patient/L506_3mm_sharp/sim_half_066/"
OUTPUT_FOLDER='./results/sim_half_066_DnCNN_sg3/'
python resolve_fly.py --m 'dncnn' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
 --output-folder $OUTPUT_FOLDER --cuda  --normalization-type $NORM_TYPE --input-img-type 'dicom' \
 --specific-epoch --se-plot --gt-folder ' ' --out-dtype 'uint16'

INPUT_FOLDER="/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/patient/L506_3mm_sharp/sim_quarter_066/"
OUTPUT_FOLDER='./results/sim_quarter_066_DnCNN_sg3/'
python resolve_fly.py --m 'dncnn' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
 --output-folder $OUTPUT_FOLDER --cuda  --normalization-type $NORM_TYPE --input-img-type 'dicom' \
 --specific-epoch --se-plot --gt-folder ' ' --out-dtype 'uint16'


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# REDNN - MSE with TV prior 
# Learning rate:0.00001 batch size:64 patch size:96
# checkpoint: last one
# trained over psuedo augmented as in our SPIE paper (sg2)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
MODEL_FOLDER='../w8_exps_4_spie_dose/checkpoints/p96/augTrTaTdT/redcnn/hvd_cpt_for_mse_tv-fbd_wd_0.0_lr_1e-05_bs_64/'
NORM_TYPE='None'

INPUT_FOLDER="/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/patient/L506_3mm_sharp/patient_disk_066/"
OUTPUT_FOLDER='./results/patient_disk_066_REDCNN_sg2/'
python resolve_fly.py --m 'redcnn' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
 --output-folder $OUTPUT_FOLDER --cuda  --normalization-type $NORM_TYPE --input-img-type 'dicom' \
 --specific-epoch --se-plot --gt-folder ' ' --out-dtype 'uint16'

INPUT_FOLDER="/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/patient/L506_3mm_sharp/patient_wire_066/"
OUTPUT_FOLDER='./results/patient_wire_066_REDCNN_sg2/'
python resolve_fly.py --m 'redcnn' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
 --output-folder $OUTPUT_FOLDER --cuda  --normalization-type $NORM_TYPE --input-img-type 'dicom' \
 --specific-epoch --se-plot --gt-folder ' ' --out-dtype 'uint16'

INPUT_FOLDER="/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/patient/L506_3mm_sharp/sim_half_066/"
OUTPUT_FOLDER='./results/sim_half_066_REDCNN_sg2/'
python resolve_fly.py --m 'redcnn' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
 --output-folder $OUTPUT_FOLDER --cuda  --normalization-type $NORM_TYPE --input-img-type 'dicom' \
 --specific-epoch --se-plot --gt-folder ' ' --out-dtype 'uint16'

INPUT_FOLDER="/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/patient/L506_3mm_sharp/sim_quarter_066/"
OUTPUT_FOLDER='./results/sim_quarter_066_REDCNN_sg2/'
python resolve_fly.py --m 'redcnn' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
 --output-folder $OUTPUT_FOLDER --cuda  --normalization-type $NORM_TYPE --input-img-type 'dicom' \
 --specific-epoch --se-plot --gt-folder ' ' --out-dtype 'uint16'
COMMENT
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# REDNN - MSE with TV prior 
# Learning rate:0.00001 batch size:64 patch size:96
# checkpoint: last one
# trained over realistic augmented as in our augmentation paper (sg3)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
MODEL_FOLDER='../w9_exps_4r_didsr/checkpoints/d95_2_d75_2_d25_p96/augFrFaTdF_2_augTrTaTdT/redcnn/hvd_cpt_for_mse_tv-fbd_reg_0.0001_wd_0.0_lr_1e-05_bs_64/'
NORM_TYPE='None'

INPUT_FOLDER="/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/patient/L506_3mm_sharp/patient_disk_066/"
OUTPUT_FOLDER='./results/patient_disk_066_REDCNN_sg3/'
python resolve_fly.py --m 'redcnn' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
 --output-folder $OUTPUT_FOLDER --cuda  --normalization-type $NORM_TYPE --input-img-type 'dicom' \
 --specific-epoch --se-plot --gt-folder ' ' --out-dtype 'uint16'

INPUT_FOLDER="/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/patient/L506_3mm_sharp/patient_wire_066/"
OUTPUT_FOLDER='./results/patient_wire_066_REDCNN_sg3/'
python resolve_fly.py --m 'redcnn' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
 --output-folder $OUTPUT_FOLDER --cuda  --normalization-type $NORM_TYPE --input-img-type 'dicom' \
 --specific-epoch --se-plot --gt-folder ' ' --out-dtype 'uint16'

INPUT_FOLDER="/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/patient/L506_3mm_sharp/sim_half_066/"
OUTPUT_FOLDER='./results/sim_half_066_REDCNN_sg3/'
python resolve_fly.py --m 'redcnn' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
 --output-folder $OUTPUT_FOLDER --cuda  --normalization-type $NORM_TYPE --input-img-type 'dicom' \
 --specific-epoch --se-plot --gt-folder ' ' --out-dtype 'uint16'

INPUT_FOLDER="/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/patient/L506_3mm_sharp/sim_quarter_066/"
OUTPUT_FOLDER='./results/sim_quarter_066_REDCNN_sg3/'
python resolve_fly.py --m 'redcnn' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
 --output-folder $OUTPUT_FOLDER --cuda  --normalization-type $NORM_TYPE --input-img-type 'dicom' \
 --specific-epoch --se-plot --gt-folder ' ' --out-dtype 'uint16'
