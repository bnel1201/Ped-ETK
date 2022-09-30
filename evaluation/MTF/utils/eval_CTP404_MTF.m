addpath('/home/brandon.nelson/Dev/PhantomSimulations/CT_simulator')
if ~exist('homedir', 'var') %checks if setpath has been run
    setpath
end
if ~exist('folder_path', 'var')
    folder_path = '/home/brandon.nelson/Data/temp/CTP404/monochromatic/diameter112mm/I0_3000000/fbp_sharp/';
end

addpath([dirname(fileparts(mfilename('fullpath')), 2) '/utils'])

outfolder = folder_path;
parentfolder = dirname(folder_path, 3);
phantom_info = read_phantom_info([parentfolder '/phantom_info_pix_idx.csv']);
ig = read_geometry_info([parentfolder '/geometry_info.csv']);
loc = phantom_info(2:end-1, 1:2);

ii = importdata([parentfolder '/image_info.csv']);
offset = ii.data;
img_sz = ig.nx;
fileinfo = dir(folder_path);
nfile = length(fileinfo)-2;

find_disk_loc = 0;

%display a image to assist a manual localization of the disk area.
if(find_disk_loc==1)
    file1 = [folder_path fileinfo(3).name]
    loc = gget_loc(file1, img_sz)
end

disk_radius = phantom_info(2, 3); %first and last disks are special, all middle disks are the measured inserts
water_atten = phantom_info(1, 6);
disk_HUs = sort(1000*(phantom_info(2:9,6))/water_atten);
roisz = ceil(disk_radius*2*1.6);
roi = round([-roisz/2:roisz/2]);
pixelsz = ig.dx;

fnames_MTF50_id = fopen([dirname(folder_path, 2) filesep 'results_MTF50.csv'], 'w');
fprintf(fnames_MTF50_id, '%s', 'filenames');
for hu_idx = 1:length(disk_HUs)
    fprintf(fnames_MTF50_id, ', %d HU', disk_HUs(hu_idx));
end

fnames_MTF10_id = fopen([dirname(folder_path, 2) filesep 'results_MTF10.csv'], 'w');
fprintf(fnames_MTF10_id, '%s', 'filenames');
for hu_idx = 1:length(disk_HUs)
    fprintf(fnames_MTF10_id, ', %d HU', disk_HUs(hu_idx));
end

for i=1:nfile
    disp(['Simulation [' num2str(i) '/' num2str(nfile) ']'])
    filename = fileinfo(i+2).name;
    filepath = [folder_path filename];
    fid = fopen(filepath);
    img = fread(fid,[img_sz img_sz], 'int16') - offset;
    fclose(fid);
       
    fprintf(fnames_MTF50_id, '\r\n%s', filename);
    fprintf(fnames_MTF10_id, '\r\n%s', filename);

    mtf_fid = fopen([dirname(folder_path, 2) filesep filename(1:end-4) '_mtf.csv'], 'w');
    esf_fid = fopen([dirname(folder_path, 2) filesep filename(1:end-4) '_esf.csv'], 'w');

    fprintf(mtf_fid, 'frequencies [1/mm]');
    fprintf(mtf_fid, ', %d HU', round(disk_HUs));
    fprintf(esf_fid, 'distance [mm]');
    fprintf(esf_fid, ', %d HU', round(disk_HUs));

    for j=1:length(loc)
        %Crop the disk ROI
        disk_img = double(img(loc(j,1)+roi, loc(j,2)+roi)); %change from unit16 to double
        expected_HU = round(disk_HUs(j));
        measured_HU = round(mean(mean(disk_img(floor(disk_radius):end-floor(disk_radius), floor(disk_radius):end-floor(disk_radius)))));
        disp(['     ' num2str(expected_HU) ' HU disk (actual: ' num2str(measured_HU) ' HU) [' num2str(j) '/' num2str(length(disk_HUs)) ']'])
        if abs((measured_HU - expected_HU)/expected_HU) > 0.01
            disp(sprintf('Warning: Measured Disk HUs (%d HU) do not match expected (%d HU)', measured_HU, expected_HU))
        end
        %estimate the MTF
        [mtf, freq, esf] = MTF_from_disk_edge(disk_img);

        freq_vector = freq/pixelsz;
        dist_vector = ig.dx*(0:length(esf)-1);

        if j == 1
            mtf_data(1, :) = freq_vector;
            esf_data(1, :) = dist_vector;
        end
        if length(mtf) ~= length(mtf_data)
            mtf_data(j + 1, :) = interp1(freq_vector, mtf, mtf_data(1, :)); % <-- double check this later... meant to account for slight differences in array length from MTF_from_disk_edge due to rounding errors
        else
            mtf_data(j + 1, :) = mtf;
        end
        esf_data(j + 1, :) = esf;

        %Estimate the mtf50% and mtf10% values
        mtf50_all(i, j) = MTF_width(mtf, 0.5, freq_vector);
        mtf10_all(i, j) = MTF_width(mtf, 0.1, freq_vector);

        fprintf(fnames_MTF50_id, ', %3.5g', [mtf50_all(i, j)]);
        fprintf(fnames_MTF10_id, ', %3.5g', [mtf10_all(i, j)]);
    end
    fprintf(mtf_fid, ['\r\n%3.5g' repmat(', %3.5g', 1, length(disk_HUs))], mtf_data);
    fclose(mtf_fid);

    fprintf(esf_fid, ['\r\n%3.5g' repmat(', %3.5g', 1, length(disk_HUs))], esf_data);
    fclose(esf_fid);

end
fclose(fnames_MTF50_id);
fclose(fnames_MTF10_id);
