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