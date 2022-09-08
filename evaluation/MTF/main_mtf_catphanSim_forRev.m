%contrast-dependent MTF from catphan scans
clear all;
%Load slice in
folder_path = '/gpfs_projects/rxz4/data/DLCT/phantom_sim/for_CT2020Conf/ctp404_proc/forPaperRev/'; %Bv44d, Bf32d
%filename = 'ctp404_fbp_smooth_256_smoothM1-R0-S3proc.raw'; %noiseless

find_disk_loc = 0;
%display a image to assist a manual localization of the disk area.
if(find_disk_loc==1)
    file1 = [folder_path fileinfo(3).name]
    fid = fopen(file1);
    img = fread(fid,[256 256], 'int16');
    fclose(fid);
    imagesc(img',[-500 900]); daspect([1 1 1]); colormap(gray);
    disp 'Go to the figure and click the center of a disk for a ROI cropping.' 
    [xi, yi] = ginput(1);
    loc = [round(xi) round(yi)];
else
    loc=[67 190; 43 129; 189 189; 68 68; 190 68]; %990, 340, 200, 120 35 HU disks
    nloc= size(loc,1);
end
    

roisz = 28;
roi = [-roisz/2:roisz/2];
pixelsz = 0.6641; %See code make_CTP404_wD45_B30.m;

img_old=0;
for i=1:5
    filename = ['ctp404_fbp_smooth_256_noisyI' num2str(i) '_smoothM1-R0-S3proc.raw']; %noisy
    filename = ['ctp404_fbp_sharp_256_noisyI' num2str(i) '_sharpM1-R0-S3proc.raw'];
    filepath = [folder_path filename]
    fid = fopen(filepath);
    img = fread(fid,[256 256], 'int16');
    fclose(fid);
    isequal(img_old, img)
    img_old = img;
    
    for j=1:nloc     
       %Crop the disk ROI
       disk_img = double(img(loc(j,1)+roi, loc(j,2)+roi)); %change from unit16 to double
       disk_HU(i,j) = mean(mean(disk_img(roisz/2+[-1:1],roisz/2+[-1:1])));

       %estimate the MTF
       [mtf, freq] = MTF_from_disk_edge(disk_img);
    
       
       freq_vector = freq/pixelsz;
      
    
       %Estimate the mtf50% and mtf10% values
       mtf50_all(i,j) = MTF_width(mtf, 0.5, freq_vector);
       mtf10_all(i,j) = MTF_width(mtf, 0.1, freq_vector);
    end
end
