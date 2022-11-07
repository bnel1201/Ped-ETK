# TODOs

## make it work

Top priority, making sure all results are there and are consistent (reliable/robust)

- [X] make sure LCD results are consistent with adults (5 dose levels)
- [ ] clean up `plot_LCD_results.py` its a mess... XD
- [ ] line 91 eval_CTP404_MTF.m% <-- double check this later, that the interp1 is working as intended meant to account for slight differences in array length from MTF_from_disk_edge due to rounding errors

- [ ] Clean up code and make sure everything runs to completion (make it work)
- [ ] Update results slides
- [ ] Then make every piece modular by figuring out the min requirements for each (LCD and MTF both expect disk centers and radii), all require directories with raw images
- [X] The. I want everything accessible via config files. I want to be able to quickly add lower dose levels and see how that changes detect ability
- [ ] Add representative anthropomorphic phantom noise reduction results

## make it right

- [ ] add unit tests and error checking to ensure inputs are correct
- [ ] code clean-up and improved documentation
- [ ] matlab -> octave + python

## make it fast

- [ ] gpu inference
- [ ] paralleize phantom generation

## immediate

- [X] Add multiple dose levels to LCD study (RZ from 10/5 meeting)
  - [X] add remaining adult reference dose level results
  - [ ] Calling the disks 10mm, 5mm, .. is inappropriate because the FOV is changing and their relative size is constant, change to size in *pixels*

## longterm

- [ ] dockerize want to move away from matlab but it is available on Docker [matlab container info](https://www.mathworks.com/help/cloudcenter/ug/matlab-container-on-docker-hub.html)
- [ ] add graphical user interface such as [streamlit](https://streamlit.io)
- [X] make test script with fewer sims and diameters to quickly iterate through pipeline to make sure everything is working (i.e. add tests before porting to octave, Julia, different computer etc... Can use FBP for tests since that behaves in a known way)
- [ ] Could Tensorboard help with interactive image inspection? to quickly check for bias and issues while training? (Prabhat has it for model training, should get his help to make sure I'm using it appropriately when I'm ready to train models.)
- [ ] Eventually swap out matlab components for octave
- [ ] consider splitting this into multiple nodes to speed up
- [ ] Add HU accuracy using sensitometry module from CTP404 to get multiple HU levels
  - [ ] requires that MTF results be performed with noise (discuss with Rongping)
- [ ] Check that I'm using the correct model and dose level results for the adult reference data (seems to high)
- [X] Start paper draft [Overleaf link to manuscript](https://www.overleaf.com/6647865587zswnmrpfsckg)
- [ ] Prepare IQ Phantom results for [AAPM Abstract](https://www.aapm.org/meetings/default.asp), paper draft
  - [ ] due March 2023
- [X] Update [Ped DLIR Wiki](https://fda.sharepoint.com/sites/CDRH-OSEL-DIDSR/DIDSR%20Wiki/Medical%20Imaging%20and%20Diagnostics/Pediatric%20DLIR/Home_PedDLIR.aspx)
- [ ] Switch lab notebook to markdown with remote on DIDSR github with private repo (or single word file with chapters like Seyed's lab notebook.)
