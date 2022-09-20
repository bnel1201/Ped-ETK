# for mtf as well as nps, resolve_fly is used instead of resolve_mtf_scaled.py or
# resolve_mtf_normalize as wire/uniform data although int16 has min value of 0

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CNN3 - MSE with L1 prior 
# Learning rate:0.001 batch size:128 patch size:55
# trained over psuedo augmented as in our SPIE paper
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
<<COMMENT
MODEL_FOLDER='../w8_exps_4_spie_dose/checkpoints/p55/augTrTaTdT/three_layers/hvd_cpt_for_mse_l1_wd_0.0_lr_0.001_bs_128/'
NORM_TYPE=None

INPUT_FOLDER="/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/wire/"
OUTPUT_FOLDER='./results/wire_CNN3/'
python resolve_fly.py --m 'three_layers' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
--output-folder $OUTPUT_FOLDER --cuda --normalization-type $NORM_TYPE --specific-epoch --se-plot \
--input-img-type 'raw' --gt-folder '' --out-dtype 'int16'

INPUT_FOLDER="/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/uniform_half/"
OUTPUT_FOLDER='./results/uniform_half_CNN3/'
python resolve_fly.py --m 'three_layers' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
--output-folder $OUTPUT_FOLDER --cuda --normalization-type $NORM_TYPE --specific-epoch --se-plot \
--input-img-type 'raw' --gt-folder '' --out-dtype 'int16'

INPUT_FOLDER="/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/uniform_quarter/"
OUTPUT_FOLDER='./results/uniform_quarter_CNN3/'
python resolve_fly.py --m 'three_layers' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
--output-folder $OUTPUT_FOLDER --cuda --normalization-type $NORM_TYPE --specific-epoch --se-plot \
--input-img-type 'raw' --gt-folder '' --out-dtype 'int16'


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# UNet - MSE with L1 prior 
# Learning rate:0.001 batch size:64 patch size:55
# checkpoint 6
# trained over psuedo augmented as in our SPIE paper
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
MODEL_FOLDER='../w8_exps_4_spie_dose/checkpoints/p55_uni_ind/augTrTaTdT/unet/hvd_cpt_for_mse_l1_wd_0.0_lr_0.001_bs_64/'
NORM_TYPE='unity_independent'

INPUT_FOLDER="/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/wire/"
OUTPUT_FOLDER='./results/wire_UNet/'
python resolve_fly.py --m 'unet' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
 --output-folder $OUTPUT_FOLDER --cuda --normalization-type $NORM_TYPE --input-img-type 'raw' \
 --specific-epoch --se-plot --chckpt-no 6 --gt-folder ' ' --out-dtype 'int16'

INPUT_FOLDER="/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/uniform_half/"
OUTPUT_FOLDER='./results/uniform_half_UNet/'
python resolve_fly.py --m 'unet' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
 --output-folder $OUTPUT_FOLDER --cuda --normalization-type $NORM_TYPE --input-img-type 'raw' \
 --specific-epoch --se-plot --chckpt-no 6 --gt-folder ' ' --out-dtype 'int16'

INPUT_FOLDER="/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/uniform_quarter/"
OUTPUT_FOLDER='./results/uniform_quarter_UNet/'
python resolve_fly.py --m 'unet' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
 --output-folder $OUTPUT_FOLDER --cuda --normalization-type $NORM_TYPE --input-img-type 'raw' \
 --specific-epoch --se-plot --chckpt-no 6 --gt-folder ' ' --out-dtype 'int16'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GAN
# Learning rate:0.0001 batch size:32 patch size:55
# checkpoint 18
# trained over psuedo augmented as in our SPIE paper
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
MODEL_FOLDER='../../gan/GAN-dn2/checkpoints/uni_ind/augment/augTrTaTdT_p55_32_lr_0.0001/'
NORM_TYPE='unity_independent'

INPUT_FOLDER="/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/wire/"
OUTPUT_FOLDER='./results/wire_GAN/'
python resolve_fly.py --m 'simpleGAN' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
 --gt-folder ' ' --output-folder $OUTPUT_FOLDER --cuda --normalization-type $NORM_TYPE --input-img-type 'raw' \
 --specific-epoch --chckpt-no 18 --se-plot  --out-dtype 'int16'

INPUT_FOLDER="/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/uniform_half/"
OUTPUT_FOLDER='./results/uniform_half_GAN/'
python resolve_fly.py --m 'simpleGAN' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
 --gt-folder ' ' --output-folder $OUTPUT_FOLDER --cuda --normalization-type $NORM_TYPE --input-img-type 'raw' \
 --specific-epoch --chckpt-no 18 --se-plot  --out-dtype 'int16'

INPUT_FOLDER="/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/uniform_quarter/"
OUTPUT_FOLDER='./results/uniform_quarter_GAN/'
python resolve_fly.py --m 'simpleGAN' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
 --gt-folder ' ' --output-folder $OUTPUT_FOLDER --cuda --normalization-type $NORM_TYPE --input-img-type 'raw' \
 --specific-epoch --chckpt-no 18 --se-plot  --out-dtype 'int16'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DnCNN - MSE with L1 prior 
# Learning rate:0.0001 batch size:32 patch size:55
# checkpoint: last one
# trained over psuedo augmented as in our SPIE paper (sg2)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
MODEL_FOLDER='../w8_exps_4_spie_dose/checkpoints/p55_uni_ind/augTrTaTdT/dncnn/hvd_cpt_for_mse_l1_wd_0.0_lr_0.0001_bs_32/'
NORM_TYPE='unity_independent'

INPUT_FOLDER="/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/wire/"
OUTPUT_FOLDER='./results/wire_DnCNN_sg2/'
python resolve_fly.py --m 'dncnn' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
 --output-folder $OUTPUT_FOLDER --cuda  --normalization-type $NORM_TYPE --input-img-type 'raw' \
 --specific-epoch --se-plot --gt-folder ' ' --out-dtype 'int16'

INPUT_FOLDER="/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/uniform_half/"
OUTPUT_FOLDER='./results/uniform_half_DnCNN_sg2/'
python resolve_fly.py --m 'dncnn' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
 --output-folder $OUTPUT_FOLDER --cuda  --normalization-type $NORM_TYPE --input-img-type 'raw' \
 --specific-epoch --se-plot --gt-folder ' ' --out-dtype 'int16'

INPUT_FOLDER="/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/uniform_quarter/"
OUTPUT_FOLDER='./results/uniform_quarter_DnCNN_sg2/'
python resolve_fly.py --m 'dncnn' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
 --output-folder $OUTPUT_FOLDER --cuda  --normalization-type $NORM_TYPE --input-img-type 'raw' \
 --specific-epoch --se-plot --gt-folder ' ' --out-dtype 'int16'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DnCNN - MSE with L1 prior 
# Learning rate:0.0001 batch size:32 patch size:55
# checkpoint: last one
# trained over realistic augmented as in our augmentation paper (sg3)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
MODEL_FOLDER='../w9_exps_4r_didsr/checkpoints/d95_2_d75_2_d25_p55_uni_ind/augFrFaTdF_2_augTrTaTdT/dncnn/hvd_cpt_for_mse_l1_reg_1e-07_wd_0.0_lr_0.0001_bs_32/'
NORM_TYPE='unity_independent'

INPUT_FOLDER="/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/wire/"
OUTPUT_FOLDER='./results/wire_DnCNN_sg3/'
python resolve_fly.py --m 'dncnn' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
 --output-folder $OUTPUT_FOLDER --cuda  --normalization-type $NORM_TYPE --input-img-type 'raw' \
 --specific-epoch --se-plot --gt-folder ' ' --out-dtype 'int16'

INPUT_FOLDER="/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/uniform_half/"
OUTPUT_FOLDER='./results/uniform_half_DnCNN_sg3/'
python resolve_fly.py --m 'dncnn' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
 --output-folder $OUTPUT_FOLDER --cuda  --normalization-type $NORM_TYPE --input-img-type 'raw' \
 --specific-epoch --se-plot --gt-folder ' ' --out-dtype 'int16'

INPUT_FOLDER="/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/uniform_quarter/"
OUTPUT_FOLDER='./results/uniform_quarter_DnCNN_sg3/'
python resolve_fly.py --m 'dncnn' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
 --output-folder $OUTPUT_FOLDER --cuda  --normalization-type $NORM_TYPE --input-img-type 'raw' \
 --specific-epoch --se-plot --gt-folder ' ' --out-dtype 'int16'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# REDNN - MSE with TV prior 
# Learning rate:0.00001 batch size:64 patch size:96
# checkpoint: last one
# trained over psuedo augmented as in our SPIE paper (sg2)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
MODEL_FOLDER='../w8_exps_4_spie_dose/checkpoints/p96/augTrTaTdT/redcnn/hvd_cpt_for_mse_tv-fbd_wd_0.0_lr_1e-05_bs_64/'
NORM_TYPE='None'

INPUT_FOLDER="/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/wire/"
OUTPUT_FOLDER='./results/wire_REDCNN_sg2/'
python resolve_fly.py --m 'redcnn' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
 --output-folder $OUTPUT_FOLDER --cuda  --normalization-type $NORM_TYPE --input-img-type 'raw' \
 --specific-epoch --se-plot --gt-folder ' ' --out-dtype 'int16'

INPUT_FOLDER="/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/uniform_half/"
OUTPUT_FOLDER='./results/uniform_half_REDCNN_sg2/'
python resolve_fly.py --m 'redcnn' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
 --output-folder $OUTPUT_FOLDER --cuda  --normalization-type $NORM_TYPE --input-img-type 'raw' \
 --specific-epoch --se-plot --gt-folder ' ' --out-dtype 'int16'

INPUT_FOLDER="/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/uniform_quarter/"
OUTPUT_FOLDER='./results/uniform_quarter_REDCNN_sg2/'
python resolve_fly.py --m 'redcnn' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
 --output-folder $OUTPUT_FOLDER --cuda  --normalization-type $NORM_TYPE --input-img-type 'raw' \
 --specific-epoch --se-plot --gt-folder ' ' --out-dtype 'int16'
COMMENT

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# REDNN - MSE with TV prior 
# Learning rate:0.00001 batch size:64 patch size:96
# checkpoint: last one
# trained over realistic augmented as in our augmentation paper (sg3)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
MODEL_FOLDER='../w9_exps_4r_didsr/checkpoints/d95_2_d75_2_d25_p96/augFrFaTdF_2_augTrTaTdT/redcnn/hvd_cpt_for_mse_tv-fbd_reg_0.0001_wd_0.0_lr_1e-05_bs_64/'
NORM_TYPE='None'

INPUT_FOLDER="/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/wire/"
OUTPUT_FOLDER='./results/wire_REDCNN_sg3/'
python resolve_fly.py --m 'redcnn' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
 --output-folder $OUTPUT_FOLDER --cuda  --normalization-type $NORM_TYPE --input-img-type 'raw' \
 --specific-epoch --se-plot --gt-folder ' ' --out-dtype 'int16'

INPUT_FOLDER="/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/uniform_half/"
OUTPUT_FOLDER='./results/uniform_half_REDCNN_sg3/'
python resolve_fly.py --m 'redcnn' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
 --output-folder $OUTPUT_FOLDER --cuda  --normalization-type $NORM_TYPE --input-img-type 'raw' \
 --specific-epoch --se-plot --gt-folder ' ' --out-dtype 'int16'

INPUT_FOLDER="/gpfs_projects/rxz4/data/DLCT/phantom_sim/2022/uniform_quarter/"
OUTPUT_FOLDER='./results/uniform_quarter_REDCNN_sg3/'
python resolve_fly.py --m 'redcnn' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
 --output-folder $OUTPUT_FOLDER --cuda  --normalization-type $NORM_TYPE --input-img-type 'raw' \
 --specific-epoch --se-plot --gt-folder ' ' --out-dtype 'int16'