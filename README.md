---
title: Geometric Phantom Evaluation
date: 2022-07-26
---

## Introduction

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
|- make_phantoms
|   |- CCT189
|   |- CTP404
|   |- utils
|   |- make_phantoms.m
|   |- run_make_phantoms.m
|- results
|   |- MTF
|   |- NPS

## Tasks

- [X] Make the adult size 1.) water phantom 2.) LCD phantom 3.) Contrast phantom
- [X] Simulate low dose scans with the in-house simulations (Polychromatic on [BHC on + off] and Monochrome)
- [X] Apply pretrained models from Prabhat on images from Step 2.
- [X] Run evaluation scripts to the results of 2. to reproduce baseline
- [X] Remake phantoms from step 1. In pediatric sizes using known reference sizes determined previously, include Newborn and 1 yr/old (going for most extreme size differences first to see most pronounced effect.)
- [X] Repeat steps 2-4 with these pediatric phantoms
- [ ] Summarize the results and present

## Phantom Generation
