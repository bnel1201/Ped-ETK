function ig = read_image_geom_info(filename)
    out = importdata(filename);
    ig = image_geom('nx', out.data(1), 'fov', out.data(end-1), 'down', out.data(end));
end