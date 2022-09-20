.PHONY : phantoms
	matlab -nodesktop -nosplash make_phantoms/make_phantoms.m

# .PHONY : denoise
denoise : 
	bash denoising/run_denoising.sh

evaluate : 
	