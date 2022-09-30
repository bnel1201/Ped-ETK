BASEDIR=/gpfs_projects/brandon.nelson/DLIR_Ped_Generalizability/geomtric_phantom_studies/CTP404/monochromatic
MTF_RESULTS=evaluation/MTF/results

.PHONY : results
results : 
	bash evaluation/run_all_evaluations.sh

.PHONY : phantoms
phantoms : $(BASEDIR)/diameter112mm/I0_3000000/fbp_sharp/fbp_sharp_v001.raw
	bash ssh_node.sh "cd make_phantoms; bash ./run_make_phantoms.sh; exit; cd .."

.PHONY : plots
plots : $(MTF_RESULTS)/plots/fbp_mtf_baseline.png $(MTF_RESULTS)/plots/mtf_redcnn.png $(MTF_RESULTS)/plots/mtf_cutoff_vals.png $(MTF_RESULTS)/plots/mtf_cutoff_vals_processed.png

# plot MTF curves
$(MTF_RESULTS)/plots/fbp_mtf_baseline.png : $(BASEDIR)/diameter112mm/I0_3000000/fbp_sharp_v001_mtf.csv
	python evaluation/MTF/plot_mtf_curves.py $^ -o $@

$(MTF_RESULTS)/plots/mtf_redcnn.png : $(BASEDIR)/diameter112mm/I0_3000000_processed/fbp_sharp_v001_mtf.csv
	python evaluation/MTF/plot_mtf_curves.py $^ -o $@ --processed

# plot MTF cutoff values

$(MTF_RESULTS)/plots/mtf_cutoff_vals.png : $(BASEDIR)/diameter112mm/I0_3000000/results_MTF50.csv
	python evaluation/MTF/plot_mtf_cutoffs.py $^ -o $@

$(MTF_RESULTS)/plots/mtf_cutoff_vals_processed.png : $(BASEDIR)/diameter112mm/I0_3000000_processed/results_MTF50.csv
	python evaluation/MTF/plot_mtf_cutoffs.py $^ -o $@ --processed

.PHONY : clean
clean :
	rm -rf results