function [status] = write_MTF(filename, freq, mtf)
    fname_stem = filename(1:end-length('.raw'));
    filename_out = [fname_stem '_mtf.csv'];
    fid = fopen(filename_out, 'w');
    fprintf(fid, 'frequencies [1/mm], MTF\r\n');
    formatSpec = '%3.5g, %3.5g \r\n';
    fprintf(fid, formatSpec, [freq; mtf]);
    status = fclose(fid);
end