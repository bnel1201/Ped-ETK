# TODOs

- [X] Address HU accuracy issue (investigate models with normalization and make sure that normalization is correct)
  - [X] remake all results and update presentations with the corrected model (due this before moving on...)
  - [X] fix LCD first...
- [ ] Could Tensorboard help with interactive image inspection? to quickly check for bias and issues while training? (Prabhat has it for model training, should get his help to make sure I'm using it appropriately when I'm ready to train models.)
- [ ] Add multiple dose levels to LCD study (RZ from 10/5 meeting)
  - [ ] (check what sims are left to complete), I think they're all done but I need to run denoisng on all of them
- [ ] make test script with fewer sims and diameters to quickly iterate through pipeline to make sure everything is working (i.e. add tests before porting to octave, Julia, different computer etc... Can use FBP for tests since that behaves in a known way)
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
