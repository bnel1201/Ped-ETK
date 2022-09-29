output_file=results/.gif
/usr/bin/ffmpeg -f image2 -pattern_type glob -framerate 0.7 -y -i 'results/images/diameter*mm_image_comparison.png' -vf "scale=1000:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" $output_file
