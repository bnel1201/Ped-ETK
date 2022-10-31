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

MODEL_FOLDER=$1

orginal_dir=$(pwd)
cd $(dirname $0)
# on CTP404 Contrast Dependent MTF phantom
for DIAMETER in 112 131 151 185 216 292
do
   for DOSELEVEL in 3000000
   do
      echo $DIAMETER $DOSELEVEL
      INPUT_FOLDER=/gpfs_projects/brandon.nelson/DLIR_Ped_Generalizability/geomtric_phantom_studies/CTP404/monochromatic/diameter"${DIAMETER}"mm/I0_"${DOSELEVEL}"/fbp_sharp/
      OUTPUT_FOLDER=/gpfs_projects/brandon.nelson/DLIR_Ped_Generalizability/geomtric_phantom_studies/CTP404/monochromatic/diameter"${DIAMETER}"mm/I0_"${DOSELEVEL}"_processed/

      NORM_TYPE='None'
      python SPIE2023_models/resolve_fly.py --m 'redcnn' --input-folder $INPUT_FOLDER --model-folder $MODEL_FOLDER \
      --output-folder $OUTPUT_FOLDER \
      --normalization-type $NORM_TYPE --input-img-type 'raw' --specific-epoch --se-plot

      # reorganize output files for evaluation scripts
      mkdir -p $OUTPUT_FOLDER/fbp_sharp
      mv $OUTPUT_FOLDER/checkpoint-25/*.raw $OUTPUT_FOLDER/fbp_sharp/
      rm -r $OUTPUT_FOLDER/checkpoint-25
   done
done

cd $orginal_dir