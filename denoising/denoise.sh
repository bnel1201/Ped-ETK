#------------------------------------------------------------------------------------------------------------------#
#  									OPTIONS
#------------------------------------------------------------------------------------------------------------------#
<< COMMENT
usage: resolve_fld.py [-h] [--model-name MODEL_NAME] --input-folder
                      INPUT_FOLDER --gt-folder GT_FOLDER --model-folder
                      MODEL_FOLDER [--output-folder OUTPUT_FOLDER]
                      --normalization-type NORMALIZATION_TYPE [--cuda]
                      [--dicom-input] [--specific-epoch]
                      [--chckpt-no CHCKPT_NO] [--se-plot]

PyTorch application of trained weight on patient dicom images

command line arguments:
  -h, --help            show this help message and exit
  --model-name MODEL_NAME, --m MODEL_NAME
                        choose the network architecture name that you are
                        going to use. Options include redcnn, dncnn,
                        unet, three_layers.
  --input-folder INPUT_FOLDER
                        directory name containing noisy input test images.
  --gt-folder GT_FOLDER
                        directory name containing test Ground Truth images.
  --model-folder MODEL_FOLDER
                        directory name containing saved checkpoints.
  --output-folder OUTPUT_FOLDER
                        path to save the output results.
  --normalization-type NORMALIZATION_TYPE
                        normalization stipulated while training weights.
  --cuda                use cuda.
  --dicom-input         If input images are in dicom format.
  --specific-epoch      If true only one specific epoch based on the chckpt-no
                        will be applied to test images. Else all checkpoints
                        (or every saved checkpoints corresponding to each
                        epoch) will be applied to test images.
  --chckpt-no CHCKPT_NO
                        epoch no. of the checkpoint to be loaded to be applied
                        to noisy images from the test set. Default is the last
                        epoch
  --se-plot             If true denoised images from test set is saved inside
                        the output-folder. Else only test stats are saved in
                        .txt format inside the output-folder.
COMMENT

INPUT_FOLDER=$1
OUTPUT_FOLDER=$2
MODEL_FOLDER=${3-'/gpfs_projects/prabhat.kc/lowdosect/transfers/transfers_4_spie/exps/exps/w8_exps_4_spie_dose/checkpoints/p96/augTrTaTdT/redcnn/hvd_cpt_for_mse_tv-fbd_wd_0.0_lr_1e-05_bs_64/'}

orginal_dir=$(pwd)
cd $(dirname $0)
# on CTP404 Contrast Dependent MTF phantom

NORM_TYPE='None'
python SPIE2023_models/resolve_fly.py --m 'redcnn' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
--output-folder $OUTPUT_FOLDER \
--normalization-type $NORM_TYPE --input-img-type 'raw' --specific-epoch --se-plot

cd $orginal_dir