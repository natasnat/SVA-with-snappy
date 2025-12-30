# Sentinel-1 SAR Spatially Variant Apodization (SVA) Filter

## 📖 Overview

This repository is part of the Master’s thesis by Stumpf (2025) [1] continued in a journal publication by Liedel et al. [2] (same first author as Stumpf, 2025) in which Spatially Variant Apodization (SVA) is applied directly to SAR imagery, and a novel amplitude-based SVA approach is introduced to preserve phase integrity for further Persistent Scatterer Interferomety (PSI) processing.

It contains a **Python implementation of SVA** for **Sentinel-1 Single Look Complex (SLC) SAR images**. The script integrates with **ESA SNAP** via the `snappy` Python API to process SAR products. It is applied **after the ESD step** of the SNAP2StaMPS workflow by Blasco et al. (2021) [3].  

The repository includes **workflow diagrams** that clearly describe the procedures for both **full-scene SVA** and **amplitude-based SVA**.  

For the amplitude-based SVA variant, a **Band Maths graph** is included for SNAP to replace the SVA-filtered phase with the original phase, preserving phase continuity.

---

## 📖 SVA Python Script

The **SVA Python script** was developed for **Sentinel-1 data integration within SNAP**. The SVA method extends the approach proposed by Wang et al. (2012) [4] to **two-dimensional (2D) processing**, incorporating both **azimuth and range directions**.  

SVA is applied **separately to the I (real) and Q (imaginary) components** of each SAR image, enabling:

- Improved sidelobe suppression  
- Preservation of mainlobe features  

The script performs the following steps:

1. **Load Sentinel-1 SLC product** using `esa-snappy`.  
2. **Extract I and Q bands**.  
3. **Compute SVA weighting function** using 2D neighbors.  
4. **Apply SVA filtering**.  
5. **Compute derived products**: amplitude and intensity.  
6. **Save filtered output** in **BEAM-DIMAP format**.

---

## ⚙️ Requirements

- Python 3.10.16  
- **SNAP-Python (snappy)** – internal SNAP plugin, automatically installed during SNAP setup.  
- **NumPy** – for array computations (`pip install numpy`)  
- **SNAP Version 9**  
- **SNAP2StaMPS Version 1** (Blasco et al., 2021)  
- Sentinel-1 data (from Alaska Satellite Facility)  

---

## 🔗 References

[1] Stumpf, N. (2025). *Dam Monitoring – Optimization of Sidelobe Suppression in Radar Images during StaMPS Persistent Scatterer Interferometry Processing*. Master’s thesis, University of Jena.

[2] Liedel, N., Ziemer, J., Jänichen, J., Schmullius, C. & Dubois, C. (2026). *Novel amplitude-based approach for reducing sidelobes in persistent scatterer interferometry processing using spatially variant apodization*. **Sensors**, 26(1), 204. https://doi.org/10.3390/s26010204

[3] Blasco, J. M. D., & Foumelis, M. (2021). *SNAP2StaMPS v1*. Retrieved August 20, 2025, from https://github.com/mdelgadoblasco/snap2stamps/tree/v1.0.1

[4] Wang, Q., Zhu, W., Li, Z., Ji, Z., & Sun, Y. (2012). *Module spatially variant apodization algorithm for enhancing radar images*. In **Proceedings of the 9th European Radar Conference** (pp. 294–297). IEEE.
