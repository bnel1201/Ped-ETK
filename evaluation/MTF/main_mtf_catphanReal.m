%contrast-dependent MTF from catphan physical scans

clear all;
%Load slice in
highdose=1;
%folder_path = '/gpfs_projects/rxz4/data/DLCT/phantom_realscan/NIH_Catphan600_Mar2020/3941_high/3949/'; 
%folder_path = '/gpfs_projects/rxz4/data/DLCT/phantom_realscan/NIH_Catphan600_Mar2020/redcnn_processed/3941_high/smoothM1-R0-S3/3945/'; 
highdose=0;
%folder_path = '/gpfs_projects/rxz4/data/DLCT/phantom_realscan/NIH_Catphan600_Mar2020/redcnn_processed/4021_full/smoothM1-R0-S3/4022/'; 
folder_path = '/gpfs_projects/rxz4/data/DLCT/phantom_realscan/NIH_Catphan600_Mar2020/redcnn_processed/4031_low/smoothM1-R0-S3/4032/'; 

fileinfo = dir(folder_path);
nfile = length(fileinfo)-2;
%sort the filename in asending order
for i=1:nfile
    filename = fileinfo(i+2).name;
    filenum(i) = str2num(filename);
end
[dummy,order] = sort(filenum,'ascend');

if(~highdose) %somehow the slice number is reversed with the file number for full and low 
	[dummy,order] = sort(filenum,'descend');
end

nCTP = 5; %number of usable slices of CTP404: 5 for 3mm, 15 for 1mm.
nstart = 15; %starting slice of CTP404: 15 for 3mm, 45 for 1mm

find_disk_loc = 0;
%display a image to assist a manual localization of the disk area.
file1 = [folder_path fileinfo(order(nstart)+2).name]
img = dicomread(file1);
info = dicominfo(file1);
%img = img + info.RescaleIntercept;
if(find_disk_loc==1)
    imagesc(img',[900 1500]); daspect([1 1 1]); colormap(gray);
    disp 'Go to the figure and click the center of a disk for a ROI cropping.' 
    [xi, yi] = ginput(1);
    locs = [round(xi) round(yi)];
else
    locs=[338 253; 328 294; 261 333; 191 294]; %[191 213]; %B30f-3mm-380mm-FBP 990HU disk [327 214]. 
   % loc=[370 191]; %B30f-3mm-240mm-FBP 990HU disk [370 191].
end
 n_locs = size(locs,1);    

pixelsz = info.PixelSpacing(1);
roisz = 2*round(12/pixelsz); %The contrast rod has a diameter of 12mm.
roi = [-roisz/2:roisz/2];
disk = zeros(length(roi), length(roi),nCTP); 

for i=1:nCTP
    i
    filename = fileinfo(order(nstart+i-1)+2).name
    filepath = [folder_path filename];
    img = dicomread(filepath);%+ info.RescaleIntercept;
    
    for j = 1:n_locs
    	loc = locs(j,:);   
    	%Crop the disk ROI
    	disk_img = double(img(loc(1)+roi, loc(2)+roi)); %change from unit16 to double
    	disk_HU(i,j) = mean(mean(disk_img(roisz/2+[-1:1],roisz/2+[-1:1])));
    	%disk(:,:,i) = disk_img;

    	%estimate the MTF
    	[mtfi, freqi] = MTF_from_disk_edge(disk_img);
    
    	mtf_all{i,j} = mtfi;
    	freqi = freqi/pixelsz;
   	freq_all{i,j} = freqi;
    
    %Estimate the mtf50% and mtf10% values
    	mtf50_all(i,j) = MTF_width(mtfi, 0.5, freqi);
    	mtf10_all(i,j) = MTF_width(mtfi, 0.1, freqi);
    end
end
[mean(mtf50_all) std(mtf50_all)]
[mean(mtf10_all) std(mtf10_all)]
disk_HU-1100 %1100 is the background HU


%test another way: combine the disk images together to estimate a single mtf
%this approach seems to way underestimate the mtf values.
%[mtf, freq] = MTF_from_disk_edge(disk);
%mtf50 = MTF_width(mtf, 0.5, freq);
%mtf10 = MTF_width(mtf, 0.1, freq);
