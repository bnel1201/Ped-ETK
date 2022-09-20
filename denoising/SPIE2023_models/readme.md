To run
-----------
# ssh to "didsr-wk46-031"
$ cd /gpfs_projects/prabhat.kc/lowdosect/transfers/transfers_4_spie/exps/exps/exps_4r_phan_insert/
$ source .bashrc4rhorovod
$ conda activate office2dosewcu10
$ chmod +x resolve_exe.sh
$ ./resolve_exe.sh

# resolve_exe.sh has summary header like loss function, learning rate, batch size, patch size on each network
# you can change parameters like ‘output data type’, checkpoints in resolve_exe.sh 
# you can also point ground truth folder in resolve_exe.sh as 
--gt-folder ‘/ground_truth_imgs/
# to obtain global metric values that will be automatically exported as “quat_file.txt”


Processed outputs
--------------------------------
# all the results are in result folder 
# SPIE trained results are tagged (_CNN3, _GAN, _Unet, _DnCNN_st2, REDCNN_st2)
# dose augmented results are tagged (_DnCNN_st3, REDCNN_st3)
