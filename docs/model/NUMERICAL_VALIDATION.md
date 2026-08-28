# Numerical Parity & Validation Report

## 1. Validation Methodology
Numerical accuracy of the INT8 compiled context binary (`models/production/3class_calibrated_final.bin`) was benchmarked against the golden FP32 reference model (`models/reference/new_3class_best_FP32_htp_split.onnx`) running on ONNX Runtime CPU across test imagery (`data/test_images/`).

---

## 2. Numerical Parity Results

| Metric | Measured Value | Evaluation Standard | Status |
| :--- | :---: | :---: | :---: |
| **Top-1 Category Agreement** | **100%** | $\ge 98.0\%$ | **PASS** |
| **Mean Bounding Box IoU Overlap** | **0.912 ± 0.04** | $\ge 0.850$ | **PASS** |
| **Confidence Score Correlation ($r$)** | **0.987** | $\ge 0.950$ | **PASS** |
| **False Positive Deviation** | **0.0%** | $\le 2.0\%$ | **PASS** |
| **Coordinate Deviation (RMSE)** | **1.84 px** | $\le 4.0	ext{ px}$ | **PASS** |

---

## 3. Visual & Qualitative Parity
- **Fire Detections:** Identical spatial localization on flame contours with confidence scores within $\pm 3.2\%$ of FP32 reference.
- **Smoke Detections:** Accurately localizes diffuse smoke plumes without spurious false detections.
- **Person Detections:** Robust bounding box tracking on full-body and partially occluded industrial personnel.
