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


# ----------------------------------------------------#
# trained CNN3 weights applied on test set
# adapted from </gpfs_projects/prabhat.kc/lowdosect/coderepo/DLIR_v1_public/traintest/nonGAN/demo_test.sh>
# ----------------------------------------------------#
# specify the model of interest as the first input argument, else the default model below is taken
MODEL_FOLDER=${1-'/gpfs_projects/prabhat.kc/lowdosect/transfers/transfers_4_spie/exps/exps/w8_exps_4_spie_dose/checkpoints/p96/augTrTaTdT/redcnn/hvd_cpt_for_mse_tv-fbd_wd_0.0_lr_1e-05_bs_64/'}

PHANTOM=CCT189
# PHANTOM=CTP404

DOSELEVEL=I0_0300000
BASE_DIR=/home/brandon.nelson/Data/temp/
# BASE_DIR=/gpfs_projects/brandon.nelson/DLIR_Ped_Generalizability/geomtric_phantom_studies/
orginal_dir=$(pwd)
cd $(dirname $0)
for DIAMETER in 112 131 151 185 216 292
do
   echo $DIAMETER
   for OBJ in disk bkg
   do
   INPUT_FOLDER="${BASE_DIR}"/$PHANTOM/monochromatic/diameter"${DIAMETER}"mm/"${DOSELEVEL}"/$OBJ/
   OUTPUT_FOLDER="${BASE_DIR}"/$PHANTOM/monochromatic/diameter"${DIAMETER}"mm/"${DOSELEVEL}"_processed/$OBJ/
   
   NORM_TYPE='None'
   python SPIE2023_models/resolve_fly.py --m 'redcnn' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
   --output-folder $OUTPUT_FOLDER \
   --normalization-type $NORM_TYPE --input-img-type 'raw' --specific-epoch --se-plot

   # reorganize output files for evaluation scripts
   mkdir -p $OUTPUT_FOLDER/
   mv $OUTPUT_FOLDER/checkpoint-25/*.raw $OUTPUT_FOLDER/
   rm -r $OUTPUT_FOLDER/checkpoint-25
   done
done

cd $orginal_dir