# Sentinel-1 SAR Spatially Variant Apodization (SVA) Filter

This repository contains a **Python implementation of SVA** for **Sentinel-1 Single Look Complex (SLC) SAR images**. The script integrates with **ESA SNAP** via the `snappy` Python API to process SAR products.

---

## 📖 Overview

The **SVA Python script** was developed for **Sentinel-1 data integration within SNAP**. The SVA method extends the approach proposed by Wang et al. (2012) [1] to **two-dimensional (2D) processing**, incorporating both **azimuth and range directions**.  

SVA is applied **separately to the I (real) and Q (imaginary) components** of each SAR image, enabling:

- Improved sidelobe suppression  
- Preservation of mainlobe features

Note: For the amplitude-based SVA variant, a Band Maths graph for use in SNAP is included in this repository to replace the SVA filtered phase with original phase. 

The script performs the following steps:

1. **Load Sentinel-1 SLC product** using `esa-snappy`.
2. **Extract I and Q bands**.
3. **Compute SVA weighting function** using 2D neighbors.
4. **Apply SVA filtering**. 
5. **Compute derived products**: amplitude and intensity.
6. **Save filtered output** in BEAM-DIMAP format.

---

## ⚙️ Requirements

- Python 3.10.16  
- **SNAP-Python (snappy)** – Snappy is an internal plugin of SNAP, automatically installed during software setup and implemented by Brockman Consult Scientific Image Processing Toolbox.  
- **NumPy** – for array computations (`pip install numpy`)

---

## 🔗 References

[1] Wang, Q.; Zhu, W.; Li, Z.; Ji, Z.; Sun, Y. (2012). *Module spatially variant apodization algorithm for enhancing radar images.* In **9th European Radar Conference** (pp. 294–297). IEEE.
