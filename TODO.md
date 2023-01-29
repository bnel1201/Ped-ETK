# TODOs

Priorities:

1. finish cleaning up figures and write manuscript draft
2. finish code clean up and refactor into RST *after* first draft while co-authors are editing

## converting to RST

### LCD module

Building upon the existing [DIDSR MO repo](https://github.com/DIDSR/VICTRE_MO)

- [ ] change input  of LCD module to be more flexible, they should just be a mask (truth mask) or pixel coordinates of the signal known exactly
- [ ] add additional filters so users can switch between LGO and Gabor, etc... (Rongping working on this)

## make it work

Top priority, making sure all results are there and are consistent (reliable/robust)

- [X] make sure LCD results are consistent with adults (5 dose levels)
- [ ] clean up `plot_LCD_results.py` its a mess... XD
- [ ] line 91 eval_CTP404_MTF.m% <-- double check this later, that the interp1 is working as intended meant to account for slight differences in array length from MTF_from_disk_edge due to rounding errors

- [X] Clean up code and make sure everything runs to completion (make it work)
- [X] Update results slides
- [X] Then make every piece modular by figuring out the min requirements for each (LCD and MTF both expect disk centers and radii), all require directories with raw images
- [X] The. I want everything accessible via config files. I want to be able to quickly add lower dose levels and see how that changes detect ability
- [ ] Add representative anthropomorphic phantom noise/MSE reduction results
  - [X] MSE against ground truth phantom
  - [x] organize by age and size (join data into csv for easy comparison)
  - [ ] Fix FOV from being fixed to adaptive based on phantom size
  - [ ] convert code oo saving out CSV files rather than h5 (use additional filter columns to encode multiple dimensions)

## make it right

- [X] include WED (TG 220 Eq 4b) to patient info csv
- [X] need to make sure I am getting the right diameter and FOV for the patient as this is important to performance, either measure it nowing pixel size or from XCAT, it's currently wrong because some images are way too zoomed in or out...
  - [X] make fixed FOV again (e.g. 340 or 480 mm, probs 480), then use that to measure diameter and make adapted FOV
- [X] replace adult reference to be adult size and adult FOV (CCT189 200mm 340mm FOV; CTP404 150mm 340mm FOV) From Rongping: "The reference images I created was based on 340mm FOV (pixel size of 340/512=0.66). I think I set the pixel size to be 0.66, if I remembered correctly"
- [ ] Consider saving out all generated CT simulation data in a database of CSV file so its easy to see what images were simulated in terms of: patient diameter, FOV, scanner, recon details, this would be saved out in the results folder under a  "simulation heading". Currently I have the Reference adult scans undergo the same processing but have a different FOV and a change the directory name, but this couples the phantom generation + CT sim with the analysis, ideally these would be decoupled which could be accomplished if I saved out all of this info and then in my analysis I could select which scans I want to use as baseline reference
  - [ ] include results summary in this csv file too (thus can assess image quality performance against age, size, WED, ....):
    - [ ] noise variance
    - [X] NPS peak
    - [x] MTF 50
    - [ ] MTF 25
    - [X] MTF 10
    - [ ] LCD auc (convert fro  h5 to csv in `eval_lcd_catphanSim.m`)
    - [ ] LCD detectability index
- [ ] add unit tests and error checking to ensure inputs are correct
- [ ] code clean-up and improved documentation
- [ ] matlab -> octave + python

## make it fast

- [X] gpu inference
- [ ] parallelize phantom generation
  - [ ] consider splitting this into multiple nodes to speed up

## immediate

- [X] Add multiple dose levels to LCD study (RZ from 10/5 meeting)
  - [X] add remaining adult reference dose level results
  - [ ] Calling the disks 10mm, 5mm, .. is inappropriate because the FOV is changing and their relative size is constant, change to size in *pixels*

## longterm (potential ORISE projects)

- [ ] Make interactive dashboard where you can click on each data point e.g. noise reduction and explore the patient and acquisition characteristics and how those compare to the training set to better understand why the model performed well or poorly(potential ORISE project)
- [ ] dockerize want to move away from matlab but it is available on Docker [matlab container info](https://www.mathworks.com/help/cloudcenter/ug/matlab-container-on-docker-hub.html)
- [ ] add graphical user interface such as [streamlit](https://streamlit.io)
- [X] make test script with fewer sims and diameters to quickly iterate through pipeline to make sure everything is working (i.e. add tests before porting to octave, Julia, different computer etc... Can use FBP for tests since that behaves in a known way)
- [ ] Could Tensorboard help with interactive image inspection? to quickly check for bias and issues while training? (Prabhat has it for model training, should get his help to make sure I'm using it appropriately when I'm ready to train models.)

- [ ] Add HU accuracy using sensitometry module from CTP404 to get multiple HU levels
  - [ ] requires that MTF results be performed with noise (discuss with Rongping)
- [ ] Check that I'm using the correct model and dose level results for the adult reference data (seems to high)
- [X] Start paper draft [Overleaf link to manuscript](https://www.overleaf.com/6647865587zswnmrpfsckg)
- [ ] Prepare IQ Phantom results for [AAPM Abstract](https://www.aapm.org/meetings/default.asp), paper draft
  - [ ] due March 2023
- [X] Update [Ped DLIR Wiki](https://fda.sharepoint.com/sites/CDRH-OSEL-DIDSR/DIDSR%20Wiki/Medical%20Imaging%20and%20Diagnostics/Pediatric%20DLIR/Home_PedDLIR.aspx)
- [ ] Switch lab notebook to markdown with remote on DIDSR github with private repo (or single word file with chapters like Seyed's lab notebook.)
