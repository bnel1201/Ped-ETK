---
title: Geometric Phantom Evaluation
date: 2022-11-04
author: Brandon John Nelson
email: Brandon.Nelson@fda.hhs.gov
---

## Introduction

This pipeline enables automatic assessment of the generalizability of objective image quality in noise reduction algorithms in pediatric populations with a focus on pretrained deep-learning-based noise reduction and reconstruction algorithms.

This flexible tool enables simulation of standard image quality phantoms (the CATPHAN CTP404 Sensitometry module, and the CATPHAN CCT189 MITA Low Contrast Detectability (LCD) phantom). A weakness of the practical use of these phantoms is that they are manufactured at a defined size representating adult anatomy and are routinely evaluated with adult protocols, meaning that their results have limited transferability to pediatric imaging protocols. This discrepency is more apparent in deep-learning based image enhancement algorithms which are particularly sensitive to changes to reconstructed field of view (smaller in pediatric protocols).

Unique to this toolkit is the ability to simulate pediatric scaled versions of these standard image quality phantoms to better evaluate these objective image quality measures under a variety of image conditions and simulations patient sizes.

## Defining an Experiment

Simulation experiments are meant to do the following:

1. generate phantoms and perform CT simulations
2. perform DLIR denoising
3. run objective image quality evaluation

These three components are defined in your `experiment`, which is a directory containing the following 2 text files:

1. a file called: `protocol`
   - this defines `BASE_DIR` where the simulated images are stored for subsequent analysis
   - `RESULTS_DIR` where measurement files are saved as .csv or .h5 files and plots are generated
   - `MODEL_FOLDER`, this is where the DLIR model is specified
2. `.phantom` files, which parameterize the phantoms and CT simulations (read the comments in the example `.phantom` files to learn more)

Two example experiments are provided in the `experiments` folder:

- `experiments/main`
- `experiments/test`

Two define a new experiment, copy and rename either of these examples.

## Running an experiment

The main syntax for running a whole experiment, both (a) phantom generation + CT simulation, (b) DLIR denoising, and (c) objective image quality assessments is using the `run_all.sh` shell script like so:

```shell
bash run_all.sh path/to/experiment
```

For example `bash run_all.sh experiments/main` will run the main experiment and `bash run_all.sh experiments/test` will run an abbreviatdd simulation experiment used for testing and developing the simulation and evaluation pipeline.

Reading the contents of this shell script reveals how different stages can be done separately such as phantom generation + CT sim alone or evaluation. A common examples are given below

### Phantom generation and CT simulation

```shell
bash make_phantoms/run_make_phantoms.sh ${BASE_DIR} ${EXPERIMENT}
```

### DLIR denoising

```shell
bash denoising/run_denoising.sh $BASE_DIR $MODEL_FOLDER
```

### Objective Image Quality Evaluation

```shell
bash evaluation/run_all_evaluations.sh $BASE_DIR $RESULTS_DIR
```

## Explanation of Directory Structure

```directory structure
|- denoising
|   |- SPIE2023_models
|   |- denoise.sh
|   |- run_denoising.sh
|- evaluation
|   |- LCD
|   |- MTF
|   |- NPS
|   |- utils
|   |- run_all_evaluations.sh
|- make_phantoms
|   |- CCT189
|   |- CTP404
|   |- utils
|   |- make_phantoms.m
|   |- run_make_phantoms.m
|- results
|   |- MTF
|   |- NPS
```

## FAQS

1. `ffmpeg` not found or my gifs are not being generated. --> `sudo apt-get install ffmpeg`
