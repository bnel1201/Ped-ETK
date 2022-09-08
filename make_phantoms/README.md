---
title: DLIR Generalizability Phantom Experiments
date: 2022-09-02
author: Brandon J. Nelson
---

## CCT189: Catphan Abdomen low contrast detectability phantom

CCT189 is is the Catphan low contrast detectability in the phanom developed by the MITA (Medical Imaging Technology Alliance) <https://www.medicalimaging.org/>

MITA is a member of NEMA who defines these standards:

https://www.nema.org/standards/view/computed-tomography-image-quality-ctiq-low-contrast-detectability-lcd-assessment-when-using-dose-reduction-technology

- [product website](https://www.phantomlab.com/catphan-mita)
- [CCT189 and 191 manual](https://static1.squarespace.com/static/5367b059e4b05a1adcd295c2/t/615ef58fec2c5c1b70a35ebc/1633613200706/CCT189andCCT191ProductGuide20211006.pdf)

- How does LCD compare to CCT189, ask Rongping

## Resources

CCT189: derives from Rongping Zeng's [make_CCT189_wD45_B30.m](/home/rxz4/ct_deeplearning/make_phantom/make_CCT189_wD45_B30.m) which was used by [MITA_LCD.m](/home/rxz4/ct_deeplearning/evaluation/MITA_LCD.m) to make results for the 2020 CT Meeting Proceedings [^1].

## References

[^1]: Zeng R, Lin CY, Li Q, et al. Performance of a deep learning-based CT image denoising method: Generalizability over dose, reconstruction kernel, and slice thickness. Medical Physics. 2022;49(2):836-853. doi:10.1002/mp.15430
