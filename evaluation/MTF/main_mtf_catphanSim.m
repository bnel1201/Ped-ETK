%contrast-dependent MTF from catphan scans
clear all;
%Load slice in
addpath('utils')
folder_path = '/gpfs_projects/rxz4/data/DLCT/phantom_sim/for_CT2020Conf/ctp404_proc/'; %Bv44d, Bf32d
folder_path = '/home/brandon.nelson/Data/temp/CTP404/monochromatic/diameter112mm/I0_3000000/fbp_sharp/';
% outfolder = '/home/brandon.nelson/Data/temp/CTP404/rxz_results'
outfolder = folder_path;
parentfolder = dirname(folder_path, 3);
phantom_info = read_phantom_info([parentfolder '/phantom_info_pix_idx.csv']);
ig = read_image_geom_info([parentfolder '/image_geom_info.csv']);
loc = phantom_info(2:end-1, 1:2);

fileinfo = dir(folder_path);
nfile = length(fileinfo)-3;

find_disk_loc = 0;
img_sz = 512;
%display a image to assist a manual localization of the disk area.
if(find_disk_loc==1)
    file1 = [folder_path fileinfo(3).name]
    fid = fopen(file1);
    img = fread(fid,[img_sz img_sz], 'int16');
    fclose(fid);
    imagesc(img',[-500 900]); daspect([1 1 1]); colormap(gray);
    disp 'Go to the figure and click the center of a disk for a ROI cropping.' 
    [xi, yi] = ginput(1);
    loc = [round(xi) round(yi)]
end

disk_radius = phantom_info(2, 3); %first and last disks are special, all middle disks are the measured inserts
roisz = ceil(disk_radius*2*1.5);
roi = round([-roisz/2:roisz/2]);
pixelsz = ig.dx;
fnames_id = fopen([dirname(folder_path, 2) filesep 'results.csv'], 'w');
fprintf(fnames_id, '%s', 'filenames, MTF 50% MTF, 10% MTF');

for i=1:nfile
    i
    filename = fileinfo(i+2).name
    filepath = [folder_path filename];
    fid = fopen(filepath);
    img = fread(fid,[img_sz img_sz], 'int16');
    fclose(fid);
       
    %Crop the disk ROI
    disk_img = double(img(loc(1,1)+roi, loc(1,2)+roi)); %change from unit16 to double
    
    %estimate the MTF
    [mtf, freq] = MTF_from_disk_edge(disk_img);
    
    %mtf_all(i,:) = mtf;
    freq_vector = freq/pixelsz;
    %freq_all(i,:) = freq_vector;
    write_MTF([dirname(folder_path, 2) filesep filename], freq, mtf);
    %Estimate the mtf50% and mtf10% values
    mtf50_all(i) = MTF_width(mtf, 0.5, freq_vector)
    mtf10_all(i) = MTF_width(mtf, 0.1, freq_vector)

    fprintf(fnames_id, '\r\n%s, ', filename);
    fprintf(fnames_id, '%3.5g, %3.5g', [mtf50_all(i), mtf10_all(i)]);
end
fclose(fnames_id);
% write_results([outfolder '/results.csv'], mtf50_all, mtf10_all);

