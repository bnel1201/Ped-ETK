---
title: Geometric Phantom Evaluation
date: 2022-07-26
---

## Introduction

## Defining an Experiment

Simulation experiments are meant to do the following:
1. generate phantoms and perform CT simulations
2. perform DLIR denoising
3. run objective image quality evaluation

These three components are defined in your `experiment`, which is a directory containing 

## Explanation of Directory Structure

|- denoising
|   |- SPIE2023_models
|   |- denoise_CCT189.sh
|   |- denoise_CTP404.sh
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

## Evaluation

```bash
make results
```

`run_all_evaluations.sh` , the directory in which to save all results can be set at the top of this file with `results_dir=/path/to_results`. This can be either an absolute directory path or a relative path, *relative to `run_all_evaluations.sh`*.

## Phantom Generation

```bash
make phantoms
```

## Run Denoising

<!-- ```bash
make denoise
``` -->

## FAQS

1. `ffmpeg` not found or my gifs are not being generated. --> `sudo apt-get install ffmpeg` 